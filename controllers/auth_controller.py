from models.user import User
import config

class AuthController:
    def __init__(self):
        self.current_user = None

    def login(self, username, password):
        user = User.authenticate(username, password)
        if not user:
            return None

        if getattr(user, 'account_status', '') == config.ACCOUNT_LOCKED:
            return None

        self.current_user = user

        return {
            'user_id': user.user_id,
            'username': user.username,
            'full_name': user.full_name,
            'role': user.role,
            'account_status': user.account_status,
            'fine_balance': user.fine_balance
        }

    def logout(self):
        self.current_user = None

    def change_password(self, user_id, old_password, new_password):
        return User.change_password(user_id, old_password, new_password)
