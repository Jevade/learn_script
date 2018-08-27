import numpy as np
print np.arange(12)
a=np.array(np.arange(12),dtype=np.float)
b=a.reshape(3,4)
print b*a.reshape(3,4)
