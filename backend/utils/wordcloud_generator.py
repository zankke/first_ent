import os
import base64
from io import BytesIO
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg') # Headless backend
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
from collections import Counter
import numpy as np
import re

def get_theProjectCompany_colormap():
    """Returns a custom colormap based on theProjectCompany brand colors (Orange and Navy/Slate)."""
    colors = [
        "#0f172a", # Slate 900
        "#1e293b", # Slate 800
        "#334155", # Slate 700
        "#ED7104", # Primary Orange
        "#f97316", # Orange 500
        "#fb923c"  # Orange 400
    ]
    return LinearSegmentedColormap.from_list("theProjectCompany", colors, N=256)

def generate_wordcloud_from_text(text_content: str, num_words: int = 100) -> (str, list):
    """Generates a word cloud from text string and returns base64 image + keywords."""
    if not text_content or len(text_content.strip()) < 10:
        return None, []

    # Simple cleaning: remove special chars, keep Korean and Alphanumeric
    cleaned_text = re.sub(r'[^가-힣a-zA-Z0-9\s]', '', text_content)
    
    # Filter out very short words (likely particles in Korean or noise)
    words = [w for w in cleaned_text.split() if len(w) > 1]
    if not words:
        return None, []
    
    word_freq = Counter(words)
    
    # Font path for Korean support
    font_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'fonts', 'NanumGothic-Bold.ttf')
    if not os.path.exists(font_path):
        # Fallback if specific font is missing
        font_path = None

    # Generate WordCloud
    wc = WordCloud(
        width=1200,
        height=600,
        background_color='white',
        font_path=font_path,
        colormap=get_theProjectCompany_colormap(),
        max_words=num_words,
        prefer_horizontal=0.7,
        relative_scaling=0.5,
        scale=2
    ).generate_from_frequencies(word_freq)

    # Convert to Base64
    img_buffer = BytesIO()
    # We can use wc.to_image() directly without matplotlib figure overhead for simple image
    wc.to_image().save(img_buffer, format='PNG')
    img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    base64_data = f"data:image/png;base64,{img_str}"

    meta_tags = [word for word, count in word_freq.most_common(20)]

    return base64_data, meta_tags

def generate_wordcloud_for_artist(artist_id: int, num_words: int = 100) -> (str, list):
    """Fetches news content for an artist, generates a word cloud, and returns base64 image + keywords.

    Returns:
        A tuple containing:
        - Base64 encoded string of the word cloud image (data:image/png;base64,...)
        - A list of prominent meta tags (top keywords).
    """
    from backend.models import News
    
    news_items = News.query.filter_by(artist_id=artist_id).all()
    if not news_items:
        return None, []

    text_content = " ".join([n.content for n in news_items if n.content])
    return generate_wordcloud_from_text(text_content, num_words)

if __name__ == '__main__':
    # This part is for testing the word cloud generator directly
    # You would need a running Flask app context or mock db for this
    # For example, create a dummy artist and news items for testing
    pass