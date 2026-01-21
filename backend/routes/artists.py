from flask import Blueprint, request, jsonify, send_file, render_template, url_for
from ..app import db
from backend.models.artist import Artist
from backend.models import Channel, ChannelStat, News

from datetime import datetime, date
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pptx import Presentation
from io import BytesIO
from werkzeug.utils import secure_filename
import os
import logging

from markdown import markdown # Import markdown library
import requests # Import requests library
from backend.utils.wikipedia_utils import get_artist_info_from_wikipedia # New import
from backend.utils.auth import require_role # Added import

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'frontend', 'public', 'images', 'artists', 'profile')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

bp = Blueprint('artists', __name__)
logger = logging.getLogger(__name__)

@bp.route('/search_and_generate_sql', methods=['GET'])
def search_and_generate_sql():
    artist_name = request.args.get('artist_name')
    if not artist_name:
        return jsonify({'error': 'Artist name is required.'}), 400

    artist_data = get_artist_info_from_wikipedia(artist_name)
    if not artist_data:
        return jsonify({'message': f'Could not find information for {artist_name} on Wikipedia.'}), 404

    # Check if artist already exists in DB
    existing_artist = Artist.query.filter_by(name=artist_name).first()

    sql_query = ""
    if existing_artist:
        sql_query = generate_update_sql(existing_artist.id, artist_data)
        artist_exists_flag = True
    else:
        sql_query = generate_insert_sql(artist_data)
        artist_exists_flag = False
    
    return jsonify({
        'sql_query': sql_query,
        'artist_data': artist_data,
        'artist_exists': artist_exists_flag
    })

def generate_insert_sql(data):
    columns = []
    values = []
    
    # Default values for fields not easily extracted or provided by user
    data.setdefault('eng_name', 'NULL')
    data.setdefault('birth_date', 'NULL')
    data.setdefault('height_cm', 'NULL')
    data.setdefault('debut_date', 'NULL')
    data.setdefault('debut_title', 'NULL')
    data.setdefault('recent_activity_category', 'NULL')
    data.setdefault('recent_activity_name', 'NULL')
    data.setdefault('genre', 'NULL')
    data.setdefault('agency_id', 'NULL')
    data.setdefault('current_agency_name', 'NULL')
    data.setdefault('nationality', 'NULL')
    data.setdefault('is_korean', 1) # Default to Korean
    data.setdefault('gender', 'NA') # Default to Not Applicable
    data.setdefault('status', 'ACTIVE')
    data.setdefault('category_id', 'NULL')
    data.setdefault('platform', 'NULL')
    data.setdefault('social_media_url', 'NULL')
    data.setdefault('profile_photo', 'NULL')
    data.setdefault('guarantee_krw', 'NULL')
    data.setdefault('wiki_summary', 'NULL')

    for key, value in data.items():
        # Ensure column names match the schema (e.g., birth_date -> birth_date)
        if key in ['name', 'eng_name', 'birth_date', 'height_cm', 'debut_date', 'debut_title',
                   'recent_activity_category', 'recent_activity_name', 'genre', 'agency_id',
                   'current_agency_name', 'nationality', 'is_korean', 'gender', 'status',
                   'category_id', 'platform', 'social_media_url', 'profile_photo',
                   'guarantee_krw', 'wiki_summary']:
            
            columns.append(key)
            sql_value = "" # Initialize sql_value
            if isinstance(value, str):
                sql_value = "'" + value.replace("'", "''") + "'"
            elif type(value).__name__ == 'date':
                sql_value = f"'{value.strftime('%Y-%m-%d')}'"
            elif value is None:
                sql_value = "NULL"
            else:
                sql_value = str(value)
            values.append(sql_value)

    return f"INSERT INTO first_ent.Artists ({', '.join(columns)}) VALUES ({', '.join(values)});"

def generate_update_sql(artist_id, data):
    set_clauses = []
    
    # Default values for fields not easily extracted or provided by user
    # These will be used if the key is not present in data
    default_values = {
        'eng_name': 'NULL',
        'birth_date': 'NULL',
        'height_cm': 'NULL',
        'debut_date': 'NULL',
        'debut_title': 'NULL',
        'recent_activity_category': 'NULL',
        'recent_activity_name': 'NULL',
        'genre': 'NULL',
        'agency_id': 'NULL',
        'current_agency_name': 'NULL',
        'nationality': 'NULL',
        'is_korean': 1, # Default to Korean
        'gender': 'NA', # Default to Not Applicable
        'status': 'ACTIVE',
        'category_id': 'NULL',
        'platform': 'NULL',
        'social_media_url': 'NULL',
        'profile_photo': 'NULL',
        'guarantee_krw': 'NULL',
        'wiki_summary': 'NULL'
    }

    for key, value in data.items():
        if key in ['name', 'eng_name', 'birth_date', 'height_cm', 'debut_date', 'debut_title',
                   'recent_activity_category', 'recent_activity_name', 'genre', 'agency_id',
                   'current_agency_name', 'nationality', 'is_korean', 'gender', 'status',
                   'category_id', 'platform', 'social_media_url', 'profile_photo',
                   'guarantee_krw', 'wiki_summary']:
            
            sql_value = ""
            if isinstance(value, str):
                sql_value = "'" + value.replace("'", "''") + "'"
            elif type(value).__name__ == 'date':
                sql_value = f"'{value.strftime('%Y-%m-%d')}'"
            elif value is None:
                sql_value = "NULL"
            else:
                sql_value = str(value)
            set_clauses.append(f"{key}={sql_value}")

    # Add default values for fields not returned by Wikipedia if they are not already in set_clauses
    for key, default_value in default_values.items():
        if key not in data and key in ['name', 'eng_name', 'birth_date', 'height_cm', 'debut_date', 'debut_title',
                   'recent_activity_category', 'recent_activity_name', 'genre', 'agency_id',
                   'current_agency_name', 'nationality', 'is_korean', 'gender', 'status',
                   'category_id', 'platform', 'social_media_url', 'profile_photo',
                   'guarantee_krw', 'wiki_summary']:
             set_clauses.append(f"{key}={default_value}")


    return f"UPDATE first_ent.Artists SET {', '.join(set_clauses)} WHERE id={artist_id};"


@bp.route('/test-image')
def test_image():
    try:
        return send_file(os.path.join(UPLOAD_FOLDER, 'park_seo_joon_2025.png'), mimetype='image/png')
    except Exception as e:
        return str(e), 500

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/profile-photos/<filename>')
def serve_profile_photo(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@bp.route('/', methods=['GET'])
def get_artists():
    """모든 아티스트 조회"""
    search_query = request.args.get('query')
    filter_status = request.args.get('status')
    filter_gender = request.args.get('gender')
    filter_nationality = request.args.get('nationality')

    artists_query = Artist.query

    if search_query:
        search_pattern = f'%{search_query}%'
        artists_query = artists_query.filter(
            db.or_(
                Artist.name.ilike(search_pattern),
                Artist.genre.ilike(search_pattern),
                Artist.nationality.ilike(search_pattern)
            )
        )
    compiled_query = artists_query.statement.compile(compile_kwargs={"literal_binds": True})
    logger.debug(f"Artist search SQL query: {compiled_query}")
    if filter_status:
        artists_query = artists_query.filter(Artist.status == filter_status)
    if filter_gender:
        artists_query = artists_query.filter(Artist.gender == filter_gender)
    if filter_nationality:
        artists_query = artists_query.filter(Artist.nationality == filter_nationality)

    artists = artists_query.all()
    
    return jsonify({
        'artists': [artist.to_dict() for artist in artists],
        'total': len(artists),
        'pages': 1,
        'current_page': 1
    })

@bp.route('/recent', methods=['GET'])
def get_recent_artists():
    """최근 등록된 아티스트 조회"""
    limit = request.args.get('limit', 5, type=int)
    recent_artists = Artist.query.order_by(Artist.debut_date.desc()).limit(limit).all()
    return jsonify([artist.to_dict() for artist in recent_artists])

@bp.route('/<int:artist_id>', methods=['GET'])
def get_artist(artist_id):
    """특정 아티스트 조회"""
    artist = Artist.query.get_or_404(artist_id)
    return jsonify(artist.to_dict())

@bp.route('/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """대시보드 통계 조회"""
    total_artists = Artist.query.count()
    # Assuming 'Channel' model exists and has a 'status' or similar field
    # For now, let's mock active channels and followers/views
    # In a real scenario, this would involve more complex queries and potentially a Channel model
    active_channels = 0 # Placeholder
    total_followers = "0M" # Placeholder
    monthly_views = "0M" # Placeholder

    return jsonify([
        {"title": "총 아티스트", "value": str(total_artists), "change": "", "changeType": "positive", "icon": "Users", "color": "from-blue-500 to-cyan-500"},
        {"title": "활성 채널", "value": str(active_channels), "change": "", "changeType": "positive", "icon": "Radio", "color": "from-purple-500 to-pink-500"},
        {"title": "총 팔로워", "value": total_followers, "change": "", "changeType": "positive", "icon": "TrendingUp", "color": "from-green-500 to-emerald-500"},
        {"title": "월간 조회수", "value": monthly_views, "change": "", "changeType": "positive", "icon": "Activity", "color": "from-orange-500 to-red-500"}
    ])

@bp.route('/dashboard/channel-performance', methods=['GET'])
def get_channel_performance():
    """대시보드 채널 성과 조회"""
    # Placeholder data for now. In a real scenario, this would query Channel and ChannelStat models.
    return jsonify([
        {"platform": "Instagram", "growth": "+15%", "posts": 24},
        {"platform": "YouTube", "growth": "+8%", "posts": 12},
        {"platform": "TikTok", "growth": "+23%", "posts": 18}
    ])

@bp.route('/', methods=['POST'])
def create_artist():
    """새 아티스트 생성"""
    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    profile_photo_path = None
    if 'profile_photos' in request.files:
        files = request.files.getlist('profile_photos')
        if files:
            # Assuming only one profile photo for now, or taking the first one
            file = files[0]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                profile_photo_path = f"/images/artists/profile/{filename}"

    # Get other form data
    data = request.form

    artist = Artist(
        name=data['name'],
        birth_date=datetime.strptime(data['birth_date'], '%Y-%m-%d').date(),
        height_cm=int(data['height_cm']) if data.get('height_cm') else None,
        debut_date=datetime.strptime(data['debut_date'], '%Y-%m-%d').date() if data.get('debut_date') else None,
        genre=data.get('genre'),
        agency_id=int(data['agency_id']) if data.get('agency_id') else None,
        nationality=data.get('nationality'),
        is_korean=data.get('is_korean') == 'true',
        gender=data.get('gender'),
        status=data.get('status'),
        category_id=int(data['category_id']) if data.get('category_id') else None,
        platform=data.get('platform'),
        social_media_url=data.get('social_media_url'),
        profile_photo=profile_photo_path
    )

    db.session.add(artist)
    db.session.commit()

    return jsonify(artist.to_dict()), 201

@bp.route('/<int:artist_id>', methods=['PUT'])
def update_artist(artist_id):
    """아티스트 정보 수정"""
    artist = Artist.query.get_or_404(artist_id)

    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    profile_photo_path = artist.profile_photo # Keep existing photo if not updated
    if 'profile_photos' in request.files:
        files = request.files.getlist('profile_photos')
        if files:
            file = files[0]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                profile_photo_path = f"/images/artists/profile/{filename}"

    # Get other form data
    data = request.form
    
    artist.name = data.get('name', artist.name)
    if data.get('birth_date'):
        artist.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
    artist.height_cm = int(data['height_cm']) if data.get('height_cm') else None
    if data.get('debut_date'):
        artist.debut_date = datetime.strptime(data['debut_date'], '%Y-%m-%d').date()
    artist.genre = data.get('genre', artist.genre)
    artist.agency_id = int(data['agency_id']) if data.get('agency_id') else None
    artist.nationality = data.get('nationality', artist.nationality)
    artist.is_korean = data.get('is_korean') == 'true'
    artist.gender = data.get('gender', artist.gender)
    artist.status = data.get('status', artist.status)
    artist.category_id = int(data['category_id']) if data.get('category_id') else None
    artist.platform = data.get('platform', artist.platform)
    artist.social_media_url = data.get('social_media_url', artist.social_media_url)
    artist.profile_photo = profile_photo_path
    artist.guarantee_krw = int(data['guarantee_krw']) if data.get('guarantee_krw') else None
    
    db.session.commit()
    
    return jsonify(artist.to_dict())

@bp.route('/report', methods=['POST'], strict_slashes=False)
def generate_artist_report():
    """선택된 아티스트에 대한 보고서 생성"""
    data = request.get_json()
    artist_ids = data.get('artist_ids', [])
    report_format = data.get('report_format', 'pdf') # 'pdf' or 'pptx'

    print(f"DEBUG: Received artist_ids for report: {artist_ids}")
    print(f"DEBUG: Received report_format: {report_format}")

    if not artist_ids:
        print("DEBUG: No artist_ids provided, returning 400.")
        return jsonify({'error': '아티스트 ID가 제공되지 않았습니다.'}), 400

    artists = Artist.query.filter(Artist.id.in_(artist_ids)).all()

    if not artists:
        return jsonify({'error': '선택된 아티스트를 찾을 수 없습니다.'}), 404

    if report_format == 'pdf': # This block will now handle Puppeteer-based PDF
        # --- NEW PUPPETEER-BASED PDF GENERATION LOGIC ---
        PUPPETEER_SERVICE_URL = "http://localhost:3001/generate-pdf" # Define Puppeteer service URL
        try:
            # Prepare data for rendering HTML template
            artist = artists[0] # Already filtered to a single artist_id, so take the first
            if not artist:
                return jsonify({'error': 'No artist data available for report generation.'}), 404

            # --- Fetch related data ---
            artist_channels = Channel.query.filter_by(artist_id=artist.id).all()
            
            # Fetch latest stats for each channel
            channel_stats_data = []
            for channel in artist_channels:
                latest_stat = ChannelStat.query.filter_by(channel_id=channel.id).order_by(ChannelStat.stat_date.desc()).first()
                if latest_stat:
                    channel_stats_data.append({
                        'platform': channel.platform,
                        'name': channel.channel_name,
                        'url': channel.channel_url,
                        'follower_count': latest_stat.follower_count,
                        'engagement_rate': float(latest_stat.engagement_rate) if latest_stat.engagement_rate else 0.0
                    })
            
            # Fetch recent news
            recent_news_articles = News.query.filter_by(artist_id=artist.id).order_by(News.published_at.desc()).limit(5).all()

            # --- Fetch Activities ---
            all_activities = Activity.query.filter_by(artist_id=artist.id).order_by(Activity.start_time.desc()).all()
            activities_cf = [a for a in all_activities if a.activity_type and ('CF' in a.activity_type.upper() or 'AD' in a.activity_type.upper())]
            activities_broadcast = [a for a in all_activities if a.activity_type and ('DRAMA' in a.activity_type.upper() or 'MOVIE' in a.activity_type.upper() or 'TV' in a.activity_type.upper())]
            activities_other = [a for a in all_activities if a not in activities_cf and a not in activities_broadcast]

            # --- Populate pages_data with comprehensive content ---
            pages_data = []

            # Page 1: Artist Overview and Social Media Performance
            artist_bio_markdown = f"""
            **Name:** {artist.name} ({artist.eng_name if artist.eng_name else 'N/A'})
            **Birth Date:** {artist.birth_date.strftime('%Y-%m-%d')}
            **Debut Date:** {artist.debut_date.strftime('%Y-%m-%d') if artist.debut_date else 'N/A'}
            **Nationality:** {artist.nationality if artist.nationality else 'N/A'}
            **Gender:** {artist.gender if artist.gender else 'N/A'}
            **Status:** {artist.status if artist.status else 'N/A'}
            **Genre:** {artist.genre if artist.genre else 'N/A'}
            **Height (cm):** {artist.height_cm if artist.height_cm else 'N/A'}
            **Guarantee (KRW):** {artist.guarantee_krw if artist.guarantee_krw else 'N/A'}
            **Social Media URL:** {artist.social_media_url if artist.social_media_url else 'N/A'}
            """
            artist_bio_html = markdown(artist_bio_markdown)

            profile_photo_filename = os.path.basename(artist.profile_photo) if artist.profile_photo else 'default.png'
            profile_photo_url = url_for('artists.serve_profile_photo', filename=profile_photo_filename, _external=True)

            page_1_content = f"""
                <section class="overview-section">
                    <div class="profile-header">
                        <div class="profile-image-container">
                             <img src="{profile_photo_url}" alt="{artist.name}" class="profile-image">
                        </div>
                        <div class="profile-info">
                            <h3>Biography</h3>
                            {artist_bio_html}
                        </div>
                    </div>
                </section>
                <section class="stats-section">
                    <h2>Social Media Performance</h2>
                    <table class="stats-table">
                        <thead>
                            <tr><th>Platform</th><th>Name</th><th>Followers</th><th>Engagement Rate</th></tr>
                        </thead>
                        <tbody>
                            {''.join([f'''
                            <tr>
                                <td>{stat['platform']}</td>
                                <td><a href="{stat['url']}">{stat['name']}</a></td>
                                <td>{stat['follower_count']:,}</td>
                                <td>{stat['engagement_rate']:.2f}%</td>
                            </tr>''' for stat in channel_stats_data]) if channel_stats_data else '<tr><td colspan="4">No social media data available.</td></tr>'}
                        </tbody>
                    </table>
                </section>
            """
            pages_data.append({'number': 1, 'content': page_1_content})
            
            # Page 2: Activities (Broadcast & CF)
            # Helper to generate activity rows
            def generate_activity_rows(activities):
                if not activities: return '<tr><td colspan="3">No activities found.</td></tr>'
                rows = []
                for act in activities:
                    start = act.start_time.strftime('%Y.%m') if act.start_time else ''
                    end = act.end_time.strftime('%Y.%m') if act.end_time else ''
                    period = f"{start} - {end}" if start or end else ''
                    rows.append(f'''
                        <tr>
                            <td class="activity-name">{act.activity_name}</td>
                            <td class="activity-type">{act.activity_type}</td>
                            <td class="activity-period">{period}</td>
                        </tr>
                    ''')
                return ''.join(rows)

            page_2_content = f"""
                <section class="activities-section">
                    <div class="activity-group">
                        <h2>Filmography (Broadcast & Movies)</h2>
                        <table class="activity-table">
                            <thead><tr><th>Title</th><th>Type</th><th>Period</th></tr></thead>
                            <tbody>
                                {generate_activity_rows(activities_broadcast)}
                            </tbody>
                        </table>
                    </div>
                    <div class="activity-group">
                        <h2>Advertising & Endorsements</h2>
                        <table class="activity-table">
                            <thead><tr><th>Brand/Campaign</th><th>Type</th><th>Period</th></tr></thead>
                            <tbody>
                                {generate_activity_rows(activities_cf)}
                            </tbody>
                        </table>
                    </div>
                </section>
            """
            pages_data.append({'number': 2, 'content': page_2_content})

            # Page 3: Recent News & Media
            page_3_content = f"""
                <section class="news-section">
                    <h2>Recent News & Media</h2>
                    <div class="news-grid">
                    {''.join([f'''
                    <div class="news-card">
                        <div class="news-header">
                            <span class="news-source">{news.media_name if news.media_name else news.source}</span>
                            <span class="news-date">{news.published_at.strftime('%Y-%m-%d') if news.published_at else 'N/A'}</span>
                        </div>
                        <h3 class="news-title"><a href="{news.url}">{news.title}</a></h3>
                        <p class="news-sentiment">Sentiment: {news.sentiment}</p>
                        <p class="news-snippet">{news.content[:200] + '...' if news.content else ''}</p>
                    </div>''' for news in recent_news_articles]) if recent_news_articles else '<p>No recent news articles available.</p>'}
                    </div>
                </section>
            """
            pages_data.append({'number': 3, 'content': page_3_content})

            # Render the HTML template (pass artist.eng_name to template)
            rendered_html = render_template(
                'report_template.html',
                report_title=f"{artist.eng_name if artist.eng_name else artist.name} Artist Report",
                artist_name=artist.eng_name if artist.eng_name else artist.name,
                generation_date=datetime.now().strftime('%Y-%m-%d'),
                author_name="FirstEnt Management", # Updated author name
                css_path=url_for('static', filename='css/report_styles.css'),
                logo_path=url_for('static', filename='images/logo.png'), # Placeholder logo
                small_logo_path=url_for('static', filename='images/small_logo.png'), # Placeholder small logo
                cover_page=True, # Set to False if no cover page
                pages=pages_data,
                header_text=f"{artist.eng_name if artist.eng_name else artist.name} - Confidential",
                footer_text="FirstEnt Management - Internal Report",
                activities_cf=activities_cf, # Pass context though we used pages_data mostly
                activities_broadcast=activities_broadcast,
                activities_other=activities_other
            )

            # --- Send HTML to Puppeteer service ---
            response = requests.post(
                PUPPETEER_SERVICE_URL,
                json={'htmlContent': rendered_html},
                timeout=60 # Timeout in seconds for Puppeteer to generate PDF
            )

            response.raise_for_status() # Raise an exception for HTTP errors

            pdf_buffer = BytesIO(response.content)
            
            # Save the generated HTML to a temporary file for inspection (optional, remove in production)
            temp_html_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                '..', 'temp', f'artist_report_{artist.id}.html'
            )
            os.makedirs(os.path.dirname(temp_html_path), exist_ok=True)
            with open(temp_html_path, 'w', encoding='utf-8') as f:
                f.write(rendered_html)
            print(f"Generated HTML saved to: {temp_html_path}")

            return send_file(
                pdf_buffer,
                download_name=f'artists_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
                mimetype='application/pdf'
            )

        except requests.exceptions.ConnectionError as e:
            logger.error(f"Could not connect to Puppeteer service: {e}", exc_info=True)
            return jsonify({'error': 'PDF 생성 서비스에 연결할 수 없습니다.'}), 500
        except requests.exceptions.Timeout:
            logger.error(f"Puppeteer service timed out.", exc_info=True)
            return jsonify({'error': 'PDF 생성 서비스 시간 초과.'}), 500
        except requests.exceptions.RequestException as e:
            logger.error(f"Error from Puppeteer service: {e}", exc_info=True)
            return jsonify({'error': f'PDF 생성 서비스 오류: {e}'}), 500
        except Exception as e:
            logger.error(f"Error generating HTML report: {e}", exc_info=True)
            return jsonify({'error': f'보고서 생성 중 오류 발생: {e}'}), 500
    elif report_format == 'pptx':
        from pptx.util import Inches, Pt
        from pptx.dml.color import RGBColor
        from PIL import Image as PImage # Alias to avoid conflict with reportlab.platypus.Image
        prs = Presentation()

        for artist in artists:
            # Cover Slide
            slide_layout = prs.slide_layouts[0] # Title Slide layout
            slide = prs.slides.add_slide(slide_layout)
            title = slide.shapes.title
            subtitle = slide.placeholders[1]

            title.text = artist.name
            subtitle.text = "Artist Commercial Proposal"

            if artist.profile_photo:
                filename_from_profile_photo = os.path.basename(artist.profile_photo)
                image_full_path = os.path.join(UPLOAD_FOLDER, filename_from_profile_photo)
                if os.path.exists(image_full_path):
                    try:
                        # Get original image dimensions using PIL
                        with PImage.open(image_full_path) as img_pil:
                            original_width, original_height = img_pil.size

                        # Define max dimensions for the slide
                        max_width_ptx = Inches(4)
                        max_height_ptx = Inches(4)

                        # Calculate aspect ratio
                        aspect_ratio = original_height / original_width

                        # Determine new dimensions while maintaining aspect ratio
                        if original_width > original_height:
                            new_width_ptx = max_width_ptx
                            new_height_ptx = max_width_ptx * aspect_ratio
                        else:
                            new_height_ptx = max_height_ptx
                            new_width_ptx = max_height_ptx / aspect_ratio
                        
                        # Ensure image fits within max bounds
                        if new_width_ptx > max_width_ptx:
                            new_width_ptx = max_width_ptx
                            new_height_ptx = max_width_ptx * aspect_ratio
                        if new_height_ptx > max_height_ptx:
                            new_height_ptx = max_height_ptx
                            new_width_ptx = max_height_ptx / aspect_ratio

                        img_left = Inches(3)
                        img_top = Inches(3)
                        slide.shapes.add_picture(image_full_path, img_left, img_top, new_width_ptx, new_height_ptx)
                    except Exception as e:
                        print(f"WARNING: Error loading cover image for PPTX report: {e}")

            # Artist Details Slide
            slide_layout = prs.slide_layouts[5] # Title and Content layout
            slide = prs.slides.add_slide(slide_layout)

            title = slide.shapes.title
            title.text = artist.name
            title.text_frame.paragraphs[0].font.size = Pt(48)
            title.text_frame.paragraphs[0].font.bold = True
            title.text_frame.paragraphs[0].font.color.rgb = RGBColor(0xED, 0x71, 0x04) # Orange

            subtitle.text = "Artist Commercial Proposal"
            subtitle.text_frame.paragraphs[0].font.size = Pt(28)
            subtitle.text_frame.paragraphs[0].font.color.rgb = RGBColor(0x36, 0x45, 0x4F) # Deep Navy

            if artist.profile_photo:
                filename_from_profile_photo = os.path.basename(artist.profile_photo)
                image_full_path = os.path.join(UPLOAD_FOLDER, filename_from_profile_photo)
                if os.path.exists(image_full_path):
                    try:
                        img_left = Inches(3)
                        img_top = Inches(3)
                        img_width = Inches(4)
                        img_height = Inches(4)
                        slide.shapes.add_picture(image_full_path, img_left, img_top, img_width, img_height)
                    except Exception as e:
                        print(f"WARNING: Error loading cover image for PPTX report: {e}")

            # Artist Details Slide
            slide_layout = prs.slide_layouts[5] # Title and Content layout
            slide = prs.slides.add_slide(slide_layout)

            title = slide.shapes.title
            title.text = f"{artist.name} - Detailed Profile"
            title.text_frame.paragraphs[0].font.size = Pt(24)
            title.text_frame.paragraphs[0].font.bold = True
            title.text_frame.paragraphs[0].font.color.rgb = RGBColor(0x36, 0x45, 0x4F) # Deep Navy

            left = Inches(0.5)
            top = Inches(1.5)
            width = Inches(6)
            height = Inches(0.5)

            # Profile Photo on details slide
            if artist.profile_photo:
                filename_from_profile_photo = os.path.basename(artist.profile_photo)
                image_full_path = os.path.join(UPLOAD_FOLDER, filename_from_profile_photo)

                if os.path.exists(image_full_path):
                    try:
                        # Get original image dimensions using PIL
                        with PImage.open(image_full_path) as img_pil:
                            original_width, original_height = img_pil.size

                        # Define max dimensions for the slide
                        max_width_ptx = Inches(2.5)
                        max_height_ptx = Inches(2.5)

                        # Calculate aspect ratio
                        aspect_ratio = original_height / original_width

                        # Determine new dimensions while maintaining aspect ratio
                        if original_width > original_height:
                            new_width_ptx = max_width_ptx
                            new_height_ptx = max_width_ptx * aspect_ratio
                        else:
                            new_height_ptx = max_height_ptx
                            new_width_ptx = max_height_ptx / aspect_ratio
                        
                        # Ensure image fits within max bounds
                        if new_width_ptx > max_width_ptx:
                            new_width_ptx = max_width_ptx
                            new_height_ptx = max_width_ptx * aspect_ratio
                        if new_height_ptx > max_height_ptx:
                            new_height_ptx = max_height_ptx
                            new_width_ptx = max_height_ptx / aspect_ratio

                        img_left = Inches(7)
                        img_top = Inches(1.5)
                        slide.shapes.add_picture(image_full_path, img_left, img_top, new_width_ptx, new_height_ptx)
                    except Exception as e:
                        txBox = slide.shapes.add_textbox(left, top, width, height)
                        tf = txBox.text_frame
                        p = tf.add_paragraph()
                        p.text = f"[Error loading image: {e}]"
                else:
                    txBox = slide.shapes.add_textbox(left, top, width, height)
                    tf = txBox.text_frame
                    p = tf.add_paragraph()
                    p.text = f"[Profile photo not found at {image_full_path}]"
            
            # Artist Details
            txBox = slide.shapes.add_textbox(left, top, width, height)
            tf = txBox.text_frame
            tf.word_wrap = True

            def add_paragraph(text_frame, text, level=0, font_size=Pt(11), bold=False, color=RGBColor(0x00, 0x00, 0x00)):
                p = text_frame.add_paragraph()
                p.text = text
                p.level = level
                p.font.size = font_size
                p.font.bold = bold
                p.font.color.rgb = color

            add_paragraph(tf, f"Artist Profile:", level=0, font_size=Pt(14), bold=True, color=RGBColor(0xED, 0x71, 0x04)) # Orange
            add_paragraph(tf, f"Name: {artist.name}", level=1)
            add_paragraph(tf, f"Gender: {artist.gender if artist.gender else 'N/A'}", level=1)
            add_paragraph(tf, f"Nationality: {artist.nationality if artist.nationality else 'N/A'}", level=1)
            add_paragraph(tf, f"Status: {artist.status if artist.status else 'N/A'}", level=1)
            add_paragraph(tf, f"Genre: {artist.genre if artist.genre else 'N/A'}", level=1)
            add_paragraph(tf, f"Category: {artist.category_id if artist.category_id else 'N/A'}", level=1)
            add_paragraph(tf, f"Height (cm): {artist.height_cm if artist.height_cm else 'N/A'}", level=1)
            add_paragraph(tf, f"Debut Date: {artist.debut_date.isoformat() if artist.debut_date else 'N/A'}", level=1)
            add_paragraph(tf, f"Guarantee (KRW): {artist.guarantee_krw if artist.guarantee_krw else 'N/A'}", level=1)

            add_paragraph(tf, f"\nSocial Media Presence:", level=0, font_size=Pt(14), bold=True, color=RGBColor(0xED, 0x71, 0x04)) # Orange
            add_paragraph(tf, f"Platform: {artist.platform if artist.platform else 'N/A'}", level=1)
            add_paragraph(tf, f"URL: {artist.social_media_url if artist.social_media_url else 'N/A'}", level=1)

            add_paragraph(tf, f"\nMedia Highlights:", level=0, font_size=Pt(14), bold=True, color=RGBColor(0xED, 0x71, 0x04)) # Orange
            if recent_news:
                for news_item in recent_news:
                    add_paragraph(tf, f"Title: {news_item.title}", level=1, bold=True)
                    add_paragraph(tf, f"Source: {news_item.source} - {news_item.published_at.strftime('%Y-%m-%d') if news_item.published_at else 'N/A'}", level=1)
                    add_paragraph(tf, f"Snippet: {news_item.content}", level=1)
            add_paragraph(tf, f"URL: {news_item.url}", level=1)
            
            # Word Cloud and Meta Tags
            wordcloud_image_path, meta_tags = generate_wordcloud_for_artist(artist.id)
            if wordcloud_image_path:
                try:
                    img_left = Inches(0.5)
                    img_top = Inches(7)
                    img_width = Inches(5)
                    img_height = Inches(2.5)
                    slide.shapes.add_picture(wordcloud_image_path, img_left, img_top, img_width, img_height)
                except Exception as e:
                    add_paragraph(tf, f"[Error loading word cloud image: {e}]", level=1)
            
            if meta_tags:
                add_paragraph(tf, f"Keywords: " + ", ".join(meta_tags), level=1)

        buffer = BytesIO()
        prs.save(buffer)
        buffer.seek(0)
        return send_file(buffer, download_name=f'artists_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pptx', mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation')

    return jsonify({'error': '지원되지 않는 보고서 형식입니다.'}), 400

@bp.route('/<int:artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    """아티스트 삭제"""
    artist = Artist.query.get_or_404(artist_id)
    # Explicitly merge the object into the current session before deletion
    artist = db.session.merge(artist)
    db.session.delete(artist)
    db.session.commit()
    
    return jsonify({'message': '아티스트가 삭제되었습니다.'}), 200

@bp.route('/upsert-from-wiki', methods=['POST'])
@require_role('admin')
def upsert_artist_from_wiki():
    data = request.get_json()
    artist_data = data.get('artist_data')

    if not artist_data or not artist_data.get('name'):
        return jsonify({'error': 'Artist data or name is missing.'}), 400

    artist_name = artist_data['name']
    existing_artist = Artist.query.filter_by(name=artist_name).first()

    try:
        if existing_artist:
            # Update existing artist
            artist = existing_artist
            message = f"아티스트 '{artist_name}' 정보가 업데이트되었습니다."
        else:
            # Create new artist
            artist = Artist()
            message = f"새로운 아티스트 '{artist_name}' 정보가 추가되었습니다."
            db.session.add(artist)

        # Map and convert data types for all fields
        artist.name = artist_data.get('name', artist.name)
        artist.eng_name = artist_data.get('eng_name', artist.eng_name)
        
        # Handle birth_date
        if artist_data.get('birth_date') and artist_data['birth_date'] != 'NULL':
            artist.birth_date = datetime.strptime(artist_data['birth_date'], '%Y-%m-%d').date()
        else:
            artist.birth_date = None # Explicitly set to None for NULL

        artist.height_cm = int(artist_data['height_cm']) if artist_data.get('height_cm') and artist_data['height_cm'] != 'NULL' else None
        
        # Handle debut_date
        if artist_data.get('debut_date') and artist_data['debut_date'] != 'NULL':
            artist.debut_date = datetime.strptime(artist_data['debut_date'], '%Y-%m-%d').date()
        else:
            artist.debut_date = None # Explicitly set to None for NULL

        artist.debut_title = artist_data.get('debut_title', artist.debut_title)
        artist.recent_activity_category = artist_data.get('recent_activity_category', artist.recent_activity_category)
        artist.recent_activity_name = artist_data.get('recent_activity_name', artist.recent_activity_name)
        artist.genre = artist_data.get('genre', artist.genre)
        artist.agency_id = int(artist_data['agency_id']) if artist_data.get('agency_id') and artist_data['agency_id'] != 'NULL' else None
        artist.current_agency_name = artist_data.get('current_agency_name', artist.current_agency_name)
        artist.nationality = artist_data.get('nationality', artist.nationality)
        artist.is_korean = artist_data.get('is_korean', artist.is_korean) in [True, 'True', 1, '1'] # Handle boolean
        artist.gender = artist_data.get('gender', artist.gender)
        artist.status = artist_data.get('status', artist.status)
        artist.category_id = int(artist_data['category_id']) if artist_data.get('category_id') and artist_data['category_id'] != 'NULL' else None
        artist.platform = artist_data.get('platform', artist.platform)
        artist.social_media_url = artist_data.get('social_media_url', artist.social_media_url)
        artist.profile_photo = artist_data.get('profile_photo', artist.profile_photo)
        artist.guarantee_krw = int(artist_data['guarantee_krw']) if artist_data.get('guarantee_krw') and artist_data['guarantee_krw'] != 'NULL' else None
        artist.wiki_summary = artist_data.get('wiki_summary', artist.wiki_summary)

        db.session.commit()
        return jsonify({'message': message, 'artist': artist.to_dict()}), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error upserting artist {artist_name} from wiki: {e}", exc_info=True)
        return jsonify({'error': f'DB 적용 중 오류 발생: {e}'}), 500

from backend.services.news_crawler import NewsCrawler # Import NewsCrawler

@bp.route('/<int:artist_id>/crawl-news', methods=['POST'])
def trigger_news_crawl(artist_id):
    """특정 아티스트에 대한 뉴스 크롤링을 수동으로 트리거"""
    artist = Artist.query.get_or_404(artist_id)
    crawler = NewsCrawler()
    news_items = crawler.search_news_for_artist(artist)
    saved_count = crawler.save_news_to_db(news_items, artist)
    return jsonify({'message': f'{artist.name}에 대한 {saved_count}개 뉴스 크롤링 및 저장 완료', 'saved_count': saved_count})
