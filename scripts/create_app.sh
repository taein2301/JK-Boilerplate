#!/bin/bash

# Check if app name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <app_name>"
    echo "Example: $0 upbit"
    exit 1
fi

APP_NAME=$1

wait_for_user() {
    echo ""
    read -p "Press Enter to continue..."
    echo ""
}

# Convert kebab-case to snake_case for file name and CamelCase for class name
# e.g., test-app -> test_app.py, TestAppApp
MODULE_NAME=$(echo "$APP_NAME" | tr '-' '_')
CLASS_NAME=$(python3 -c "print(''.join(word.capitalize() for word in '$APP_NAME'.split('-')) + 'App')")

mkdir -p app/core/
FILE_PATH="app/core/${MODULE_NAME}.py"

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

# Setup .env file
wait_for_user
echo ""
echo "--------------------------------"
echo "Setting up .env file..."

if [ ! -f ".env" ]; then
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "✅ Created .env from env.example"
    else
        echo "⚠️  env.example not found. Skipping .env creation."
    fi
else
    echo "✅ .env already exists. Skipping."
fi
echo "--------------------------------"



# Git Remote Setup
wait_for_user
echo ""
echo "--------------------------------"
echo "Checking Git Configuration..."

if git remote | grep -q "^upstream$"; then
    echo "✅ 'upstream' remote already exists. Skipping git setup."
else
    if git remote | grep -q "^origin$"; then
        echo "🔄 Renaming 'origin' to 'upstream'..."
        git remote rename origin upstream

        NEW_ORIGIN="https://github.com/taein2301/${APP_NAME}.git"
        echo "➕ Adding new 'origin' remote: $NEW_ORIGIN"
        git remote add origin "$NEW_ORIGIN"

        # Create private GitHub repository if it does not exist
        REPO_NAME=$(basename "$NEW_ORIGIN" .git)
        if ! gh repo view "$REPO_NAME" > /dev/null 2>&1; then
            echo "🛠️ Creating private GitHub repository $REPO_NAME"
            gh repo create "$REPO_NAME" --private --confirm
        fi
    fi
fi
echo "--------------------------------"

# Git commit and push
wait_for_user
echo ""
echo "--------------------------------"
echo "Committing changes..."

git add .
git commit -m "feat: Add ${APP_NAME} app

🤖 Generated with create_app.sh script"

if git remote | grep -q "^origin$"; then
    echo "📤 Pushing to origin..."
    git push origin main
    echo "✅ Pushed to origin/main"
else
    echo "⚠️  No 'origin' remote found. Skipping push."
fi
echo "--------------------------------"

echo ""
echo "✅ Setup complete! You can now run:"
echo "   uv run app ${APP_NAME} --env dev"
echo ""
