# models/instagram.py
"""
Instagram API 응답 데이터를 위한 SQLAlchemy ORM 모델
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, BigInteger, DateTime, 
    ForeignKey, Text, JSON, Numeric, UniqueConstraint, Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class InstagramUser(Base):
    """Instagram 사용자 기본 정보"""
    __tablename__ = 'InstagramUsers'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    pk = Column(String(100), unique=True, nullable=False, index=True, 
                comment='Instagram 사용자 PK')
    pk_id = Column(String(100), comment='Instagram 사용자 ID')
    username = Column(String(100), unique=True, nullable=False, index=True)
    full_name = Column(String(255))
    is_private = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False, index=True)
    is_business = Column(Boolean, default=False, index=True)
    account_type = Column(Integer, comment='계정 타입 (0: 일반, 1: 비즈니스, 2: 크리에이터)')
    biography = Column(Text)
    profile_pic_url = Column(String(500))
    profile_pic_id = Column(String(100))
    has_anonymous_profile_picture = Column(Boolean, default=False)
    media_count = Column(Integer, default=0)
    follower_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    mutual_followers_count = Column(Integer, default=0)
    following_tag_count = Column(Integer, default=0)
    is_favorite = Column(Boolean, default=False)
    is_interest_account = Column(Boolean, default=False)
    is_bestie = Column(Boolean, default=False)
    is_supervision_features_enabled = Column(Boolean, default=False)
    profile_pic_url_wrapped = Column(String(500))
    external_url = Column(String(500))
    external_lynx_url = Column(String(500))
    show_fb_link_on_profile = Column(Boolean, default=False)
    primary_profile_link_type = Column(Integer)
    follow_friction_type = Column(Integer)
    has_biography_translation = Column(Boolean, default=False)
    total_igtv_videos = Column(Integer, default=0)
    has_igtv_series = Column(Boolean, default=False)
    has_videos = Column(Boolean, default=False)
    total_clips_count = Column(Integer, default=0)
    total_ar_effects = Column(Integer, default=0)
    usertags_count = Column(Integer, default=0)
    has_highlight_reels = Column(Boolean, default=False)
    has_guides = Column(Boolean, default=False)
    show_shoppable_feed = Column(Boolean, default=False)
    shoppable_posts_count = Column(Integer, default=0)
    merchant_checkout_style = Column(String(50))
    seller_shoppable_feed_type = Column(String(50))
    num_visible_storefront_products = Column(Integer, default=0)
    has_active_affiliate_shop = Column(Boolean, default=False)
    is_eligible_for_smb_support_flow = Column(Boolean, default=False)
    is_eligible_for_lead_center = Column(Boolean, default=False)
    is_experienced_advertiser = Column(Boolean, default=False)
    lead_details_app_id = Column(String(100))
    displayed_action_button_type = Column(String(50))
    direct_messaging = Column(String(50))
    fb_page_call_to_action_id = Column(String(100))
    is_call_to_action_enabled = Column(Boolean, default=False)
    is_profile_audio_call_enabled = Column(Boolean, default=False)
    interop_messaging_user_fbid = Column(BigInteger)
    can_add_fb_group_link_on_profile = Column(Boolean, default=False)
    is_facebook_onboarded_charity = Column(Boolean, default=False)
    has_active_charity_business_profile_fundraiser = Column(Boolean, default=False)
    transparency_product_enabled = Column(Boolean, default=False)
    is_potential_business = Column(Boolean, default=False)
    request_contact_enabled = Column(Boolean, default=False)
    is_memorialized = Column(Boolean, default=False)
    open_external_url_with_in_app_browser = Column(Boolean, default=False)
    has_exclusive_feed_content = Column(Boolean, default=False)
    has_fan_club_subscriptions = Column(Boolean, default=False)
    remove_message_entrypoint = Column(Boolean, default=False)
    show_account_transparency_details = Column(Boolean, default=False)
    existing_user_age_collection_enabled = Column(Boolean, default=False)
    show_post_insights_entry_point = Column(Boolean, default=False)
    has_public_tab_threads = Column(Boolean, default=False)
    auto_expand_chaining = Column(Boolean, default=False)
    is_new_to_instagram = Column(Boolean, default=False)
    highlight_reshare_disabled = Column(Boolean, default=False)
    has_nft_posts = Column(Boolean, default=False)
    has_music_on_profile = Column(Boolean, default=False)
    include_direct_blacklist_status = Column(Boolean, default=False)
    profile_context = Column(String(255))
    professional_conversion_suggested_account_type = Column(Integer)
    can_hide_category = Column(Boolean, default=False)
    can_hide_public_contacts = Column(Boolean, default=False)
    should_show_category = Column(Boolean, default=False)
    is_category_tappable = Column(Boolean, default=False)
    should_show_public_contacts = Column(Boolean, default=False)
    
    # 관계
    business_contacts = relationship(
        'InstagramBusinessContact', 
        back_populates='user', 
        cascade='all, delete-orphan'
    )
    hd_profile_pics = relationship(
        'InstagramHDProfilePic', 
        back_populates='user', 
        cascade='all, delete-orphan'
    )
    charity_fundraisers = relationship(
        'InstagramCharityFundraiser', 
        back_populates='user', 
        cascade='all, delete-orphan'
    )
    fan_clubs = relationship(
        'InstagramFanClub', 
        back_populates='user', 
        cascade='all, delete-orphan'
    )
    bio_links = relationship(
        'InstagramBioLink', 
        back_populates='user', 
        cascade='all, delete-orphan'
    )
    profile_context_links = relationship(
        'InstagramProfileContextLink', 
        back_populates='user', 
        cascade='all, delete-orphan'
    )
    profile_context_mutual_follows = relationship(
        'InstagramProfileContextMutualFollow', 
        back_populates='user', 
        cascade='all, delete-orphan'
    )
    profile_context_facepile_users = relationship(
        'InstagramProfileContextFacepileUser', 
        back_populates='user', 
        cascade='all, delete-orphan'
    )
    creator_shopping_info = relationship(
        'InstagramCreatorShoppingInfo', 
        back_populates='user', 
        uselist=False, 
        cascade='all, delete-orphan'
    )
    pinned_channels = relationship(
        'InstagramPinnedChannel', 
        back_populates='user', 
        uselist=False, 
        cascade='all, delete-orphan'
    )
    account_badges = relationship(
        'InstagramAccountBadge', 
        back_populates='user', 
        cascade='all, delete-orphan'
    )
    user_pronouns = relationship(
        'InstagramUserPronoun', 
        back_populates='user', 
        cascade='all, delete-orphan'
    )
    api_search_results = relationship(
        'InstagramAPISearchResult', 
        back_populates='user', 
        cascade='all, delete-orphan'
    )
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_username_pk', 'username', 'pk'),
        Index('idx_verified_business', 'is_verified', 'is_business'),
        Index('idx_created_at', 'created_at'),
    )


class InstagramBusinessContact(Base):
    """비즈니스 연락처 정보"""
    __tablename__ = 'InstagramBusinessContacts'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('InstagramUsers.id', ondelete='CASCADE'), 
                     nullable=False, index=True)
    address_street = Column(String(255))
    business_contact_method = Column(String(50))
    city_id = Column(String(100))
    city_name = Column(String(100))
    contact_phone_number = Column(String(20))
    public_email = Column(String(255))
    public_phone_country_code = Column(String(10))
    public_phone_number = Column(String(20))
    whatsapp_number = Column(String(20))
    zip = Column(String(20))
    instagram_location_id = Column(String(100))
    latitude = Column(Numeric(10, 6))
    longitude = Column(Numeric(10, 6))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship('InstagramUser', back_populates='business_contacts')


class InstagramHDProfilePic(Base):
    """HD 프로필 사진 버전"""
    __tablename__ = 'InstagramHDProfilePics'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('InstagramUsers.id', ondelete='CASCADE'), 
                     nullable=False, index=True)
    width = Column(Integer)
    height = Column(Integer)
    url = Column(String(500))
    url_wrapped = Column(String(500))
    url_downloadable = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('InstagramUser', back_populates='hd_profile_pics')


class InstagramCharityFundraiser(Base):
    """자선 펀드레이저 정보"""
    __tablename__ = 'InstagramCharityFundraisers'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('InstagramUsers.id', ondelete='CASCADE'), 
                     nullable=False, index=True)
    charity_pk = Column(String(100))
    is_facebook_onboarded_charity = Column(Boolean, default=False)
    has_active_fundraiser = Column(Boolean, default=False)
    can_viewer_donate = Column(Boolean, default=False)
    donation_disabled_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship('InstagramUser', back_populates='charity_fundraisers')


class InstagramFanClub(Base):
    """팬 클럽 정보"""
    __tablename__ = 'InstagramFanClubs'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('InstagramUsers.id', ondelete='CASCADE'), 
                     nullable=False, index=True)
    fan_club_id = Column(String(100))
    fan_club_name = Column(String(255))
    is_fan_club_referral_eligible = Column(Boolean)
    fan_consideration_page_revamp_eligiblity = Column(Boolean)
    is_fan_club_gifting_eligible = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship('InstagramUser', back_populates='fan_clubs')


class InstagramBioLink(Base):
    """바이오 링크"""
    __tablename__ = 'InstagramBioLinks'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('InstagramUsers.id', ondelete='CASCADE'), 
                     nullable=False, index=True)
    link_id = Column(String(100))
    url = Column(String(500))
    lynx_url = Column(String(500))
    link_type = Column(String(50))
    title = Column(String(255))
    group_id = Column(String(100))
    open_external_url_with_in_app_browser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('InstagramUser', back_populates='bio_links')


class InstagramProfileContextLink(Base):
    """프로필 컨텍스트 링크"""
    __tablename__ = 'InstagramProfileContextLinks'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('InstagramUsers.id', ondelete='CASCADE'), 
                     nullable=False, index=True)
    start_pos = Column(Integer)
    end_pos = Column(Integer)
    username = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('InstagramUser', back_populates='profile_context_links')


class InstagramProfileContextMutualFollow(Base):
    """프로필 컨텍스트 상호 팔로우"""
    __tablename__ = 'InstagramProfileContextMutualFollows'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('InstagramUsers.id', ondelete='CASCADE'), 
                     nullable=False, index=True)
    mutual_follow_user_id = Column(BigInteger, 
                                   ForeignKey('InstagramUsers.id', ondelete='CASCADE'), 
                                   nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('InstagramUser', back_populates='profile_context_mutual_follows')


class InstagramProfileContextFacepileUser(Base):
    """프로필 컨텍스트 페이스파일 사용자"""
    __tablename__ = 'InstagramProfileContextFacepileUsers'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('InstagramUsers.id', ondelete='CASCADE'), 
                     nullable=False, index=True)
    facepile_user_pk = Column(String(100))
    facepile_username = Column(String(100))
    facepile_full_name = Column(String(255))
    facepile_is_private = Column(Boolean, default=False)
    facepile_pk_id = Column(String(100))
    facepile_profile_pic_url = Column(String(500))
    facepile_profile_pic_id = Column(String(100))
    facepile_is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('InstagramUser', back_populates='profile_context_facepile_users')


class InstagramCreatorShoppingInfo(Base):
    """크리에이터 쇼핑 정보"""
    __tablename__ = 'InstagramCreatorShoppingInfo'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('InstagramUsers.id', ondelete='CASCADE'), 
                     nullable=False, unique=True, index=True)
    linked_merchant_accounts = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship('InstagramUser', back_populates='creator_shopping_info')


class InstagramPinnedChannel(Base):
    """핀 고정된 채널"""
    __tablename__ = 'InstagramPinnedChannels'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('InstagramUsers.id', ondelete='CASCADE'), 
                     nullable=False, unique=True, index=True)
    pinned_channels_list = Column(JSON)
    has_public_channels = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship('InstagramUser', back_populates='pinned_channels')


class InstagramAccountBadge(Base):
    """계정 배지"""
    __tablename__ = 'InstagramAccountBadges'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('InstagramUsers.id', ondelete='CASCADE'), 
                     nullable=False, index=True)
    badge_type = Column(String(100))
    badge_name = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('InstagramUser', back_populates='account_badges')


class InstagramUserPronoun(Base):
    """사용자 대명사"""
    __tablename__ = 'InstagramUserPronouns'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('InstagramUsers.id', ondelete='CASCADE'), 
                     nullable=False, index=True)
    pronoun = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('InstagramUser', back_populates='user_pronouns')


class InstagramAPISearchResult(Base):
    """API 조회 기록"""
    __tablename__ = 'InstagramAPISearchResults'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('InstagramUsers.id', ondelete='CASCADE'), 
                     nullable=False, index=True)
    status = Column(String(50), default='success')
    raw_response = Column(JSON)
    api_called_at = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('InstagramUser', back_populates='api_search_results')
