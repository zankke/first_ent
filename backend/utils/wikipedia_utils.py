# backend/utils/wikipedia_utils.py

import wikipediaapi
from datetime import datetime
import re
import logging

logger = logging.getLogger(__name__)

# Keywords for filtering disambiguation pages
ENTERTAINMENT_KEYWORDS_KO = ['배우', '가수', '모델', '방송인', '아이돌', '멤버', '그룹', '엔터테인먼트', '연기자', '예술가', '뮤지컬', '아나운서', '코메디언', '인플루언서']
EXCLUDE_KEYWORDS_KO = ['정치인', '기업인',  '감독', '선수', '학자', '교수', ] # '축구 선수', '야구 선수', '운동선수', '만화가' 

ENTERTAINMENT_KEYWORDS_EN = ['actor', 'singer', 'model', 'entertainer', 'idol', 'member', 'group', 'actress', 'artist', 'musical']
EXCLUDE_KEYWORDS_EN = ['politician', 'footballer', 'baseball player', 'businessman', 'executive', 'announcer', 'director', 'player', 'scholar', 'professor', 'athlete', 'cartoonist']

def _extract_artist_details(page, artist_name, used_wiki_instance) -> dict:
    """
    Extracts artist details from a given WikipediaPage object.
    """
    artist_info = {}
    
    # Extract summary
    artist_info['wiki_summary'] = page.summary

    # Extract specific fields from page content
    text = page.text

    # Helper to extract a single line value
    def extract_field(pattern):
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None

    # Name and English Name (assuming primary search is Korean name)
    artist_info['name'] = artist_name
    eng_name_match = re.search(r'영어 이름\s*[:=]\s*(.*?)\n', text)
    if eng_name_match:
        artist_info['eng_name'] = eng_name_match.group(1).strip()
    else:
        # Attempt to find English name in parentheses at the beginning of summary
        eng_name_paren_match = re.search(r'^(.*?)\((.*?)\)', artist_info['wiki_summary'])
        if eng_name_paren_match:
            artist_info['eng_name'] = eng_name_paren_match.group(2).strip()
        else:
            # Fallback to English Wikipedia title if available and different
            if used_wiki_instance.language == 'en' and artist_name.lower() != page.title.lower():
                artist_info['eng_name'] = page.title

    # Birth Date
    birth_date_str = extract_field(r'출생일\s*[:=]\s*(\d{4}년\s*\d{1,2}월\s*\d{1,2}일)')
    if birth_date_str:
        try:
            birth_date_str = birth_date_str.replace('년', '-').replace('월', '-').replace('일', '').strip()
            artist_info['birth_date'] = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        except ValueError:
            artist_info['birth_date'] = None
    
    # Height
    height_cm_str = extract_field(r'신체\s*[:=].*?(\d{2,3})cm')
    if height_cm_str:
        artist_info['height_cm'] = int(height_cm_str)

    # Debut Date
    debut_date_str = extract_field(r'데뷔\s*[:=]\s*(\d{4}년\s*\d{1,2}월\s*\d{1,2}일)')
    if debut_date_str:
        try:
            debut_date_str = debut_date_str.replace('년', '-').replace('월', '-').replace('일', '').strip()
            artist_info['debut_date'] = datetime.strptime(debut_date_str, '%Y-%m-%d').date()
        except ValueError:
            artist_info['debut_date'] = None

    # Debut Title
    debut_title_str = extract_field(r'데뷔곡\s*[:=]\s*(.*?)\n')
    if debut_title_str:
        artist_info['debut_title'] = debut_title_str

    # Genre
    genre_str = extract_field(r'장르\s*[:=]\s*(.*?)\n')
    if genre_str:
        artist_info['genre'] = genre_str

    # Current Agency Name
    agency_str = extract_field(r'소속사\s*[:=]\s*(.*?)\n')
    if agency_str:
        artist_info['current_agency_name'] = agency_str

    # Nationality
    nationality_str = extract_field(r'국적\s*[:=]\s*(.*?)\n')
    if nationality_str:
        artist_info['nationality'] = nationality_str
        artist_info['is_korean'] = ('대한민국' in nationality_str or '한국' in nationality_str)
    else:
        # Assume Korean if not explicitly stated and using Korean Wikipedia
        if used_wiki_instance.language == 'ko':
            artist_info['is_korean'] = True

    # Gender
    gender_str = extract_field(r'성별\s*[:=]\s*(.*?)\n')
    if gender_str:
        if '여성' in gender_str or '여자' in gender_str:
            artist_info['gender'] = 'WOMAN'
        elif '남성' in gender_str or '남자' in gender_str:
            artist_info['gender'] = 'MEN'
        else:
            artist_info['gender'] = 'NA' # Not Applicable/Unknown

    artist_info['recent_activity_category'] = None
    artist_info['recent_activity_name'] = None

    return artist_info

def get_artist_info_from_wikipedia(artist_name: str) -> dict:
    """
    Searches Wikipedia for artist information and extracts relevant details.
    
    Args:
        artist_name: The name of the artist to search for.
        
    Returns:
        A dictionary containing extracted artist information, or an empty dictionary if not found.
    """
    
    wiki_wiki_ko = wikipediaapi.Wikipedia(
        language='ko',
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent='FirstEnt-Artist-Management-Framework/1.0 (contact@example.com)' # Added user_agent
    )

    page_py = wiki_wiki_ko.page(artist_name)
    used_wiki_instance = wiki_wiki_ko # Keep track of which Wikipedia instance was used

    if not page_py.exists():
        # Try searching in English Wikipedia if not found in Korean
        wiki_wiki_en = wikipediaapi.Wikipedia(
            language='en', 
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent='FirstEnt-Artist-Management-Framework/1.0 (contact@example.com)' # Added user_agent
        )
        page_py = wiki_wiki_en.page(artist_name)
        used_wiki_instance = wiki_wiki_en # Update to English instance if found there
        if not page_py.exists():
            return {} # Artist not found in both languages

    # --- Disambiguation handling ---
    if page_py.is_disambiguation:
        logger.info(f"Disambiguation page found for {artist_name}. Analyzing links...")
        
        candidates = []
        for title in page_py.links.keys():
            candidate_page = used_wiki_instance.page(title)
            if candidate_page.exists() and not candidate_page.is_disambiguation:
                summary = candidate_page.summary.lower()
                text = candidate_page.text.lower()
                
                is_entertainment = False
                if used_wiki_instance.language == 'ko':
                    if any(kw in summary for kw in ENTERTAINMENT_KEYWORDS_KO) or any(kw in text for kw in ENTERTAINMENT_KEYWORDS_KO):
                        is_entertainment = True
                    is_excluded = any(kw in summary for kw in EXCLUDE_KEYWORDS_KO) or any(kw in text for kw in EXCLUDE_KEYWORDS_KO)
                else: # English
                    if any(kw in summary for kw in ENTERTAINMENT_KEYWORDS_EN) or any(kw in text for kw in ENTERTAINMENT_KEYWORDS_EN):
                        is_entertainment = True
                    is_excluded = any(kw in summary for kw in EXCLUDE_KEYWORDS_EN) or any(kw in text for kw in EXCLUDE_KEYWORDS_EN)

                if is_entertainment and not is_excluded:
                    candidates.append(candidate_page)
                    logger.info(f"Found potential artist candidate: {candidate_page.title}")
        
        if candidates:
            # For simplicity, pick the first suitable candidate. More complex logic could be added here.
            # E.g., prioritize by summary length, relevance to original artist_name, etc.
            logger.info(f"Selecting '{candidates[0].title}' from disambiguation candidates.")
            return _extract_artist_details(candidates[0], artist_name, used_wiki_instance)
        else:
            logger.info(f"No suitable entertainment artist found on disambiguation page for {artist_name}.")
            return {} # No suitable artist found on disambiguation page

    # Now call the helper function to extract details for a non-disambiguation page
    return _extract_artist_details(page_py, artist_name, used_wiki_instance)

if __name__ == '__main__':
    # Example usage
    artist_name = "아이유" # IU
    info = get_artist_info_from_wikipedia(artist_name)
    if info:
        print(f"Information for {artist_name}:")
        for key, value in info.items():
            print(f"  {key}: {value}")
    else:
        print(f"Could not find information for {artist_name}.")

    artist_name_en = "BTS" # Example for English search
    info_en = get_artist_info_from_wikipedia(artist_name_en)
    if info_en:
        print(f"\nInformation for {artist_name_en}:")
        for key, value in info_en.items():
            print(f"  {key}: {value}")
    else:
        print(f"Could not find information for {artist_name_en}.")