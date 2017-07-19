import json

def get_json():
    js = dict()
    flag = True
    for i in range(10000000):
        key = 'key%s' %i
        js.setdefault(key, i)
        # if len(json.dumps(js).encode('utf-8')) > 1024*1024:
        #     break
    return js
print(get_json())