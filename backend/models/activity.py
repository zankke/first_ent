from backend.app import db
from datetime import datetime

class Activity(db.Model):
    __tablename__ = 'Activities'

    id = db.Column(db.BigInteger, primary_key=True)
    artist_id = db.Column(db.BigInteger, db.ForeignKey('Artists.id'), nullable=False) # Assuming link to Artist
    activity_name = db.Column(db.Text, nullable=False)
    activity_type = db.Column(db.Text)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    location = db.Column(db.Text)
    manager_id = db.Column(db.BigInteger, db.ForeignKey('Staff.id'))

    # Relationships
    artist = db.relationship('Artist', lazy=True)
    manager = db.relationship('Staff', backref='managed_activities', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'artist_id': self.artist_id,
            'activity_name': self.activity_name,
            'activity_type': self.activity_type,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'location': self.location,
            'manager_id': self.manager_id,
            'manager_name': self.manager.name if self.manager else None
        }
