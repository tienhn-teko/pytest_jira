# coding=utf-8
import json


def json_dump(obj, **kwargs):
    try:
        return json.dumps(obj, ensure_ascii=False, **kwargs)
    except:
        return str(obj)
