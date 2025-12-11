class User:
    def __init__(self, ID, firstname, middlename=None, lastname="", email="", username="", role="user", status="inactive"):
        self.ID = ID
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.email = email
        self.username = username
        self.role = role
        self.status = status

    def full_name(self):
        """Return a sensible full name while skipping missing parts.

        This avoids returning 'None' for missing middlename or producing
        extra spaces when parts are empty.
        """
        parts = [p for p in (self.firstname, self.middlename, self.lastname) if p]
        return " ".join(parts).strip()

    def is_admin(self):
        """Safely check whether the user has the admin role (case-insensitive)."""
        return bool(getattr(self, 'role', None)) and str(self.role).lower() == "admin"

    def activate(self):
        self.status = "active"

    def deactivate(self):
        self.status = "inactive"

    def __repr__(self):
        return f"User(ID={self.ID!r}, username={self.username!r}, email={self.email!r}, role={self.role!r}, status={self.status!r})"
