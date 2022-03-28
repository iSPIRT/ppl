# The Badal DSL

_This is an early-stage, incomplete, and unreviewed draft. Anything can change at any time_

## Introduction

The idea of Badal.DSL is to provide users with a high-level language
to specify schemas. This not only would make it easy for use to
quickly implement different scehmas for demos and PoCs, but more
importantly, it would make it easier for someone to understand schemas
in Badal by abstracting away the low-level details in badal.schema and
allowing them to focus on the high-level concepts and "business logic"

The "DSL" is really just a set of Python classes which use
metaprogramming to generate/call the underlying badal.schema code
based on a high-level description provided via the classes and
attributes of the DSL. This is similar to the way Django ORM abstracts
away the low-level RDBMS code by using the `Model` class and related
classes.

## Core DSL Classes

The DSL is primarily based on these classes: Attribute, State, Claim, Proof, Transaction, and Schema.

The Attribute and State classes abstract away the details of
`add_attribute_type` and `add_state_type` from `badal.schema`. Here is
an example of a `State` definition using the DSL (with only a few
important data-members shown):

    :::python
    class Utxo(dsl.State):
        owner_id = dsl.PublicID(scheme='g16')
        amount = dsl.Amount(uom='inr', precision=3)

This code will result in two `add_attribute_type` calls and one
`add_state_type` call.

The `Claim` class allows the specification of ZKP code that needs to
be incorporated in the proof for the transaction. All the claims of a
transaction together should guarantee that the transaction is valid.

The `TransactionCore` dataclass contains data-members specifying the
input state types and output state types for this transaction.

    :::python
    @dataclass
    class TransferCore(dsl.TransactionCore):
        inputs = dsl.Array(Utxo, type="input", max_length=2)
        outputs = dsl.Array(Utxo, type="output", max_length=2)
        # note: these are only input and output states
        # no other attributes are allowed in a TransactionCore
       
The `Transaction` class puts it all together by extending the
`TransactionCore` by adding a more data-members (specifically, the
data-members that are not incorporated in the signatures) and methods.
Here is an example of a `Transaction` definition (with only a few
important data-members shown):

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

- method: `hash() -> StateHash` returns a hash of the contents of the state
  - The hash function used will be collision resistant, preimage
    resistant, and second preimage resistant

- method: `owners() -> list[PublicId]`
  - This method returns a list of values of attributes in this state
    that represent _owners_ of this state. The signatures of all of these
    are required for a transaction to be able to cancel this state.
    - Note: every state must have at least one owner
    - Note: there can be more than one owners
    - TODO: we should also allow k-of-n ownership, but the details of
      how to do that need to be worked out
    - Note: It is not necessary that all the `PublicId` attributes in a state
      are owners. Specifying `non_owner=True` in the attribute definition
      indicates that this is a `PublicId` attribute but does not represent an
      owner and thus need not sign a transaction canceling this state

- TODO **nonce**: we need a mechanism to ensure that no two states can
  result in the same `StateHash`. Because of the properties of the
  hash function this can only happen if all the values of the
  attributes in the state are the same as that of another state.
  - Note: This can be easily guaranteed by embedding a GUID in
    each state. However, we need to be careful with stuffing
    data members in states because each extra byte in the state
    increases the cost of ZKP generation
  - What is the smallest nonce we can include in a state to guarantee
    uniqueness?
    - Specifically, a GUID or a timestamp might actually not provide
      strong guarantees of preimage resistance and we might necesssarily
      need a cryptographic nonce?
  - Does each state contain a timestamp? We should avoid this if possible
    because it makes proofs more expensive without really giving us
    a cryptographically safe nonce

- At the end of the transaction, the entire contents of each output
  state (including the nonces) need to be sent by the transaction
  creator ("sender") to the state owners

## Details of `Transaction`

At the wallet provider, the Transaction class has the following metadata:

- TransactionCore: All the data-members from the transaction core,
  which includes:
  - input data-members: In the example above, there is just one data-member
    `inputs` which has all the input states because they are all of
    the same type (`Utxo`). However, it is possible to have multiple
    data-members with different state values. Each represents a state being
    canceled.
  - output data-members: Similarly, one or more data-members representing
    the `outputs`.
    - whether a state represents an input or an output is deduced from the
      type declaration

- claims: Tuple of names of classes representing the claims being made in this
  transaction. Each claim class will contribute code to the ZKP program
  for this transaction

- method: `get_owners() -> list[PublicId]`
  - a method returning a list of `PublicId`s whose signatures are
    needed for the transaction to be valid.
  - If there are duplicates among the owners of the different input
    states, then this method will remove duplicates
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
    the owners for validating a transaction and this is what is
    sent to the ZKP program
  - TODO: it should return `TransferCore` not `TransactionCore`
    Need to doublecheck that this doesn't cause any problems.

- method: `get_zkp_program_inputs() -> list[str]`
  - a method returning the commandline arguments to be provided to the
    `get_zkp_program()`
    - Question: should this be json instead of `list[str]`?
  - At a minimum, this includes the `transaction_core` as a private input
    `input_hashes` and `output_hashes` as public inputs, the `signatures`.
    - TODO: Decide whether `signatures` is a private or public input

## Details of `Signature`

TODO: we need to figure out what signature scheme we're using

The `get_owners` method has the following properties:

- The `get_owners` method creates a list of `PublicId`s whose
  signatures are needed for a transaction to be valid.
- All the `owners` will only come from the `inputs`. The `outputs` do
  not contribute to the `owners`.
- Each `input` state might contribute 0, 1, or more `PublicId`s to the
  list. It is possible that two different states have the same owner
  so they contribute only one unique `PublicId`. It is possible that some
  state might contribute two or more.
  - TODO: We should extend this to allow more complex things like
    2-of-3 signatures

The `signatures` list has the following properties:

- The `proof` will construct the owners array and prove that every
  owner in every state exists in the owners array
- The `proof` will also assert that
  `signature[i] == sign(transaction_core, self.get_owners()[i])`
- All signatures will have to be provided externally. Badal.DSL
  does not have a way of creating the signature of the transaction.
  Typically, Badal code will output the `transaction_core` and
  the `get_owners()` list. The user has to generate the corresponding
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
- construct the owners list
- for each owner in each state assert that it is included in the owners list
- for each owner: compute `sign(transaction_core, owners[i])`
  and assert that this is equal to `signatures[i]`
- assertions related to the chaining pointers if necessary (see
  comment at Notary)


### Code specific to this transaction type:

- Code for each `Claim` in the transaction
  - each claim gets the `transaction_core` as input and the `Claim`
    definition contains the code to extract the relevant information
    from the `transaction_core` and assert the appropriate constraint
  - remember, the same `transaction_core` that is used in the claims
    is also used in computing the `StateHash`es, thus ensuring validity
    of the transaction

## Notary

At the notary, one transaction has the following data:

- inputs: `list[StateHash]` corresponding to states being canceled
  - Note: `StateHash` will always be unique. See discussion under
    `State` for more details of this.
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

- Confirm that `inputs` represent active states on the ledger, meaning
  that for each input:
  - confirm that it exists in the `outputs` of one and only one of the
    previous transactions, and
  - and it does not exist in the `inputs` of any previous transaction
- Confirm that `outputs` represents new states:
  - this means confirming that none of the outputs exist in
    the inputs or outputs of any of the previous transactions
- Verify the proof
- Add a timestamp to the transaction
- Hash the transaction and use that as a `transaction_id`
- Sign the transaction

The signed transaction is appended to the ledger and the
`transaction_id` is returned to the caller
