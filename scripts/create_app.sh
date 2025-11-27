#!/bin/bash

# Check if app name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <app_name>"
    echo "Example: $0 upbit"
    exit 1
fi

APP_NAME=$1
CLASS_NAME="$(tr '[:lower:]' '[:upper:]' <<< ${APP_NAME:0:1})${APP_NAME:1}App"
mkdir -p app/core/
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

# Setup .env file
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

# Update main.py automatically
echo ""
echo "--------------------------------"
echo "Updating app/main.py..."

MAIN_PY="app/main.py"
NEW_CODE="    if app_name == \"${APP_NAME}\":
        from app.core.${APP_NAME} import ${CLASS_NAME}

        ${CLASS_NAME}().run()
    el"

# Find the line with 'else:' in run_app function and insert before it
if grep -q "def run_app" "$MAIN_PY"; then
    # Use awk to insert before else in run_app function
    awk -v code="$NEW_CODE" '
    /^def run_app/ { in_func=1 }
    /^def / && !/^def run_app/ && in_func { in_func=0 }
    in_func && /^    else:/ && !done {
        print code "se:"
        done=1
        next
    }
    { print }
    ' "$MAIN_PY" > "${MAIN_PY}.tmp" && mv "${MAIN_PY}.tmp" "$MAIN_PY"
    echo "✅ Updated $MAIN_PY with new app routing"
else
    echo "⚠️  Could not auto-update $MAIN_PY. Please add manually:"
    echo ""
    echo "    if app_name == \"${APP_NAME}\":"
    echo "        from app.core.${APP_NAME} import ${CLASS_NAME}"
    echo "        ${CLASS_NAME}().run()"
    echo ""
fi
echo "--------------------------------"

# Git Remote Setup
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
