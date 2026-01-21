from datetime import datetime
from backend.app import db

class Channel(db.Model):
    __tablename__ = 'channels'
    
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.BigInteger, db.ForeignKey('Artists.id'), nullable=False)
    platform = db.Column(db.Enum('instagram', 'youtube', 'tiktok', 'twitter'), nullable=False)
    channel_id = db.Column(db.String(100), nullable=False)
    channel_name = db.Column(db.String(200))
    channel_url = db.Column(db.Text)
    follower_count = db.Column(db.Integer, default=0)
    following_count = db.Column(db.Integer, default=0)
    post_count = db.Column(db.Integer, default=0)
    is_verified = db.Column(db.Boolean, default=False)
    last_sync_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계
    stats = db.relationship('ChannelStat', backref='channel', lazy=True, cascade='all, delete-orphan')
    posts = db.relationship('Post', backref='channel', lazy=True, cascade='all, delete-orphan')
    
    __table_args__ = (
        db.UniqueConstraint('artist_id', 'platform', 'channel_id', name='unique_channel'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'artist_id': self.artist_id,
            'platform': self.platform,
            'channel_id': self.channel_id,
            'channel_name': self.channel_name,
            'channel_url': self.channel_url,
            'follower_count': self.follower_count,
            'following_count': self.following_count,
            'post_count': self.post_count,
            'is_verified': self.is_verified,
            'last_sync_at': self.last_sync_at.isoformat() if self.last_sync_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
