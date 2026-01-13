from datetime import datetime
from backend.app import db
import json

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)
    post_id = db.Column(db.String(100), nullable=False)
    post_url = db.Column(db.Text)
    caption = db.Column(db.Text)
    media_type = db.Column(db.Enum('image', 'video', 'carousel'), nullable=False)
    media_urls = db.Column(db.JSON)
    like_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    share_count = db.Column(db.Integer, default=0)
    posted_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('channel_id', 'post_id', name='unique_post'),
    )
    
    def set_media_urls(self, urls):
        """미디어 URL 리스트를 JSON으로 저장"""
        if isinstance(urls, list):
            self.media_urls = urls
        else:
            self.media_urls = []
    
    def get_media_urls(self):
        """저장된 미디어 URL 리스트를 반환"""
        return self.media_urls if self.media_urls else []
    
    def to_dict(self):
        return {
            'id': self.id,
            'channel_id': self.channel_id,
            'post_id': self.post_id,
            'post_url': self.post_url,
            'caption': self.caption,
            'media_type': self.media_type,
            'media_urls': self.get_media_urls(),
            'like_count': self.like_count,
            'comment_count': self.comment_count,
            'share_count': self.share_count,
            'posted_at': self.posted_at.isoformat(),
            'created_at': self.created_at.isoformat()
        }
