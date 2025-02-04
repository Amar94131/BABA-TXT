# SHIVAM
# Add your details here and then deploy by clicking on HEROKU Deploy button
import os

API_ID    = os.environ.get("API_ID", "26513107")
API_HASH  = os.environ.get("API_HASH", "f14ce4b58dc8812cfc9665588472f2d4")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7601649831:AAEMQ9chNVKZe2hm4wEHN4nmgBd8vqeOvKI") 

FORCE_SUB_CHANNEL_1 = int(os.environ.get("FORCE_SUB_CHANNEL_1", "-1002330754414"))
FORCE_SUB_CHANNEL_2 = int(os.environ.get("FORCE_SUB_CHANNEL_2", "-1002377421372"))
FORCE_SUB_CHANNEL_3 = int(os.environ.get("FORCE_SUB_CHANNEL_3", "-1002156040011"))
FORCE_SUB_CHANNEL_4 = int(os.environ.get("FORCE_SUB_CHANNEL_4", "-1002264356410"))
FORCE_PIC = os.environ.get("FORCE_PIC", "https://envs.sh/pNw.jpg")
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "Hello {first}\n\n<b>You need to join in my Channel/Group to use me\n\nKindly Please join Channel</b>")

#AUTH_CHANNELS = os.environ.get("AUTH_CHANNEL", "-1002156040011, -1002377421372")  # ✅ os.environ का सही उपयोग करें
#AUTH_CHANNELS = [int(channel_id) for channel_id in AUTH_CHANNELS.split(",")]

#WEBHOOK = True  # Don't change this
#PORT = int(os.environ.get("PORT", 8080))  # Default to 8000 if not set





#AUTH_CHANNELS = environ.get("AUTH_CHANNEL", "-1002330754414")
#AUTH_CHANNELS = [int(channel_id) for channel_id in AUTH_CHANNELS.split(",")]
#WEBHOOK = True  # Don't change this
#PORT = int(os.environ.get("PORT", 8080))  # Default to 8000 if not set

