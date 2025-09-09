import requests
import sys

PROMETHEUS_URL = "http://localhost:9090"

PROMQL_QUERY = 'sum(rate(http_requests_total{status_code=~"2.."}[5m])) / sum(rate(http_requests_total[5m]))'

SLO_THRESHOLD = 0.999  # 99.9%

def get_availability():
    try:
        response = requests.get(f'{PROMETHEUS_URL}/api/v1/query', params={'query': PROMQL_QUERY})
        result = response.json()
        
        if not result['data']['result']:
            print("No data returned. This usually means Prometheus hasn't scraped metrics or no requests occurred in the last 5 minutes.")
            print("Make sure your Flask app is running and being hit by traffic (try running load-test.js).")
            sys.exit(1)

        value = float(result['data']['result'][0]['value'][1])
        return value
    except Exception as e:
        print("Failed to parse availability metric:", str(e))
        sys.exit(1)

availability = get_availability()

print(f"Current availability: {availability * 100:.2f}%")

if availability < SLO_THRESHOLD:
    print("SLO violated. Deployment halted.")
    sys.exit(1)
else:
    print("SLO met. Proceeding with deployment.")
    sys.exit(0)
