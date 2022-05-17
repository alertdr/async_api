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

    data = [
        {
            'id': 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a', 'name': 'George Lucas',
            'roles': ['writer', 'director'],
            'films_as_director': ['3d825f60-9fff-4dfe-b294-1a45fa1e115d'],
            'films_as_writer': ['4af6c9c9-0be0-4864-b1e9-7f87dd59ee1f', '3d825f60-9fff-4dfe-b294-1a45fa1e115d'],
            'films_as_actor': []
        },
        {
            'id': '5b4bf1bc-3397-4e83-9b17-8b10c6544ed1', 'name': 'Harrison Ford', 'roles': ['actor'],
            'films_as_actor': ['4af6c9c9-0be0-4864-b1e9-7f87dd59ee1f', '3d825f60-9fff-4dfe-b294-1a45fa1e115d'],
            'films_as_director': [],
            'films_as_writer': []
        },
        {
            'id': '5b4bf1bc-3397-4e83-9b17-8b10c6544ed2', 'name': 'Immanuel Cant', 'roles': ['writer'],
            'films_as_actor': [],
            'films_as_director': [],
            'films_as_writer': ['3d825f60-9fff-4dfe-b294-1a45fa1e115d']
        }
    ]

    expected = [{'uuid': item['id'], 'full_name': item['name'], 'roles': item['roles'],
                 'actor_ids': item['films_as_actor'], 'writer_ids': item['films_as_writer'],
                 'director_ids': item['films_as_director']} for item in data]
