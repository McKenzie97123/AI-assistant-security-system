import os
import re
import time
import secrets
import operator
import logging
from flask import Flask, request, jsonify, render_template_string, session

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", secrets.token_hex(32))
logging.basicConfig(level=logging.INFO)

_OPS = {"+": operator.add, "-": operator.sub, "*": operator.mul}

HTML = """<!DOCTYPE html>
<html>
<head>
  <title>Test Web App</title>
  <meta charset="utf-8">
</head>
<body>
<h1>Test Web Application</h1>

<h2>Contact</h2>
<form action="/contact" method="post">
  <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
  <input name="name" placeholder="Name"><br>
  <input name="email" placeholder="Email"><br>
  <textarea name="message" placeholder="Message"></textarea><br>
  <p>Captcha: <span id="captcha-q">{{ captcha_q }}</span> = ?
     <input name="captcha_answer" placeholder="Answer" size="4">
  </p>
  <button type="submit">Send</button>
</form>

<h2>Login</h2>
<form action="/login" method="post">
  <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
  <input name="username" placeholder="Username"><br>
  <input name="password" type="password" placeholder="Password"><br>
  <p>Captcha: <span id="captcha-q">{{ captcha_q }}</span> = ?
     <input name="captcha_answer" placeholder="Answer" size="4">
  </p>
  <button type="submit">Login</button>
</form>
</body>
</html>"""


def _new_captcha() -> tuple[str, int]:
    """Zwraca (wyrażenie, odpowiedź). Proste działania — symulujemy że bot je rozwiązuje."""
    import random
    a, b = random.randint(1, 9), random.randint(1, 9)
    op_sym = random.choice(["+", "-", "*"])
    if op_sym == "-" and b > a:
        a, b = b, a
    return f"{a} {op_sym} {b}", _OPS[op_sym](a, b)


def _verify(form) -> tuple[bool, str]:
    """Sprawdza CSRF token i odpowiedź na CAPTCHA. Zwraca (ok, powód_błędu)."""
    if form.get("csrf_token") != session.get("csrf_token"):
        return False, "invalid_csrf"
    try:
        if int(form.get("captcha_answer", "")) != session.get("captcha_answer"):
            return False, "invalid_captcha"
    except ValueError:
        return False, "invalid_captcha"
    return True, ""


@app.route("/")
def index():
    session["csrf_token"] = secrets.token_hex(16)
    captcha_q, captcha_ans = _new_captcha()
    session["captcha_answer"] = captcha_ans
    return render_template_string(
        HTML,
        csrf_token=session["csrf_token"],
        captcha_q=captcha_q,
    )


@app.route("/contact", methods=["POST"])
def contact():
    ok, reason = _verify(request.form)
    if not ok:
        app.logger.warning(f"contact REJECTED from {request.remote_addr}: {reason}")
        return jsonify({"status": "error", "reason": reason}), 403
    app.logger.info(f"contact from {request.remote_addr}: {request.form.get('email')}")
    return jsonify({"status": "ok"})


@app.route("/login", methods=["POST"])
def login():
    ok, reason = _verify(request.form)
    if not ok:
        app.logger.warning(f"login REJECTED from {request.remote_addr}: {reason}")
        return jsonify({"status": "error", "reason": reason}), 403
    app.logger.info(f"login from {request.remote_addr}: {request.form.get('username')}")
    return jsonify({"status": "ok"})


@app.route("/register", methods=["POST"])
def register():
    ok, reason = _verify(request.form)
    if not ok:
        app.logger.warning(f"register REJECTED from {request.remote_addr}: {reason}")
        return jsonify({"status": "error", "reason": reason}), 403
    app.logger.info(f"register from {request.remote_addr}: {request.form.get('email')}")
    return jsonify({"status": "ok"})


@app.route("/health")
def health():
    return jsonify({"status": "healthy", "timestamp": time.time()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
