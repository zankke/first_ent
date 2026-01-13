from backend.app import create_app, db
from backend.models import Artist

app = create_app()
app.app_context().push()

genres = db.session.query(Artist.genre).distinct().all()

for genre in genres:
    print(genre[0])
