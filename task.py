from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

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

# Create the tables in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
session = Session()

# Example: Add a new article to the database
article = Article(
    title='Example Article',
    content='This is an example article.',
    publication_date=datetime(2022, 1, 1, 12, 0, 0),  # Use datetime object
    source_url='https://example.com'
)
session.add(article)
session.commit()

# Query the database and print the titles of all articles
articles = session.query(Article).all()
for article in articles:
    print(article.title)

# Close the session
session.close()
