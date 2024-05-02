import caller 

from chatclient import Chatclient

from flask import Flask, request, jsonify, session
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config["CORS_HEADERS"] = "Content-Type"
app.secret_key = "your_secret_key"


"""
Main function called by router that generates response based on user input and openai api
"""
def chatbot_response(user_input:str, client:Chatclient, title:str):    
    if client.has_page:
        msg = f"Of course, I accessed the wikipedia page titled {title} to better assist you.\n"
        return msg + client.generate_with_prompt(user_input)
    else:
        print("1-3")
        msg = f"I didn't get a wikipediapage titled {title}, I will help you to the best of my knowledge.\n" 
        return msg + client.generate_without_prompt(user_input)

"""
Route to test server connection
"""
@app.route("/hello_world", methods=["GET"])
def hello_world():
    """
    A simple endpoint that returns 'Hello World'.

    This is used for testing server functionality.
    """
    return "Hello World"

"""
Route to post response to front end
"""
@app.route("/get-response", methods=["POST"])
def get_response():
    """
    Endpoint to handle user messages and return chatbot responses.
    """
    user_input = request.json.get('message')
    
    if "start new question" in user_input.lower():
        title = caller.new_title(user_input)
        session["title"] = title
        print(session.get("title"))
    else:
        title = session.get("title")
        print(f"This is stored title {title}")

    if title is None: 
        return jsonify({"response": "No conversation history found."}), 400

    
    client = caller.new_chat(title)
    response = chatbot_response(user_input, client, title)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)


