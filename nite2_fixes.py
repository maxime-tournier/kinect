
# monkey-patching yo !
import ctypes

# patch for nite library missing symbols
orig = ctypes.CDLL.__getattr__
def patch(self, name):
    try:
        return orig(self, name)
    except:
        print 'warning, symbol not found:', name
        return ctypes.CFUNCTYPE(None)
ctypes.CDLL.__getattr__ = patch

# disable strongly-typed enums since they cause errors with &
from primesense import utils
del utils.CEnumMeta.__new__

