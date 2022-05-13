movies_mapping = {
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

single_film = {
    '_index': 'movies', '_id': '3d825f60-9fff-4dfe-b294-1a45fa1e115d',
    '_source': {
        'id': '3d825f60-9fff-4dfe-b294-1a45fa1e115d', 'title': 'Star Wars: Episode IV - A New Hope',
        'description': 'The Imperial Forces, under orders from cruel Darth Vader, hold Princess Leia hostage in their efforts to quell the rebellion against the Galactic Empire. Luke Skywalker and Han Solo, captain of the Millennium Falcon, work together with the companionable droid duo R2-D2 and C-3PO to rescue the beautiful princess, help the Rebel Alliance and restore freedom and justice to the Galaxy.',
        'imdb_rating': 8.6, 'creation_date': None,
        'genre': [{'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff', 'name': 'Action'},
                  {'id': '120a21cf-9097-479e-904a-13dd7198c1dd', 'name': 'Adventure'},
                  {'id': 'b92ef010-5e4c-4fd0-99d6-41b6456272cd', 'name': 'Fantasy'},
                  {'id': '6c162475-c7ed-4461-9184-001ef3d9f26e', 'name': 'Sci-Fi'}],
        'actors': [{'id': 'b5d2b63a-ed1f-4e46-8320-cf52a32be358', 'name': 'Carrie Fisher'},
                   {'id': '5b4bf1bc-3397-4e83-9b17-8b10c6544ed1', 'name': 'Harrison Ford'},
                   {'id': '26e83050-29ef-4163-a99d-b546cac208f8', 'name': 'Mark Hamill'},
                   {'id': 'e039eedf-4daf-452a-bf92-a0085c68e156', 'name': 'Peter Cushing'}],
        'director': [{'id': 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a', 'name': 'George Lucas'}],
        'writers': [{'id': 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a', 'name': 'George Lucas'}],
        'directors_names': ['George Lucas'],
        'actors_names': ['Carrie Fisher', 'Harrison Ford', 'Mark Hamill', 'Peter Cushing'],
        'writers_names': ['George Lucas'],
        'genres_names': ['Action', 'Adventure', 'Fantasy', 'Sci-Fi']
    }
}
single_film2 = {
    '_index': 'movies', '_id': '0312ed51-8833-413f-bff5-0e139c11264a',
    '_source': {
        'id': '0312ed51-8833-413f-bff5-0e139c11264a',
        'title': 'Star Wars: Episode V - The Empire Strikes Back',
        'description': "Luke Skywalker, Han Solo, Princess Leia and Chewbacca face attack by the Imperial forces and its AT-AT walkers on the ice planet Hoth. While Han and Leia escape in the Millennium Falcon, Luke travels to Dagobah in search of Yoda. Only with the Jedi master's help will Luke survive when the dark side of the Force beckons him into the ultimate duel with Darth Vader.",
        'imdb_rating': 8.7, 'creation_date': None,
        'genre': [{'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff', 'name': 'Action'},
                  {'id': '120a21cf-9097-479e-904a-13dd7198c1dd', 'name': 'Adventure'},
                  {'id': 'b92ef010-5e4c-4fd0-99d6-41b6456272cd', 'name': 'Fantasy'},
                  {'id': '6c162475-c7ed-4461-9184-001ef3d9f26e', 'name': 'Sci-Fi'}],
        'actors': [{'id': 'efdd1787-8871-4aa9-b1d7-f68e55b913ed', 'name': 'Billy Dee Williams'},
                   {'id': 'b5d2b63a-ed1f-4e46-8320-cf52a32be358', 'name': 'Carrie Fisher'},
                   {'id': '5b4bf1bc-3397-4e83-9b17-8b10c6544ed1', 'name': 'Harrison Ford'},
                   {'id': '26e83050-29ef-4163-a99d-b546cac208f8', 'name': 'Mark Hamill'}],
        'director': [{'id': '1989ed1e-0c0b-4872-9dfb-f5ed13c764e2', 'name': 'Irvin Kershner'}],
        'writers': [{'id': 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a', 'name': 'George Lucas'},
                    {'id': '3217bc91-bcfc-44eb-a609-82d228115c50', 'name': 'Lawrence Kasdan'},
                    {'id': 'ed149438-4d76-45c9-861b-d3ed48ccbf0c', 'name': 'Leigh Brackett'}],
        'directors_names': ['Irvin Kershner'],
        'actors_names': ['Billy Dee Williams', 'Carrie Fisher', 'Harrison Ford', 'Mark Hamill'],
        'writers_names': ['George Lucas', 'Lawrence Kasdan', 'Leigh Brackett'],
        'genres_names': ['Action', 'Adventure', 'Fantasy', 'Sci-Fi']
    }
}

expected_films = [
    {"uuid": "3d825f60-9fff-4dfe-b294-1a45fa1e115d", "title": "Star Wars: Episode IV - A New Hope", "imdb_rating": 8.6},
    {"uuid": "0312ed51-8833-413f-bff5-0e139c11264a", "title": "Star Wars: Episode V - The Empire Strikes Back",
     "imdb_rating": 8.7}
]
