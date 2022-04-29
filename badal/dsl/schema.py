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


class PublicId:
    ...


class RandomBits:
    '''For nonces'''
    ...


class StateMetaInfo:
    '''Stores meta information about a state subclass: like attributes etc'''
    def __init__(self) -> None:
        self.attributes: dict[str, 'Attribute'] = {}

    def add_attribute(self, name: str, attribute: 'Attribute') -> None:
        # Django uses a sorted list; I don't see why we shouldn't use a dict
        self.attributes[name] = attribute


class StateMetaclass(type):
    '''Metaclass for State

    Whenever we create a new class S derived from
    State, an S._meta = StateMetaInfo() is created
    and then all the attributes of S which are 
    instances of Attribute are actually added to
    S._meta.attributes 

    Later, when we create instances of S, the 
    contents of S.attributes will be used to decide
    how to convert the attribute values to and from json
    and to and from Zokrates data types and in general
    will know how to deal with the attribute values
    because the attribute type and the additional parameters
    (like precision) are stored in S.attributes

    TODO: In the long term, State should allow abstract and proxy 
    states for composability. 
    But, this can get surprisingly tricky, so probably better to do 
    this at a later stage.
    See: https://medium.com/swlh/how-django-use-data-descriptors-metaclasses-for-data-modelling-14b307280fce 
    for a discussion of what all Django has to handle while doing
    this
    '''
    def __new__(mcls, name, bases, attrs, **kwargs):
        # Don't do any special processing for State
        # We only want to do special processing for classes
        # derived from State.
        # parents will be empty only for State
        # All others will have at least State as a parent
        parents = [b for b in bases if isinstance(b, StateMetaclass)]
        if not parents:
            return super().__new__(mcls, name, bases, attrs)

        # Separate the special attributes (which have meta meaning)
        # from the regular attributes
        meta_attrs: dict[str, Attribute] = {}
        regular_attrs: dict[str, object] = {}

        for obj_name, obj in attrs.items():
            if is_attribute(obj):
                meta_attrs[obj_name] = obj
            else:
                regular_attrs[obj_name] = obj

        new_class = super().__new__(mcls, name, bases, regular_attrs, **kwargs)
        new_class._meta = StateMetaInfo()

        for obj_name, obj in meta_attrs.items():
            obj.add_to_statemeta(new_class, obj_name)



class State(metaclass=StateMetaclass):
    # See `class Utxo` in README.md for example of how to use this
    owner: PublicId
    nonce: RandomBits
    ...


class ZKPSystem:
   ...


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
    See `class Transfer` in README.md for an example of how to use this
    '''
    creator: PublicId
    signatures: list[Signature]
    proof: Proof
    # inputs, outputs, claims to be defined by subclass
    
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
    
