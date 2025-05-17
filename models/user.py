from datetime import datetime
from enum import Enum
from supabase import create_client
import os
from config.supabase_config import supabase

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

    @staticmethod
    def get_by_id(user_id):
        response = supabase.table('users').select('*').eq('id', user_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def get_by_email(email):
        response = supabase.table('users').select('*').eq('email', email).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def get_all():
        response = supabase.table('users').select('*').execute()
        return response.data

    @staticmethod
    def create(data):
        response = supabase.table('users').insert(data).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def update(user_id, data):
        response = supabase.table('users').update(data).eq('id', user_id).execute()
        return response.data[0] if response.data else None 