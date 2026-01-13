# services/instagram_service.py
"""
Instagram API 응답 데이터 처리 및 DB 저장 서비스
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from models.instagram import (
    InstagramUser, InstagramBusinessContact, InstagramHDProfilePic,
    InstagramCharityFundraiser, InstagramFanClub, InstagramBioLink,
    InstagramProfileContextLink, InstagramProfileContextMutualFollow,
    InstagramProfileContextFacepileUser, InstagramCreatorShoppingInfo,
    InstagramPinnedChannel, InstagramAccountBadge, InstagramUserPronoun,
    InstagramAPISearchResult
)

logger = logging.getLogger(__name__)


class InstagramService:
    """Instagram 데이터 처리 서비스"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def insert_instagram_user(self, user_data: Dict[str, Any]) -> Optional[InstagramUser]:
        """
        API 응답 데이터로부터 사용자 정보 삽입
        
        Args:
            user_data: Instagram API 응답의 'user' 객체
            
        Returns:
            생성된 InstagramUser 객체 또는 None
        """
        try:
            # 기존 사용자 확인
            existing_user = self.db.query(InstagramUser).filter(
                InstagramUser.pk == user_data.get('pk')
            ).first()
            
            if existing_user:
                logger.info(f"사용자 {user_data.get('username')} 이미 존재. 업데이트 중...")
                return self._update_instagram_user(existing_user, user_data)
            
            # 새 사용자 생성
            new_user = InstagramUser(
                pk=user_data.get('pk'),
                pk_id=user_data.get('pk_id'),
                username=user_data.get('username'),
                full_name=user_data.get('full_name'),
                is_private=user_data.get('is_private', False),
                is_verified=user_data.get('is_verified', False),
                is_business=user_data.get('is_business', False),
                account_type=user_data.get('account_type'),
                biography=user_data.get('biography'),
                profile_pic_url=user_data.get('profile_pic_url'),
                profile_pic_id=user_data.get('profile_pic_id'),
                has_anonymous_profile_picture=user_data.get('has_anonymous_profile_picture', False),
                media_count=user_data.get('media_count', 0),
                follower_count=user_data.get('follower_count', 0),
                following_count=user_data.get('following_count', 0),
                mutual_followers_count=user_data.get('mutual_followers_count', 0),
                following_tag_count=user_data.get('following_tag_count', 0),
                is_favorite=user_data.get('is_favorite', False),
                is_interest_account=user_data.get('is_interest_account', False),
                is_bestie=user_data.get('is_bestie', False),
                is_supervision_features_enabled=user_data.get('is_supervision_features_enabled', False),
                profile_pic_url_wrapped=user_data.get('profile_pic_url_wrapped'),
                external_url=user_data.get('external_url'),
                external_lynx_url=user_data.get('external_lynx_url'),
                show_fb_link_on_profile=user_data.get('show_fb_link_on_profile', False),
                primary_profile_link_type=user_data.get('primary_profile_link_type'),
                follow_friction_type=user_data.get('follow_friction_type'),
                has_biography_translation=user_data.get('has_biography_translation', False),
                total_igtv_videos=user_data.get('total_igtv_videos', 0),
                has_igtv_series=user_data.get('has_igtv_series', False),
                has_videos=user_data.get('has_videos', False),
                total_clips_count=user_data.get('total_clips_count', 0),
                total_ar_effects=user_data.get('total_ar_effects', 0),
                usertags_count=user_data.get('usertags_count', 0),
                has_highlight_reels=user_data.get('has_highlight_reels', False),
                has_guides=user_data.get('has_guides', False),
                show_shoppable_feed=user_data.get('show_shoppable_feed', False),
                shoppable_posts_count=user_data.get('shoppable_posts_count', 0),
                merchant_checkout_style=user_data.get('merchant_checkout_style'),
                seller_shoppable_feed_type=user_data.get('seller_shoppable_feed_type'),
                num_visible_storefront_products=user_data.get('num_visible_storefront_products', 0),
                has_active_affiliate_shop=user_data.get('has_active_affiliate_shop', False),
                is_eligible_for_smb_support_flow=user_data.get('is_eligible_for_smb_support_flow', False),
                is_eligible_for_lead_center=user_data.get('is_eligible_for_lead_center', False),
                is_experienced_advertiser=user_data.get('is_experienced_advertiser', False),
                lead_details_app_id=user_data.get('lead_details_app_id'),
                displayed_action_button_type=user_data.get('displayed_action_button_type'),
                direct_messaging=user_data.get('direct_messaging'),
                fb_page_call_to_action_id=user_data.get('fb_page_call_to_action_id'),
                is_call_to_action_enabled=user_data.get('is_call_to_action_enabled', False),
                is_profile_audio_call_enabled=user_data.get('is_profile_audio_call_enabled', False),
                interop_messaging_user_fbid=user_data.get('interop_messaging_user_fbid'),
                can_add_fb_group_link_on_profile=user_data.get('can_add_fb_group_link_on_profile', False),
                is_facebook_onboarded_charity=user_data.get('is_facebook_onboarded_charity', False),
                has_active_charity_business_profile_fundraiser=user_data.get('has_active_charity_business_profile_fundraiser', False),
                transparency_product_enabled=user_data.get('transparency_product_enabled', False),
                is_potential_business=user_data.get('is_potential_business', False),
                request_contact_enabled=user_data.get('request_contact_enabled', False),
                is_memorialized=user_data.get('is_memorialized', False),
                open_external_url_with_in_app_browser=user_data.get('open_external_url_with_in_app_browser', False),
                has_exclusive_feed_content=user_data.get('has_exclusive_feed_content', False),
                has_fan_club_subscriptions=user_data.get('has_fan_club_subscriptions', False),
                remove_message_entrypoint=user_data.get('remove_message_entrypoint', False),
                show_account_transparency_details=user_data.get('show_account_transparency_details', False),
                existing_user_age_collection_enabled=user_data.get('existing_user_age_collection_enabled', False),
                show_post_insights_entry_point=user_data.get('show_post_insights_entry_point', False),
                has_public_tab_threads=user_data.get('has_public_tab_threads', False),
                auto_expand_chaining=user_data.get('auto_expand_chaining', False),
                is_new_to_instagram=user_data.get('is_new_to_instagram', False),
                highlight_reshare_disabled=user_data.get('highlight_reshare_disabled', False),
                has_nft_posts=user_data.get('has_nft_posts', False),
                has_music_on_profile=user_data.get('has_music_on_profile', False),
                include_direct_blacklist_status=user_data.get('include_direct_blacklist_status', False),
                profile_context=user_data.get('profile_context'),
                professional_conversion_suggested_account_type=user_data.get('professional_conversion_suggested_account_type'),
                can_hide_category=user_data.get('can_hide_category', False),
                can_hide_public_contacts=user_data.get('can_hide_public_contacts', False),
                should_show_category=user_data.get('should_show_category', False),
                is_category_tappable=user_data.get('is_category_tappable', False),
                should_show_public_contacts=user_data.get('should_show_public_contacts', False),
            )
            
            self.db.add(new_user)
            self.db.flush()
            
            # 관련 데이터 처리
            self._insert_related_data(new_user, user_data)
            
            self.db.commit()
            logger.info(f"사용자 {user_data.get('username')} 성공적으로 저장됨")
            return new_user
            
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"무결성 오류: {str(e)}")
            return None
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"데이터베이스 오류: {str(e)}")
            return None
        except Exception as e:
            self.db.rollback()
            logger.error(f"예상치 못한 오류: {str(e)}")
            return None
    
    def _update_instagram_user(self, user: InstagramUser, user_data: Dict[str, Any]) -> InstagramUser:
        """기존 사용자 정보 업데이트"""
        user.full_name = user_data.get('full_name', user.full_name)
        user.is_private = user_data.get('is_private', user.is_private)
        user.is_verified = user_data.get('is_verified', user.is_verified)
        user.biography = user_data.get('biography', user.biography)
        user.profile_pic_url = user_data.get('profile_pic_url', user.profile_pic_url)
        user.media_count = user_data.get('media_count', user.media_count)
        user.follower_count = user_data.get('follower_count', user.follower_count)
        user.following_count = user_data.get('following_count', user.following_count)
        user.mutual_followers_count = user_data.get('mutual_followers_count', user.mutual_followers_count)
        
        self._insert_related_data(user, user_data)
        self.db.commit()
        return user
    
    def _insert_related_data(self, user: InstagramUser, user_data: Dict[str, Any]) -> None:
        """관련 데이터(연락처, 링크, 배지 등) 삽입"""
        
        # 비즈니스 연락처
        if any([user_data.get(f) for f in ['address_street', 'city_name', 'contact_phone_number']]):
            self._insert_business_contact(user, user_data)
        
        # HD 프로필 사진
        if 'hd_profile_pic_versions' in user_data and user_data['hd_profile_pic_versions']:
            self._insert_hd_profile_pics(user, user_data['hd_profile_pic_versions'])
        
        # 자선 정보
        if 'charity_profile_fundraiser_info' in user_data:
            self._insert_charity_fundraiser(user, user_data['charity_profile_fundraiser_info'])
        
        # 팬 클럽 정보
        if 'fan_club_info' in user_data:
            self._insert_fan_club(user, user_data['fan_club_info'])
        
        # 바이오 링크
        if 'bio_links' in user_data and user_data['bio_links']:
            self._insert_bio_links(user, user_data['bio_links'])
        
        # 프로필 컨텍스트 링크
        if 'profile_context_links_with_user_ids' in user_data and user_data['profile_context_links_with_user_ids']:
            self._insert_profile_context_links(user, user_data['profile_context_links_with_user_ids'])
        
        # 프로필 컨텍스트 상호 팔로우
        if 'profile_context_mutual_follow_ids' in user_data and user_data['profile_context_mutual_follow_ids']:
            self._insert_profile_context_mutual_follows(user, user_data['profile_context_mutual_follow_ids'])
        
        # 프로필 컨텍스트 페이스파일 사용자
        if 'profile_context_facepile_users' in user_data and user_data['profile_context_facepile_users']:
            self._insert_facepile_users(user, user_data['profile_context_facepile_users'])
        
        # 크리에이터 쇼핑 정보
        if 'creator_shopping_info' in user_data:
            self._insert_creator_shopping_info(user, user_data['creator_shopping_info'])
        
        # 핀 고정된 채널
        if 'pinned_channels_info' in user_data:
            self._insert_pinned_channels(user, user_data['pinned_channels_info'])
        
        # 계정 배지
        if 'account_badges' in user_data and user_data['account_badges']:
            self._insert_account_badges(user, user_data['account_badges'])
        
        # 사용자 대명사
        if 'pronouns' in user_data and user_data['pronouns']:
            self._insert_pronouns(user, user_data['pronouns'])
    
    def _insert_business_contact(self, user: InstagramUser, user_data: Dict[str, Any]) -> None:
        """비즈니스 연락처 삽입"""
        contact_data = {
            'address_street': user_data.get('address_street'),
            'business_contact_method': user_data.get('business_contact_method'),
            'city_id': user_data.get('city_id'),
            'city_name': user_data.get('city_name'),
            'contact_phone_number': user_data.get('contact_phone_number'),
            'public_email': user_data.get('public_email'),
            'public_phone_country_code': user_data.get('public_phone_country_code'),
            'public_phone_number': user_data.get('public_phone_number'),
            'whatsapp_number': user_data.get('whatsapp_number'),
            'zip': user_data.get('zip'),
            'instagram_location_id': user_data.get('instagram_location_id'),
            'latitude': user_data.get('latitude'),
            'longitude': user_data.get('longitude'),
        }
        
        business_contact = InstagramBusinessContact(user_id=user.id, **contact_data)
        user.business_contacts.append(business_contact)
    
    def _insert_hd_profile_pics(self, user: InstagramUser, pic_versions: List[Dict[str, Any]]) -> None:
        """HD 프로필 사진 버전 삽입"""
        for pic in pic_versions:
            hd_pic = InstagramHDProfilePic(
                user_id=user.id,
                width=pic.get('width'),
                height=pic.get('height'),
                url=pic.get('url'),
                url_wrapped=pic.get('url_wrapped'),
                url_downloadable=pic.get('url_downloadable')
            )
            user.hd_profile_pics.append(hd_pic)
    
    def _insert_charity_fundraiser(self, user: InstagramUser, charity_data: Dict[str, Any]) -> None:
        """자선 펀드레이저 정보 삽입"""
        fundraiser = InstagramCharityFundraiser(
            user_id=user.id,
            charity_pk=charity_data.get('pk'),
            is_facebook_onboarded_charity=charity_data.get('is_facebook_onboarded_charity', False),
            has_active_fundraiser=charity_data.get('has_active_fundraiser', False),
            can_viewer_donate=charity_data.get('consumption_sheet_config', {}).get('can_viewer_donate', False),
            donation_disabled_message=charity_data.get('consumption_sheet_config', {}).get('donation_disabled_message')
        )
        user.charity_fundraisers.append(fundraiser)
    
    def _insert_fan_club(self, user: InstagramUser, fan_club_data: Dict[str, Any]) -> None:
        """팬 클럽 정보 삽입"""
        fan_club = InstagramFanClub(
            user_id=user.id,
            fan_club_id=fan_club_data.get('fan_club_id'),
            fan_club_name=fan_club_data.get('fan_club_name'),
            is_fan_club_referral_eligible=fan_club_data.get('is_fan_club_referral_eligible'),
            fan_consideration_page_revamp_eligiblity=fan_club_data.get('fan_consideration_page_revamp_eligiblity'),
            is_fan_club_gifting_eligible=fan_club_data.get('is_fan_club_gifting_eligible')
        )
        user.fan_clubs.append(fan_club)
    
    def _insert_bio_links(self, user: InstagramUser, bio_links: List[Dict[str, Any]]) -> None:
        """바이오 링크 삽입"""
        for link in bio_links:
            bio_link = InstagramBioLink(
                user_id=user.id,
                link_id=link.get('link_id'),
                url=link.get('url'),
                lynx_url=link.get('lynx_url'),
                link_type=link.get('link_type'),
                title=link.get('title'),
                group_id=link.get('group_id'),
                open_external_url_with_in_app_browser=link.get('open_external_url_with_in_app_browser', False)
            )
            user.bio_links.append(bio_link)
    
    def _insert_profile_context_links(self, user: InstagramUser, links: List[Dict[str, Any]]) -> None:
        """프로필 컨텍스트 링크 삽입"""
        for link in links:
            context_link = InstagramProfileContextLink(
                user_id=user.id,
                start_pos=link.get('start'),
                end_pos=link.get('end'),
                username=link.get('username')
            )
            user.profile_context_links.append(context_link)
    
    def _insert_profile_context_mutual_follows(self, user: InstagramUser, mutual_follow_ids: List[int]) -> None:
        """프로필 컨텍스트 상호 팔로우 삽입"""
        for mutual_id in mutual_follow_ids:
            mutual_follow = InstagramProfileContextMutualFollow(
                user_id=user.id,
                mutual_follow_user_id=mutual_id
            )
            user.profile_context_mutual_follows.append(mutual_follow)
    
    def _insert_facepile_users(self, user: InstagramUser, facepile_users: List[Dict[str, Any]]) -> None:
        """프로필 컨텍스트 페이스파일 사용자 삽입"""
        for facepile_user in facepile_users:
            facepile = InstagramProfileContextFacepileUser(
                user_id=user.id,
                facepile_user_pk=facepile_user.get('pk'),
                facepile_username=facepile_user.get('username'),
                facepile_full_name=facepile_user.get('full_name'),
                facepile_is_private=facepile_user.get('is_private', False),
                facepile_pk_id=facepile_user.get('pk_id'),
                facepile_profile_pic_url=facepile_user.get('profile_pic_url'),
                facepile_profile_pic_id=facepile_user.get('profile_pic_id'),
                facepile_is_verified=facepile_user.get('is_verified', False)
            )
            user.profile_context_facepile_users.append(facepile)
    
    def _insert_creator_shopping_info(self, user: InstagramUser, shopping_info: Dict[str, Any]) -> None:
        """크리에이터 쇼핑 정보 삽입"""
        creator_shopping = InstagramCreatorShoppingInfo(
            user_id=user.id,
            linked_merchant_accounts=shopping_info.get('linked_merchant_accounts', [])
        )
        user.creator_shopping_info = creator_shopping
    
    def _insert_pinned_channels(self, user: InstagramUser, pinned_info: Dict[str, Any]) -> None:
        """핀 고정된 채널 삽입"""
        pinned_channels = InstagramPinnedChannel(
            user_id=user.id,
            pinned_channels_list=pinned_info.get('pinned_channels_list', []),
            has_public_channels=pinned_info.get('has_public_channels', False)
        )
        user.pinned_channels = pinned_channels
    
    def _insert_account_badges(self, user: InstagramUser, badges: List[Any]) -> None:
        """계정 배지 삽입"""
        for badge in badges:
            if isinstance(badge, dict):
                account_badge = InstagramAccountBadge(
                    user_id=user.id,
                    badge_type=badge.get('badge_type'),
                    badge_name=badge.get('badge_name')
                )
            else:
                account_badge = InstagramAccountBadge(
                    user_id=user.id,
                    badge_type=str(badge)
                )
            user.account_badges.append(account_badge)
    
    def _insert_pronouns(self, user: InstagramUser, pronouns: List[str]) -> None:
        """사용자 대명사 삽입"""
        for pronoun in pronouns:
            user_pronoun = InstagramUserPronoun(
                user_id=user.id,
                pronoun=pronoun
            )
            user.user_pronouns.append(user_pronoun)
    
    def insert_api_search_result(self, user_id: int, status: str, 
                                raw_response: Optional[Dict[str, Any]] = None) -> InstagramAPISearchResult:
        """API 조회 기록 삽입"""
        search_result = InstagramAPISearchResult(
            user_id=user_id,
            status=status,
            raw_response=raw_response
        )
        self.db.add(search_result)
        self.db.commit()
        return search_result
    
    def get_instagram_user(self, username: str) -> Optional[InstagramUser]:
        """사용자명으로 Instagram 사용자 조회"""
        return self.db.query(InstagramUser).filter(
            InstagramUser.username == username
        ).first()
    
    def get_instagram_user_by_pk(self, pk: str) -> Optional[InstagramUser]:
        """PK로 Instagram 사용자 조회"""
        return self.db.query(InstagramUser).filter(
            InstagramUser.pk == pk
        ).first()
    
    def get_verified_users(self, limit: int = 100) -> List[InstagramUser]:
        """인증된 사용자 목록 조회"""
        return self.db.query(InstagramUser).filter(
            InstagramUser.is_verified == True
        ).limit(limit).all()
    
    def get_business_users(self, limit: int = 100) -> List[InstagramUser]:
        """비즈니스 계정 목록 조회"""
        return self.db.query(InstagramUser).filter(
            InstagramUser.is_business == True
        ).limit(limit).all()
    
    def search_users_by_follower_count(self, min_followers: int = 0, 
                                      max_followers: int = None, 
                                      limit: int = 100) -> List[InstagramUser]:
        """팔로워 수로 사용자 검색"""
        query = self.db.query(InstagramUser).filter(
            InstagramUser.follower_count >= min_followers
        )
        if max_followers:
            query = query.filter(InstagramUser.follower_count <= max_followers)
        return query.limit(limit).all()
