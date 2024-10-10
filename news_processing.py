# news_processing.py
import feedparser
from datetime import datetime
from database import Article, session

# List of RSS feeds
feeds = [
    'http://rss.cnn.com/rss/cnn_topstories.rss',
    'http://qz.com/feed',
    'http://feeds.foxnews.com/foxnews/politics',
    'http://feeds.reuters.com/reuters/businessNews',
    'http://feeds.feedburner.com/NewshourWorld',
    'https://feeds.bbci.co.uk/news/world/asia/india/rss.xml'
]

def fetch_and_store_articles():
    for feed in feeds:
        # Parse the feed
        feed_data = feedparser.parse(feed)
        
        # Loop through the entries in the feed
        for entry in feed_data.entries:
            # Use 'summary' if it exists, otherwise fall back to 'content' or set as empty
            content = getattr(entry, 'summary', '') or (entry.content[0].value if hasattr(entry, 'content') and entry.content else '')

            # Get the publication date safely
            if hasattr(entry, 'published_parsed'):
                publication_date = datetime(*entry.published_parsed[:6])  # Convert to datetime
            else:
                publication_date = None  # Set to None or handle as needed

            # Create a new Article instance
            article = Article(
                title=entry.title,
                content=content,
                publication_date=publication_date,  # Handle as None if not available
                source_url=entry.link
            )
            # Add the article to the session
            session.add(article)

    # Commit the session to save the articles to the database
    session.commit()

if __name__ == '__main__':
    fetch_and_store_articles()
    print("Articles fetched and stored successfully!")
