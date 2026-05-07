from flask import Flask, request, jsonify, render_template_string
import time
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

HTML = """<!DOCTYPE html>
<html>
<head><title>Test Web App</title></head>
<body>
<h1>Test Web Application</h1>
<h2>Contact</h2>
<form action="/contact" method="post">
  <input name="name" placeholder="Name"><br>
  <input name="email" placeholder="Email"><br>
  <textarea name="message" placeholder="Message"></textarea><br>
  <button type="submit">Send</button>
</form>
<h2>Login</h2>
<form action="/login" method="post">
  <input name="username" placeholder="Username"><br>
  <input name="password" type="password" placeholder="Password"><br>
  <button type="submit">Login</button>
</form>
</body>
</html>"""


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/contact", methods=["POST"])
def contact():
    app.logger.info(f"contact from {request.remote_addr}: {request.form.get('email')}")
    return jsonify({"status": "ok"})


@app.route("/login", methods=["POST"])
def login():
    app.logger.info(f"login from {request.remote_addr}: {request.form.get('username')}")
    return jsonify({"status": "ok"})


@app.route("/register", methods=["POST"])
def register():
    app.logger.info(f"register from {request.remote_addr}: {request.form.get('email')}")
    return jsonify({"status": "ok"})


@app.route("/health")
def health():
    return jsonify({"status": "healthy", "timestamp": time.time()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
