#!/bin/bash

# Check if app name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <app_name>"
    echo "Example: $0 upbit"
    exit 1
fi

APP_NAME=$1
CLASS_NAME="$(tr '[:lower:]' '[:upper:]' <<< ${APP_NAME:0:1})${APP_NAME:1}App"
FILE_PATH="app/core/${APP_NAME}.py"

# Check if file already exists
if [ -f "$FILE_PATH" ]; then
    echo "Error: File $FILE_PATH already exists."
    exit 1
fi

# Create the file with boilerplate code
cat <<EOF > "$FILE_PATH"
from app.utils.app import App
from app.utils.logger import logger

class ${CLASS_NAME}(App):
    def run(self):
        super().run()
        
        logger.info("${APP_NAME} App is running!")
        # Add your business logic here
        
EOF

echo "✅ Created $FILE_PATH"
echo ""
echo "Next steps:"
echo "1. Open app/main.py"
echo "2. Add the following code to the run_app function:"
echo ""
echo "    if app_name == \"${APP_NAME}\":"
echo "        from app.core.${APP_NAME} import ${CLASS_NAME}"
echo "        ${CLASS_NAME}().run()"
echo ""
