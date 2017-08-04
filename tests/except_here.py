#!/usr/bin/env python3

print('before')
try:
    foo = 'foo'
    raise Exception
except Exception:
    import eipy.here
print('after')
