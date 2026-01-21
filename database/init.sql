-- AI 기반 Artist Management Framework Database Schema
-- Database: first_ent

USE first_ent;

-- 1. Artists 테이블 (아티스트 기본 정보)
CREATE TABLE artists (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    real_name VARCHAR(100),
    birth_date DATE,
    gender ENUM('male', 'female', 'other'),
    nationality VARCHAR(50),
    agency VARCHAR(100),
    debut_date DATE,
    status ENUM('active', 'inactive', 'retired') DEFAULT 'active',
    profile_image_url TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. Channels 테이블 (채널 정보)
CREATE TABLE channels (
    id INT PRIMARY KEY AUTO_INCREMENT,
    artist_id INT NOT NULL,
    platform ENUM('instagram', 'youtube', 'tiktok', 'twitter') NOT NULL,
    channel_id VARCHAR(100) NOT NULL,
    channel_name VARCHAR(200),
    channel_url TEXT,
    follower_count INT DEFAULT 0,
    following_count INT DEFAULT 0,
    post_count INT DEFAULT 0,
    is_verified BOOLEAN DEFAULT FALSE,
    last_sync_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (artist_id) REFERENCES artists(id) ON DELETE CASCADE,
    UNIQUE KEY unique_channel (artist_id, platform, channel_id)
);

-- 3. Accounts 테이블 (계정 관리)
CREATE TABLE accounts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'manager', 'viewer') DEFAULT 'viewer',
    is_active BOOLEAN DEFAULT TRUE,
    last_login_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 4. Boards 테이블 (게시판)
CREATE TABLE boards (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    author_id INT NOT NULL,
    board_type ENUM('notice', 'announcement', 'general') DEFAULT 'general',
    is_published BOOLEAN DEFAULT FALSE,
    view_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES accounts(id) ON DELETE CASCADE
);

-- 5. API_Keys 테이블 (API 키 관리)
CREATE TABLE api_keys (
    id INT PRIMARY KEY AUTO_INCREMENT,
    platform ENUM('instagram', 'youtube', 'tiktok', 'twitter') NOT NULL,
    api_name VARCHAR(100) NOT NULL,
    api_key TEXT NOT NULL,
    api_secret TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    last_used_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 6. Database_Configs 테이블 (DB 연결 정보)
CREATE TABLE database_configs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    config_name VARCHAR(100) NOT NULL UNIQUE,
    host VARCHAR(100) NOT NULL,
    port INT NOT NULL,
    database_name VARCHAR(100) NOT NULL,
    username VARCHAR(100) NOT NULL,
    password_encrypted TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 7. Channel_Stats 테이블 (채널 통계)
CREATE TABLE channel_stats (
    id INT PRIMARY KEY AUTO_INCREMENT,
    channel_id INT NOT NULL,
    stat_date DATE NOT NULL,
    follower_count INT DEFAULT 0,
    following_count INT DEFAULT 0,
    post_count INT DEFAULT 0,
    engagement_rate DECIMAL(5,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE,
    UNIQUE KEY unique_channel_date (channel_id, stat_date)
);

-- 8. Posts 테이블 (게시물 정보)
CREATE TABLE posts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    channel_id INT NOT NULL,
    post_id VARCHAR(100) NOT NULL,
    post_url TEXT,
    caption TEXT,
    media_type ENUM('image', 'video', 'carousel') NOT NULL,
    media_urls JSON,
    like_count INT DEFAULT 0,
    comment_count INT DEFAULT 0,
    share_count INT DEFAULT 0,
    posted_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE,
    UNIQUE KEY unique_post (channel_id, post_id)
);

-- 9. News 테이블 (뉴스 기사)
CREATE TABLE news (
    id INT PRIMARY KEY AUTO_INCREMENT,
    artist_id INT NOT NULL,
    title VARCHAR(500) NOT NULL,
    content TEXT,
    url TEXT NOT NULL,
    source VARCHAR(200),
    published_at TIMESTAMP NULL,
    crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sentiment ENUM('positive', 'negative', 'neutral') DEFAULT 'neutral',
    relevance_score FLOAT DEFAULT 0.0,
    keywords JSON,
    is_processed BOOLEAN DEFAULT FALSE,
    thumbnail TEXT, -- 썸네일 이미지 URL
    media_name VARCHAR(255), -- 미디어 이름 (예: 연합뉴스, 조선일보)
    FOREIGN KEY (artist_id) REFERENCES artists(id) ON DELETE CASCADE,
    UNIQUE KEY unique_news_url (url)
);

-- 인덱스 생성
CREATE INDEX idx_artists_status ON artists(status);
CREATE INDEX idx_channels_platform ON channels(platform);
CREATE INDEX idx_channels_artist ON channels(artist_id);
CREATE INDEX idx_boards_type ON boards(board_type);
CREATE INDEX idx_boards_author ON boards(author_id);
CREATE INDEX idx_channel_stats_date ON channel_stats(stat_date);
CREATE INDEX idx_posts_channel ON posts(channel_id);
CREATE INDEX idx_posts_posted_at ON posts(posted_at);
CREATE INDEX idx_news_artist ON news(artist_id);
CREATE INDEX idx_news_crawled_at ON news(crawled_at);
CREATE INDEX idx_news_sentiment ON news(sentiment);

-- 초기 데이터 삽입
INSERT INTO accounts (username, email, password_hash, role) VALUES 
('admin', 'admin@firstent.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J7v5Q5K2', 'admin');

INSERT INTO artists (name, real_name, nationality, agency, status) VALUES 
('Sample Artist', '홍길동', 'Korea', 'theProjectCompany', 'active');

INSERT INTO channels (artist_id, platform, channel_id, channel_name, follower_count) VALUES 
(1, 'instagram', 'sample_artist_ig', 'Sample Artist Instagram', 10000),
(1, 'youtube', 'UCsample123', 'Sample Artist YouTube', 5000);

-- Sample News Data
INSERT INTO news (artist_id, title, content, url, source, published_at, sentiment, relevance_score, keywords, thumbnail, media_name) VALUES
(1, 'Sample Artist, New Album Release!', 'Sample Artist has announced the release of their new album "Echoes" next month. Fans are eagerly awaiting the new sound.', 'https://sample.news/artist1-album', 'Music Daily', NOW() - INTERVAL 5 DAY, 'positive', 0.85, '["Sample Artist", "New Album", "Echoes"]', 'https://picsum.photos/seed/sampleartist1/200/200', 'Music News'),
(1, 'Sample Artist spotted at Fashion Week', 'Sample Artist made a surprise appearance at Seoul Fashion Week, showcasing a bold new style.', 'https://sample.news/artist1-fashion', 'Fashion Beat', NOW() - INTERVAL 2 DAY, 'neutral', 0.70, '["Sample Artist", "Fashion Week", "Seoul"]', 'https://picsum.photos/seed/sampleartist2/200/200', 'Style Magazine'),
(1, 'Controversy surrounding Sample Artist's latest single', 'Some critics have expressed mixed feelings about Sample Artist's latest single, citing its experimental sound.', 'https://sample.news/artist1-controversy', 'The Critic', NOW() - INTERVAL 1 DAY, 'negative', 0.60, '["Sample Artist", "Single", "Controversy"]', 'https://picsum.photos/seed/sampleartist3/200/200', 'Review Hub');
