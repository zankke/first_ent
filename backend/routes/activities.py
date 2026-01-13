from flask import Blueprint, request, jsonify
from backend.app import db
from backend.models import Activity, Artist, Staff
from datetime import datetime

bp = Blueprint('activities', __name__)

@bp.route('/', methods=['POST'])
def create_activity():
    """새 활동 생성"""
    data = request.get_json()
    
    artist_id = data.get('artist_id')
    if not artist_id or not Artist.query.get(artist_id):
        return jsonify({'error': '유효한 아티스트 ID가 필요합니다.'}), 400

    activity = Activity(
        artist_id=artist_id,
        activity_name=data['activity_name'],
        activity_type=data.get('activity_type'),
        start_time=datetime.fromisoformat(data['start_time']) if data.get('start_time') else None,
        end_time=datetime.fromisoformat(data['end_time']) if data.get('end_time') else None,
        location=data.get('location'),
        manager_id=data.get('manager_id')
    )
    
    db.session.add(activity)
    db.session.commit()
    
    return jsonify(activity.to_dict()), 201

@bp.route('/', methods=['GET'])
def get_activities():
    """모든 활동 조회 (아티스트 ID로 필터링 가능)"""
    artist_id = request.args.get('artist_id', type=int)
    
    query = Activity.query
    if artist_id:
        query = query.filter_by(artist_id=artist_id)
        
    activities = query.all()
    return jsonify([activity.to_dict() for activity in activities])

@bp.route('/<int:activity_id>', methods=['GET'])
def get_activity(activity_id):
    """특정 활동 조회"""
    activity = Activity.query.get_or_404(activity_id)
    return jsonify(activity.to_dict())

@bp.route('/<int:activity_id>', methods=['PUT'])
def update_activity(activity_id):
    """활동 정보 수정"""
    activity = Activity.query.get_or_404(activity_id)
    data = request.get_json()
    
    activity.activity_name = data.get('activity_name', activity.activity_name)
    activity.activity_type = data.get('activity_type', activity.activity_type)
    activity.start_time = datetime.fromisoformat(data['start_time']) if data.get('start_time') else activity.start_time
    activity.end_time = datetime.fromisoformat(data['end_time']) if data.get('end_time') else activity.end_time
    activity.location = data.get('location', activity.location)
    activity.manager_id = data.get('manager_id', activity.manager_id)
    
    db.session.commit()
    
    return jsonify(activity.to_dict())

@bp.route('/<int:activity_id>', methods=['DELETE'])
def delete_activity(activity_id):
    """활동 삭제"""
    activity = Activity.query.get_or_404(activity_id)
    db.session.delete(activity)
    db.session.commit()
    
    return jsonify({'message': '활동이 삭제되었습니다.'}), 200
