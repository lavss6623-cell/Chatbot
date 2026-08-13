from flask import Flask, render_template, request, jsonify

from src.chatbot import TNEAChatbot

import traceback

# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)


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
        return jsonify({
            "error": "No JSON data received."
        }), 400

    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "error": "Message cannot be empty."
        }), 400

    try:

        response = bot.process_message(message)

        return jsonify({
            "response": response,
            "state": bot.state.to_dict()
        })

    except Exception as e:

        print("\n========== CHATBOT ERROR ==========")
        traceback.print_exc()
        print("===================================\n")

        return jsonify({
            "error": str(e)
        }), 500

# ============================================================
# RESET CHAT
# ============================================================

@app.route("/reset", methods=["POST"])
def reset():

    global bot

    bot = TNEAChatbot()

    return jsonify({
        "message": "Conversation reset successfully.",
        "state": bot.state.to_dict()
    })


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )