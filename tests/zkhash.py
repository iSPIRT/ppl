import sys
from pysnark.runtime import snark, PrivVal, for_each_in
from pysnark.hash import ggh_hash, int_to_bits

# Run as python zkhash.py public_hash private_input

# The computation
@snark
def check_hash(public_hash, private_input):
    ggh_hash(private_input).assert_eq(public_hash)


# Supporting calculations

# Provide default values for the inputs just for
# convenience of running this from the command line

default_hash = 12159113912127441302481669165612839028677601711152277646610726095099155477934
the_ultimate_answer = 42

if len(sys.argv) >= 2:
    output_hash = int(sys.argv[1])
else:
    output_hash = default_hash

if len(sys.argv) >= 3:
    input_int = int(sys.argv[2])
else:
    input_int = the_ultimate_answer

# Convert the second input to a private input
private_input = [PrivVal(x) for x in int_to_bits(input_int)]

check_hash(output_hash, private_input)
