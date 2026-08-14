from email.mime import message

from flask import Flask, render_template, request, jsonify

from src.chatbot import TNEAChatbot

import traceback

# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)

@app.errorhandler(400)
def handle_bad_request(error):
    return jsonify({
        "error": "Invalid JSON request."
    }), 400
    
@app.errorhandler(415)
def handle_unsupported_media_type(error):
    return jsonify({
        "error": "Content-Type must be application/json."
    }), 415

# ============================================================
# CHATBOT INSTANCE
# ============================================================

bot = TNEAChatbot()


# ============================================================
# HOME PAGE
# ============================================================


@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# CHAT API
# ============================================================


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data received."}), 400

    message = data.get("message")


    if message is None:
        return jsonify({"error": "Message cannot be empty."}), 400

    if not isinstance(message, str):
        return jsonify({"error": "Message must be a string."}), 400

    message = message.strip()

    if not message:
        return jsonify({"error": "Message cannot be empty."}), 400

    try:

        response = bot.process_message(message)

        return jsonify({"response": response, "state": bot.state.to_dict()})

    except Exception as e:

        print("\n========== CHATBOT ERROR ==========")
        traceback.print_exc()
        print("===================================\n")

        return jsonify({"error": str(e)}), 500

# ============================================================
# RESET CHAT
# ============================================================


@app.route("/reset", methods=["POST"])
def reset():

    global bot

    bot = TNEAChatbot()

    return jsonify(
        {"message": "Conversation reset successfully.", "state": bot.state.to_dict()}
    )


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
