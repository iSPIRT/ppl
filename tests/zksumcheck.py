import sys
from pysnark.runtime import snark, PubVal,PrivVal, for_each_in
from pysnark.hash import ggh_hash, int_to_bits

@snark
def sumcheck(x,p_1,p_2):
    x.assert_le(p_1+p_2 )


if len(sys.argv) >= 4:
    claim = int(sys.argv[1])
    first = int(sys.argv[2])
    second= int(sys.argv[3])
    public_claim = PubVal(claim)
    private_first = PrivVal(first)
    private_second= PrivVal(second)
    sumcheck(public_claim,private_first,private_second)
else:
    claim = 100 
    first = 23
    second= 77
    public_claim = PubVal(claim)
    private_first = PrivVal(first)
    private_second= PrivVal(second)
    sumcheck(public_claim,private_first,private_second)



