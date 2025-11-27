#!/bin/bash

# Check if batch name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <batch_name>"
    echo "Example: $0 my-batch"
    exit 1
fi

BATCH_NAME=$1
# Convert kebab-case or snake_case to CamelCase for class name
# e.g., my-batch -> MyBatchBatch
CLASS_NAME="$(tr '[:lower:]' '[:upper:]' <<< ${BATCH_NAME:0:1})${BATCH_NAME:1}Batch"
# Simple conversion logic, might need adjustment for complex names but good for now
FILE_PATH="app/core/${BATCH_NAME}.py"

# Check if file already exists
if [ -f "$FILE_PATH" ]; then
    echo "Error: File $FILE_PATH already exists."
    exit 1
fi

# Create the file with boilerplate code
cat <<EOF > "$FILE_PATH"
from app.utils.batch import BatchJob
from app.utils.logger import logger

class ${CLASS_NAME}(BatchJob):
    def run(self):
        super().run()
        
        logger.info("${BATCH_NAME} Batch is running!")
        # Add your batch logic here
        
    def _process_item(self, item):
        # Implement item processing logic if needed
        pass

EOF

echo "✅ Created $FILE_PATH"
echo ""
echo "Next steps:"
echo "1. Open app/main.py"
echo "2. Add the following code to the run_batch function:"
echo ""
echo "    if batch_name == \"${BATCH_NAME}\":"
echo "        from app.core.${BATCH_NAME} import ${CLASS_NAME}"
echo "        ${CLASS_NAME}().run()"
echo ""
