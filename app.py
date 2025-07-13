# app.py
# Luminal Q ka apna backend API.
# Yeh user prompts ko receive karega aur AI integration ko handle karega.
# app.py
# Luminal Q ka apna backend API.
# Current directory ko Python path mein add karein
# Taki relative imports kaam kar saken jab app.py ko directly run kiya jaye
# sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import subprocess # Generated apps ko run karne ke liye (abhi ke liye dummy use)

# Utils modules ko import karein
# ... other imports ...

# Utils modules ko import karein (Absolute Imports)
# Hum current directory ko Python path mein add karenge taaki 'utils' package mil sake
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.llm_handler import generate_code_from_prompt
from utils.file_manager import save_generated_app
from config import GENERATED_APPS_DIR # GENERATED_APPS_DIR ko config se import karein
app = Flask(__name__)
CORS(app)

# Root endpoint (sirf test karne ke liye)
@app.route('/')
def home():
    return jsonify({"message": "Luminal Q Backend API chal raha hai! Ready for prompts."})

# Prompt receive karne aur app generate karne ke liye endpoint
@app.route('/generate-app', methods=['POST'])
def generate_app():
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({"error": "Prompt missing in request"}), 400

    user_prompt = data['prompt']
    # User se app type bhi le sakte hain, abhi ke liye default HTML/CSS/JS rakhte hain
    app_type = data.get('app_type', 'HTML/CSS/JS') # Frontend se app_type bhi aa sakta hai
    app_name = "generated_app_" + str(abs(hash(user_prompt)))[:8] # Prompt se unique naam banayein

    print(f"Received prompt from frontend: {user_prompt}")
    print(f"Attempting to generate {app_type} app with name: {app_name}")

    generated_app_path = ""
    generated_app_url = ""
    status_message = ""

    try:
        # Step 1: LLM se code generate karein
        # generate_code_from_prompt function ab LLM ko call karegi
        generated_code_content = generate_code_from_prompt(user_prompt, app_type)

        if generated_code_content.startswith("Error:"):
            raise Exception(generated_code_content)

        # Step 2: Generated code ko files mein save karein
        # save_generated_app function files ko generated_apps folder mein save karegi
        app_full_path = save_generated_app(app_name, generated_code_content, app_type)

        generated_app_path = app_full_path
        # Abhi ke liye, hum user ko local file path denge.
        # Future mein, hum in apps ko serve karenge ya deploy karenge.
        if app_type == "HTML/CSS/JS":
            generated_app_url = f"file:///{os.path.join(generated_app_path, 'index.html').replace(os.sep, '/')}"
        elif app_type == "Python/Flask":
            # Flask app ke liye, hum local server start karne ka process yahaan add kar sakte hain
            # Ya user ko instructions de sakte hain. Abhi ke liye, dummy URL.
            generated_app_url = f"http://127.0.0.1:5001/{app_name}" # Example dummy URL for Flask
            status_message += " (Flask app ko manually run karna hoga)"
        else:
            generated_app_url = f"file:///{generated_app_path.replace(os.sep, '/')}"


        status_message = f"App successfully generated ({app_type})."

    except Exception as e:
        print(f"Error during app generation: {e}")
        return jsonify({"error": f"App generation failed: {str(e)}"}), 500

    # Response
    return jsonify({
        "status": "success",
        "message": status_message,
        "generated_url": generated_app_url,
        "received_prompt": user_prompt
    }), 200

# Agar yeh file directly run ki jaati hai
# Agar yeh file directly run ki jaati hai
if __name__ == '__main__':
    # Flask app ko run karne se pehle FLASK_APP environment variable set karein
    # Isse Flask ko pata chalega ki 'app' naam ka module kahan hai
    # os.environ['FLASK_APP'] = 'app'
    # Flask app ko port 5000 par run karein
    app.run(debug=True, port=5000)