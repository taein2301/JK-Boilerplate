from app.utils.batch import BatchJob
from app.utils.logger import logger

class DataProcessorBatch(BatchJob):
    def run(self):
        super().run()
        
        logger.info("data-processor Batch is running!")
        # Add your batch logic here
        
    def _process_item(self, item):
        # Implement item processing logic if needed
        pass

