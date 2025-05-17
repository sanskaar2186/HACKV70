from datetime import datetime
from enum import Enum

class UserRole(Enum):
    ADMIN = "admin"
    SUPERVISOR = "supervisor"
    WORKER = "worker"
    CLIENT = "client"

class User:
    def __init__(self, uid, email, role, name=None, created_at=None):
        self.uid = uid
        self.email = email
        self.role = role
        self.name = name
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            'uid': self.uid,
            'email': self.email,
            'role': self.role,
            'name': self.name,
            'created_at': self.created_at.isoformat()
        } 