from elasticsearch import Elasticsearch

# Initialize Elasticsearch client
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# Define the index name
index_name = 'soccernet'

# Query for documents with missing start_time or end_time
response = es.search(
    index=index_name,
    body={
        "query": {
            "bool": {
                "should": [
                    { "bool": { "must_not": { "exists": { "field": "transcription.segments.start_time" } } } },
                    { "bool": { "must_not": { "exists": { "field": "transcription.segments.end_time" } } } }
                ]
            }
        },
        "_source": ["transcription.segments.start_time", "transcription.segments.end_time"],
        "size": 100  # Limit results if necessary
    }
)

# Check and print the results
if response['hits']['total']['value'] > 0:
    print(f"Found {response['hits']['total']['value']} documents with missing start_time or end_time.")
    for hit in response['hits']['hits']:
        print(hit['_source'])
else:
    print("No documents with missing start_time or end_time found.")
