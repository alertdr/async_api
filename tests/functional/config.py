import os

API_DOMAIN = os.getenv('API_DOMAIN', '127.0.0.1')
API_PORT = os.getenv('API_PORT', 8000)

API_URL = f'http://{API_DOMAIN}:{API_PORT}'
ELASTIC_HOST = os.getenv('ELASTIC_HOST', '127.0.0.1')

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'
