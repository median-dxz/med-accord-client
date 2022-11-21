import os
from hashlib import md5

from accord_client import baseDir

CachePath = os.path.join(baseDir, "cache")


def store_to_cache(byteData: bytes, key: str):
    with open(os.path.join(CachePath, key), "wb") as f:
        f.write(byteData)


def get_from_cache(data: bytes):
    key = md5(data).digest().hex()
    if not contain(key):
        store_to_cache(data, key)
    return os.path.join(CachePath, key)


def contain(key) -> bool:
    file_list = os.listdir(CachePath)
    return file_list.count(key) > 0
