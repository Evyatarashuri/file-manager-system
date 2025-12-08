# worker/app/subscribers/file_uploaded_subscriber.py

import json
import signal
import threading
from typing import Optional

from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPICallError

from app.config.logging import get_logger
from app.config.settings import settings
from app.consumers.file_uploaded_consumer import FileUploadedConsumer

logger = get_logger("worker-subscriber")

PROJECT_ID: str = settings.PROJECT_ID
SUBSCRIPTION: str = settings.PUBSUB_FILE_UPLOADED_SUB

consumer = FileUploadedConsumer()

_shutdown_event = threading.Event()


def _process_message(payload: dict) -> bool:
    """
    Business logic handler for file-related events.
    Returns True on success, False on recoverable failure.
    """
    event = payload.get("event")

    if event == "FILE_UPLOADED":
        consumer.handle(payload)
        return True

    logger.warning(f"Unknown event type received: {event}")
    return False


def _callback(message: pubsub_v1.subscriber.message.Message) -> None:
    """
    Pub/Sub callback responsible for:
    - decoding message
    - delegating to business logic
    - acknowledging (ACK) or negative acknowledging (NACK)
    """
    logger.info("Incoming message received — callback triggered")

    try:
        payload_raw = message.data.decode("utf-8")
        payload = json.loads(payload_raw)
        logger.info(f"Received event: {payload}")

    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode message body: {e} | data={message.data!r}")
        # Invalid payload, do not retry forever; ACK to drop it.
        message.ack()
        return

    try:
        success = _process_message(payload)

        if success:
            message.ack()
            logger.info(f"ACK message_id={message.message_id}")
        else:
            # Let Pub/Sub retry according to subscription settings / DLQ.
            message.nack()
            logger.warning(f"NACK (recoverable) message_id={message.message_id}")

    except Exception as e:
        # Unexpected error during processing.
        logger.error(f"Unhandled error while processing message_id={message.message_id}: {e}", exc_info=True)
        # NACK so that Pub/Sub can redeliver or move to DLQ if configured.
        message.nack()


def _handle_signal(sig, frame) -> None:
    """
    Signal handler for graceful shutdown in container / VM.
    """
    logger.warning(f"Shutdown signal received: {sig}")
    _shutdown_event.set()


def start_file_events_consumer(timeout: Optional[int] = None) -> None:
    """
    Starts a long-running Pub/Sub subscriber for file events.

    - Listens on FILE_UPLOADED subscription.
    - Uses flow control to limit concurrency.
    - Supports graceful shutdown via SIGINT/SIGTERM.
    """

    if not PROJECT_ID or not SUBSCRIPTION:
        raise RuntimeError("PROJECT_ID or PUBSUB_FILE_UPLOADED_SUB is not configured")

    subscription_path = f"projects/{PROJECT_ID}/subscriptions/{SUBSCRIPTION}"
    logger.info(f"Worker listening on: {subscription_path}")

    subscriber = pubsub_v1.SubscriberClient()

    flow_control = pubsub_v1.types.FlowControl(
        max_messages=30,      # concurrency of in-flight messages
        max_bytes=10 * 1024 * 1024,  # 10MB in-flight
    )

    streaming_pull = subscriber.subscribe(
        subscription_path,
        callback=_callback,
        flow_control=flow_control,
    )

    logger.info("Worker subscriber started (Pub/Sub streaming pull)")

    # Register OS signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    try:
        # Wait until shutdown event is set
        while not _shutdown_event.is_set():

            logger.info("Worker alive — waiting for Pub/Sub messages...")  # heartbeat log

            # `.result()` would block forever; instead poll shutdown event
            streaming_pull_future = streaming_pull
            
            try:
                # Give the future a short timeout to remain responsive to shutdown
                streaming_pull_future.result(timeout=5)
            except TimeoutError:
                # Normal: no messages or idle, loop again and check shutdown flag
                continue
            except GoogleAPICallError as e:
                logger.error(f"Streaming pull error from Pub/Sub: {e}", exc_info=True)
                # Optionally sleep / backoff here before re-looping
            except Exception as e:
                logger.error(f"Unexpected error in streaming pull: {e}", exc_info=True)

    finally:
        logger.warning("Shutting down Pub/Sub subscriber...")
        streaming_pull.cancel()
        subscriber.close()
        logger.info("Worker subscriber shutdown complete")
