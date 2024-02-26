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

def save_interaction(session_id, question, answer, question_type, response_type):
    history_file = 'interaction_history.json'
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    qa_pair = {
        "question": question,
        "question_type": question_type,
        "answer": {
            "type": response_type,  
            "content": answer
        },
        "timestamp": timestamp
    }

    if os.path.exists(history_file):
        with open(history_file, 'r+') as file:
            try:
                history = json.load(file)
            except json.JSONDecodeError:
                history = {}
    else:
        history = {}

    if session_id not in history:
        history[session_id] = {"exchanges": [qa_pair]}
    else:
        history[session_id]["exchanges"].append(qa_pair)

    with open(history_file, 'w') as file:
        json.dump(history, file, indent=4)


def classify_question_type(question):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "system", "content": "Classify the following question as sports/mathematics/programming or anything. give me one word reply"},
            {"role": "user", "content": question}
        ]
    )
    question_type = response.choices[0].message.content
    return question_type

def classify_response_via_api(answer):

    query = f"Does the following response contain code?\n\n{answer}"
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": query}
        ]
    )
    
    api_answer = response.choices[0].message.content.lower()
    
    if "yes" in api_answer:
        return "code"
    else:
        return "string"


@app.route("/")
def index(): 
    session.clear()
    custom_session_id = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{secrets.token_urlsafe(4)}"
    session['chat_id'] = custom_session_id
    return render_template("index.html")

@app.route('/get', methods=['GET'])
def get_bot_response():
    userText = request.args.get('msg')
    question_type = classify_question_type(userText)
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": userText}
        ]
    )

    answer = response.choices[0].message.content
    print(answer)
    response_type = classify_response_via_api(answer)
    qa_pair = [userText, answer]  

    save_interaction(session['chat_id'], userText, answer, question_type, response_type)  

    print(qa_pair)
    return answer

if __name__ == "__main__":
    app.run(debug=True)