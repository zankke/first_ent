from datetime import datetime
from backend.app import db

class Board(db.Model):
    __tablename__ = 'boards'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('Users.uqid'), nullable=False)
    board_type = db.Column(db.Enum('notice', 'announcement', 'general'), default='general')
    is_published = db.Column(db.Boolean, default=False)
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # relationship
    author = db.relationship('Account', backref=db.backref('boards', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author_id': self.author_id,
            'author_name': self.author.uname if self.author else 'Unknown',
            'board_type': self.board_type,
            'is_published': self.is_published,
            'view_count': self.view_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
