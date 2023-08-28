"""
Generates fixtures from an external es instance containing indexed data.
Run with ELASTICSEARCH_PASSWORD, ELASTICSEARCH_URL, and ELASTICSEARCH_USERNAME.
"""

import json
import os

from elasticsearch import Elasticsearch


def get_fixtures_from_index(es, index, count):
    response = es.search(
        index=index,
        query={'match_all': {}},
        size=count,
        )
    return [h['_source'] for h in response['hits']['hits']]


def get_fixtures(count):
    es = Elasticsearch(
        os.environ['ELASTICSEARCH_URL'],
        basic_auth=(
            os.environ.get('ELASTICSEARCH_USERNAME'),
            os.environ.get('ELASTICSEARCH_PASSWORD'),
            ),
        )

    indexes = ['webcontents', 'webapi', 'dataset', 'notebooks']
    fixtures_dir = os.path.dirname(os.path.abspath(__file__))

    for index in indexes:
        fixtures = get_fixtures_from_index(es, index, count=count)
        with open(f'{fixtures_dir}/{index}.json', 'w') as f:
            json.dump(fixtures, f, indent=2)


if __name__ == '__main__':
    get_fixtures(100)
