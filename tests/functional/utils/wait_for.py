import logging
import os

from elasticsearch import Elasticsearch
from redis import Redis

from backoff import backoff


@backoff()
def wait_for_es():
    es = Elasticsearch(os.getenv('ELASTIC_HOST'))
    if es.ping():
        logging.info('Elasticsearch is ready')
    else:
        raise ConnectionError('Elasticsearch')


@backoff()
def wait_for_redis():
    redis = Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))
    if redis.ping():
        logging.info('Redis is ready')


if __name__ == '__main__':
    wait_for_es()
    wait_for_redis()
