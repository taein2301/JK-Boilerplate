from app.utils.config import config
from app.utils.logger import logger
from app.utils.telegram import telegram
from app.utils.supabase import supabase

class BatchJob:
    def __init__(self):
        self.batch_size = config.api_configs.get("batch.size", 50)

    def run(self):
        logger.info("🔄 Starting Sample Batch Job")
        
        start_time = logger.info(f"Batch Size: {self.batch_size}")
        supabase.insert_event("start", {"type": "batch", "batch_size": self.batch_size})
        
        try:
            # Mock processing - process items efficiently
            items = range(1, 11)
            processed_count = 0
            
            for item in items:
                self._process_item(item)
                processed_count += 1
                
            logger.info(f"✅ Batch Job Completed Successfully - Processed {processed_count} items")
            telegram.send_sync(f"✅ Sample Batch Job Completed ({processed_count} items)")
            supabase.insert_event("stop", {"type": "batch", "items_processed": processed_count})
            
        except Exception as e:
            logger.error(f"Batch Job Error: {e}", exc_info=True)
            telegram.send_sync(f"🚨 Batch Job Failed: {e}")
            supabase.insert_event("abnormal_stop", {"type": "batch", "error": str(e)})
            raise

    def _process_item(self, item):
        """Process a single item. Override this method in subclasses."""
        logger.debug(f"Processing item {item}...")
