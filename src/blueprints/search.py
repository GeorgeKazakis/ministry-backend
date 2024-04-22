import json
from datetime import datetime
from flask import Blueprint, request, Response
from elasticsearch import Elasticsearch

search = Blueprint("search", __name__)


def multiword_query(search_term: str):
    return {
        "query": {
            "bool": {
                "should": [{
                    "match": {
                        "remit": {
                            "query": search_term,
                            "fuzziness": "AUTO"
                        }
                    }
                }, {
                    "match_phrase": {
                        "remit": search_term
                    }
                }, {
                    "match": {
                        "organization_name": {
                            "query": search_term,
                            "fuzziness": "AUTO"
                        }
                    }
                }, {
                    "match_phrase": {
                        "organization_name": search_term
                    }
                }]
            }
        }
    }


def create_query(search_term: str) -> dict:
    query = {
        "query": {
            "multi_match": {
                "query": f"{search_term}",
                "type": "best_fields",
                "fields": ["*"],
                "fuzziness": "AUTO",
                "tie_breaker": 0.3
            }
        }
    }
    return query


@search.route("/search/", methods=["POST"])
def search_remit():

    data = request.get_json()

    search_term: str = data['search_term']

    search_body = create_query(search_term)

    es = Elasticsearch("http://localhost:9200", http_auth=('elastic', '1234'))

    search_response = es.search(index="foreis,monades", body=search_body)

    hits: list[dict] = search_response['hits']['hits']

    return Response(json.dumps({
        "count": len(hits),
        "hits": hits
    }),
                    mimetype="application/json",
                    status=200)
