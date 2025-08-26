from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from ECS Fargate via GitHub Actions! 🚀 Version 4.0.2 from rohit kumar yadav Now i'm more advanced this is Blue green deployment"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

