
# backend/config.py

import os # Yeh line add karein

# Apni Google Gemini API key yahaan daalein
GEMINI_API_KEY = "AIzaSyAWVaV-lKMvhhZgr7EBOK_eLnwzWQgzJtk"

# Generated apps ke liye base directory
# Yeh 'backend' folder ke parallel 'generated_apps' folder ko point karega
GENERATED_APPS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "generated_apps")

# Google Generative AI model ka naam jo hum use karenge
# ...
GEMINI_MODEL_NAME = "gemini-1.5-flash-latest" # Is line ko update karein