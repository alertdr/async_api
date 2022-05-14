class Persons:
    mapping = {
        "settings": {
            "refresh_interval": "1s",
            "analysis": {
                "filter": {
                    "english_stop": {
                        "type": "stop",
                        "stopwords": "_english_"
                    },
                    "english_stemmer": {
                        "type": "stemmer",
                        "language": "english"
                    },
                    "english_possessive_stemmer": {
                        "type": "stemmer",
                        "language": "possessive_english"
                    },
                    "russian_stop": {
                        "type": "stop",
                        "stopwords": "_russian_"
                    },
                    "russian_stemmer": {
                        "type": "stemmer",
                        "language": "russian"
                    }
                },
                "analyzer": {
                    "ru_en": {
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "english_stop",
                            "english_stemmer",
                            "english_possessive_stemmer",
                            "russian_stop",
                            "russian_stemmer"
                        ]
                    }
                }
            }
        },
        "mappings": {
            "dynamic": "strict",
            "properties": {
                "id": {
                    "type": "keyword"
                },
                "name": {
                    "type": "text",
                    "analyzer": "ru_en"
                },
                "roles": {
                    "type": "keyword"
                },
                "films_as_actor": {
                    "type": "keyword"
                },
                "films_as_director": {
                    "type": "keyword"
                },
                "films_as_writer": {
                    "type": "keyword"
                }
            }
        }
    }
    person1 = {
        '_index': 'persons', '_id': 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a',
        '_source': {
            'id': 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a', 'name': 'George Lucas',
            'roles': ['writer', 'director'],
            'films_as_director': ['3d825f60-9fff-4dfe-b294-1a45fa1e115d'],
            'films_as_writer': ['0312ed51-8833-413f-bff5-0e139c11264a', '3d825f60-9fff-4dfe-b294-1a45fa1e115d'],
            'films_as_actor': None
        }
    }
    person2 = {
        '_index': 'persons', '_id': '5b4bf1bc-3397-4e83-9b17-8b10c6544ed1',
        '_source': {
            'id': '5b4bf1bc-3397-4e83-9b17-8b10c6544ed1', 'name': 'Harrison Ford', 'roles': ['actor'],
            'films_as_actor': ['0312ed51-8833-413f-bff5-0e139c11264a', '3d825f60-9fff-4dfe-b294-1a45fa1e115d'],
            'films_as_director': None,
            'films_as_writer': None
        }
    }
    expected_person1 = {
        'uuid': 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a', 'full_name': 'George Lucas',
        'roles': ['writer', 'director'],
        'writer_ids': ['0312ed51-8833-413f-bff5-0e139c11264a', '3d825f60-9fff-4dfe-b294-1a45fa1e115d'],
        'director_ids': ['3d825f60-9fff-4dfe-b294-1a45fa1e115d']
    }
    expected_person2 = {
        'uuid': '5b4bf1bc-3397-4e83-9b17-8b10c6544ed1', 'full_name': 'Harrison Ford',
        'roles': ['actor'],
        'actor_ids': ['0312ed51-8833-413f-bff5-0e139c11264a', '3d825f60-9fff-4dfe-b294-1a45fa1e115d']
    }
    expected_persons = [expected_person2, expected_person1]
    expected_cache = '{"id": "5b4bf1bc-3397-4e83-9b17-8b10c6544ed1", "name": "Harrison Ford", "roles": ["actor"], "films_as_actor": ["0312ed51-8833-413f-bff5-0e139c11264a", "3d825f60-9fff-4dfe-b294-1a45fa1e115d"], "films_as_director": null, "films_as_writer": null}'
    expected_cache2 = ('{"id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a", "name": "George Lucas", '
                       '"roles": ["writer", "director"], "films_as_actor": null, '
                       '"films_as_director": ["3d825f60-9fff-4dfe-b294-1a45fa1e115d"], '
                       '"films_as_writer": ["0312ed51-8833-413f-bff5-0e139c11264a", '
                       '"3d825f60-9fff-4dfe-b294-1a45fa1e115d"]}')
