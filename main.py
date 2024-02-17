# from flask import Flask, render_template, request, jsonify
# import openai
# import config
# import json

# openai.api_key = config.API_KEY

# app = Flask(__name__)

# def save_interaction(qa_pair):
#     with open('interaction_history.json', 'a') as file:
#         json.dump(qa_pair, file)
#         file.write('\n')

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route('/get', methods=['GET'])
# def get_bot_response():
#     userText = request.args.get('msg')
#     response = openai.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "user", "content": userText}
#         ]
#     )

#     answer = response.choices[0].message.content

#     qa_pair = {
#         "question": userText,
#         "answer": answer
#     }

#     save_interaction(qa_pair)

#     print(qa_pair)
#     return str(answer)

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request, jsonify, session
import openai
import config
import json
import os
from flask_session import Session  # Ensure Flask-Session is installed
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
    # session['chat_id'] = session.sid  # Generate unique session ID
    session.clear()  # Clear existing session data
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
    qa_pair = [userText, answer]  # Adjust to list of lists structure

    save_interaction(session['chat_id'], qa_pair)  # Use session ID for tracking

    print(qa_pair)
    return answer

if __name__ == "__main__":
    app.run(debug=True)
