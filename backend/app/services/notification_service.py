class NotificationService:
    def __init__(self):
        pass  # placeholder for sending emails via SES, SendGrid, etc.

    def notify_user(self, user_id: str, message: str):
        # In production: send email, push notification, in-app message
        print(f"[NOTIFY] To {user_id}: {message}")

    def notify_admin(self, message: str):
        print(f"[ADMIN-NOTIFY] {message}")


# Not in use for now - but could be useful later