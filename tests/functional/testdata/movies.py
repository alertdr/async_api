import copy

from .base import Error


class Movies(Error):
    mapping = {
        'settings': {
            'refresh_interval': '1s',
            'analysis': {
                'filter': {
                    'english_stop': {
                        'type': 'stop',
                        'stopwords': '_english_'
                    },
                    'english_stemmer': {
                        'type': 'stemmer',
                        'language': 'english'
                    },
                    'english_possessive_stemmer': {
                        'type': 'stemmer',
                        'language': 'possessive_english'
                    },
                    'russian_stop': {
                        'type': 'stop',
                        'stopwords': '_russian_'
                    },
                    'russian_stemmer': {
                        'type': 'stemmer',
                        'language': 'russian'
                    }
                },
                'analyzer': {
                    'ru_en': {
                        'tokenizer': 'standard',
                        'filter': [
                            'lowercase',
                            'english_stop',
                            'english_stemmer',
                            'english_possessive_stemmer',
                            'russian_stop',
                            'russian_stemmer'
                        ]
                    }
                }
            }
        },
        'mappings': {
            'dynamic': 'strict',
            'properties': {
                'id': {
                    'type': 'keyword'
                },
                'imdb_rating': {
                    'type': 'float'
                },
                'genre': {
                    'type': 'nested',
                    'dynamic': 'strict',
                    'properties': {
                        'id': {
                            'type': 'keyword'
                        },
                        'name': {
                            'type': 'keyword'
                        }
                    }
                },
                'genres_names': {
                    'type': 'keyword'
                },
                'creation_date': {
                    'type': 'date'
                },
                'title': {
                    'type': 'text',
                    'analyzer': 'ru_en',
                    'fields': {
                        'raw': {
                            'type': 'keyword'
                        }
                    }
                },
                'description': {
                    'type': 'text',
                    'analyzer': 'ru_en'
                },
                'director': {
                    'type': 'nested',
                    'dynamic': 'strict',
                    'properties': {
                        'id': {
                            'type': 'keyword'
                        },
                        'name': {
                            'type': 'text',
                            'analyzer': 'ru_en'
                        }
                    }
                },
                'directors_names': {
                    'type': 'text',
                    'analyzer': 'ru_en'
                },
                'actors_names': {
                    'type': 'text',
                    'analyzer': 'ru_en'
                },
                'writers_names': {
                    'type': 'text',
                    'analyzer': 'ru_en'
                },
                'actors': {
                    'type': 'nested',
                    'dynamic': 'strict',
                    'properties': {
                        'id': {
                            'type': 'keyword'
                        },
                        'name': {
                            'type': 'text',
                            'analyzer': 'ru_en'
                        }
                    }
                },
                'writers': {
                    'type': 'nested',
                    'dynamic': 'strict',
                    'properties': {
                        'id': {
                            'type': 'keyword'
                        },
                        'name': {
                            'type': 'text',
                            'analyzer': 'ru_en'
                        }
                    }
                }
            }
        }
    }

    data = [
        {
            'id': '4af6c9c9-0be0-4864-b1e9-7f87dd59ee1f',
            'title': 'Star Trek',
            'description': "On the day of James Kirk's birth, his father dies on his damaged",
            'imdb_rating': 7.9,
            'creation_date': None,
            'genre': [{'id': '120a21cf-9097-479e-904a-13dd7198c1dd', 'name': 'Adventure'},
                      {'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff', 'name': 'Action'}],
            'actors': [{'id': '5b4bf1bc-3397-4e83-9b17-8b10c6544ed1', 'name': 'Harrison Ford'}],
            'director': [{'id': 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a', 'name': 'George Lucas'}],
            'writers': [{'id': 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a', 'name': 'George Lucas'},
                        {'id': '5b4bf1bc-3397-4e83-9b17-8b10c6544ed2', 'name': 'Immanuel Cant'}],
            'directors_names': ['George Lucas'],
            'actors_names': ['Harrison Ford'],
            'writers_names': ['George Lucas'],
            'genres_names': ['Adventure']
        },
        {
            'id': '3d825f60-9fff-4dfe-b294-1a45fa1e115d',
            'title': 'Star Wars: Episode IV - A New Hope',
            'description': 'The Imperial Forces,',
            'imdb_rating': 8.6,
            'creation_date': None,
            'genre': [{'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff', 'name': 'Action'}],
            'actors': [{'id': 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a', 'name': 'George Lucas'},
                       {'id': '5b4bf1bc-3397-4e83-9b17-8b10c6544ed1', 'name': 'Harrison Ford'}],
            'director': [{'id': '5b4bf1bc-3397-4e83-9b17-8b10c6544ed9', 'name': 'Cant Immanuel'}],
            'writers': [{'id': '5b4bf1bc-3397-4e83-9b17-8b10c6544ed2', 'name': 'Immanuel Cant'}],
            'directors_names': ['Cant Immanuel'],
            'actors_names': ['George Lucas', 'Harrison Ford'],
            'writers_names': ['Immanuel Cant'],
            'genres_names': []
        }
    ]

    @classmethod
    def _get_data_copy(cls):
        return copy.deepcopy(cls.data)

    @classmethod
    def expected(cls) -> list:
        expected_data = list()
        replaced_keys = ['actors', 'director', 'writers']
        keys_repr = ['uuid', 'title', 'description', 'imdb_rating', 'genre', 'actors', 'directors', 'writers']
        data = cls._get_data_copy()
        for item in data:
            for key in item:
                if key == 'genre':
                    for genre in item['genre']:
                        genre['uuid'] = genre.pop('id')
                if key in replaced_keys:
                    for person in item[key]:
                        person['uuid'] = person.pop('id', None)
                        person['full_name'] = person.pop('name', None)
            if 'director' in item:
                item['directors'] = item.pop('director')
            new_item = {key: item[key] for key in item.keys() if key in keys_repr}
            new_item['uuid'] = item['id']
            expected_data.append(new_item)
        return expected_data

    @classmethod
    def expected_short(cls):
        expected_data = list()
        data = cls._get_data_copy()
        for item in data:
            new_item = dict()
            new_item['uuid'] = item['id']
            new_item['title'] = item['title']
            new_item['imdb_rating'] = item['imdb_rating']
            expected_data.append(new_item)
        return expected_data

    @classmethod
    @property
    def genres(cls):
        data = cls._get_data_copy()
        genres = list()
        for item in data:
            genres.extend([elem['id'] for elem in item['genre'] if 'id' in elem])
        uniq = list(set(genres))
        count = [genres.count(i) for i in uniq]
        return zip(uniq, count)
