import os
import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, render_template, request

# Load environment variables
load_dotenv()

# Retrieve API key
api_key = os.getenv("GEMINI_API_KEY")

# Configure the Gemini API
genai.configure(api_key=api_key)

# Use a supported Gemini 1.5 model (gemini-1.5-flash-001)
model = genai.GenerativeModel("models/gemini-1.5-flash-001")

# Create the Flask app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/allocate", methods=["POST"])
def allocate():
    project_title = request.form["project_title"]
    team_members = request.form["team_members"]

    # Prompt to assign roles
    prompt = f"""
    You are a smart project manager. Given the project: "{project_title}" and team members: {team_members}, assign suitable roles to each member based on common team roles like: 
    - Project Lead
    - Developer
    - Tester
    - Documentation
    - Research

    Format the response clearly with names and assigned roles.
    """

    # Start chat and send message to Gemini API
    chat = model.start_chat()
    response = chat.send_message(prompt)
    result = response.text

    # Render result on a new page
    return render_template("result.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
