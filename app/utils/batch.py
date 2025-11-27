from app.utils.config import config
from app.utils.logger import logger
from app.utils.telegram import telegram
from app.utils.supabase import supabase

class BatchJob:
    def __init__(self):
        pass

    def run(self):
        logger.info("🔄 Starting Batch Job")
        
        supabase.insert_event("start", {"type": "batch"})
        
        try:
            logger.info("Executing batch logic...")
            # Subclasses should implement their logic here
            
            logger.info("✅ Batch Job Completed Successfully")
            telegram.send_sync("✅ Batch Job Completed")
            supabase.insert_event("stop", {"type": "batch"})
            
        except Exception as e:
            logger.error(f"Batch Job Error: {e}", exc_info=True)
            telegram.send_sync(f"🚨 Batch Job Failed: {e}")
            supabase.insert_event("abnormal_stop", {"type": "batch", "error": str(e)})
            raise

    def _process_item(self, item):
        """Process a single item. Override this method in subclasses."""
        pass
