from supabase import create_client, Client
from flask import current_app

# Supabase configuration
SUPABASE_URL = 'https://dgdvqnwmhgqgarwuxirj.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRnZHZxbndtaGdxZ2Fyd3V4aXJqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc0MjI1MzksImV4cCI6MjA2Mjk5ODUzOX0.0m17nX308i9nd9h3TgJBq35nAdNI0Ro-9Jgdm49TwrI'

try:
    # Initialize Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Error initializing Supabase client: {str(e)}")
    raise