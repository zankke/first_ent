# backend/utils/wikipedia_utils.py

import wikipediaapi
from datetime import datetime
import re
import logging

logger = logging.getLogger(__name__)
import logging

logger = logging.getLogger(__name__)

# Keywords for filtering disambiguation pages
logger = logging.getLogger(__name__)

# Keywords for filtering disambiguation pages
ENTERTAINMENT_KEYWORDS_KO = ['배우', '가수', '모델', '방송인', '아이돌', '멤버', '그룹', '엔터테인먼트', '연기자', '예술가', '뮤지컬', '아나운서', '코메디언', '인플루언서']
EXCLUDE_KEYWORDS_KO = ['정치인', '기업인', '감독', '선수', '학자', '교수']

ENTERTAINMENT_KEYWORDS_EN = ['actor', 'singer', 'model', 'broadcaster', 'idol', 'member', 'group', 'entertainment', 'actor', 'artist', 'musical', 'announcer', 'comedian', 'influencer']
EXCLUDE_KEYWORDS_EN = ['politician', 'businessman', 'director', 'player', 'scholar', 'professor']

import wikipediaapi
import requests
from datetime import datetime
import re
import logging

logger = logging.getLogger(__name__)

# Keywords for filtering disambiguation pages
ENTERTAINMENT_KEYWORDS_KO = ['배우', '가수', '모델', '방송인', '아이돌', '멤버', '그룹', '엔터테인먼트', '연기자', '예술가', '뮤지컬', '아나운서', '코메디언', '인플루언서']
EXCLUDE_KEYWORDS_KO = ['정치인', '기업인', '감독', '선수', '학자', '교수']

ENTERTAINMENT_KEYWORDS_EN = ['actor', 'singer', 'model', 'broadcaster', 'idol', 'member', 'group', 'entertainment', 'actor', 'artist', 'musical', 'announcer', 'comedian', 'influencer']
EXCLUDE_KEYWORDS_EN = ['politician', 'businessman', 'director', 'player', 'scholar', 'professor']

def get_raw_wikitext(title, lang='ko'):
    """Fetches raw wikitext using MediaWiki API."""
    url = f"https://{lang}.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "page": title,
        "prop": "wikitext",
        "format": "json",
        "redirects": 1
    }
    headers = {
        "User-Agent": "theProjectCompanyArtistManagement/1.0 (contact@example.com)"
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        if "parse" in data and "wikitext" in data["parse"]:
            return data["parse"]["wikitext"]["*"]
    except Exception as e:
        logger.error(f"Error fetching wikitext: {e}")
    return None

def _extract_artist_details(page, artist_name, used_wiki_instance) -> dict:
    """
    Extracts artist details using both wikipediaapi (for summary) and raw wikitext (for infobox).
    """
    search_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    artist_info = {
        'name': artist_name,
        'eng_name': None,
        'birth_date': None,
        'height_cm': None,
        'debut_date': None,
        'debut_title': None,
        'genre': None,
        'current_agency_name': None,
        'nationality': None,
        'is_korean': False,
        'gender': 'NA',
        'recent_activity_name': None,
        'recent_activity_category': None,
        'wiki_summary': page.summary,
        'sources': [{
            'title': f"{page.title} (Wikipedia)", 
            'uri': page.fullurl,
            'source': 'wikipedia.org',
            'search_date': search_date,
            'thumbnail': 'https://www.google.com/s2/favicons?domain=wikipedia.org&sz=64'
        }]
    }
    
    lang = used_wiki_instance.language
    wikitext = get_raw_wikitext(page.title, lang)

    # Extract some external links as additional sources if available
    ext_links = re.findall(r'\[(https?://[^\s\]]+)\s+([^\]]+)\]', wikitext or "")
    for link_uri, link_title in ext_links[:5]: # Take top 5
        domain = link_uri.split('//')[-1].split('/')[0].replace('www.', '')
        artist_info['sources'].append({
            'title': link_title, 
            'uri': link_uri,
            'source': domain,
            'search_date': search_date,
            'thumbnail': f"https://www.google.com/s2/favicons?domain={domain}&sz=64"
        })
    
    if not wikitext:
        logger.warning(f"Could not retrieve wikitext for {page.title}")
        return artist_info

    def clean_val(val):
        if not val: return None
        # Remove [[links]]
        val = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]', r'\1', val)
        # Remove {{templates}}
        val = re.sub(r'\{\{[^}]+\}\}', '', val)
        # Remove <ref> tags
        val = re.sub(r'<ref[^>]*>.*?</ref>', '', val, flags=re.DOTALL)
        val = re.sub(r'<[^>]+>', '', val)
        return val.strip()

    # 1. English Name
    eng_match = re.search(r'\|\s*(?:영어 이름|English name|영어)\s*=\s*(.*?)\n', wikitext, re.IGNORECASE)
    if eng_match:
        artist_info['eng_name'] = clean_val(eng_match.group(1))
    
    if not artist_info['eng_name']:
        match = re.search(r'\(([a-zA-Z\s,]+)\)', artist_info['wiki_summary'])
        if match:
            artist_info['eng_name'] = match.group(1).split(',')[0].strip()

    # 2. Birth Date
    birth_template = re.search(r'\{\{(?:출생일|birth date).*?\|(\d{4})\|(\d{1,2})\|(\d{1,2})', wikitext)
    if birth_template:
        artist_info['birth_date'] = f"{birth_template.group(1)}-{int(birth_template.group(2)):02d}-{int(birth_template.group(3)):02d}"
    else:
        birth_match = re.search(r'\|\s*(?:출생일|출생|birth_date)\s*=\s*(.*?)\n', wikitext)
        if birth_match:
            date_part = re.search(r'(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일', birth_match.group(1))
            if date_part:
                artist_info['birth_date'] = f"{date_part.group(1)}-{int(date_part.group(2)):02d}-{int(date_part.group(3)):02d}"

    # 3. Debut Date
    debut_match = re.search(r'\|\s*(?:데뷔|debut|활동 시작|활동 시작일)\s*=\s*(.*?)\n', wikitext, re.IGNORECASE)
    if debut_match:
        val = debut_match.group(1)
        date_part = re.search(r'(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일', val)
        if date_part:
            artist_info['debut_date'] = f"{date_part.group(1)}-{int(date_part.group(2)):02d}-{int(date_part.group(3)):02d}"
        else:
            date_part_alt = re.search(r'(\d{4})\.(\d{1,2})\.(\d{1,2})', val)
            if date_part_alt:
                artist_info['debut_date'] = f"{date_part_alt.group(1)}-{int(date_part_alt.group(2)):02d}-{int(date_part_alt.group(3)):02d}"
            else:
                year_part = re.search(r'(\d{4})년', val)
                if year_part:
                    artist_info['debut_date'] = f"{year_part.group(1)}-01-01"

    # 4. Height
    height_match = re.search(r'\|\s*(?:신체|키|height|size)\s*=\s*(.*?)\n', wikitext, re.IGNORECASE)
    if height_match:
        h_val = re.search(r'(\d{3}(?:\.\d+)?)', height_match.group(1))
        if h_val:
            artist_info['height_cm'] = int(float(h_val.group(1)))

    # 5. Agency
    agency_match = re.search(r'\|\s*(?:소속사|agent|label|agency)\s*=\s*(.*?)\n', wikitext, re.IGNORECASE)
    if agency_match:
        artist_info['current_agency_name'] = clean_val(agency_match.group(1))

    # 6. Genre
    genre_match = re.search(r'\|\s*(?:장르|genre|style)\s*=\s*(.*?)\n', wikitext, re.IGNORECASE)
    if genre_match:
        artist_info['genre'] = clean_val(genre_match.group(1))

    # 7. Nationality
    nat_match = re.search(r'\|\s*(?:국적|nationality|country)\s*=\s*(.*?)\n', wikitext, re.IGNORECASE)
    if nat_match:
        nat = clean_val(nat_match.group(1))
        artist_info['nationality'] = nat
        artist_info['is_korean'] = ('대한민국' in nat or '한국' in nat)
    else:
        if lang == 'ko':
            artist_info['is_korean'] = True
            artist_info['nationality'] = '대한민국'

    # 8. Gender
    cats = "".join(page.categories.keys())
    if '여자' in cats or '여성' in cats or 'Female' in cats:
        artist_info['gender'] = 'WOMAN'
    elif '남자' in cats or '남성' in cats or 'Male' in cats:
        artist_info['gender'] = 'MEN'

    # 9. Recent Activity
    activity_match = re.search(r'\|\s*(?:최근 활동|주요 작품|최근작|활동|recent activity)\s*=\s*(.*?)\n', wikitext, re.IGNORECASE)
    if activity_match:
        artist_info['recent_activity_name'] = clean_val(activity_match.group(1))
    
    if not artist_info['recent_activity_name']:
        # Try to find recent works from categories or summary
        if '배우' in cats or '영화' in cats or 'Actor' in cats:
            artist_info['recent_activity_category'] = '드라마/영화'
        elif '가수' in cats or 'Singer' in cats or 'Idol' in cats:
            artist_info['recent_activity_category'] = '음악'

    return artist_info

    return artist_info

def _is_disambiguation(page) -> bool:
    """
    Helper function to check if a page is a disambiguation page.
    Wikipedia-API v0.8.1 removed is_disambiguation attribute.
    """
    disambig_categories = [
        '분류:모든 동음이의어 문서', 
        '분류:동음이의어 문서',
        'Category:All disambiguation pages',
        'Category:Disambiguation pages'
    ]
    return any(cat in page.categories for cat in disambig_categories)

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
        user_agent='theProjectCompany-Artist-Management-Framework/1.0 (contact@example.com)' # Added user_agent
    )

    page_py = wiki_wiki_ko.page(artist_name)
    used_wiki_instance = wiki_wiki_ko # Keep track of which Wikipedia instance was used

    if not page_py.exists():
        # Try searching in English Wikipedia if not found in Korean
        wiki_wiki_en = wikipediaapi.Wikipedia(
            language='en', 
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent='theProjectCompany-Artist-Management-Framework/1.0 (contact@example.com)' # Added user_agent
        )
        page_py = wiki_wiki_en.page(artist_name)
        used_wiki_instance = wiki_wiki_en # Update to English instance if found there
        if not page_py.exists():
            return {} # Artist not found in both languages

    # --- Disambiguation handling ---
    if _is_disambiguation(page_py):
        logger.info(f"Disambiguation page found for {artist_name}. Analyzing links...")
        
        candidates = []
        for title in page_py.links.keys():
            candidate_page = used_wiki_instance.page(title)
            if candidate_page.exists() and not _is_disambiguation(candidate_page):
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