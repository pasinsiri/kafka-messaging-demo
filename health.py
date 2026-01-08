from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
@app.route("/health")
def health():
    return "Kafka is alive", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)