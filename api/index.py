import sys
import os

# Add root folder to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Export app for Vercel
app = app
