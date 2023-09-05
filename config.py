import os

import dj_database_url
import dotenv

dotenv.load_dotenv()

DATABASES = {
    "default": dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
    )
}

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

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
