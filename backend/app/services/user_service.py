from app.repositories.firestore_repo import FirestoreRepo

class UserService:
    def __init__(self):
        self.firestore = FirestoreRepo()

    def get_user(self, user_id: str):
        return self.firestore.get_user_document(user_id)

    def save_preferences(self, user_id: str, prefs: dict):
        self.firestore.update_user_document(user_id, {"preferences": prefs})

    def get_preferences(self, user_id: str):
        user = self.firestore.get_user_document(user_id)
        return user.get("preferences", {}) if user else {}
