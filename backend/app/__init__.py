from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    @app.route('/images/<path:filename>')
    def serve_image(filename):
        images_dir = os.path.join(app.root_path, '..', 'assets', 'images')
        return send_from_directory(images_dir, filename)


    # 설정
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

    # Construct SQLALCHEMY_DATABASE_URI from individual components
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')

    if db_user and db_password and db_host and db_port and db_name:
        encoded_password = quote_plus(db_password)
        app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"
    else:
        # Fallback to DATABASE_URL if individual components are not set
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print(f"SQLALCHEMY_DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    app.config['MIGRATE_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..', 'database', 'migrations')
    
    # 확장 초기화
    db.init_app(app)
    migrate.init_app(app, db, directory=os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..', 'database', 'migrations'))
    CORS(app, resources={r"/api/*": {"origins": [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3002",
        "http://127.0.0.1:5002",
        "http://localhost:5002",
        "http://konikt-ai.kr:3000",
    ]}})
    # Configure logging for debug messages
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    # 라우트 등록
    from backend.routes import artists, channels, accounts, boards, api_keys, news, dashboard, activities, instagram, auth

    #from routes import artists, channels, accounts, boards, api_keys, news
    app.register_blueprint(auth.bp, url_prefix='/api/auth')
    app.register_blueprint(artists.bp, url_prefix='/api/artists')
    app.register_blueprint(channels.bp, url_prefix='/api/channels')
    app.register_blueprint(accounts.bp, url_prefix='/api/accounts')
    app.register_blueprint(boards.bp, url_prefix='/api/boards')
    app.register_blueprint(api_keys.bp, url_prefix='/api/api-keys')
    app.register_blueprint(news.bp, url_prefix='/api/news')
    app.register_blueprint(dashboard.bp, url_prefix='/api/dashboard')
    app.register_blueprint(activities.bp, url_prefix='/api/activities')
    app.register_blueprint(instagram.bp, url_prefix='/api/instagram')

    # 스케줄러 초기화
    # news_scheduler.init_app(app)
    
    return app
