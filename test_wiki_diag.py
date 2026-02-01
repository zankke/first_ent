import wikipediaapi
import sys

def diag(artist_name):
    wiki_wiki = wikipediaapi.Wikipedia(
        language='ko',
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent='theProjectCompanyArtistManagement/1.0 (contact@example.com)'
    )
    page = wiki_wiki.page(artist_name)
    if not page.exists():
        print(f"Page {artist_name} does not exist")
        return

    print("--- TITLE ---")
    print(page.title)
    print("\n--- SUMMARY ---")
    print(page.summary[:500])
    print("\n--- TEXT START (1000 chars) ---")
    print(page.text[:2000])
    print("\n--- CATEGORIES ---")
    print(list(page.categories.keys())[:10])

if __name__ == "__main__":
    diag("아이유")

