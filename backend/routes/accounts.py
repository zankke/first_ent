from flask import Blueprint, request, jsonify
from ..app import db
from backend.models import Account
from backend.utils.auth import require_auth, require_role
from datetime import datetime
import os
import re

bp = Blueprint('accounts', __name__)

@bp.route('/', methods=['GET'])
@require_auth
def get_accounts():
    """모든 계정 조회"""
    try:
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
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:account_id>', methods=['GET'])
@require_auth
def get_account(account_id):
    """특정 계정 조회"""
    try:
        account = Account.query.get_or_404(account_id)
        return jsonify(account.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
@require_role('admin')
def create_account():
    """새 계정 생성"""
    try:
        data = request.get_json()
        
        # 1. 필수 필드 유효성 검사
        required_fields = ['uid', 'uemail', 'password', 'level', 'uname']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} 필드는 필수입니다.'}), 400
        
        uid = data['uid']
        uemail = data['uemail']
        password = data['password']
        level = data['level']
        uname = data['uname']

        # 2. 이메일 형식 유효성 검사
        if not re.match(r"[^@]+@[^@]+\.[^@]+", uemail):
            return jsonify({'error': '유효하지 않은 이메일 형식입니다.'}), 400

        # 3. 비밀번호 길이 유효성 검사 (최소 8자)
        if len(password) < 8:
            return jsonify({'error': '비밀번호는 최소 8자 이상이어야 합니다.'}), 400

        # 4. 역할(level) 유효성 검사
        allowed_levels = ['admin', 'manager', 'viewer']
        if level not in allowed_levels:
            return jsonify({'error': f"유효하지 않은 역할입니다. 허용되는 역할: {', '.join(allowed_levels)}"}), 400

        # 5. 중복 확인
        if Account.query.filter_by(uid=uid).first():
            return jsonify({'error': '이미 존재하는 사용자명(UID)입니다.'}), 400
        
        if Account.query.filter_by(uemail=uemail).first():
            return jsonify({'error': '이미 존재하는 이메일입니다.'}), 400

        if Account.query.filter_by(uname=uname).first():
            return jsonify({'error': '이미 존재하는 이름(UNAME)입니다.'}), 400
        
        account = Account(
            uid=uid,
            uemail=uemail,
            level=level,
            uname=uname,
            status='Y'
        )
        account.set_password(password)
        
        db.session.add(account)
        db.session.commit()
        
        return jsonify(account.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:account_id>', methods=['PUT'])
@require_role('admin', 'manager')
def update_account(account_id):
    """계정 정보 수정"""
    try:
        account = Account.query.get_or_404(account_id)
        data = request.get_json()
        
        if 'uid' in data and data['uid'] != account.uid:
            if Account.query.filter_by(uid=data['uid']).first():
                return jsonify({'error': '이미 존재하는 사용자명입니다.'}), 400
            account.uid = data['uid']

        if 'uname' in data and data['uname'] != account.uname:
            if Account.query.filter_by(uname=data['uname']).first():
                return jsonify({'error': '이미 존재하는 이름입니다.'}), 400
            account.uname = data['uname']
        
        if 'uemail' in data and data['uemail'] != account.uemail:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", data['uemail']):
                return jsonify({'error': '유효하지 않은 이메일 형식입니다.'}), 400
            if Account.query.filter_by(uemail=data['uemail']).first():
                return jsonify({'error': '이미 존재하는 이메일입니다.'}), 400
            account.uemail = data['uemail']
        
        if 'password' in data and data['password']:
            if len(data['password']) < 8:
                return jsonify({'error': '비밀번호는 최소 8자 이상이어야 합니다.'}), 400
            account.set_password(data['password'])
        
        if 'level' in data:
            allowed_levels = ['admin', 'manager', 'viewer']
            if data['level'] not in allowed_levels:
                return jsonify({'error': f"유효하지 않은 역할입니다. 허용되는 역할: {', '.join(allowed_levels)}"}), 400
            account.level = data['level']
            
        if 'status' in data:
            if data['status'] not in ['Y', 'N']:
                return jsonify({'error': '유효하지 않은 상태입니다.'}), 400
            account.status = data['status']
        
        db.session.commit()
        
        return jsonify(account.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:account_id>', methods=['DELETE'])
@require_role('admin')
def delete_account(account_id):
    """계정 삭제"""
    try:
        account = Account.query.get_or_404(account_id)
        db.session.delete(account)
        db.session.commit()
        
        return jsonify({'message': '계정이 삭제되었습니다.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# @bp.route('/login', methods=['POST'])
# def login():
#     """로그인 - Supabase로 대체됨"""
#     # Supabase 인증을 사용하므로 이 엔드포인트는 더 이상 사용되지 않습니다.
#     return jsonify({'error': 'This endpoint has been replaced with Supabase authentication'}), 410
