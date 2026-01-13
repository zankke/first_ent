from flask import Blueprint, request, jsonify
from backend.app import db
from backend.models import Channel, Artist
from datetime import datetime

bp = Blueprint('channels', __name__)

@bp.route('/', methods=['GET'])
def get_channels():
    """모든 채널 조회"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    platform = request.args.get('platform')
    artist_id = request.args.get('artist_id', type=int)
    
    query = Channel.query
    
    if platform:
        query = query.filter(Channel.platform == platform)
    if artist_id:
        query = query.filter(Channel.artist_id == artist_id)
    
    channels = query.join(Artist, Channel.artist_id == Artist.id).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'channels': [dict(channel.to_dict(), artist_name=artist.name) for channel, artist in channels.items],
        'total': channels.total,
        'pages': channels.pages,
        'current_page': page
    })

@bp.route('/<int:channel_id>', methods=['GET'])
def get_channel(channel_id):
    """특정 채널 조회"""
    channel = Channel.query.get_or_404(channel_id)
    artist = Artist.query.get_or_404(channel.artist_id)
    channel_data = channel.to_dict()
    channel_data['artist_name'] = artist.name
    return jsonify(channel_data)

@bp.route('/', methods=['POST'])
def create_channel():
    """새 채널 생성"""
    data = request.get_json()
    
    # 아티스트 존재 확인
    artist = Artist.query.get_or_404(data['artist_id'])
    
    channel = Channel(
        artist_id=data['artist_id'],
        platform=data['platform'],
        channel_id=data['channel_id'],
        channel_name=data.get('channel_name'),
        channel_url=data.get('channel_url'),
        follower_count=data.get('follower_count', 0),
        following_count=data.get('following_count', 0),
        post_count=data.get('post_count', 0),
        is_verified=data.get('is_verified', False)
    )
    
    db.session.add(channel)
    db.session.commit()
    
    return jsonify(channel.to_dict()), 201

@bp.route('/<int:channel_id>', methods=['PUT'])
def update_channel(channel_id):
    """채널 정보 수정"""
    channel = Channel.query.get_or_404(channel_id)
    data = request.get_json()
    
    channel.channel_name = data.get('channel_name', channel.channel_name)
    channel.channel_url = data.get('channel_url', channel.channel_url)
    channel.follower_count = data.get('follower_count', channel.follower_count)
    channel.following_count = data.get('following_count', channel.following_count)
    channel.post_count = data.get('post_count', channel.post_count)
    channel.is_verified = data.get('is_verified', channel.is_verified)
    
    db.session.commit()
    
    return jsonify(channel.to_dict())

@bp.route('/<int:channel_id>', methods=['DELETE'])
def delete_channel(channel_id):
    """채널 삭제"""
    channel = Channel.query.get_or_404(channel_id)
    db.session.delete(channel)
    db.session.commit()
    
    return jsonify({'message': '채널이 삭제되었습니다.'}), 200

@bp.route('/<int:channel_id>/sync', methods=['POST'])
def sync_channel_data(channel_id):
    """채널 데이터 동기화"""
    channel = Channel.query.get_or_404(channel_id)
    
    # TODO: 실제 API 호출 로직 구현
    # Instagram, YouTube API를 통해 최신 데이터 가져오기
    
    channel.last_sync_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': '채널 데이터가 동기화되었습니다.',
        'last_sync_at': channel.last_sync_at.isoformat()
    })
