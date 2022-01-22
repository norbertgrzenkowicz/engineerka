import numpy as np


a = np.matrix('0; 1')
b = np.matrix('9 8')

ans = a*b

c = np.matrix('0 1; -3 -5')
d = np.matrix('0; 1')

ans = c*d

print(a*b)
print(" ")
print(ans)