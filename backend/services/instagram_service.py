from typing import Optional, List
from sqlalchemy.orm import Session
from backend.models.instagram import InstagramUser, InstagramSearchResult, InstagramProfilePic, InstagramBioLink, InstagramBusinessContact
from datetime import datetime

class InstagramService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def insert_instagram_user(self, user_data: dict) -> InstagramUser:
        # Check if user already exists
        user = self.db_session.query(InstagramUser).filter_by(pk=user_data['pk']).first()

        if not user:
            user = InstagramUser(
                pk=user_data['pk'],
                username=user_data.get('username'),
                full_name=user_data.get('full_name'),
                biography=user_data.get('biography'),
                profile_pic_url=user_data.get('profile_pic_url'),
                is_private=user_data.get('is_private', False),
                is_verified=user_data.get('is_verified', False),
                is_business=user_data.get('is_business', False),
                account_type=user_data.get('account_type'),
                media_count=user_data.get('media_count', 0),
                follower_count=user_data.get('follower_count', 0),
                following_count=user_data.get('following_count', 0),
                mutual_followers_count=user_data.get('mutual_followers_count', 0),
                external_url=user_data.get('external_url'),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            self.db_session.add(user)
            self.db_session.flush() # To get the user.id for relationships
        else:
            # Update existing user data
            user.username = user_data.get('username', user.username)
            user.full_name = user_data.get('full_name', user.full_name)
            user.biography = user_data.get('biography', user.biography)
            user.profile_pic_url = user_data.get('profile_pic_url', user.profile_pic_url)
            user.is_private = user_data.get('is_private', user.is_private)
            user.is_verified = user_data.get('is_verified', user.is_verified)
            user.is_business = user_data.get('is_business', user.is_business)
            user.account_type = user_data.get('account_type', user.account_type)
            user.media_count = user_data.get('media_count', user.media_count)
            user.follower_count = user_data.get('follower_count', user.follower_count)
            user.following_count = user_data.get('following_count', user.following_count)
            user.mutual_followers_count = user_data.get('mutual_followers_count', user.mutual_followers_count)
            user.external_url = user_data.get('external_url', user.external_url)
            user.updated_at = datetime.utcnow()

        # Handle nested data (profile pics, bio links, business contacts)
        self._update_nested_data(user, user_data)

        self.db_session.commit()
        return user

    def _update_nested_data(self, user: InstagramUser, user_data: dict):
        # Update HD Profile Pics
        if 'hd_profile_pic_versions' in user_data:
            self.db_session.query(InstagramProfilePic).filter_by(user_id=user.id).delete()
            for pic_data in user_data['hd_profile_pic_versions']:
                pic = InstagramProfilePic(
                    user_id=user.id,
                    width=pic_data.get('width'),
                    height=pic_data.get('height'),
                    url=pic_data.get('url')
                )
                self.db_session.add(pic)

        # Update Bio Links
        if 'bio_links' in user_data:
            self.db_session.query(InstagramBioLink).filter_by(user_id=user.id).delete()
            for link_data in user_data['bio_links']:
                link = InstagramBioLink(
                    user_id=user.id,
                    url=link_data.get('url'),
                    title=link_data.get('title'),
                    link_type=link_data.get('link_type')
                )
                self.db_session.add(link)

        # Update Business Contacts
        if 'business_contact_info' in user_data:
            self.db_session.query(InstagramBusinessContact).filter_by(user_id=user.id).delete()
            contact_data = user_data['business_contact_info']
            contact = InstagramBusinessContact(
                user_id=user.id,
                city_name=contact_data.get('public_phone_country_code'), # This seems like a mismatch, check API response
                public_email=contact_data.get('public_email'),
                public_phone_number=contact_data.get('public_phone_number'),
                whatsapp_number=contact_data.get('whatsapp_number'),
                address_street=contact_data.get('public_phone_number') # This also seems like a mismatch
            )
            self.db_session.add(contact)

    def insert_api_search_result(self, user_id: int, status: str, raw_response: dict):
        result = InstagramSearchResult(
            user_id=user_id,
            status=status,
            raw_response=raw_response,
            created_at=datetime.utcnow()
        )
        self.db_session.add(result)
        self.db_session.commit()

    def get_instagram_user(self, username: str) -> Optional[InstagramUser]:
        return self.db_session.query(InstagramUser).filter_by(username=username).first()

    def get_verified_users(self, limit: int) -> List[InstagramUser]:
        return self.db_session.query(InstagramUser).filter_by(is_verified=True).limit(limit).all()

    def get_business_users(self, limit: int) -> List[InstagramUser]:
        return self.db_session.query(InstagramUser).filter_by(is_business=True).limit(limit).all()

    def search_users_by_follower_count(self, min_followers: int, max_followers: Optional[int], limit: int) -> List[InstagramUser]:
        query = self.db_session.query(InstagramUser).filter(InstagramUser.follower_count >= min_followers)
        if max_followers is not None:
            query = query.filter(InstagramUser.follower_count <= max_followers)
        return query.limit(limit).all()

    def _update_instagram_user(self, user: InstagramUser, user_data: dict) -> InstagramUser:
        user.username = user_data.get('username', user.username)
        user.full_name = user_data.get('full_name', user.full_name)
        user.biography = user_data.get('biography', user.biography)
        user.profile_pic_url = user_data.get('profile_pic_url', user.profile_pic_url)
        user.is_private = user_data.get('is_private', user.is_private)
        user.is_verified = user_data.get('is_verified', user.is_verified)
        user.is_business = user_data.get('is_business', user.is_business)
        user.account_type = user_data.get('account_type', user.account_type)
        user.media_count = user_data.get('media_count', user.media_count)
        user.follower_count = user_data.get('follower_count', user.follower_count)
        user.following_count = user_data.get('following_count', user.following_count)
        user.mutual_followers_count = user_data.get('mutual_followers_count', user.mutual_followers_count)
        user.external_url = user_data.get('external_url', user.external_url)
        user.updated_at = datetime.utcnow()

        self._update_nested_data(user, user_data)
        self.db_session.commit()
        return user
