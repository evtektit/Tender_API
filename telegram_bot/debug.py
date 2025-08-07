print("🟡 debug.py: стартует")

import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
print(f"BOT_TOKEN = {BOT_TOKEN}")
