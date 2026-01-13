from flask import Blueprint, request, jsonify
from backend.app import db
from backend.models import Account
from backend.utils.auth import require_auth, require_role
from datetime import datetime
import os

bp = Blueprint('accounts', __name__)

@bp.route('/', methods=['GET'])
@require_auth
def get_accounts():
    """모든 계정 조회"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    level = request.args.get('level')
    status = request.args.get('status')
    
    query = Account.query
    
    if level:
        query = query.filter(Account.level == level)
    if status is not None:
        query = query.filter(Account.status == status)
    
    accounts = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'accounts': [account.to_dict() for account in accounts.items],
        'total': accounts.total,
        'pages': accounts.pages,
        'current_page': page
    })

@bp.route('/<int:account_id>', methods=['GET'])
def get_account(account_id):
    """특정 계정 조회"""
    account = Account.query.get_or_404(account_id)
    return jsonify(account.to_dict())

@bp.route('/', methods=['POST'])
@require_role('admin')
def create_account():
    """새 계정 생성"""
    data = request.get_json()
    
    # 중복 확인
    if Account.query.filter_by(uid=data['username']).first():
        return jsonify({'error': '이미 존재하는 사용자명입니다.'}), 400
    
    if Account.query.filter_by(uemail=data['email']).first():
        return jsonify({'error': '이미 존재하는 이메일입니다.'}), 400
    
    account = Account(
        uid=data['username'],
        uemail=data['email'],
        level=data.get('role', 'viewer')
    )
    account.set_password(data['password'])
    
    db.session.add(account)
    db.session.commit()
    
    return jsonify(account.to_dict()), 201

@bp.route('/<int:account_id>', methods=['PUT'])
@require_role('admin', 'manager')
def update_account(account_id):
    """계정 정보 수정"""
    account = Account.query.get_or_404(account_id)
    data = request.get_json()
    
    if 'username' in data and data['username'] != account.uid:
        if Account.query.filter_by(uid=data['username']).first():
            return jsonify({'error': '이미 존재하는 사용자명입니다.'}), 400
        account.uid = data['username']
    
    if 'email' in data and data['email'] != account.uemail:
        if Account.query.filter_by(uemail=data['email']).first():
            return jsonify({'error': '이미 존재하는 이메일입니다.'}), 400
        account.uemail = data['email']
    
    if 'password' in data:
        account.set_password(data['password'])
    
    account.level = data.get('role', account.level)
    account.status = data.get('is_active', account.status)
    
    db.session.commit()
    
    return jsonify(account.to_dict())

@bp.route('/<int:account_id>', methods=['DELETE'])
@require_role('admin')
def delete_account(account_id):
    """계정 삭제"""
    account = Account.query.get_or_404(account_id)
    db.session.delete(account)
    db.session.commit()
    
    return jsonify({'message': '계정이 삭제되었습니다.'}), 200

# @bp.route('/login', methods=['POST'])
# def login():
#     """로그인 - Supabase로 대체됨"""
#     # Supabase 인증을 사용하므로 이 엔드포인트는 더 이상 사용되지 않습니다.
#     return jsonify({'error': 'This endpoint has been replaced with Supabase authentication'}), 410
