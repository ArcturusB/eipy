#!/usr/bin/env python3

import eipy

print('before')
try:
    foo = 'foo'
    raise Exception
except Exception:
    eipy.sh()
print('between')
try:
    bar = 'bar'
    raise Exception
except Exception:
    eipy.sh()
print('after')
