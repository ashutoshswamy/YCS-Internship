from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello world!"

@app.route("/get_user/<user_id>", methods = ["GET"])
def get_user(user_id):
    user_data = {
        "user_id": user_id,
        "name": "John Doe",
        "email": "johndoe.example@gmail.com"
    }

    extra = request.args.get("extra")
    if extra:
        user_data["extra"] = extra

    return jsonify(user_data), 200

@app.route("/create_user", methods = ["POST"])
def create_user():
    data = request.get_json()

    return (data), 201

if __name__ == "__main__":
    app.run(debug=True)