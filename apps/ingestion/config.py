import os
from pathlib import Path
from dotenv import load_dotenv

_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(_root / ".env.local")

SUPABASE_URL: str = os.environ.get("NEXT_PUBLIC_SUPABASE_URL", os.environ.get("SUPABASE_URL", ""))
SUPABASE_KEY: str = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
COC_API_TOKEN: str = os.environ["COC_API_TOKEN"]
COC_BASE_URL: str = "https://api.clashofclans.com/v1"

if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL / NEXT_PUBLIC_SUPABASE_URL is not set")
