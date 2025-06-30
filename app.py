from flask import Flask, render_template, request, jsonify, session
from chatbot_logic import get_response, is_in_plan_mode, update_plan_session, reset_plan

app = Flask(__name__)
app.secret_key = "super_secret_key"

@app.route("/")
def index():
    reset_plan(session)
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    response = get_response(user_message, session)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
