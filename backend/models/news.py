from datetime import datetime
from backend.app import db
import json

class News(db.Model):
    __tablename__ = 'news'
    
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artists.id'), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text)
    url = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(200))
    published_at = db.Column(db.DateTime)
    crawled_at = db.Column(db.DateTime, default=datetime.utcnow)
    sentiment = db.Column(db.Enum('positive', 'negative', 'neutral'), default='neutral')
    relevance_score = db.Column(db.Float, default=0.0)
    keywords = db.Column(db.JSON)  # 키워드 리스트를 JSON으로 저장
    is_processed = db.Column(db.Boolean, default=False)
    thumbnail = db.Column(db.Text) # 썸네일 이미지 URL
    media_name = db.Column(db.String(255)) # 미디어 이름 (예: 연합뉴스, 조선일보)
    
    # 관계
    artist = db.relationship('Artist', backref='news_articles', lazy=True)
    
    def set_keywords(self, keywords_list):
        """키워드 리스트를 JSON으로 저장"""
        if isinstance(keywords_list, list):
            self.keywords = keywords_list
        else:
            self.keywords = []
    
    def get_keywords(self):
        """저장된 키워드 리스트를 반환"""
        return self.keywords if self.keywords else []
    
    def to_dict(self):
        return {
            'id': self.id,
            'artist_id': self.artist_id,
            'artist_name': self.artist.name if self.artist else None,
            'title': self.title,
            'content': self.content,
            'url': self.url,
            'source': self.source,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'crawled_at': self.crawled_at.isoformat(),
            'sentiment': self.sentiment,
            'relevance_score': self.relevance_score,
            'keywords': self.get_keywords(),
            'is_processed': self.is_processed,
            'thumbnail': self.thumbnail,
            'media_name': self.media_name
        }
