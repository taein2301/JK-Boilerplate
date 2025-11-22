import time
from app.utils.config import config
from app.utils.logger import logger
from app.utils.telegram import telegram
from app.utils.supabase import supabase

class BatchJob:
    def __init__(self):
        self.batch_size = config.api_configs.get("batch.size", 50)

    def run(self):
        logger.info("🔄 Starting Sample Batch Job")
        
        supabase.insert_event("start", {"type": "batch"})
        
        try:
            logger.info(f"Batch Size: {self.batch_size}")
            
            # Mock processing
            items = range(1, 11)
            for item in items:
                self._process_item(item)
                
            logger.info("✅ Batch Job Completed Successfully")
            telegram.send_sync("✅ Sample Batch Job Completed")
            
        except Exception as e:
            logger.error(f"Batch Job Error: {e}")
            telegram.send_sync(f"🚨 Batch Job Failed: {e}")
            supabase.insert_event("abnormal_stop", {"error": str(e)})
            raise
        finally:
            supabase.insert_event("stop", {"type": "batch"})

    def _process_item(self, item):
        logger.debug(f"Processing item {item}...")
        time.sleep(0.1)
