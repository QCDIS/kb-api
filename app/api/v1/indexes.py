import os

from elasticsearch import Elasticsearch


# Index to search for each resource type
index = {
    'web_pages': 'webcontents',
    'apis': 'webapi',
    'datasets': 'dataset',
    'notebooks': 'notebooks',
    None: ['webcontents', 'webapi', 'dataset', 'notebooks'],
    }

# Search parameters for each resource type
search_params = {
    'web_pages': {
        'fields': ['title', 'pageContetnts', 'organizations', 'topics',
                   'people', 'workOfArt', 'files', 'locations', 'dates',
                   'researchInfrastructure'],
        'type': 'best_fields',
        'minimum_should_match': '100%',
        },
    'apis': {
        'fields': ['name', 'description', 'category', 'provider',
                   'serviceType', 'architecturalStyle'],
        'type': 'best_fields',
        'minimum_should_match': '50%',
        },
    'datasets': {
        'fields': ['description', 'keywords', 'contact', 'publisher',
                   'citation', 'genre', 'creator', 'headline', 'abstract',
                   'theme', 'producer', 'author', 'sponsor', 'provider',
                   'title', 'instrument', 'maintainer', 'editor',
                   'copyrightHolder', 'contributor', 'contentLocation',
                   'about', 'rights', 'useConstraints', 'status', 'scope',
                   'metadataProfile', 'metadataIdentifier', 'distributionInfo',
                   'dataQualityInfo', 'contentInfo', 'repo',
                   'essential_variables', 'potential_topics'],
        'type': 'best_fields',
        'minimum_should_match': '50%',
        },
    'notebooks': {
        'fields': ['name', 'description'],
        'type': 'best_fields',
        'minimum_should_match': '50%',
        },
    None: {
        'fields': ['publisher', 'producer', 'organizations', 'rights',
                   'useConstraints', 'potential_topics',
                   'researchInfrastructure', 'metadataIdentifier',
                   'serviceType', 'metadataProfile', 'topics', 'genre',
                   'pageContetnts', 'creator', 'citation', 'description',
                   'copyrightHolder', 'title', 'keywords', 'author',
                   'maintainer', 'status', 'dataQualityInfo', 'abstract',
                   'locations', 'instrument', 'contentInfo', 'headline',
                   'workOfArt', 'sponsor', 'contributor', 'people', 'files',
                   'contentLocation', 'about', 'architecturalStyle', 'editor',
                   'theme', 'dates', 'repo', 'name', 'category', 'scope',
                   'distributionInfo', 'provider', 'contact',
                   'essential_variables'],
        'type': 'best_fields',
        'minimum_should_match': '50%',
        }
    }

# Functions to convert indexed documents into API results, for each index
doc_converters = {
    'webcontents': lambda doc: {
        'resource_type': 'web_pages',
        'title': ' '.join(doc.get('title')),
        'description': ' '.join(doc.get('pageContetnts')),
        'url': doc.get('url')[0],
        'details': {
            'research_infrastructure':
                doc.get('researchInfrastructure', [{}])[0].get('acronym'),
            },
        },
    'webapi': lambda doc: {
        'resource_type': 'apis',
        'title': ' '.join(doc.get('name')),
        'description': ' '.join(doc.get('description')),
        'url': doc.get('url')[0],
        'details': {
            },
        },
    'dataset': lambda doc: {
        'resource_type': 'datasets',
        'title': ' '.join(doc.get('title')),
        'description': ' '.join(doc.get('description')),
        'url': doc.get('source')[0],
        'details': {
            'repository': ', '.join(doc.get('repo')),
            },
        },
    'notebooks': lambda doc: {
        'resource_type': 'notebooks',
        'title': doc.get('name'),
        'description': doc.get('description'),
        'url': doc.get('html_url'),
        'details': {
            'repository': doc.get('source'),
            },
        },
    }


def convert_hits(hits):
    results = []
    for hit in hits:
        converter = doc_converters[hit['_index']]
        res = converter(hit['_source'])
        results.append(res)
    return results


def search(resource_type: str | None, q: str, skip: int, limit: int):

    es = Elasticsearch(
        os.environ['ELASTICSEARCH_URL'],
        http_auth=[
            os.environ.get('ELASTICSEARCH_USERNAME'),
            os.environ.get('ELASTICSEARCH_PASSWORD'),
            ],
        )

    query_body = {
        'from': skip,
        'size': limit,
        'query': {
            'bool': {
                'must': {
                    'multi_match': {
                        'query': q,
                        **search_params[resource_type],
                        }
                    },
                }
            },
        }
    response = es.search(
        index=index[resource_type],
        body=query_body,
        )
    return convert_hits(response['hits']['hits'])
