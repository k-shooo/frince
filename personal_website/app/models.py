class User:
    def __init__(self, ID, firstname, middlename, lastname, email, username, role, status):
        self.ID = ID
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.email = email
        self.username = username
        self.role = role
        self.status = status

    def full_name(self):
        return f"{self.firstname} {self.middlename} {self.lastname}"

    def is_admin(self):
        return self.role.lower() == "admin"

    def activate(self):
        self.status = "active"

    def deactivate(self):
        self.status = "inactive"
