# Instagram Channel 데이터베이스 스키마 설계

## 1. 메인 테이블 - InstagramUsers (인스타그램 사용자 정보)

```sql
CREATE TABLE `InstagramUsers` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `pk` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL UNIQUE COMMENT 'Instagram 사용자 PK',
  `pk_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'Instagram 사용자 ID',
  `username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '사용자명',
  `full_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '전체 이름',
  `is_private` tinyint(1) DEFAULT '0' COMMENT '비공개 계정 여부',
  `is_verified` tinyint(1) DEFAULT '0' COMMENT '인증 배지 여부',
  `is_business` tinyint(1) DEFAULT '0' COMMENT '비즈니스 계정 여부',
  `account_type` int DEFAULT NULL COMMENT '계정 타입 (0: 일반, 1: 비즈니스, 2: 크리에이터)',
  `biography` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '프로필 소개',
  `profile_pic_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '프로필 사진 URL',
  `profile_pic_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '프로필 사진 ID',
  `has_anonymous_profile_picture` tinyint(1) DEFAULT '0' COMMENT '익명 프로필 사진 여부',
  `media_count` int DEFAULT 0 COMMENT '게시물 수',
  `follower_count` int DEFAULT 0 COMMENT '팔로워 수',
  `following_count` int DEFAULT 0 COMMENT '팔로잉 수',
  `mutual_followers_count` int DEFAULT 0 COMMENT '상호 팔로워 수',
  `following_tag_count` int DEFAULT 0 COMMENT '팔로잉 태그 수',
  `is_favorite` tinyint(1) DEFAULT '0' COMMENT '즐겨찾기 여부',
  `is_interest_account` tinyint(1) DEFAULT '0' COMMENT '관심 계정 여부',
  `is_bestie` tinyint(1) DEFAULT '0' COMMENT '베스트 친구 여부',
  `is_supervision_features_enabled` tinyint(1) DEFAULT '0' COMMENT '감시 기능 활성화 여부',
  `profile_pic_url_wrapped` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '감싼 프로필 사진 URL',
  `external_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '외부 링크',
  `external_lynx_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'Lynx 외부 링크',
  `show_fb_link_on_profile` tinyint(1) DEFAULT '0' COMMENT '프로필에 Facebook 링크 표시 여부',
  `primary_profile_link_type` int DEFAULT NULL COMMENT '주요 프로필 링크 타입',
  `follow_friction_type` int DEFAULT NULL COMMENT '팔로우 마찰 타입',
  `has_biography_translation` tinyint(1) DEFAULT '0' COMMENT '소개 번역 가능 여부',
  `total_igtv_videos` int DEFAULT 0 COMMENT 'IGTV 비디오 총 개수',
  `has_igtv_series` tinyint(1) DEFAULT '0' COMMENT 'IGTV 시리즈 여부',
  `has_videos` tinyint(1) DEFAULT '0' COMMENT '비디오 보유 여부',
  `total_clips_count` int DEFAULT 0 COMMENT '클립 총 개수',
  `total_ar_effects` int DEFAULT 0 COMMENT 'AR 이펙트 총 개수',
  `usertags_count` int DEFAULT 0 COMMENT '태그된 게시물 수',
  `has_highlight_reels` tinyint(1) DEFAULT '0' COMMENT '하이라이트 릴 여부',
  `has_guides` tinyint(1) DEFAULT '0' COMMENT '가이드 여부',
  `show_shoppable_feed` tinyint(1) DEFAULT '0' COMMENT '쇼핑 가능한 피드 표시 여부',
  `shoppable_posts_count` int DEFAULT 0 COMMENT '쇼핑 가능한 게시물 수',
  `merchant_checkout_style` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '판매자 결제 스타일',
  `seller_shoppable_feed_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '판매자 쇼핑 피드 타입',
  `num_visible_storefront_products` int DEFAULT 0 COMMENT '표시 가능한 상점 상품 수',
  `has_active_affiliate_shop` tinyint(1) DEFAULT '0' COMMENT '활성 제휴 상점 여부',
  `is_eligible_for_smb_support_flow` tinyint(1) DEFAULT '0' COMMENT 'SMB 지원 흐름 적격 여부',
  `is_eligible_for_lead_center` tinyint(1) DEFAULT '0' COMMENT '리드 센터 적격 여부',
  `is_experienced_advertiser` tinyint(1) DEFAULT '0' COMMENT '경험 많은 광고주 여부',
  `lead_details_app_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '리드 세부정보 앱 ID',
  `displayed_action_button_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '표시된 작업 버튼 타입',
  `direct_messaging` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '직접 메시징',
  `fb_page_call_to_action_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'Facebook 페이지 CTA ID',
  `is_call_to_action_enabled` tinyint(1) DEFAULT '0' COMMENT 'CTA 활성화 여부',
  `is_profile_audio_call_enabled` tinyint(1) DEFAULT '0' COMMENT '프로필 오디오 호출 활성화 여부',
  `interop_messaging_user_fbid` bigint COMMENT 'Interop 메시징 사용자 Facebook ID',
  `can_add_fb_group_link_on_profile` tinyint(1) DEFAULT '0' COMMENT '프로필에 Facebook 그룹 링크 추가 가능 여부',
  `is_facebook_onboarded_charity` tinyint(1) DEFAULT '0' COMMENT 'Facebook 온보딩 자선 단체 여부',
  `has_active_charity_business_profile_fundraiser` tinyint(1) DEFAULT '0' COMMENT '활성 자선 비즈니스 프로필 펀드레이저 여부',
  `transparency_product_enabled` tinyint(1) DEFAULT '0' COMMENT '투명성 제품 활성화 여부',
  `is_potential_business` tinyint(1) DEFAULT '0' COMMENT '잠재적 비즈니스 여부',
  `request_contact_enabled` tinyint(1) DEFAULT '0' COMMENT '연락처 요청 활성화 여부',
  `is_memorialized` tinyint(1) DEFAULT '0' COMMENT '추도 계정 여부',
  `open_external_url_with_in_app_browser` tinyint(1) DEFAULT '0' COMMENT '앱 내 브라우저로 외부 URL 열기 여부',
  `has_exclusive_feed_content` tinyint(1) DEFAULT '0' COMMENT '독점 피드 콘텐츠 여부',
  `has_fan_club_subscriptions` tinyint(1) DEFAULT '0' COMMENT '팬 클럽 구독 여부',
  `remove_message_entrypoint` tinyint(1) DEFAULT '0' COMMENT '메시지 진입점 제거 여부',
  `is_bestie_v2` tinyint(1) DEFAULT '0' COMMENT '베스트 친구 v2 여부',
  `show_account_transparency_details` tinyint(1) DEFAULT '0' COMMENT '계정 투명성 세부정보 표시 여부',
  `existing_user_age_collection_enabled` tinyint(1) DEFAULT '0' COMMENT '기존 사용자 나이 수집 활성화 여부',
  `show_post_insights_entry_point` tinyint(1) DEFAULT '0' COMMENT '게시물 인사이트 진입점 표시 여부',
  `has_public_tab_threads` tinyint(1) DEFAULT '0' COMMENT '공개 탭 스레드 여부',
  `auto_expand_chaining` tinyint(1) DEFAULT '0' COMMENT '자동 확장 체이닝 여부',
  `is_new_to_instagram` tinyint(1) DEFAULT '0' COMMENT 'Instagram 신규 여부',
  `highlight_reshare_disabled` tinyint(1) DEFAULT '0' COMMENT '하이라이트 재공유 비활성화 여부',
  `has_nft_posts` tinyint(1) DEFAULT '0' COMMENT 'NFT 게시물 여부',
  `has_music_on_profile` tinyint(1) DEFAULT '0' COMMENT '프로필에 음악 여부',
  `include_direct_blacklist_status` tinyint(1) DEFAULT '0' COMMENT '직접 블랙리스트 상태 포함 여부',
  `profile_context` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '프로필 컨텍스트',
  `professional_conversion_suggested_account_type` int DEFAULT NULL COMMENT '전문가 전환 제안 계정 타입',
  `can_hide_category` tinyint(1) DEFAULT '0' COMMENT '카테고리 숨기기 가능 여부',
  `can_hide_public_contacts` tinyint(1) DEFAULT '0' COMMENT '공개 연락처 숨기기 가능 여부',
  `should_show_category` tinyint(1) DEFAULT '0' COMMENT '카테고리 표시 여부',
  `is_category_tappable` tinyint(1) DEFAULT '0' COMMENT '카테고리 탭 가능 여부',
  `should_show_public_contacts` tinyint(1) DEFAULT '0' COMMENT '공개 연락처 표시 여부',
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP COMMENT '생성 날짜',
  `updated_at` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정 날짜',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_pk` (`pk`),
  UNIQUE KEY `uk_username` (`username`),
  KEY `idx_is_business` (`is_business`),
  KEY `idx_is_verified` (`is_verified`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
```

## 2. 비즈니스 연락처 테이블 - InstagramBusinessContacts

```sql
CREATE TABLE `InstagramBusinessContacts` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL COMMENT '사용자 ID (FK)',
  `address_street` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '거리 주소',
  `business_contact_method` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '비즈니스 연락 방법',
  `city_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '도시 ID',
  `city_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '도시명',
  `contact_phone_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '연락처 전화번호',
  `public_email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '공개 이메일',
  `public_phone_country_code` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '공개 전화 국가 코드',
  `public_phone_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '공개 전화번호',
  `whatsapp_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'WhatsApp 번호',
  `zip` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '우편번호',
  `instagram_location_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'Instagram 위치 ID',
  `latitude` decimal(10,6) COMMENT '위도',
  `longitude` decimal(10,6) COMMENT '경도',
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `InstagramUsers`(`id`) ON DELETE CASCADE,
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
```

## 3. HD 프로필 사진 버전 테이블 - InstagramHDProfilePics

```sql
CREATE TABLE `InstagramHDProfilePics` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL COMMENT '사용자 ID (FK)',
  `width` int COMMENT '너비',
  `height` int COMMENT '높이',
  `url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'URL',
  `url_wrapped` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '감싼 URL',
  `url_downloadable` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '다운로드 가능 URL',
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `InstagramUsers`(`id`) ON DELETE CASCADE,
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
```

## 4. 생략 정보 (Charity Profile Fundraiser) 테이블 - InstagramCharityFundraisers

```sql
CREATE TABLE `InstagramCharityFundraisers` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL COMMENT '사용자 ID (FK)',
  `charity_pk` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '자선 단체 PK',
  `is_facebook_onboarded_charity` tinyint(1) DEFAULT '0',
  `has_active_fundraiser` tinyint(1) DEFAULT '0',
  `can_viewer_donate` tinyint(1) DEFAULT '0',
  `donation_disabled_message` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `InstagramUsers`(`id`) ON DELETE CASCADE,
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
```

## 5. 팬 클럽 정보 테이블 - InstagramFanClubs

```sql
CREATE TABLE `InstagramFanClubs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL COMMENT '사용자 ID (FK)',
  `fan_club_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '팬 클럽 ID',
  `fan_club_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '팬 클럽 이름',
  `is_fan_club_referral_eligible` tinyint(1) DEFAULT NULL COMMENT '팬 클럽 추천 적격 여부',
  `fan_consideration_page_revamp_eligiblity` tinyint(1) DEFAULT NULL COMMENT '팬 고려 페이지 개편 적격 여부',
  `is_fan_club_gifting_eligible` tinyint(1) DEFAULT NULL COMMENT '팬 클럽 선물 적격 여부',
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `InstagramUsers`(`id`) ON DELETE CASCADE,
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
```

## 6. 바이오 링크 테이블 - InstagramBioLinks

```sql
CREATE TABLE `InstagramBioLinks` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL COMMENT '사용자 ID (FK)',
  `link_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '링크 ID',
  `url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'URL',
  `lynx_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'Lynx URL',
  `link_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '링크 타입',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '제목',
  `group_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '그룹 ID',
  `open_external_url_with_in_app_browser` tinyint(1) DEFAULT '0' COMMENT '앱 내 브라우저로 열기 여부',
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `InstagramUsers`(`id`) ON DELETE CASCADE,
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
```

## 7. 프로필 컨텍스트 링크 테이블 - InstagramProfileContextLinks

```sql
CREATE TABLE `InstagramProfileContextLinks` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL COMMENT '사용자 ID (FK)',
  `start_pos` int COMMENT '시작 위치',
  `end_pos` int COMMENT '종료 위치',
  `username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '사용자명',
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `InstagramUsers`(`id`) ON DELETE CASCADE,
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
```

## 8. 프로필 컨텍스트 상호 팔로우 테이블 - InstagramProfileContextMutualFollows

```sql
CREATE TABLE `InstagramProfileContextMutualFollows` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL COMMENT '사용자 ID (FK)',
  `mutual_follow_user_id` bigint NOT NULL COMMENT '상호 팔로우 사용자 ID',
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `InstagramUsers`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`mutual_follow_user_id`) REFERENCES `InstagramUsers`(`id`) ON DELETE CASCADE,
  KEY `idx_user_id` (`user_id`),
  KEY `idx_mutual_follow_user_id` (`mutual_follow_user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
```

## 9. 프로필 컨텍스트 페이스파일 사용자 테이블 - InstagramProfileContextFacepileUsers

```sql
CREATE TABLE `InstagramProfileContextFacepileUsers` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL COMMENT '주 사용자 ID (FK)',
  `facepile_user_pk` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '페이스파일 사용자 PK',
  `facepile_username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '페이스파일 사용자명',
  `facepile_full_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '페이스파일 사용자 전체 이름',
  `facepile_is_private` tinyint(1) DEFAULT '0',
  `facepile_pk_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `facepile_profile_pic_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `facepile_profile_pic_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `facepile_is_verified` tinyint(1) DEFAULT '0',
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `InstagramUsers`(`id`) ON DELETE CASCADE,
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
```

## 10. 크리에이터 쇼핑 정보 테이블 - InstagramCreatorShoppingInfo

```sql
CREATE TABLE `InstagramCreatorShoppingInfo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL COMMENT '사용자 ID (FK)',
  `linked_merchant_accounts` json COMMENT '연결된 판매자 계정 (JSON 배열)',
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `InstagramUsers`(`id`) ON DELETE CASCADE,
  UNIQUE KEY `uk_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
```

## 11. 핀 고정된 채널 정보 테이블 - InstagramPinnedChannels

```sql
CREATE TABLE `InstagramPinnedChannels` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL COMMENT '사용자 ID (FK)',
  `pinned_channels_list` json COMMENT '핀 고정된 채널 목록 (JSON 배열)',
  `has_public_channels` tinyint(1) DEFAULT '0' COMMENT '공개 채널 여부',
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `InstagramUsers`(`id`) ON DELETE CASCADE,
  UNIQUE KEY `uk_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
```

## 12. 계정 배지 테이블 - InstagramAccountBadges

```sql
CREATE TABLE `InstagramAccountBadges` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL COMMENT '사용자 ID (FK)',
  `badge_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '배지 타입',
  `badge_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '배지 이름',
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `InstagramUsers`(`id`) ON DELETE CASCADE,
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
```

## 13. 사용자 대명사 테이블 - InstagramUserPronouns

```sql
CREATE TABLE `InstagramUserPronouns` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL COMMENT '사용자 ID (FK)',
  `pronoun` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '대명사',
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `InstagramUsers`(`id`) ON DELETE CASCADE,
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
```

## 14. 조회 기록 테이블 - InstagramAPISearchResults

```sql
CREATE TABLE `InstagramAPISearchResults` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL COMMENT '사용자 ID (FK)',
  `status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'success' COMMENT 'API 응답 상태',
  `raw_response` json COMMENT 'API 원본 응답 (필요시)',
  `api_called_at` timestamp DEFAULT CURRENT_TIMESTAMP COMMENT 'API 호출 시간',
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `InstagramUsers`(`id`) ON DELETE CASCADE,
  KEY `idx_user_id` (`user_id`),
  KEY `idx_api_called_at` (`api_called_at`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
```

---

## 인덱스 전략

### 주요 인덱스
- `InstagramUsers.pk`: UNIQUE (API PK 기반 검색 최적화)
- `InstagramUsers.username`: UNIQUE (사용자명 검색)
- `InstagramUsers.is_business`: 비즈니스 계정 필터링
- `InstagramUsers.is_verified`: 인증 계정 필터링
- `InstagramUsers.created_at`: 최신 조회 데이터 검색

### 외래키 인덱스
- 모든 FK에 대해 자동으로 인덱스 생성됨

---

## Python ORM 예제 (SQLAlchemy)

```python
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, BigInteger, DateTime, ForeignKey, Text, JSON, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class InstagramUser(Base):
    __tablename__ = 'InstagramUsers'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    pk = Column(String(100), unique=True, nullable=False, comment='Instagram 사용자 PK')
    pk_id = Column(String(100))
    username = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(255))
    is_private = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    is_business = Column(Boolean, default=False)
    biography = Column(Text)
    profile_pic_url = Column(String(500))
    media_count = Column(Integer, default=0)
    follower_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    mutual_followers_count = Column(Integer, default=0)
    # ... 기타 컬럼들
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계
    business_contacts = relationship('InstagramBusinessContact', back_populates='user', cascade='all, delete-orphan')
    hd_profile_pics = relationship('InstagramHDProfilePic', back_populates='user', cascade='all, delete-orphan')
    bio_links = relationship('InstagramBioLink', back_populates='user', cascade='all, delete-orphan')
    # ... 기타 관계들

class InstagramBusinessContact(Base):
    __tablename__ = 'InstagramBusinessContacts'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('InstagramUsers.id', ondelete='CASCADE'), nullable=False)
    address_street = Column(String(255))
    business_contact_method = Column(String(50))
    city_name = Column(String(100))
    contact_phone_number = Column(String(20))
    public_email = Column(String(255))
    whatsapp_number = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship('InstagramUser', back_populates='business_contacts')

# ... 기타 클래스들
```

---

## 데이터 삽입 예제

```python
from sqlalchemy.orm import Session

def insert_instagram_user(session: Session, user_data: dict):
    """API 응답 데이터로부터 사용자 정보 삽입"""
    
    new_user = InstagramUser(
        pk=user_data['pk'],
        pk_id=user_data.get('pk_id'),
        username=user_data['username'],
        full_name=user_data.get('full_name'),
        is_private=user_data.get('is_private', False),
        is_verified=user_data.get('is_verified', False),
        is_business=user_data.get('is_business', False),
        biography=user_data.get('biography'),
        profile_pic_url=user_data.get('profile_pic_url'),
        media_count=user_data.get('media_count', 0),
        follower_count=user_data.get('follower_count', 0),
        following_count=user_data.get('following_count', 0),
        # ... 기타 필드들
    )
    
    # 비즈니스 연락처 추가
    if any([user_data.get(f) for f in ['address_street', 'city_name', 'contact_phone_number']]):
        business_contact = InstagramBusinessContact(
            address_street=user_data.get('address_street'),
            business_contact_method=user_data.get('business_contact_method'),
            city_name=user_data.get('city_name'),
            # ... 기타 필드들
        )
        new_user.business_contacts.append(business_contact)
    
    # HD 프로필 사진 추가
    if 'hd_profile_pic_versions' in user_data:
        for pic_version in user_data['hd_profile_pic_versions']:
            hd_pic = InstagramHDProfilePic(
                width=pic_version.get('width'),
                height=pic_version.get('height'),
                url=pic_version.get('url'),
                url_wrapped=pic_version.get('url_wrapped'),
                url_downloadable=pic_version.get('url_downloadable')
            )
            new_user.hd_profile_pics.append(hd_pic)
    
    # 바이오 링크 추가
    if 'bio_links' in user_data:
        for bio_link in user_data['bio_links']:
            link = InstagramBioLink(
                link_id=bio_link.get('link_id'),
                url=bio_link.get('url'),
                lynx_url=bio_link.get('lynx_url'),
                link_type=bio_link.get('link_type'),
                title=bio_link.get('title'),
            )
            new_user.bio_links.append(link)
    
    session.add(new_user)
    session.commit()
    
    return new_user
```

---

## 마이그레이션 예제 (Alembic)

```bash
# 초기 마이그레이션 생성
alembic init migrations

# 마이그레이션 생성 (자동)
alembic revision --autogenerate -m "Create Instagram tables"

# 마이그레이션 적용
alembic upgrade head
```

---

## 주요 설계 고려사항

### 1. **정규화 (Normalization)**
- 복잡한 중첩 객체를 별도 테이블로 분리
- 1:N 관계를 외래키로 관리
- 데이터 중복 최소화

### 2. **확장성**
- 새로운 필드 추가 용이한 구조
- JSON 컬럼을 사용하여 유연성 확보 (복잡한 객체의 경우)
- 계층적 관계 처리 (예: 프로필 컨텍스트)

### 3. **성능**
- 주요 검색 컬럼에 인덱스 적용
- 유니크 제약으로 중복 데이터 방지
- 타임스탬프로 변경 추적 가능

### 4. **데이터 무결성**
- Foreign Key 제약 조건으로 참조 무결성 보장
- CASCADE DELETE로 고아 데이터 방지
- UNIQUE 제약으로 데이터 일관성 유지

### 5. **문자 인코딩**
- UTF8MB4 사용으로 이모지 및 다국어 지원
- Instagram의 국제적 특성 반영

---

## 주의사항

1. **pk 필드**: Instagram이 발급하는 고유 사용자 ID로, 매우 큰 정수이므로 VARCHAR로 저장
2. **JSON 컬럼**: MySQL 5.7 이상 필요
3. **대용량 데이터**: API 호출 시 응답 데이터를 트랜잭션으로 처리하여 일관성 유지
4. **캐시 전략**: 변경 빈도가 낮은 데이터는 캐시 고려 (Redis 등)
5. **Privacy**: 개인정보 보호를 위해 적절한 권한 관리 필요

