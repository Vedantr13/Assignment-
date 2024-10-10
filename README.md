THIS PROJECT IS AN ASSIGNMENT SUBMITTED BY VEDANT RANSING FOR INTERN ROLE IN TEN TIMES ONLINE PT.LTD

News Articles Processing Project
This project demonstrates how to parse news articles from RSS feeds, process them using Python, store them in a database, and retrieve them for further analysis. The project uses SQLAlchemy for ORM (Object Relational Mapping) and SQLite as the database.

Table of Contents
Project Overview
Features
Tech Stack
Installation
How to Use
Project Structure
Contributing
License
Project Overview
The project is designed to fetch news articles from several RSS feeds, parse the content, and store the articles into a database for future reference and processing. It includes functionality for error handling when parsing data, particularly in cases where RSS fields might be missing or formatted incorrectly.

Features
Fetch articles from RSS feeds: Parse and store articles with attributes like title, content, publication date, and source URL.
Store articles and categories in a SQLite database: Organized data model using SQLAlchemy.
Error handling for missing or malformed RSS data.
Celery is used for asynchronous task execution (such as fetching RSS feeds).
Dummy data generator: Populate the database with dummy articles and categories for testing purposes.
Tech Stack
Python: Core programming language.
SQLAlchemy: ORM for database management.
SQLite: Lightweight database for article storage.
Celery: Distributed task queue for managing asynchronous jobs.
feedparser: Library for parsing RSS feeds.
