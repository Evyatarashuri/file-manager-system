import time
from app.events.pubsub_subscriber import start_file_events_consumer
from app.config.logging import get_logger


logger = get_logger("worker-main")


def main():
    logger.info("Starting File Upload Pub/Sub Worker...")

    try:
        # Start streaming pull subscriber (infinite loop inside)
        start_file_events_consumer()

    except KeyboardInterrupt:
        logger.warning("KeyboardInterrupt detected — shutting down gracefully...")

    except Exception as e:
        logger.error(f"Worker crashed unexpectedly: {e}", exc_info=True)

        # Optional: allow auto-restart if using `systemd` / Docker restart policy
        logger.info("Attempting restart in 5 seconds...")
        time.sleep(5)
        main()


if __name__ == "__main__":
    main()
