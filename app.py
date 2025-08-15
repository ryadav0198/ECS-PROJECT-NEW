from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from ECS Fargate via GitHub Actions! 🚀 Version 1 from rohit"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

