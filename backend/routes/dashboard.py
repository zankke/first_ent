from flask import Blueprint, jsonify
from backend.app import db
from backend.models import Artist, Channel, ChannelStat, News # Assuming these models exist
from sqlalchemy import func

def format_number_to_k_m(num):
    if num is None:
        return "N/A"
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    if num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)

bp = Blueprint('dashboard', __name__)

@bp.route('/stats', methods=['GET'], strict_slashes=False)
def get_dashboard_stats():
    """대시보드 통계 데이터 제공"""
    total_artists = Artist.query.count()
    total_channels = Channel.query.count()
    total_news = News.query.count()

    stats = [
        {"icon": "Users", "color": "from-blue-500 to-cyan-500", "value": str(total_artists), "title": "총 아티스트", "change": "+2%"},
        {"icon": "Radio", "color": "from-green-500 to-emerald-500", "value": str(total_channels), "title": "총 채널", "change": "+5%"},
        {"icon": "TrendingUp", "color": "from-purple-500 to-pink-500", "value": str(total_news), "title": "총 뉴스", "change": "+10%"},
        {"icon": "Activity", "color": "from-orange-500 to-red-500", "value": "7", "title": "활성 모니터링", "change": ""},
    ]
    return jsonify(stats)

@bp.route('/recent-artists', methods=['GET'], strict_slashes=False)
def get_recent_artists():
    """최근 등록된 아티스트 목록 제공"""
    # Fetch recent artists, e.g., by latest debut_date or creation date
    # For now, let's assume 'id' can represent recency if no creation timestamp is available
    artists = Artist.query.order_by(Artist.id.desc()).limit(5).all() # Get up to 5 recent artists

    recent_artists_data = []
    for artist in artists:
        # Fetch associated channels for each artist
        channels = Channel.query.filter_by(artist_id=artist.id).all()
        
        # Aggregate channel info (platform and followers)
        channel_info = []
        for channel in channels:
            # Assuming ChannelStat has 'followers' and is linked to Channel by 'channel_id'
            latest_stat = ChannelStat.query.filter_by(channel_id=channel.id).order_by(ChannelStat.recorded_date.desc()).first()
            followers = format_number_to_k_m(latest_stat.follower_count) if latest_stat else "N/A"
            channel_info.append({
                "platform": channel.platform, # Assuming 'platform' field exists in Channel model
                "followers": followers
            })

        recent_artists_data.append({
            "name": artist.name,
            "profile_photo": artist.profile_photo if artist.profile_photo else "",
            "channels": channel_info # List of channel details
        })
    
    return jsonify(recent_artists_data)

@bp.route('/channel-performance', methods=['GET'], strict_slashes=False)
def get_channel_performance():
    """채널 성과 데이터 제공"""
    # TODO: 실제 채널 성과 데이터 로직 구현
    # 예시 데이터
    channel_performance = [
        {"platform": "Instagram", "growth": "+15%", "posts": "120"},
        {"platform": "Youtube", "growth": "+10%", "posts": "80"},
    ]
    return jsonify(channel_performance)
