class User:
    def __init__(self, user_id, username, password_hash, full_name, email, role, status):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.full_name = full_name
        self.email = email
        self.role = role
        self.status = status

    def is_admin(self):
        return self.role.lower() == "admin"

    def is_active(self):
        return self.status.lower() == "active"

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"
