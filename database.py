from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Database setup
Base = declarative_base()
engine = create_engine('sqlite:///news.db')
Session = sessionmaker(bind=engine)

# Define Article and Category classes
class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    publication_date = Column(DateTime)
    source_url = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)

# Create all tables
print("Creating database and tables...")
Base.metadata.create_all(engine)
print("Database and tables created successfully!")

# Create a new session
session = Session()

# Example data
categories = ['politics', 'business', 'sports']
articles = [
    {
        'title': 'Example Article',
        'content': 'This is an example article.',
        'publication_date': datetime(2022, 1, 1, 12, 0, 0),
        'source_url': 'https://example.com',
        'category_id': None  # to be assigned later
    }
]

# Insert categories
print("Inserting categories into the database...")
for category in categories:
    category_obj = Category(name=category)
    session.add(category_obj)
session.commit()  # Commit the categories
print("Categories inserted successfully!")

# Insert articles
print("Inserting articles into the database...")
for article in articles:
    # Assign category ID (example, assigning the first category)
    article['category_id'] = session.query(Category).filter_by(name='politics').first().id
    article_obj = Article(**article)
    session.add(article_obj)
session.commit()  # Commit the articles
print("Articles inserted successfully!")

# Close the session
session.close()
print("Database operations completed successfully!")
