# backend/utils/gemini_utils.py

import os
import json
import logging
from datetime import datetime
import google.generativeai as genai

logger = logging.getLogger(__name__)

ARTIST_SCHEMA_DEF = """
CREATE TABLE Artists (
id bigint NOT NULL AUTO_INCREMENT,
name varchar(100) NOT NULL,
eng_name varchar(100) DEFAULT NULL,
birth_date date DEFAULT NULL,
height_cm int DEFAULT NULL,
debut_date date DEFAULT NULL,
debut_title varchar(200) DEFAULT NULL,
recent_activity_category varchar(100) DEFAULT NULL,
recent_activity_name varchar(200) DEFAULT NULL,
genre varchar(100) DEFAULT NULL,
agency_id bigint DEFAULT NULL,
current_agency_name varchar(100) DEFAULT NULL,
nationality varchar(100) DEFAULT NULL,
is_korean tinyint(1) DEFAULT '1',
gender enum('WOMAN','MEN','NA','EXTRA','FOREIGN') DEFAULT NULL,
status enum('ACTIVE','INACTIVE','PAUSED','RETIRED','UNKNOWN') DEFAULT 'ACTIVE',
category_id bigint DEFAULT NULL,
platform varchar(50) DEFAULT NULL,
social_media_url varchar(255) DEFAULT NULL,
profile_photo varchar(255) DEFAULT NULL,
guarantee_krw bigint DEFAULT NULL,
wiki_summary text COMMENT 'Wikipedia Summary',
PRIMARY KEY (id)
);
"""

def search_artist_ai(artist_name: str, is_update: bool = False):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY not found in environment")
        return None

    genai.configure(api_key=api_key)
    
    # Define the response schema to force strict JSON structure
    response_schema = {
        "type": "object",
        "properties": {
            "searchStatus": {"type": "string", "enum": ["SUCCESS", "AMBIGUOUS", "NOT_FOUND"]},
            "statusMessage": {"type": "string"},
            "profile": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "eng_name": {"type": "string"},
                    "birth_date": {"type": "string"}, # YYYY-MM-DD
                    "height_cm": {"type": "integer"},
                    "debut_date": {"type": "string"}, # YYYY-MM-DD
                    "debut_title": {"type": "string"},
                    "recent_activity_category": {"type": "string"},
                    "recent_activity_name": {"type": "string"},
                    "genre": {"type": "string"},
                    "current_agency_name": {"type": "string"},
                    "nationality": {"type": "string"},
                    "is_korean": {"type": "boolean"},
                    "gender": {"type": "string", "enum": ["WOMAN", "MEN", "NA"]},
                    "status": {"type": "string"},
                    "social_media_url": {"type": "string"},
                    "profile_photo": {"type": "string"},
                    "wiki_summary": {"type": "string"}
                },
                "required": ["name", "debut_date", "height_cm", "recent_activity_name"]
            },
            "sqlQuery": {"type": "string"},
            "pythonScript": {"type": "string"}
        },
        "required": ["searchStatus", "profile", "sqlQuery"]
    }

    system_prompt = f"""You are a high-speed Data Assistant specialized in Korean Entertainment.
    Target: "{artist_name}". 
    
    INSTRUCTIONS:
    1. Deep Search: Use Google Search, Naver Search, & Wikipedia. 
    2. Data Accuracy: You MUST find the following for "{artist_name}":
       - Exact Debut Date: Look for "데뷔" or "데뷔일" (e.g. IU debuted 2008-09-18).
       - Height: Look for "신체" or "키" (e.g. IU is 162cm).
       - Recent Project: Find their latest drama, movie, or music album (e.g. "The Winning", "Broker").
    3. Mapping: Map info to the SQL schema: {ARTIST_SCHEMA_DEF}.
    4. Code Generation: Generate a SQL {'UPDATE' if is_update else 'INSERT'} query and a automation Python script.
    5. Prioritize Google(SERP) > Wikipedia > Naver > SCRIBD.
    6. Return valid JSON only."""

    try:
        # Using gemini-2.0-flash for speed and reliability
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            tools=[{"google_search": {}}],
            system_instruction=system_prompt
        )

        response = model.generate_content(
            f"Thoroughly search for Korean artist: {artist_name}. Find debut date, height, and recent works specifically.",
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
                response_schema=response_schema
            )
        )
        
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            # Fallback for unexpected formatting
            text = response.text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            data = json.loads(text)
        
        if data.get('searchStatus') != 'SUCCESS' and not data.get('profile'):
            logger.warning(f"AI Search status for {artist_name}: {data.get('searchStatus')} - {data.get('statusMessage')}")
            return None

        sources = []
        search_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if response.candidates and response.candidates[0].grounding_metadata:
            gm = response.candidates[0].grounding_metadata
            
            # Extract from grounding_chunks
            if gm.grounding_chunks:
                for chunk in gm.grounding_chunks:
                    if chunk.web:
                        uri = chunk.web.uri
                        domain = uri.split('//')[-1].split('/')[0].replace('www.', '')
                        sources.append({
                            'title': chunk.web.title, 
                            'uri': uri,
                            'source': domain,
                            'search_date': search_date,
                            'thumbnail': f"https://www.google.com/s2/favicons?domain={domain}&sz=64"
                        })
        
        # Define source priority mapping
        priority_map = {
            'google.com': 1,
            'wikipedia.org': 2,
            'naver.com': 3,
            'scribd.com': 4
        }

        def get_priority(source_item):
            src = source_item['source'].lower()
            for key, val in priority_map.items():
                if key in src:
                    return val
            return 99

        # Deduplicate and sort
        unique_sources = []
        seen_uris = set()
        for s in sources:
            if s['uri'] not in seen_uris:
                unique_sources.append(s)
                seen_uris.add(s['uri'])
        
        unique_sources.sort(key=lambda x: (get_priority(x), x['title']))
        
        return {
            'profile': data.get('profile'),
            'sql_query': data.get('sqlQuery'),
            'python_script': data.get('pythonScript'),
            'sources': unique_sources
        }

    except Exception as e:
        logger.error(f"Error in Gemini search for {artist_name}: {e}", exc_info=True)
        return None
