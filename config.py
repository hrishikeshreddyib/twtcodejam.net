import dotenv
import os
import urllib.parse as urlparse

dotenv.load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")

url = urlparse.urlparse(os.environ["DATABASE_URL"])  # os.environ['DATABASE_URL']
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",  # your database
        "NAME": str(dbname),
        "USER": user,
        "PASSWORD": password,
        "HOST": host,
        "PORT": port,
    }
}

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(", ")

# Discord stuff
TOKEN: str = os.environ.get("TOKEN")  # > https://discord.com/developers/applications
LOG_WEBHOOK = os.environ.get(
    "LOG_WEBHOOK"
)  # create webhook in the server for a channel and paste here
CODEJAM_WEBHOOK = os.environ.get(
    "CODEJAM_WEBHOOK"
)  # to receive codejam notifications set this up for a channel in
# your discord server and
# paste the link
CODEJAM_INFO_CHANNEL_WEBHOOK = os.environ.get("CODEJAM_INFO_CHANNEL_WEBHOOK")
