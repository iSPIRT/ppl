import sys
from pysnark.runtime import snark

@snark
def cube(x):
    return x*x*x

print("The cube of", sys.argv[1], "is", cube(int(sys.argv[1])))


