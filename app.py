from flask import Flask, request
import random, time
from prometheus_client import Counter, Summary, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Custom Metrics
REQUEST_LATENCY = Summary('request_latency_seconds', 'Latency of HTTP requests')
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['status_code'])

@app.route('/')
@REQUEST_LATENCY.time()
def homepage():
    delay = random.uniform(0.1, 1.5)
    time.sleep(delay)

    # Randomly simulate 5xx errors
    if random.random() < 0.1:
        REQUEST_COUNT.labels(status_code='500').inc()
        return 'Internal Server Error', 500

    REQUEST_COUNT.labels(status_code='200').inc()
    return f"Hello from SLO Monitoring App!! Delay: {round(delay, 2)}s"

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
