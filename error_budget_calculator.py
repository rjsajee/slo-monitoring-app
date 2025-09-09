import requests
from slo_config import SLO

PROMETHEUS_URL = "http://localhost:9090/api/v1/query"

total_window = SLO["window_minutes"] * 60
error_budget = (100 - SLO["availability"]) / 100 * total_window

def query_prometheus(promql):
    try:
        response = requests.get(PROMETHEUS_URL, params={'query': promql})
        result = response.json()['data']['result']
        if not result:
            print(f"No data for query: {promql}")
            return 0.0
        return float(result[0]['value'][1])
    except Exception as e:
        print(f"Error querying Prometheus: {e}")
        return 0.0

error_rate_query = 'sum(rate(http_requests_total{status_code=~"5.."}[5m]))'
total_rate_query = 'sum(rate(http_requests_total[5m]))'

error_rate = query_prometheus(error_rate_query)
total_rate = query_prometheus(total_rate_query)

if total_rate > 0:
    availability = (1 - error_rate / total_rate) * 100
else:
    availability = 100

used_budget_percent = max(0, (100 - availability))
used_budget_seconds = (used_budget_percent / 100) * total_window
remaining_budget_seconds = error_budget - used_budget_seconds

print(f"Availability: {availability:.2f}%")
print(f"Error Budget: {error_budget:.1f} seconds allowed")
print(f"Used Budget: {used_budget_seconds:.1f} seconds")
print(f"Remaining Budget: {remaining_budget_seconds:.1f} seconds")
