from flask import Flask, render_template, request, jsonify, session
import openai
import config
import json
import os
from flask_session import Session
import os
import secrets
from datetime import datetime

openai.api_key = config.API_KEY

app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "your_secret_key"
Session(app)

def save_interaction(session_id, qa_pair):
    history_file = 'interaction_history.json'
    if os.path.exists(history_file):
        with open(history_file, 'r+') as file:
            try:
                history = json.load(file)
            except json.JSONDecodeError:
                history = {}
    else:
        history = {}

    if session_id not in history:
        history[session_id] = [qa_pair]
    else:
        history[session_id].append(qa_pair)

    with open(history_file, 'w') as file:
        json.dump(history, file, indent=4)

@app.route("/")
def index():
    # session['chat_id'] = session.sid  
    session.clear()
    custom_session_id = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{secrets.token_urlsafe(4)}"
    session['chat_id'] = custom_session_id
    return render_template("index.html")

@app.route('/get', methods=['GET'])
def get_bot_response():
    userText = request.args.get('msg')
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": userText}
        ]
    )

    answer = response.choices[0].message.content
    qa_pair = [userText, answer]  

    save_interaction(session['chat_id'], qa_pair)  

    print(qa_pair)
    return answer

if __name__ == "__main__":
    app.run(debug=True)