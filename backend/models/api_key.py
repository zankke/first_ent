from datetime import datetime
from backend.app import db

class APIKey(db.Model):
    __tablename__ = 'api_keys'
    
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.Enum('instagram', 'youtube', 'tiktok', 'twitter'), nullable=False)
    api_name = db.Column(db.String(100), nullable=False)
    api_key = db.Column(db.Text, nullable=False)
    api_secret = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    last_used_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'platform': self.platform,
            'api_name': self.api_name,
            'api_key': self.api_key[:10] + '...' if len(self.api_key) > 10 else self.api_key,  # 보안을 위해 일부만 표시
            'is_active': self.is_active,
            'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
