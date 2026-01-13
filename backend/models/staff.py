from backend.app import db

class Staff(db.Model):
    __tablename__ = 'Staff'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Add other staff-related fields as needed

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
