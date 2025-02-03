# SHIVAM
# Add your details here and then deploy by clicking on HEROKU Deploy button
import os

API_ID    = os.environ.get("API_ID", "26513107")
API_HASH  = os.environ.get("API_HASH", "f14ce4b58dc8812cfc9665588472f2d4")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7601649831:AAEMQ9chNVKZe2hm4wEHN4nmgBd8vqeOvKI") 

AUTH_CHANNELS = os.environ.get("AUTH_CHANNEL", "-1002330754414")  # ✅ os.environ का सही उपयोग करें
AUTH_CHANNELS = [int(channel_id) for channel_id in AUTH_CHANNELS.split(",")]

#WEBHOOK = True  # Don't change this
#PORT = int(os.environ.get("PORT", 8080))  # Default to 8000 if not set





#AUTH_CHANNELS = environ.get("AUTH_CHANNEL", "-1002330754414")
#AUTH_CHANNELS = [int(channel_id) for channel_id in AUTH_CHANNELS.split(",")]
#WEBHOOK = True  # Don't change this
#PORT = int(os.environ.get("PORT", 8080))  # Default to 8000 if not set

