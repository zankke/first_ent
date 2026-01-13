from datetime import datetime
from backend.app import db

class InstagramProfilePic(db.Model):
    __tablename__ = 'instagram_profile_pics'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('instagram_users.id'), nullable=False)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    url = db.Column(db.String(500))

    def to_dict(self):
        return {
            'width': self.width,
            'height': self.height,
            'url': self.url
        }

class InstagramBioLink(db.Model):
    __tablename__ = 'instagram_bio_links'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('instagram_users.id'), nullable=False)
    url = db.Column(db.String(500))
    title = db.Column(db.String(255))
    link_type = db.Column(db.String(50))

    def to_dict(self):
        return {
            'url': self.url,
            'title': self.title,
            'link_type': self.link_type
        }

class InstagramBusinessContact(db.Model):
    __tablename__ = 'instagram_business_contacts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('instagram_users.id'), nullable=False)
    city_name = db.Column(db.String(255))
    public_email = db.Column(db.String(255))
    public_phone_number = db.Column(db.String(255))
    whatsapp_number = db.Column(db.String(255))
    address_street = db.Column(db.String(255))

    def to_dict(self):
        return {
            'city_name': self.city_name,
            'public_email': self.public_email,
            'public_phone_number': self.public_phone_number,
            'whatsapp_number': self.whatsapp_number,
            'address_street': self.address_street
        }

class InstagramUser(db.Model):
    __tablename__ = 'instagram_users'

    id = db.Column(db.Integer, primary_key=True)
    pk = db.Column(db.String(255), unique=True, nullable=False) # Primary Key from Instagram
    username = db.Column(db.String(255), unique=True, nullable=False)
    full_name = db.Column(db.String(255))
    biography = db.Column(db.Text)
    profile_pic_url = db.Column(db.String(500))
    is_private = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    is_business = db.Column(db.Boolean, default=False)
    account_type = db.Column(db.String(50)) # e.g., 'Personal', 'Business'
    media_count = db.Column(db.Integer, default=0)
    follower_count = db.Column(db.Integer, default=0)
    following_count = db.Column(db.Integer, default=0)
    mutual_followers_count = db.Column(db.Integer, default=0)
    external_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    hd_profile_pics = db.relationship('InstagramProfilePic', backref='user', lazy=True, cascade='all, delete-orphan')
    bio_links = db.relationship('InstagramBioLink', backref='user', lazy=True, cascade='all, delete-orphan')
    business_contacts = db.relationship('InstagramBusinessContact', backref='user', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'pk': self.pk,
            'username': self.username,
            'full_name': self.full_name,
            'biography': self.biography,
            'profile_pic_url': self.profile_pic_url,
            'is_private': self.is_private,
            'is_verified': self.is_verified,
            'is_business': self.is_business,
            'account_type': self.account_type,
            'media_count': self.media_count,
            'follower_count': self.follower_count,
            'following_count': self.following_count,
            'mutual_followers_count': self.mutual_followers_count,
            'external_url': self.external_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'hd_profile_pics': [pic.to_dict() for pic in self.hd_profile_pics],
            'bio_links': [link.to_dict() for link in self.bio_links],
            'business_contacts': [contact.to_dict() for contact in self.business_contacts]
        }

class InstagramSearchResult(db.Model):
    __tablename__ = 'instagram_search_results'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('instagram_users.id'), nullable=False)
    status = db.Column(db.String(50))
    raw_response = db.Column(db.JSON) # Store raw JSON response
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('InstagramUser', backref='search_results', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'raw_response': self.raw_response,
            'created_at': self.created_at.isoformat()
        }
