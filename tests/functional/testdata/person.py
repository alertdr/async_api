single_person = {
    '_index': 'persons', '_id': 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a',
    '_source': {
        'id': 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a', 'name': 'George Lucas',
        'roles': ['actor', 'director', 'writer'],
        'films_as_actor': [
            '19babc93-62f5-481a-b6fe-9ebfef689cbc',
            '3a28f10a-433e-431c-8e7b-cc3f90af5a41',
            '3b1d0e70-42e5-4c9b-98cf-2681c420a99b',
            '3ba6c11a-0db6-4144-bc9d-c7e04b817dd2',
            '943946ed-4a2b-4c71-8e0b-a58a11bd1323',
            'dc2dbf5d-de5d-4153-a049-51ba44f15e04'
        ],
        'films_as_director': [
            '3b914679-1f5e-4cbd-8044-d13d35d5236c',
            '3d825f60-9fff-4dfe-b294-1a45fa1e115d',
            '516f91da-bd70-4351-ba6d-25e16b7713b7',
            'c4c5e3de-c0c9-4091-b242-ceb331004dfd',
            'f241a62c-2157-432a-bbeb-9c579c8bc18b'
        ],
        'films_as_writer': [
            '025c58cd-1b7e-43be-9ffb-8571a613579b',
            '0312ed51-8833-413f-bff5-0e139c11264a',
            '0659e0e6-504e-4482-8aa9-f7530f36cae2',
            '07f8bdbe-5246-4dfc-8d38-85043aeb307b',
            '118fd71b-93cd-4de5-95a4-e1485edad30e',
            '12a8279d-d851-4eb9-9d64-d690455277cc',
            '134989c3-3b20-4ae7-8092-3e8ad2333d59',
            '3b914679-1f5e-4cbd-8044-d13d35d5236c',
            '3cb639db-cd8a-48b0-90e3-9def109a4492',
            '3d825f60-9fff-4dfe-b294-1a45fa1e115d',
            '46f15353-2add-415d-9782-fa9c5b8083d5',
            '48495445-f04d-4d4c-9249-1faa28fc64eb',
            '4f53452f-a402-4a76-89fd-f034eeb8d657',
            '516f91da-bd70-4351-ba6d-25e16b7713b7',
            '57beb3fd-b1c9-4f8a-9c06-2da13f95251c',
            '5c612da0-9c15-48db-b46e-e6c82b071a9b',
            '5d62b55c-1ed5-4563-ae80-10c4baa21a36',
            '6313d0f5-e6a6-4071-a0c2-3d737fd1d56d',
            '64aa7000-698f-4332-b52f-9469e4d44ee1',
            '6cb927b3-4760-46c8-9002-ff4a47d57a4a',
            '73ecd1e6-6326-405a-b51b-69008f383b72',
            '75609cee-bc87-493d-8c1f-32c7e8ccc368',
            '88faa02d-f26f-40a1-9cc6-8045ed08d51e',
            '92dcddff-a70e-497c-92dc-0da12d1d528a',
            '983e0b41-dd17-4fd6-b4e7-771f975fdc19',
            '991d143e-1342-4f7c-abf0-a9ede3abba20',
            'a8f6bd5b-036a-4d79-b952-3c7b5aa3ea83',
            'b503ced6-fff1-493a-ad41-73449b55ffee',
            'c35dc09c-8ace-46be-8941-7e50b768ec33',
            'c4c5e3de-c0c9-4091-b242-ceb331004dfd',
            'c8f57f93-b02a-40d4-ba55-9600cceddd7e',
            'cd19b384-babd-4b0c-ba0a-5c272bcf0238',
            'cddf9b8f-27f9-4fe9-97cb-9e27d4fe3394',
            'd6a7409f-87cd-49d7-8803-951a7352c2ce',
            'daae47e4-cbd0-4ffd-a150-55201b357d5b',
            'dcab54f1-6958-4699-b3f5-2fb92c185b33',
            'e5a21648-59b1-4672-ac3b-867bcd64b6ea',
            'e99620fb-11bb-481b-8702-a14efa6bb0ef',
            'f241a62c-2157-432a-bbeb-9c579c8bc18b',
            'f553752e-71c7-4ea0-b780-41408516d0f4'
        ]
    }
}
single_person2 = {
    '_index': 'persons', '_id': '5b4bf1bc-3397-4e83-9b17-8b10c6544ed1',
    '_source': {
        'id': '5b4bf1bc-3397-4e83-9b17-8b10c6544ed1', 'name': 'Harrison Ford', 'roles': ['actor'],
        'films_as_actor': [
            '025c58cd-1b7e-43be-9ffb-8571a613579b', '0312ed51-8833-413f-bff5-0e139c11264a',
            '134989c3-3b20-4ae7-8092-3e8ad2333d59', '3b1d0e70-42e5-4c9b-98cf-2681c420a99b',
            '3d825f60-9fff-4dfe-b294-1a45fa1e115d', '4f53452f-a402-4a76-89fd-f034eeb8d657',
            'b6b8a3b7-1c12-45a8-9da7-4b20db8867df', 'c7bd11a4-30bf-4077-a618-97c3e5525427',
            'cddf9b8f-27f9-4fe9-97cb-9e27d4fe3394', 'dbb9b244-483b-4592-9194-4938338419bc',
            'f241a62c-2157-432a-bbeb-9c579c8bc18b'
        ], 'films_as_director': None,
        'films_as_writer': None}
}

expected_single_person = {
    "uuid": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a", "full_name": "George Lucas",
    "roles": ["actor", "director", "writer"],
    "actor_ids": [
        "19babc93-62f5-481a-b6fe-9ebfef689cbc", "3a28f10a-433e-431c-8e7b-cc3f90af5a41",
        "3b1d0e70-42e5-4c9b-98cf-2681c420a99b", "3ba6c11a-0db6-4144-bc9d-c7e04b817dd2",
        "943946ed-4a2b-4c71-8e0b-a58a11bd1323", "dc2dbf5d-de5d-4153-a049-51ba44f15e04"
    ],
    "writer_ids": [
        "025c58cd-1b7e-43be-9ffb-8571a613579b", "0312ed51-8833-413f-bff5-0e139c11264a",
        "0659e0e6-504e-4482-8aa9-f7530f36cae2", "07f8bdbe-5246-4dfc-8d38-85043aeb307b",
        "118fd71b-93cd-4de5-95a4-e1485edad30e", "12a8279d-d851-4eb9-9d64-d690455277cc",
        "134989c3-3b20-4ae7-8092-3e8ad2333d59", "3b914679-1f5e-4cbd-8044-d13d35d5236c",
        "3cb639db-cd8a-48b0-90e3-9def109a4492", "3d825f60-9fff-4dfe-b294-1a45fa1e115d",
        "46f15353-2add-415d-9782-fa9c5b8083d5", "48495445-f04d-4d4c-9249-1faa28fc64eb",
        "4f53452f-a402-4a76-89fd-f034eeb8d657", "516f91da-bd70-4351-ba6d-25e16b7713b7",
        "57beb3fd-b1c9-4f8a-9c06-2da13f95251c", "5c612da0-9c15-48db-b46e-e6c82b071a9b",
        "5d62b55c-1ed5-4563-ae80-10c4baa21a36", "6313d0f5-e6a6-4071-a0c2-3d737fd1d56d",
        "64aa7000-698f-4332-b52f-9469e4d44ee1", "6cb927b3-4760-46c8-9002-ff4a47d57a4a",
        "73ecd1e6-6326-405a-b51b-69008f383b72", "75609cee-bc87-493d-8c1f-32c7e8ccc368",
        "88faa02d-f26f-40a1-9cc6-8045ed08d51e", "92dcddff-a70e-497c-92dc-0da12d1d528a",
        "983e0b41-dd17-4fd6-b4e7-771f975fdc19", "991d143e-1342-4f7c-abf0-a9ede3abba20",
        "a8f6bd5b-036a-4d79-b952-3c7b5aa3ea83", "b503ced6-fff1-493a-ad41-73449b55ffee",
        "c35dc09c-8ace-46be-8941-7e50b768ec33", "c4c5e3de-c0c9-4091-b242-ceb331004dfd",
        "c8f57f93-b02a-40d4-ba55-9600cceddd7e", "cd19b384-babd-4b0c-ba0a-5c272bcf0238",
        "cddf9b8f-27f9-4fe9-97cb-9e27d4fe3394", "d6a7409f-87cd-49d7-8803-951a7352c2ce",
        "daae47e4-cbd0-4ffd-a150-55201b357d5b", "dcab54f1-6958-4699-b3f5-2fb92c185b33",
        "e5a21648-59b1-4672-ac3b-867bcd64b6ea", "e99620fb-11bb-481b-8702-a14efa6bb0ef",
        "f241a62c-2157-432a-bbeb-9c579c8bc18b",
        "f553752e-71c7-4ea0-b780-41408516d0f4"
    ],
    "director_ids": [
        "3b914679-1f5e-4cbd-8044-d13d35d5236c",
        "3d825f60-9fff-4dfe-b294-1a45fa1e115d",
        "516f91da-bd70-4351-ba6d-25e16b7713b7",
        "c4c5e3de-c0c9-4091-b242-ceb331004dfd",
        "f241a62c-2157-432a-bbeb-9c579c8bc18b"
    ]
}
expected_single_person2 = {
    "uuid": "5b4bf1bc-3397-4e83-9b17-8b10c6544ed1", "full_name": "Harrison Ford",
    "roles": ["actor"],
    "actor_ids": [
        "025c58cd-1b7e-43be-9ffb-8571a613579b", "0312ed51-8833-413f-bff5-0e139c11264a",
        "134989c3-3b20-4ae7-8092-3e8ad2333d59", "3b1d0e70-42e5-4c9b-98cf-2681c420a99b",
        "3d825f60-9fff-4dfe-b294-1a45fa1e115d", "4f53452f-a402-4a76-89fd-f034eeb8d657",
        "b6b8a3b7-1c12-45a8-9da7-4b20db8867df", "c7bd11a4-30bf-4077-a618-97c3e5525427",
        "cddf9b8f-27f9-4fe9-97cb-9e27d4fe3394", "dbb9b244-483b-4592-9194-4938338419bc",
        "f241a62c-2157-432a-bbeb-9c579c8bc18b"
    ]
}
expected_persons = [expected_single_person2, expected_single_person]
expected_cache = '{"id": "5b4bf1bc-3397-4e83-9b17-8b10c6544ed1", "name": "Harrison Ford", "roles": ["actor"], "films_as_actor": ["025c58cd-1b7e-43be-9ffb-8571a613579b", "0312ed51-8833-413f-bff5-0e139c11264a", "134989c3-3b20-4ae7-8092-3e8ad2333d59", "3b1d0e70-42e5-4c9b-98cf-2681c420a99b", "3d825f60-9fff-4dfe-b294-1a45fa1e115d", "4f53452f-a402-4a76-89fd-f034eeb8d657", "b6b8a3b7-1c12-45a8-9da7-4b20db8867df", "c7bd11a4-30bf-4077-a618-97c3e5525427", "cddf9b8f-27f9-4fe9-97cb-9e27d4fe3394", "dbb9b244-483b-4592-9194-4938338419bc", "f241a62c-2157-432a-bbeb-9c579c8bc18b"], "films_as_director": null, "films_as_writer": null}'
