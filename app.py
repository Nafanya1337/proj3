from flask import Flask, render_template, request
import os
from datetime import datetime
import redis

app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", "6379"))

redis_client = None
redis_available = False

try:
    redis_client = redis.Redis(
        host=redis_host,
        port=redis_port,
        decode_responses=True,
        socket_connect_timeout=1,
        socket_timeout=1,
    )
    redis_client.ping()
    redis_available = True
except Exception:
    redis_client = None
    redis_available = False


@app.route("/")
def home():
    visits = 1

    if redis_available and redis_client is not None:
        try:
            visits = redis_client.incr("page_visits")
        except Exception:
            pass

    forwarded_for = request.headers.get("X-Forwarded-For", "")
    if forwarded_for:
        client_ip = forwarded_for.split(",")[0].strip()
    else:
        client_ip = request.remote_addr or "unknown"

    user_agent = request.headers.get("User-Agent", "unknown")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return render_template(
        "index.html",
        visits=visits,
        client_ip=client_ip,
        user_agent=user_agent,
        current_time=current_time,
        redis_available=redis_available,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
