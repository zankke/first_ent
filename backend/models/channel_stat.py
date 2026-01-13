from datetime import datetime, date
from backend.app import db

class ChannelStat(db.Model):
    __tablename__ = 'channel_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)
    stat_date = db.Column(db.Date, nullable=False)
    follower_count = db.Column(db.Integer, default=0)
    following_count = db.Column(db.Integer, default=0)
    post_count = db.Column(db.Integer, default=0)
    engagement_rate = db.Column(db.Numeric(5, 2), default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('channel_id', 'stat_date', name='unique_channel_date'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'channel_id': self.channel_id,
            'stat_date': self.stat_date.isoformat(),
            'follower_count': self.follower_count,
            'following_count': self.following_count,
            'post_count': self.post_count,
            'engagement_rate': float(self.engagement_rate),
            'created_at': self.created_at.isoformat()
        }
