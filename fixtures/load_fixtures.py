"""
Generates fixtures into a local es instance.

Host and credentials are hardcoded on purpose, to avoid loading fixtures to
an external es instance.
"""

import json
import os

from elasticsearch import Elasticsearch


def load_fixtures():
    es = Elasticsearch(
        'http://localhost:9200/',
        basic_auth=('elastic', 'elastic'),
        )

    indexes = ['webcontents', 'webapi', 'dataset', 'notebooks']
    fixtures_dir = os.path.dirname(os.path.abspath(__file__))

    for index in indexes:
        with open(f'{fixtures_dir}/{index}.json', 'r') as f:
            fixtures = json.load(f)
            for fixture in fixtures:
                es.index(index=index, document=fixture)


if __name__ == '__main__':
    load_fixtures()
