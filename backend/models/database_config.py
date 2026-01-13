from datetime import datetime
from backend.app import db
from cryptography.fernet import Fernet
import base64
import os

class DatabaseConfig(db.Model):
    __tablename__ = 'database_configs'
    
    id = db.Column(db.Integer, primary_key=True)
    config_name = db.Column(db.String(100), nullable=False, unique=True)
    host = db.Column(db.String(100), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    database_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password_encrypted = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def _get_encryption_key(self):
        """암호화 키를 가져오거나 생성"""
        key = os.getenv('ENCRYPTION_KEY')
        if not key:
            key = Fernet.generate_key()
            os.environ['ENCRYPTION_KEY'] = key.decode()
        return key
    
    def set_password(self, password):
        """비밀번호를 암호화하여 저장"""
        key = self._get_encryption_key()
        f = Fernet(key)
        self.password_encrypted = f.encrypt(password.encode()).decode()
    
    def get_password(self):
        """암호화된 비밀번호를 복호화"""
        key = self._get_encryption_key()
        f = Fernet(key)
        return f.decrypt(self.password_encrypted.encode()).decode()
    
    def to_dict(self):
        return {
            'id': self.id,
            'config_name': self.config_name,
            'host': self.host,
            'port': self.port,
            'database_name': self.database_name,
            'username': self.username,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
