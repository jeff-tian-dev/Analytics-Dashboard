from supabase import create_client, Client
from .config import SUPABASE_URL, SUPABASE_KEY


def get_db() -> Client:
    """Create a fresh Supabase client per call to avoid stale HTTP/2 connections."""
    return create_client(SUPABASE_URL, SUPABASE_KEY)
