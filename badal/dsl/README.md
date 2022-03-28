# The Badal DSL

_This is an early-stage, incomplete, and unreviewed draft. Anything can change at any time_

## Introduction

The idea of Badal.DSL is to provide users with a high-level language to specify schemas. This not only would make it easy for use to quickly implement different scehmas for demos and PoCs, but more importantly, it would make it easier for someone to understand schemas in Badal by abstracting away the low-level details in badal.schema and allowing them to focus on the high-level concepts and "business logic"

The "DSL" is really just a set of Python classes which use metaprogramming to generate/call the underlying badal.schema code based on a high-level description provided via the classes and attributes of the DSL. This is similar to the way Django ORM abstracts away the low-level RDBMS code by using the `Model` class and related classes.

## Core DSL Classes

The DSL is primarily based on these classes: Attribute, State, Claim, Proof, Transaction, and Schema.

The Attribute and State classes abstract away the details of `add_attribute_type` and `add_state_type` from `badal.schema`. Here is an example of a `State` definition using the DSL (with only a few important fields shown):

    :::python
    class Utxo(dsl.State):
        owner_id = dsl.PublicID(scheme='g16')
        amount = dsl.Amount(uom='inr', precision=3)

This code will result in two `add_attribute_type` calls and one `add_state_type` call.

The `Claim` class allows the specification of ZKP code that needs to be incorporated in the proof for the transaction. All the claims of a transaction together should guarantee that the transaction is valid.

The `TransactionCore` dataclass contains fields specifying the input state types and output state types for this transaction.

    :::python
    @dataclass
    class TransferCore(dsl.TransactionCore):
        inputs = dsl.Array(Utxo, type="input", max_length=2)
        outputs = dsl.Array(Utxo, type="output", max_length=2)
        # note: these are only input and output states
        # no other fields are allowed in a TransactionCore
       
The `Transaction` class puts it all together by extending the `TransactionCore` by adding a more fields (specifically, the fields that are not incorporated in the signatures) and methods. Here is an example of a `Transaction` definition (with only a few important fields shown):

    :::python
    class Transfer(TransferCore, dsl.Transaction):
        # inherits the data members of TransferCore
        claims = (AmountsMatchClaim, UtxoTypesMatchClaim)
        signatures: list[Signature]
        input_hashes: list[StateHash]
        output_hashes: list[StateHash]
        proof: Proof

One important function of these classes is to automatically create code in the chosen ZKP language (_e.g._ Zokrates or circom) to create appropriate data-structures for each attribute type, for each state type, and for the transaction core. They also create functions to initialize and manipulate these data-structures. For example, when using Zokrates, this would result in the creation of `struct owner_id_t`, `struct amount_t`, `struct utxo_t`, and `struct transfer_core_t`, along with functions `init_owner_id`, `init_amount`, `init_utxo`, and `init_transfer_core`.

## Details of `State`

A state has the following important properties:

- method: `hash() -> StateHash` returns a collision-resistant hash and
  preimage resistant hash of the contents of the state
- TODO: we need a mechanism to ensure that no two states can result in
  the same `StateHash`. Because of the properties of the hash function
  this can only happen if all the values of the attributes in the state
  are the same as that of another state.
  - Note: This can be easily guaranteed by embedding a GUID in
    each state. However, we need to be careful with stuffing
    data members in states because each extra byte in the state
    increases the cost of ZKP generation
  - Does each state contain a timestamp? Is it absolutely necessary?
  - What is the smallest nonce we can include in a state to guarantee
    uniqueness?

## Details of `Transaction`

At the wallet provider, the Transaction class has the following metadata:

- TransactionCore: All the fields from the transaction core, which includes:
  - input fields: A one or more fields representing the input state
    types. In the example above, there is just one field `inputs` which
    has all the inputs because they are all of the same type (`Utxo`).
    However, it is possible to have multiple fields with different state
    values. Each represents a state being canceled.
  - output fields: Similarly, one or more fields representing the `outputs`.
  - whether a state represents an input or an output is deduced from the
    type declaration
- claims: Tuple of names of classes representing the claims being made in this
  transaction. Each claim class will contribute code to the ZKP program
  for this transaction
- method: `get_signatories() -> list[PublicId]`
  - a method returning a list of `PublicId`s whose signatures are
    needed for the transaction to be valid.
  - TODO: the details of how this works needs to be worked out
- method: `get_zkp_program() -> str`
  - a method returning the (automatically generated) ZKP program
    corresponding to this transaction
  - See section `Proof` for details of what this ZKP program contains
  - the `proof` for a specific transaction instance will be the result
    of running this program with the private data of that transaction
- method: `get_transaction_core() -> TransactionCore`
  - returns an instance of the `TransactionCore` populated with the
    actual input and output state instances. This is what is signed by
    the signatories for validating a transaction and this is what is
    sent to the ZKP program
  - TODO: it should return `TransferCore` not `TransactionCore`
    Need to doublecheck that this doesn't cause any problems.
- method: `get_zkp_program_inputs() -> list[str]`
  - a method returning the commandline arguments to be provided to the
    `get_zkp_program()`
    - Question: should this be json instead of `list[str]`?
  - At a minimum, this includes the `transaction_core` and `signatures`
    `input_hashes` and `output_hashes`

## Details of `Signature`

The `get_signatories` method has the following properties:

- The `get_signatories` method creates a list of `PublicId`s whose
  signatures are needed for a transaction to be valid.
  - Optimization: remove duplicates from this list
- All the `signatories` will only come from the `inputs`. The `outputs` do
  not contribute to the `signatories`.
- Each `input` state might contribute 0, 1, or more `PublicId`s to the
  list. It is possible that two different states have the same owner
  so they contribute only one unique `PublicId`. It is possible that some
  state might contribute two or more.
  - TODO: We should extend this to allow more complex things like
    2-of-3 signatures

The `signatures` list has the following properties:

- The `proof` will assert that the number of signatures is same as the
  number of signatories
- The `proof` will also assert that
  `signature[i] == sign(transaction_core, self.get_signatories()[i])`
- All signatures will have to be provided externally. Badal.DSL
  does not have a way of creating the signature of the transaction.
  Typically, Badal code will output the `transaction_core` and
  the `get_signatories()` list. The user has to generate the corresponding
  signatures and input them into the system. This is because, for
  safety, we will assume that Badal code never stores the private key
  for any signatures.

  The wallet provider will usually have methods to save private keys
  and sign transactions, but for now we'll assume that is a separate
  library.
  - For now, we're assuming that it is the job of the transaction
    submitting wallet provider to collect all the signatures via
    out-of-band methods

## Details of `Proof`

The ZKP program auto-generated for a transaction class has the
following components in it:

### Code common to all transactions:

- compute the `StateHash` for each input and and assert that it is
  equal to the corresponding `input_hashes[i]`.
- do the same for `output_hashes`  
- assert that `get_signatories()` was computed properly
  - TODO: Details of this need to be worked out
- for each signatory: compute `sign(transaction_core, signatories[i])`
  and assert that this is equal to `signatures[i]`
- assertions related to the chaining pointers if necessary (see
  comment at Notary)

### Code specific to this transaction type:

- Code for each `Claim` in the transaction
  - each claim gets the `transaction_core` as input
    and the `Claim` definition contains the code to
    extract the relevant information from the `transaction_core`
    and assert the appropriate constraint

## Notary

At the notary, one a transaction has the following data:

- inputs: `list[StateHash]` corresponding to states being canceled
  - Note: Currently assuming that a `StateHash` will always be unique.
    See discussion under `State` for more details of this.
- outputs: `list[StateHash]` corresponding to states being created
- TODO: chaining pointers: 
  - Additionally, the transaction on the ledger probably needs
    to include state hashes of earlier states or hashes of earlier
    transactions for chaining purposes. The chaining would help
    maintain integrity of the ledger. The details of this need to
    be worked out.
  - TODO: Figure out whether the chaining is done by the wallet provider
    or the notary or both
- proof

The notary does the following:

- Confirm that `inputs` represent active states on the ledger
  - this means confirming that each input exists in the `outputs`
    of one and only one of the previous transactions
- Confirm that `outputs` represents new states
  - this means confirming that none of the outputs exist in
    the inputs or outputs of any of the previous transactions
- Verify the proof

The transaction is appended to the ledger 
