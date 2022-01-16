import gc, sys

del globals()['bdev']
del sys.modules['flashbdev']

config = getattr(getattr(__import__('yuri.sys_config'), 'sys_config'), 'config')

print(str(globals()))
print()
print(str(sys.modules))