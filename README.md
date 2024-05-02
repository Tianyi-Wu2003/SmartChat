# SMARTCHAT

The chatbot application that incorporates up-to-date information from Wikipedia.

## Instructions

After downloading all files:

1. Run the backend with "python3 chatbot_app.py" in terminal
2. Open index.html in your browser
3. Copy your server address (url after Running on) and paste it in the blank of the html
4. Ping the server - if you get hello world, your server is working properly.

## Project Structure

- wikipage.py: This file implements the back-end logic for processing user inputs, particularly handling requests related to Wikipedia pages. It includes functionality to search and fetch information from Wikipedia, likely by parsing the user input and fetching relevant data.
- chatclient.py: This file implements the chatclient class that keeps track of title, wikipage, and makes api call to openai api with appropriate prompts.
- chatbot_app.py: This script forms the main back-end server, managing incoming HTTP requests from clients. It includes endpoints to handle different types of requests, processing them and generating appropriate responses to return to the client. The script integrates with wikipage.py and manages response generation logic.
- index.html: This is the main front-end interface for users, offering a simple design for interacting with the chatbot.

## Functionality

- Server Communication: The web interface communicates with the server by sending HTTP requests, primarily through functions in chatclient.py.
- Ping Server: Users can check the server's connectivity by pinging it, displayed by a response message.
- Message Exchange: Users can send messages to the chatbot, triggering a response generated by the server. The server processes the input, querying Wikipedia if possible, and returns a response displayed on the interface.
- Dynamic UI: The front-end manages message exchanges dynamically, updating the chat container with user and bot messages in a smooth scrolling manner.
