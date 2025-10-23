#!/bin/bash

# Exit on any error
set -e

# Log file for debugging
exec 1> >(logger -s -t $(basename $0)) 2>&1

echo "Starting deployment at $(date)"

# Function to check if command succeeded
check_status() {
    if [ $? -eq 0 ]; then
        echo "✓ $1 successful"
    else
        echo "✗ $1 failed"
        exit 1
    fi
}

# Navigate to project directory
cd /home/joseph/project-q
check_status "Changed to project directory"

# Store current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Currently on branch: $BRANCH"

# Fetch all remotes
echo "Fetching updates..."
git fetch --all
check_status "Git fetch"

# Check if we're behind the remote
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})
BASE=$(git merge-base @ @{u})

if [ $LOCAL = $REMOTE ]; then
    echo "Up-to-date, no deployment needed"
    exit 0
elif [ $LOCAL = $BASE ]; then
    echo "Behind remote, updating..."
    # Pull latest changes
    git pull
    check_status "Git pull"
else
    echo "Local changes exist. Please commit or stash them first."
    exit 1
fi

# Activate virtual environment and update dependencies
echo "Activating virtual environment..."
source venv/bin/activate
check_status "Virtual environment activation"

echo "Installing/updating dependencies..."
pip install -r requirements.txt
check_status "Dependencies installation"

# Navigate to Django project directory
cd webapp
check_status "Changed to webapp directory"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput
check_status "Static files collection"

# Run migrations
echo "Running database migrations..."
python manage.py migrate
check_status "Database migrations"

# Restart the service
echo "Restarting Gunicorn service..."
sudo systemctl restart project-q
check_status "Service restart"

echo "✨ Deployment completed successfully at $(date)!"
