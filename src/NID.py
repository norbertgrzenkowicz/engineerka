
import math


 
r1 =  math.exp(-pow(10, -5)*8670) * math.exp(-pow(10, -6)*8670) * math.exp(-pow(10, -5)*8670 * 5) * math.exp(-pow(10, -6)*8670 * 5)
r2 = math.exp(-pow(10, -4)*8670) * math.exp(-pow(10, -5)*8670 * 3)
r3 =  math.exp(pow(10, -5)* 8670 * -2.08)

qs1 = (1-r1)*(1-r2)

rs1 = 1 - qs1

rs =  r3*rs1
qs = 1 - rs

print(rs, qs)
print(qs1, rs1, r1, r2, r3)