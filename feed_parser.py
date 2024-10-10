import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

import feedparser
from celery import Celery
import nltk
from nltk.tokenize import word_tokenize
from nltk.classify import NaiveBayesClassifier
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

# Create a database engine
engine = create_engine('sqlite:///news_articles.db')

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a base class for declarative class definitions
Base = declarative_base()

# Define the Article class
class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    publication_date = Column(DateTime)
    source_url = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', backref='articles')

# Define the Category class
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)

# Create the database tables if they don't exist
Base.metadata.create_all(engine)

# Initialize Celery
app = Celery('my_app', broker='redis://localhost:6379/0')  # Use Redis as broker
app.conf.result_backend = 'rpc://'  # Adjust to your result backend

# Load the category classification model (you can use a pre-trained model or train your own)
nltk.download('punkt')

# Simple training data for Naive Bayes classifier
train_data = [
    ({'word': 'politics'}, 'politics'),
    ({'word': 'government'}, 'politics'),
    ({'word': 'election'}, 'politics'),
    ({'word': 'business'}, 'business'),
    ({'word': 'market'}, 'business'),
    ({'word': 'company'}, 'business'),
    ({'word': 'sports'}, 'sports'),
    ({'word': 'game'}, 'sports'),
    ({'word': 'team'}, 'sports'),
    # Add more categories and words as needed
]

# Train the Naive Bayes Classifier
category_model = NaiveBayesClassifier.train(train_data)

# Define the process_article task
@app.task
def process_article(article):
    try:
        # Tokenize the article content
        tokens = word_tokenize(article['content'])
        
        # Classify the article into a category
        category = category_model.classify(dict([(word, True) for word in tokens]))
        
        # Update the database with the assigned category
        session = Session()
        article_obj = Article(
            title=article['title'],
            content=article['content'],
            publication_date=article['publication_date'],
            source_url=article['source_url']
        )
        
        # Check if category exists
        category_obj = session.query(Category).filter_by(name=category).first()
        if category_obj is None:
            category_obj = Category(name=category)
            session.add(category_obj)
            session.commit()
        
        # Set the category_id for the article
        article_obj.category_id = category_obj.id
        session.add(article_obj)
        session.commit()
    except Exception as e:
        print(f"Error processing article: {e}")

def parse_feeds(feeds):
    articles = []
    for feed in feeds:
        parsed_feed = feedparser.parse(feed)
        for entry in parsed_feed.entries:
            article = {
                'title': entry.get('title', ''),
                'content': entry.get('summary', ''),
                'publication_date': entry.get('published', ''),
                'source_url': entry.get('link', '')
            }
            articles.append(article)
    return articles

def main():
    feeds = [
        'http://rss.cnn.com/rss/cnn_topstories.rss',
        'http://qz.com/feed',
        'http://feeds.foxnews.com/foxnews/politics',
        'http://feeds.reuters.com/reuters/businessNews',
        'http://feeds.feedburner.com/NewshourWorld',
        'https://feeds.bbci.co.uk/news/world/asia/india/rss.xml'
    ]
    articles = parse_feeds(feeds)
    for article in articles:
        process_article.delay(article)

if __name__ == '__main__':
    main()
