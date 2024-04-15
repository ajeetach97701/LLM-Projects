import redis 
import os, json
from dotenv import load_dotenv

REDIS_SERVER = "localhost"

cache = redis.Redis(REDIS_SERVER)

def setData(request_id, request_data):
    value = json.dumps(request_data)
    cache.set(request_data, value)
    cache.expire(request_id, 60*60*8)
    
def getData(request_id):
    value = cache.get(request_id)
    if value is not None:
        return json.loads(value)
    return None

def deleteData(request_id):
    cache.delete(request_id)
    
def flushAll():
    cache.flushall()