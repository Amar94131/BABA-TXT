# SHIVAM
# Add your details here and then deploy by clicking on HEROKU Deploy button
import os

API_ID    = os.environ.get("API_ID", "26513107")
API_HASH  = os.environ.get("API_HASH", "f14ce4b58dc8812cfc9665588472f2d4")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7601649831:AAEMQ9chNVKZe2hm4wEHN4nmgBd8vqeOvKI") 

#WEBHOOK = True  # Don't change this
PORT = int(os.environ.get("PORT", 5000))  # Default to 8000 if not set

