import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from backend.app import db
from backend.models import News

def generate_wordcloud_for_artist(artist_id: int, num_words: int = 50, output_dir: str = './temp') -> (str, list):
    """Fetches news content for an artist, generates a word cloud image, and extracts meta tags.

    Args:
        artist_id: The ID of the artist.
        num_words: The maximum number of words to include in the word cloud and meta tags.
        output_dir: Directory to save the word cloud image.

    Returns:
        A tuple containing:
        - The absolute path to the generated word cloud image.
        - A list of prominent meta tags (top keywords).
    """
    news_content = ""
    news_items = News.query.filter_by(artist_id=artist_id).all()

    if not news_items:
        return None, []

    for news in news_items:
        if news.content:
            news_content += news.content + " "

    if not news_content:
        return None, []

    # Basic text cleaning (can be expanded with more sophisticated NLP if needed)
    cleaned_text = ' '.join(word.lower() for word in news_content.split() if word.isalnum())

    # Generate word cloud
    font_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'fonts', 'NanumGothic-Regular.ttf')
    wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=font_path).generate(cleaned_text)
    
    # Save word cloud image
    os.makedirs(output_dir, exist_ok=True)
    image_filename = f"wordcloud_{artist_id}.png"
    image_path = os.path.join(output_dir, image_filename)
    wordcloud.to_file(image_path)

    # Extract meta tags (top keywords)
    words = cleaned_text.split()
    word_counts = Counter(words)
    meta_tags = [word for word, count in word_counts.most_common(num_words)]

    return os.path.abspath(image_path), meta_tags

if __name__ == '__main__':
    # This part is for testing the word cloud generator directly
    # You would need a running Flask app context or mock db for this
    # For example, create a dummy artist and news items for testing
    pass