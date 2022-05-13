import os
from time import sleep

from elasticsearch import Elasticsearch
from redis import Redis


def wait_for_es():
    for i in range(1, 121):
        es = Elasticsearch(os.getenv('ELASTIC_HOST'))
        if es.ping():
            print('Elasticsearch is ready')
            return
        print(f'Waiting for elasticsearch > {i}s')
        sleep(1)
    else:
        exit(1)


def wait_for_redis():
    for i in range(1, 121):
        try:
            redis = Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))
            if redis.ping():
                print('Redis is ready')
                return
        except BaseException:
            print(f'Waiting for redis > {i}s')
        sleep(1)
    else:
        exit(1)


if __name__ == '__main__':
    wait_for_es()
    wait_for_redis()
