import requests
import elasticsearch

# Check Elasticsearch server version
try:
    response = requests.get('http://localhost:9200')
    if response.status_code == 200:
        server_info = response.json()
        print(f"Elasticsearch server version: {server_info['version']['number']}")
    else:
        print(f"Unexpected status code: {response.status_code}")
except requests.ConnectionError as e:
    print(f"Error connecting to Elasticsearch via HTTP: {e}")

# Check Elasticsearch client version
print(f"Elasticsearch client version: {elasticsearch.__version__}")