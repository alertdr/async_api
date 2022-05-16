class Movies:
    mapping = {
        "mappings": {
            "properties": {
                "actors": {
                    "type": "nested",
                    "properties": {
                        "id": {
                            "type": "keyword"
                        }
                    }
                },
                "genre": {
                    "type": "nested",
                    "properties": {
                        "id": {
                            "type": "keyword"
                        },
                        "name": {
                            "type": "keyword"
                        }
                    }
                },
                "director": {
                    "type": "nested",
                    "properties": {
                        "id": {
                            "type": "keyword"
                        },
                        "name": {
                            "type": "text",
                        }
                    }
                },
                "writers": {
                    "type": "nested",
                    "properties": {
                        "id": {
                            "type": "keyword"
                        },
                        "name": {
                            "type": "text"
                        }
                    }
                }
            }
        }
    }
    film1 = {
        '_index': 'movies', '_id': '3d825f60-9fff-4dfe-b294-1a45fa1e115d',
        '_source': {
            'id': '3d825f60-9fff-4dfe-b294-1a45fa1e115d', 'title': 'Star Wars: Episode IV - A New Hope',
            'description': 'Test.',
            'imdb_rating': 8.6, 'creation_date': None,
            'genre': [{'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff', 'name': 'Action'}],
            'actors': [{'id': '5b4bf1bc-3397-4e83-9b17-8b10c6544ed1', 'name': 'Harrison Ford'}],
            'director': [{'id': 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a', 'name': 'George Lucas'}],
            'writers': [{'id': 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a', 'name': 'George Lucas'}],
            'directors_names': ['George Lucas'],
            'actors_names': ['Harrison Ford'],
            'writers_names': ['George Lucas'],
            'genres_names': ['Action']
        }
    }
    film2 = {
        '_index': 'movies', '_id': '0312ed51-8833-413f-bff5-0e139c11264a',
        '_source': {
            'id': '0312ed51-8833-413f-bff5-0e139c11264a',
            'title': 'Star Wars: Episode V - The Empire Strikes Back',
            'description': "Test.",
            'imdb_rating': 8.7, 'creation_date': None,
            'genre': [{'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff', 'name': 'Action'}],
            'actors': [{'id': '5b4bf1bc-3397-4e83-9b17-8b10c6544ed1', 'name': 'Harrison Ford'}],
            'writers': [{'id': 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a', 'name': 'George Lucas'}],
            'actors_names': ['Harrison Ford'],
            'writers_names': ['George Lucas'],
            'genres_names': ['Action']
        }
    }
    expected_films = [
        {"uuid": "3d825f60-9fff-4dfe-b294-1a45fa1e115d", "title": "Star Wars: Episode IV - A New Hope", "imdb_rating": 8.6},
        {"uuid": "0312ed51-8833-413f-bff5-0e139c11264a", "title": "Star Wars: Episode V - The Empire Strikes Back",
         "imdb_rating": 8.7}
    ]
