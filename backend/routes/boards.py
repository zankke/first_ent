from flask import Blueprint, request, jsonify
from ..app import db
from backend.models import Board, Account

bp = Blueprint('boards', __name__)

@bp.route('/', methods=['GET'])
def get_boards():
    """모든 게시글 조회"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    board_type = request.args.get('board_type')
    is_published = request.args.get('is_published', type=bool)
    
    query = Board.query
    
    if board_type:
        query = query.filter(Board.board_type == board_type)
    if is_published is not None:
        query = query.filter(Board.is_published == is_published)
    
    boards = query.order_by(Board.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'boards': [board.to_dict() for board in boards.items],
        'total': boards.total,
        'pages': boards.pages,
        'current_page': page
    })

@bp.route('/<int:board_id>', methods=['GET'])
def get_board(board_id):
    """특정 게시글 조회"""
    board = Board.query.get_or_404(board_id)
    
    # 조회수 증가
    board.view_count += 1
    db.session.commit()
    
    return jsonify(board.to_dict())

@bp.route('/', methods=['POST'])
def create_board():
    """새 게시글 생성"""
    data = request.get_json()
    
    # 작성자 확인
    author = Account.query.get_or_404(data['author_id'])
    
    board = Board(
        title=data['title'],
        content=data.get('content', ''),
        author_id=data['author_id'],
        board_type=data.get('board_type', 'general'),
        is_published=data.get('is_published', False)
    )
    
    db.session.add(board)
    db.session.commit()
    
    return jsonify(board.to_dict()), 201

@bp.route('/<int:board_id>', methods=['PUT'])
def update_board(board_id):
    """게시글 수정"""
    board = Board.query.get_or_404(board_id)
    data = request.get_json()
    
    board.title = data.get('title', board.title)
    board.content = data.get('content', board.content)
    board.board_type = data.get('board_type', board.board_type)
    board.is_published = data.get('is_published', board.is_published)
    
    db.session.commit()
    
    return jsonify(board.to_dict())

@bp.route('/<int:board_id>', methods=['DELETE'])
def delete_board(board_id):
    """게시글 삭제"""
    board = Board.query.get_or_404(board_id)
    db.session.delete(board)
    db.session.commit()
    
    return jsonify({'message': '게시글이 삭제되었습니다.'}), 200
