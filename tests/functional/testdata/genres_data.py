import uuid


class Genre:
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
                    "type": "keyword"
                },
                "description": {
                    "type": "text",
                    "analyzer": "ru_en"
                }
            }
        }
    }
    names = ['Arcada', 'Adult only', 'Киношка', 'Крутой фильмак']
    data = [{'id': str(uuid.uuid4()), 'name': name, 'description': name} for name in names]
    expected = [{'uuid': item['id'], 'name': item['name']} for item in data]
