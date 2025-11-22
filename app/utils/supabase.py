from supabase import create_client, Client
from app.utils.config import config
from app.utils.logger import logger

class SupabaseService:
    def __init__(self):
        self.client: Client = None
        if config.supabase.url and config.supabase.key:
            try:
                self.client = create_client(config.supabase.url, config.supabase.key)
                logger.info("Supabase client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase: {e}")
        else:
            logger.warning("Supabase credentials not found. Skipping initialization.")

    def insert_event(self, event_type: str, payload: dict):
        if not self.client:
            return
        
        try:
            data = {
                "app_name": config.name,
                "env": config.env,
                "event_type": event_type,
                "payload": payload
            }
            self.client.table("app_events").insert(data).execute()
        except Exception as e:
            logger.error(f"Failed to insert event to Supabase: {e}")

supabase = SupabaseService()
