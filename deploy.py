from celery import Celery

# Initialize the Celery app
app = Celery('news_processor', broker='redis://localhost:6379/0')

# Auto-discover tasks from the specified module(s)
app.autodiscover_tasks(['news_processor'])  # Replace 'my_app' with the actual name of the module where your tasks are defined


