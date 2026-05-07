import os
import time
import random
import string
import threading
import logging
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(threadName)s] %(message)s")
logger = logging.getLogger(__name__)

TARGET_URL = os.getenv("TARGET_URL", "http://ai-protection-svc:8000")
RPS = float(os.getenv("REQUESTS_PER_SECOND", "2.0"))
ATTACK_TYPE = os.getenv("ATTACK_TYPE", "form_spam")
THREAD_COUNT = int(os.getenv("THREAD_COUNT", "1"))

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "python-requests/2.32"})


def _rand(n=8):
    return "".join(random.choices(string.ascii_lowercase, k=n))


def _email():
    return f"{_rand()}@{_rand()}.com"


def spam_contact():
    while True:
        try:
            r = SESSION.post(
                f"{TARGET_URL}/contact",
                data={"name": _rand(10), "email": _email(), "message": " ".join(_rand(6) for _ in range(8))},
                timeout=5,
            )
            logger.info(f"contact → {r.status_code}")
        except Exception as e:
            logger.warning(f"contact error: {e}")
        time.sleep(1.0 / RPS)


def bruteforce_login():
    usernames = ["admin", "root", "user", "test", "guest", "administrator"]
    while True:
        try:
            r = SESSION.post(
                f"{TARGET_URL}/login",
                data={"username": random.choice(usernames), "password": _rand(10)},
                timeout=5,
            )
            logger.info(f"login → {r.status_code}")
        except Exception as e:
            logger.warning(f"login error: {e}")
        time.sleep(1.0 / RPS)


def mixed():
    fns = [spam_contact, bruteforce_login]
    random.choice(fns)()


ATTACKS = {
    "form_spam": spam_contact,
    "login_bruteforce": bruteforce_login,
    "mixed": mixed,
}


def main():
    fn = ATTACKS.get(ATTACK_TYPE, spam_contact)
    threads = [threading.Thread(target=fn, name=f"bot-{i}", daemon=True) for i in range(THREAD_COUNT)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
