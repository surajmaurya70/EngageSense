#!/bin/bash
# 🚀 Auto Push & Deploy Script for EngageSense

echo "🧠 EngageSense Auto Deployment Started..."

# Navigate to repo
cd ~/Downloads/EngageSense/EngageSense || exit

# Stage all changes
git add .

# Commit with timestamp
git commit -m "🚀 Auto update: $(date '+%d-%b-%Y %I:%M %p')"

# Push to main branch
git push origin main

echo ""
echo "✅ Code pushed to GitHub successfully!"

# Streamlit deployment trigger (your public app)
echo "🌐 Opening Streamlit app..."
open "https://surajmaurya70-engagesense-app-o7zhrq.streamlit.app/"

echo ""
echo "💫 Deployment complete! Check Streamlit Cloud for live updates."

