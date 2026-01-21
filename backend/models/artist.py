from datetime import datetime
from backend.app import db

class Artist(db.Model):
    __tablename__ = 'Artists'
    
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    eng_name = db.Column(db.String(100), nullable=True) # Added eng_name
    birth_date = db.Column(db.Date, nullable=False)
    height_cm = db.Column(db.Integer)
    debut_date = db.Column(db.Date)
    debut_title = db.Column(db.String(200), nullable=True) # Added
    recent_activity_category = db.Column(db.String(100), nullable=True) # Added
    recent_activity_name = db.Column(db.String(200), nullable=True) # Added
    genre = db.Column(db.String(100))
    agency_id = db.Column(db.BigInteger)
    current_agency_name = db.Column(db.String(100), nullable=True) # Added
    nationality = db.Column(db.String(100))
    is_korean = db.Column(db.Boolean, default=True)
    gender = db.Column(db.Enum('WOMAN', 'MEN', 'NA', 'EXTRA', 'FOREIGN')) # Added 'NA'
    status = db.Column(db.String(50))
    category_id = db.Column(db.BigInteger)
    platform = db.Column(db.String(50))
    social_media_url = db.Column(db.String(255))
    profile_photo = db.Column(db.String(255))
    guarantee_krw = db.Column(db.BigInteger, nullable=True) # New field
    wiki_summary = db.Column(db.Text, nullable=True) # Added

    # Relationships
    activities = db.relationship('Activity', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'eng_name': self.eng_name, # Added eng_name to to_dict
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'height_cm': self.height_cm,
            'debut_date': self.debut_date.isoformat() if self.debut_date else None,
            'debut_title': self.debut_title, # Added
            'recent_activity_category': self.recent_activity_category, # Added
            'recent_activity_name': self.recent_activity_name, # Added
            'genre': self.genre,
            'agency_id': self.agency_id,
            'current_agency_name': self.current_agency_name, # Added
            'nationality': self.nationality,
            'is_korean': self.is_korean,
            'gender': self.gender,
            'status': self.status,
            'category_id': self.category_id,
            'platform': self.platform,
            'social_media_url': self.social_media_url,
            'profile_photo': self.profile_photo,
            'guarantee_krw': self.guarantee_krw,
            'wiki_summary': self.wiki_summary # Added
        }
