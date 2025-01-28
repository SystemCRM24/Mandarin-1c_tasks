from dotenv import load_dotenv
import os

load_dotenv()

BITRIX_WEBHOOK = os.environ.get("BITRIX_WEBHOOK")
