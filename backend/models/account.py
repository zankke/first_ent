from datetime import datetime
from backend.app import db
import bcrypt

class Account(db.Model):
    __tablename__ = 'Users'
    
    uqid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(50), nullable=False, unique=True)
    uemail = db.Column(db.String(100), nullable=False, unique=True)
    upass = db.Column(db.String(255), nullable=False)
    level = db.Column(db.String(10), default='viewer')
    status = db.Column(db.String(10), default='Y')
    last_login = db.Column(db.DateTime)
    regdate = db.Column(db.DateTime, default=datetime.utcnow)
    uname = db.Column(db.String(30), nullable=False, unique=True) # Added uname column

    # 관계
    # boards = db.relationship('Board', backref='author', lazy=True)
    
    def set_password(self, password):
        """비밀번호를 해시화하여 저장"""
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.upass = hashed.decode('utf-8')
    
    def check_password(self, password):
        """비밀번호 확인"""
        return bcrypt.checkpw(password.encode('utf-8'), self.upass.encode('utf-8'))
    
    def to_dict(self):
        return {
            'uqid': self.uqid,
            'uid': self.uid,
            'name': self.uname, # Changed to uname
            'uemail': self.uemail,
            'level': self.level,
            'status': self.status,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'regdate': self.regdate.isoformat()
        }
