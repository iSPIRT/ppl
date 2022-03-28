# WARNING: Obsolete. This code is not consistent with the
# latest thinking. See badal/dsl/README.md for the
# latest thinking


from ppl.badal.dsl import spec as s

class PublicId(s.Attribute):
    '''
    Automatically generates:
    - In badal.schema: Appropriate AttributeType subclass
    - In ZKP: struct for this attribute type and methods
              to initialize and otherwise manipulate this
              attribute 
    '''
    pass


class Amount(s.Attribute):
    def __init__(self, uom: str, precision: int = 2, **kwargs):
        ...

class Notes(s.Attribute):
    pass


class Utxo(s.State):
    '''
    Automatically generates:
    - In badal.schema: Appropriate StateType subclass
                       Also, code to automatically convert
                       from Python native data types to 
                       the correct AttributeType.
                       Thus: `utxo.amount = 42` should work fine
    - In ZKP: struct for this state and functions to manipulate them
              function to generate ID of this state?
              function to hash this state
    '''
    owner_id = PublicId()
    amount = Amount(uom='inr', precision=3)

    def __init__(self,
                 from_id: str|PublicId,
                 to_id: str|PublicId,
                 amount: int|Amount):
        self.amount = amount
        self.from_id = from_id
        self.to_id = to_id


class AmountsMatchClaim(s.ZokratesClaim):
    '''
    Check that the sum of input amounts matches the sum of output amounts

    Each input is a tuple of (param_name, expression)

    The param_name must match one of the parameters of the
    function in the code

    The expression must be a valid expression for extracting an 
    appropriate Zokrates type from one of the states of the transaction

    TODO: N and M: how are they specified/fixed?
          Does this automatically fix the size of transaction_content?
    '''
    function_name = 'amounts_match'
    code='''
    def amounts_match(TxnBinary<M,N> txn_binary):
      u64 input_sum = 0
      for u32 i in 0..N do
        input_sum = input_sum + txn_binary.inputs[i].amount.value
      endfor

      u64 output_sum = 0
      for u32 j in 0..M do
        output_sum = output_sum + txn_binary.outputs[j].amount.value
      endfor

      assert(input_sum == output_sum)
    '''


class UOMsMatchClaim(s.ZokratesClaim):
    '''Checks that all UOMs in the transaction are the same'''
    function_name = 'uoms_match'
    code='''
    def uoms_match(TxnBinary<M,N> txn_binary):
      u32 first_uom = txn_binary.inputs[0].amount.uom
      
      for u32 i in 1..N do
        assert(first_uom == txn_binary.inputs[i].amount.uom)
      endfor

      for u32 j in 0..M do
        assert(first_uom == txn_binary.outputs[j].amount.uom)
      endfor
    '''


class ValidSignaturesClaim(s.ZokratesClaim):
    '''
    Check that the signatures are valid, and the necessary ones are there
    '''
    @s.ZokratesClaim.input
    def input_public_ids(self,
                         txn: s.Transaction) -> s.ZokratesClaim.Array:
        return self.to_array([self.to_field(input.to_id)
                              for input in txn.inputs])

    @s.ZokratesClaim.input
    def content(self,
                txn: s.Transaction) -> s.ZokratesClaim.Array:
        '''Convert the core transaction data into an array of fields

        This "content" is what is going to be "signed" by all the
        existing owners of the input IOUs

        TODO: How do we handle "size"?
        '''
        return self.to_array(
            [self.to_field()]
        )

    @s.ZokratesClaim.input
    def signatures(self,
                   txn: s.Transaction) -> s.ZokratesClaim.MultiArray:
        return self.to_multi_array(
            [self.to_field(sig for sig in txn.signatures)],
            shape=(2, len(txn.signatures))
        )

    code='''
    def valid_signatures(field[N] input_public_ids, 
                         field[?] transaction_content,
                         field[2][N] signatures):
      for u32 i in 0..N do
         field[2] sig = ppl_signature(transaction_content, input_public_ids[i])
         ppl_signature_check(sig, signatures[i])
      endfor
    '''


class Transfer(s.Transaction):
    '''Payment cancelling multiple IOUs and creating multiple new ones'''
    claims = (AmountsMatchClaim, UtxoTypesMatchClaim, ValidSignaturesClaim)

    def __init__(self,
                 inputs: list[Utxo],  
                 outputs: list[Utxo]) -> None:
        self.inputs = inputs
        self.outputs = outputs
        self.signatures: list[s.Signature] = []

    def sign(self, signatures: list[s.Signature]) -> None:
        self.signatures = signatures
        # We probably want to check the signatures in python
        # first before creating the proof
        # That would be far more efficient

    def create_proof(self) -> s.Proof:
        return ''


class StableINR(s.Spec):
    uri = 'http://ispirt.org/stableinr/spec'
    name = 'INR StableCoin Spec'
    version = '0.1'
    contract_model = 'zokrates_one_oh'
    signature_type = ''

    attributes = [PublicId, Amount, Notes]
    states = [Utxo,]
    transactions = [Transfer,]
    actions: list[s.Action] = []
    
    
