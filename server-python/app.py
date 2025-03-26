import os
from dotenv import load_dotenv
from flask import Flask, request, Response, stream_with_context
from flask_cors import CORS
from google import genai
from google.genai import types


# Load environment variables from a .env file located in the same directory
load_dotenv()

# Initialize a Flask application
app = Flask(__name__)

# Apply CORS to the Flask app which allows it to accept requests from all domains
CORS(app)

# Initialize the client with the API key obtained from the environment variable
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))


def convert_history(history):
    """
    Convert history from dict format to Content objects expected by the API.

    Args:
        history: List of chat history objects with role and parts

    Returns:
        List of Content objects
    """
    content_history = []

    for message in history:
        role = message.get("role")
        parts = message.get("parts", [])

        # Process parts based on their type
        processed_parts = []
        for part in parts:
            if isinstance(part, dict) and "text" in part:
                # If part is a dictionary with a text key
                processed_parts.append(types.Part(text=part["text"]))
            elif isinstance(part, str):
                # If part is a simple string
                processed_parts.append(types.Part(text=part))
            else:
                # Skip any parts that don't fit the expected formats
                continue

        # Create a Content object with appropriate role and processed parts
        content = types.Content(
            role="user" if role == "user" else "model",
            parts=processed_parts,
        )
        content_history.append(content)

    return content_history


@app.route("/chat", methods=["POST"])
def chat():
    """
    Processes user input and returns AI-generated responses.

    Args:
        None (uses Flask `request` object to access POST data)

    Returns:
        A JSON object with a key "text" that contains the AI-generated response.
    """
    # Parse the incoming JSON data into variables.
    data = request.json
    msg = data.get("chat", "")
    raw_history = data.get("history", [])

    # Convert the history to the expected Content format
    history = convert_history(raw_history)

    # Create chat session with properly formatted history
    chat_session = client.chats.create(model="gemma-3-27b-it", history=history)

    # Send the latest user input to the model and get the response
    response = chat_session.send_message(message=msg)

    return {"text": response.text}


@app.route("/stream", methods=["POST"])
def stream():
    """
    Streams AI responses for real-time chat interactions.

    Args:
        None (uses Flask `request` object to access POST data)

    Returns:
        A Flask `Response` object that streams the AI-generated responses.
    """

    def generate():
        # Parse the incoming JSON data into variables.
        data = request.json
        msg = data.get("chat", "")
        raw_history = data.get("history", [])

        # Convert the history to the expected Content format
        history = convert_history(raw_history)

        # Create chat session with properly formatted history
        chat_session = client.chats.create(model="gemma-3-27b-it", history=history)

        # Send the latest user input to the model and stream the response
        for chunk in chat_session.send_message_stream(message=msg):
            yield f"{chunk.text}"

    return Response(stream_with_context(generate()), mimetype="text/event-stream")


# Configure the server to run on port 9000
if __name__ == "__main__":
    app.run(port=os.environ.get("PORT", 5000))
