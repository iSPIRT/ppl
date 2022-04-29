# WARNING: Obsolete. This code is not consistent with the
# latest thinking. See badal/dsl/README.md for the
# latest thinking

from __future__ import annotations

from typing import Any, TypeGuard

from badal.schema.attribute_types import AttributeType, Visibility

class Attribute:
    uri: str = ''
    id: str = ''
    name: str = ''

    def __init__(self,
                 required: bool = False,
                 visibility: Visibility = Visibility.Private,
                 **kwargs):
        self.attribute_type = AttributeType(
            self.uri, self.id, self.name, visibility)

    def add_to_statemeta(self, cls, name: str) -> None:
        '''Register attribute with `name` on the `cls`'''
        self.name = name
        self.state_class = cls
        cls._meta.add_attribute(name, self)

    def to_python_obj(self):
        '''return in-memory representation of this attribute value 

        i.e. return a Python object this value
        '''
        ...

    def to_json(self) -> str:
        ...


def is_attribute(attr_value: Any) -> TypeGuard[Attribute]:
    '''Check if attr_value is an Attribute

    Note: in Django, the similar check isn't isinstance(a, Field)
    They do it using hasattr(v, 'contribute_to_class').
    We could have done hasattr(v, 'add_to_statemeta') which is 
    technically more pythonic, but I think that would unnecessarily 
    add complexity to already complex code
    '''
    return isinstance(attr_value, Attribute)


class State:
    

    ...
    

class ZKPSystem:
    def 



class Claim:
    '''A claim represents a guarantee regarding a transaction 
    and is specified via code in the ZKP language being used

    Conceptually: A claim is the compile time information describing
    what needs to be proved. At runtime a claim accesses the actual
    (private) data of the transaction to produce a proof.

    Actually, what happens is this: At compile time, the code for the 
    claim gets included in the ZKP program associated with the 
    transaction. Thus, the ZKP program consists of: 1. some 
    initialization code to take the private and public inputs
    and put them in a common structure that the other parts of
    the proof can access, 2. the code for each of the claims in
    the transaction which will access the common data from #1, 
    3. code for claims that are common to all transactions 
    (for example, computing the hashes of all the input and 
    output states and asserting that they match the corresponding
    public hashes on the ledger), and 4. a "main program" which
    calls all this code.


    Thus, at runtime, when the ZKP program is executed to produce
    the proof, automatically the code for every claim gets executed
    and thus the proof proves all the claims in the transaction.
    '''
    ...


class Proof:
    '''A proof is the output of running the ZKP program.

    For more details see the comment at Claim
    '''
    ...


class ZokratesClaim(Claim):
    Array: type
    MultiArray: type
    ...


class StateHashesMatchClaim(ZokratesClaim):
    function_name = 'state_hashes_match'
    code = '''
    def state_hashes_match(TxnBinary<M,N> txn_binary, 
                           field[2][N] input_hashes,
                           field[2][M] output_hashes):
      for u32 i in 0..N do
        ppl_signature(txn_binary.state[i])    
      endfor
    '''


class ZokratesProof(Proof):
    ...


class Signature:
    ...


class Transaction:
    '''
    Every transaction has a list of input states (which will be caceled), 
    a list of output states (which are being created), and a 
    list of claims (for which proofs need to be submitted)

    In addition to the listed claims, every transaction has an implict 
    '''
    ...
    inputs: list[State]
    outputs: list[State]

    claims: tuple[Claim]
    signatures: list[Signature]

    def create_txn_binary_type(self):
        '''
        Create transaction binary datatype

        For example, for Zokrates, this creates the TxnBinary struct
        '''

    def create_txn_binary(self):
        '''
        Creates transaction binary data which can be passed to
        the individual proof functions
        '''

    def create_ZKP_program(self):
        '''
        Create the ZKP program corresponding to this transaction type

        This is a compile time operation
        
        This creates the following pieces:
        1. Defines the "type" (if any) for the whole transaction type.
           This could involve defining the types for each
           individual state type.
        2. Create the function which takes all the state data items
           and initializes an instance of the transaction type. This
           could invilve defining the init functions for each state
           type
        3. Create the functions for each claim of this transaction
        4. Create the main function which takes all the inputs
           and calls the functions in #2 and #3
        '''
        ...

    

    ...


class Action:
    ...


class Spec:
    uri: str
    name: str
    version: str 
    contract_model: str
    proof_model: str = 'Zokrates'
    depends_upon: list[Spec] = []
    
    attributes = list[Attribute]
    transactions = list[Transaction]
    # attrs, states, transactions, actions
    
