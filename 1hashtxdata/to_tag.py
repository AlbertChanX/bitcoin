from timetools import get_time

with open('tag.py', 'a') as f:
    f.write('#updatetime: %s \n' % get_time())
