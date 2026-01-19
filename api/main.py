from flask import Flask, jsonify
from redis import Redis, RedisError
from http import HTTPStatus
from config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD, API_HOST, API_PORT

redis_client = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
    decode_responses=True,
)

app = Flask(__name__)


@app.route("/")
def index():
    count = redis_client.incr("counter")
    return jsonify({"count": count, "meta": "version 2"}), HTTPStatus.OK


@app.route("/ping")
def ping():
    try:
        redis_client.ping()
    except RedisError as e:
        return jsonify(
            {"message": "Redis connection error", "detail": str(e)}
        ), HTTPStatus.SERVICE_UNAVAILABLE
    return jsonify({"message": "pong"}), HTTPStatus.OK


if __name__ == "__main__":
    app.run(host=API_HOST, port=API_PORT)
