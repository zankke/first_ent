import wikipedia
import datetime
import re
import sys

print("sys.path:", sys.path)

def artist_exists_in_db(artist_name: str) -> bool:
    """
    Placeholder function to simulate checking if an artist exists in the database.
    In a real application, this would query the database.
    """
    # For demonstration, let's assume a few artists exist
    existing_artists = ["아이유", "방탄소년단", "블랙핑크", "IU", "NewJeans"]
    return artist_name in existing_artists

def _clean_text(text: str) -> str:
    """Cleans text by removing reference brackets like [1], [2]."""
    return re.sub(r'\\[d+\\]', '', text).strip()

def extract_artist_info_from_wikipedia(artist_name: str) -> dict:
    """
    Searches Wikipedia for artist information and extracts relevant details.
    Prioritizes Korean Wikipedia, then falls back to English.
    """
    info = {
        'name': artist_name,
        'eng_name': None,
        'birth_date': None,
        'height_cm': None,
        'debut_date': None,
        'debut_title': None,
        'recent_activity_category': None,
        'recent_activity_name': None,
        'genre': None,
        'current_agency_name': None,
        'nationality': None,
        'gender': 'NA', # Default to NA
        'is_korean': 1, # Default to 1 (Korean)
        'wiki_summary': None
    }

    current_lang = None
    page = None
    try:
        # Try Korean Wikipedia first
        wikipedia.set_lang("ko")
        page = wikipedia.page(artist_name, auto_suggest=True, redirect=True)
        current_lang = "ko"
    except wikipedia.exceptions.PageError:
        try:
            # Fallback to English Wikipedia
            wikipedia.set_lang("en")
            page = wikipedia.page(artist_name, auto_suggest=True, redirect=True)
            current_lang = "en"
        except wikipedia.exceptions.PageError:
            print(f"No Wikipedia page found for '{artist_name}'.")
            return info
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"Disambiguation page found for '{artist_name}'. Trying first option: {e.options[0]}")
            try:
                wikipedia.set_lang("en")
                page = wikipedia.page(e.options[0], auto_suggest=True, redirect=True)
                current_lang = "en"
            except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):
                print(f"Could not resolve disambiguation for '{artist_name}'.")
                return info
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"Disambiguation page found for '{artist_name}'. Trying first option: {e.options[0]}")
        try:
            wikipedia.set_lang("ko")
            page = wikipedia.page(e.options[0], auto_suggest=True, redirect=True)
            current_lang = "ko"
        except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):
            print(f"Could not resolve disambiguation for '{artist_name}'.")
            return info


    if page:
        info['wiki_summary'] = _clean_text(page.summary)

        # Name / English Name
        if current_lang == "ko":
            # Check if the page title itself is primarily English (e.g., searching "뉴진스" but title is "NewJeans")
            if re.match(r'^[A-Za-z\s\-\'’]+$', page.title):
                info['eng_name'] = page.title
                # Try to find the Korean name in the summary, e.g., "NewJeans(뉴진스)"
                ko_name_from_summary = re.search(r'\(([가-힣\s]+)\)', info['wiki_summary'])
                if ko_name_from_summary:
                    info['name'] = ko_name_from_summary.group(1).strip()
                else: # Fallback: if no Korean name found in summary, use original artist_name if it was Korean
                    if re.match(r'^[가-힣\s]+$', artist_name):
                        info['name'] = artist_name
                    else:
                        info['name'] = page.title # Fallback to English name if no Korean name can be found
            else: # Page title is likely Korean
                info['name'] = page.title # Assume page title is the Korean name
                # Try to extract English name from title (e.g., "아이유(IU)")
                eng_name_match_in_title = re.search(r'\(([^)]+)\)', page.title)
                if eng_name_match_in_title:
                    extracted_eng = eng_name_match_in_title.group(1).split(',')[0].strip()
                    # Ensure it looks like an English name and not a birth name or other info
                    if re.match(r'^[A-Za-z\s\-\'’]+$', extracted_eng):
                        info['eng_name'] = extracted_eng
                
                if not info['eng_name']: # If not found in title, try summary
                    # Regex to find English name in summary like "아이유 (IU, 본명: 이지은)"
                    # This targets the first English-looking word in parenthesis after the Korean name.
                    eng_name_from_summary = re.search(r'(?:[ㄱ-힣]+)\s*\((?P<eng_name>[A-Za-z\s\-\'’]+)(?:,|\)|\s본명)', info['wiki_summary'])
                    if eng_name_from_summary:
                        info['eng_name'] = eng_name_from_summary.group('eng_name').strip()


        elif current_lang == "en":
            info['eng_name'] = page.title # Assume page title is the English name

            # Try to find Korean name in the summary or first sentence, e.g., "IU (아이유)"
            ko_name_match_in_summary = re.search(r'\(([가-힣\s]+)\)', info['wiki_summary'])
            if ko_name_match_in_summary:
                info['name'] = ko_name_match_in_summary.group(1).strip()
            
            if not info['name']: # If Korean name still not found, try to use artist_name as Korean if it's Korean
                if re.match(r'^[가-힣\s]+$', artist_name): # Check if the original search term was Korean
                    info['name'] = artist_name 
                else:
                    info['name'] = info['eng_name'] # Fallback to English name if no Korean name can be found


        content = page.content

        # Birth Date
        # Regex to capture date in YYYY년 M월 D일 or YYYY-MM-DD format from content
        birth_date_match = re.search(r'(생년월일|출생|출생일)\s*[:=]?\s*(\d{4}년\s*\d{1,2}월\s*\d{1,2}일|\d{4}[년\s\-](\d{1,2})[월\s\-](\d{1,2})일?|\d{4}-\d{1,2}-\d{1,2})', content)
        if birth_date_match:
            date_str = birth_date_match.group(2)
            date_str = date_str.replace('년', '-').replace('월', '-').replace('일', '').replace(' ', '').strip()
            # Handle cases like "YYYY-MM" or "YYYY" if day is missing, default to 01
            try:
                if re.match(r'^\d{4}-\d{1,2}-\d{1,2}$', date_str):
                    info['birth_date'] = datetime.datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
                elif re.match(r'^\d{4}-\d{1,2}$', date_str):
                    info['birth_date'] = datetime.datetime.strptime(date_str + '-01', '%Y-%m-%d').strftime('%Y-%m-%d')
                elif re.match(r'^\d{4}$', date_str):
                    info['birth_date'] = datetime.datetime.strptime(date_str + '-01-01', '%Y-%m-%d').strftime('%Y-%m-%d')
            except ValueError:
                pass
        
        if not info['birth_date']: # Try from wiki_summary if not found in content
            birth_date_summary_match = re.search(r'(\d{4}년\s*\d{1,2}월\s*\d{1,2}일|\d{4}[년\s\-](\d{1,2})[월\s\-](\d{1,2})일?|\d{4}-\d{1,2}-\d{1,2})', info['wiki_summary'])
            if birth_date_summary_match:
                date_str = birth_date_summary_match.group(1)
                date_str = date_str.replace('년', '-').replace('월', '-').replace('일', '').replace(' ', '').strip()
                try:
                    if re.match(r'^\d{4}-\d{1,2}-\d{1,2}$', date_str):
                        info['birth_date'] = datetime.datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
                    elif re.match(r'^\d{4}-\d{1,2}$', date_str):
                        info['birth_date'] = datetime.datetime.strptime(date_str + '-01', '%Y-%m-%d').strftime('%Y-%m-%d')
                    elif re.match(r'^\d{4}$', date_str):
                        info['birth_date'] = datetime.datetime.strptime(date_str + '-01-01', '%Y-%m-%d').strftime('%Y-%m-%d')
                except ValueError:
                    pass

        # Height
        # Regex to capture height in cm, e.g., "161.8 cm"
        height_match = re.search(r'(신장|키)\s*[:=]?\s*(\d{2,3}(?:\.\d+)?)\s*cm', content)
        if height_match:
            try:
                info['height_cm'] = int(float(height_match.group(2)))
            except ValueError:
                pass

        # Debut Date and Title
        # Regex to capture: (데뷔|활동 시작일)\s*:\s*(DATE)\s*(?:로)?\s*(?:[ARTIST_NAME]의)?\s*(TITLE)?\s*(?:데뷔|활동)?
        debut_match = re.search(r'(데뷔|활동 시작일)\s*:\s*((\d{4}년\s*\d{1,2}월\s*\d{1,2}일|\d{4}-\d{1,2}-\d{1,2}))(?:\\[d+\\])?(?:로\s*(?:' + re.escape(artist_name) + r')?\s*(?:의\s*)?([^\n,.]+)?(?:데뷔|활동))?', content)
        if debut_match:
            date_str = debut_match.group(2).replace('년', '-').replace('월', '-').replace('일', '').replace(' ', '')
            try:
                info['debut_date'] = datetime.datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
            except ValueError:
                pass
            if debut_match.group(3): # This group should capture the debut title if present
                info['debut_title'] = _clean_text(debut_match.group(3))

        # Genre
        genre_match = re.search(r'(장르|음악 장르)\s*:\s*([^\n]+)', content)
        if genre_match:
            info['genre'] = _clean_text(genre_match.group(2).split(',')[0]) # Take first genre

        # Agency
        agency_match = re.search(r'(소속사|기획사)\s*:\s*([^\n]+)', content)
        if agency_match:
            info['current_agency_name'] = _clean_text(agency_match.group(2).split(',')[0]) # Take first agency

        # Nationality
        nationality_match = re.search(r'(국적|국가)\s*:\s*([^\n]+)', content)
        if nationality_match:
            info['nationality'] = _clean_text(nationality_match.group(2).split(',')[0])
            if '대한민국' not in info['nationality'] and 'South Korea' not in info['nationality'] and info['nationality'] is not None:
                info['is_korean'] = 0 # Set to 0 if nationality is explicitly not Korean and not None
        
        if not info['nationality']: # Try from wiki_summary if not found in content
            # This regex will look for patterns like "한국계 미국인" (Korean-American) or "국적: 미국"
            nationality_summary_match = re.search(r'(국적|국가|출신|계)\s*[:=]?\s*([^\n,]+)', info['wiki_summary'])
            if nationality_summary_match:
                info['nationality'] = _clean_text(nationality_summary_match.group(2).split(',')[0])
                if '대한민국' not in info['nationality'] and 'South Korea' not in info['nationality'] and info['nationality'] is not None:
                    info['is_korean'] = 0

        # Gender (simple heuristic for Korean names - might need refinement)
        if '성별' in content:
            gender_ko_match = re.search(r'성별\s*:\s*(여성|남성)', content)
            if gender_ko_match:
                info['gender'] = 'WOMAN' if '여성' in gender_ko_match.group(1) else 'MEN'
        elif 'gender' in content: # English pages
            gender_en_match = re.search(r'gender\s*=\s*(female|male)', content, re.IGNORECASE)
            if gender_en_match:
                info['gender'] = 'WOMAN' if 'female' in gender_en_match.group(1).lower() else 'MEN'


    return info

def generate_sql_query(artist_name: str) -> str:
    """
    Generates an SQL INSERT or UPDATE query for the Artists table
    based on Wikipedia information.
    """
    artist_data = extract_artist_info_from_wikipedia(artist_name)
    
    # Fill in default values for fields not easily extractable or not provided by Wikipedia
    artist_data['status'] = 'ACTIVE'
    artist_data['guarantee_krw'] = 0
    artist_data['recent_activity_category'] = artist_data.get('recent_activity_category') or 'UNKNOWN'
    artist_data['recent_activity_name'] = artist_data.get('recent_activity_name') or 'UNKNOWN'
    artist_data['platform'] = artist_data.get('platform') or 'UNKNOWN'
    artist_data['social_media_url'] = artist_data.get('social_media_url') or None
    artist_data['profile_photo'] = artist_data.get('profile_photo') or None
    artist_data['agency_id'] = artist_data.get('agency_id') or 'NULL'
    artist_data['category_id'] = artist_data.get('category_id') or 'NULL'

    # Ensure name is not None, use eng_name if korean name not found during parsing
    if not artist_data['name'] and artist_data['eng_name']:
        artist_data['name'] = artist_data['eng_name']
    elif not artist_data['name']:
        artist_data['name'] = artist_name # Fallback to original search term

    print("artist_data before sql_values generation:", artist_data)
    # Define single quote constants to avoid f-string backslash issues
    SINGLE_QUOTE = "'"
    DOUBLE_SINGLE_QUOTE = "''"

    # Format values for SQL
    sql_values = {}
    for key, value in artist_data.items():
        if value is None or value == 'NULL':
            sql_values[key] = 'NULL'
        elif isinstance(value, str):
            # Escape single quotes by replacing ' with ''
            sql_values[key] = f"{SINGLE_QUOTE}{value.replace(SINGLE_QUOTE, DOUBLE_SINGLE_QUOTE)}{DOUBLE_SINGLE_QUOTE}"
        else:
            sql_values[key] = str(value)
    print("sql_values before update/insert:", sql_values)
    
    # Check if artist exists to determine INSERT or UPDATE
    clean_artist_name = artist_data['name'].strip("'" ) if artist_data['name'] else artist_name
    if artist_exists_in_db(clean_artist_name):
        # Generate UPDATE query
        update_fields = []
        for col in [
            'name', 'eng_name', 'birth_date', 'height_cm', 'debut_date',
            'debut_title', 'recent_activity_category', 'recent_activity_name',
            'genre', 'agency_id', 'current_agency_name', 'nationality',
            'is_korean', 'gender', 'status', 'category_id', 'platform',
            'social_media_url', 'profile_photo', 'guarantee_krw', 'wiki_summary'
        ]:
            # Only update if the value is not NULL, or if it's explicitly set to NULL and not agency_id/category_id
            if sql_values[col] != 'NULL' or (sql_values[col] == 'NULL' and col not in ['agency_id', 'category_id']):
                 update_fields.append(f"{col}={sql_values[col]}")


        # For the purpose of this exercise, we need to decide how to identify an artist for UPDATE.
        # Since we don't have IDs from the DB, we'll assume `name` is unique for updates.
        # In a real scenario, you'd fetch the existing artist's ID.
        return f"""UPDATE first_ent.Artists
SET {', '.join(update_fields)}
WHERE name={sql_values['name']};"""
    else:
        # Generate INSERT query
        columns = []
        values = []
        for col in [
            'name', 'eng_name', 'birth_date', 'height_cm', 'debut_date',
            'debut_title', 'recent_activity_category', 'recent_activity_name',
            'genre', 'agency_id', 'current_agency_name', 'nationality',
            'is_korean', 'gender', 'status', 'category_id', 'platform',
            'social_media_url', 'profile_photo', 'guarantee_krw', 'wiki_summary'
        ]:
            columns.append(col)
            values.append(sql_values[col])

        # id is AUTO_INCREMENT, so we don't include it in INSERT.
        return f"""INSERT INTO first_ent.Artists
({', '.join(columns)})
VALUES({', '.join(values)});
"""

if __name__ == "__main__":
    # Example Usage:
    artist = "아이유"
    sql_query = generate_sql_query(artist)
    print(f"SQL Query for '{artist}':\n{sql_query}\n")

    artist_not_in_db = "뉴진스" # This artist is not in our simulated DB
    sql_query_new = generate_sql_query(artist_not_in_db)
    print(f"SQL Query for '{artist_not_in_db}' (new artist):\n{sql_query_new}\n")

    artist_eng = "IU" # This artist is in our simulated DB
    sql_query_eng = generate_sql_query(artist_eng)
    print(f"SQL Query for '{artist_eng}' (existing artist, English name):\n{sql_query_eng}\n")

    artist_unknown = "존재하지않는 아티스트"
    sql_query_unknown = generate_sql_query(artist_unknown)
    print(f"SQL Query for '{artist_unknown}' (unknown artist):\n{sql_query_unknown}\n")