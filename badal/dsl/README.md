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

## Basic DSL Classes

The DSL is primarily based on these classes: PublicId, Attribute, State, Claim, Proof, Transaction, and Schema.

The PublicId class represents a wallet owner. In Badal this can either
be a person or an entity. 

The Attribute and State classes abstract away the details of
`add_attribute_type` and `add_state_type` from `badal.schema`. Here is
an example of a `State` definition using the DSL (with only a few
important data-members shown):

    :::python
    class Utxo(dsl.State):
        # inherits `owner` and `nonce` from
        # the dsl.State base class
        amount = dsl.Amount(uom='inr', precision=3)

This code will result in three `add_attribute_type` calls (one for
`owner: PublicId`, one for `nonce: RandomBits`, and one for `amount`)
and one `add_state_type` call.

The `Claim` class allows the specification of ZKP code that needs to
be incorporated in the proof for the transaction. All the claims of a
transaction together should guarantee that the transaction is valid.

The `Transaction` class puts it all together. Here is an example of a
`Transaction` definition with important data-members shown:

    :::python
    class Transfer(dsl.Transaction):
        # Inherited from dsl.transaction
        #   creator: PublicId
        #   signatures: list[Signature]
        #   proof: Proof
        inputs = dsl.Array(Utxo, type="input", max_length=2)
        outputs = dsl.Array(Utxo, type="output", max_length=2)
        claims = (AmountsMatchClaim, UtxoTypesMatchClaim)

A note on terminology: 

- Transaction creator: the wallet/entity creating this transaction.
  Usually this is the owner of one of the input states.
- Transaction endorsers: the owners of the input states (other than
  the transaction creator). For a transaction to be valid, the
  transaction creator must collect signatures of all the endorsers.
  A transaction with a single input state has 0 endorsers
- Recipients: These are owners of the output states being created by
  the transaction. Note: a transaction does not require the signatures
  of the recipients (except those recipients who are also endorsers)

A new transaction class usually defines one or more data members representing input states to be canceled and one or more data members representing output states to be created, and a tuple of `Claim` classes. 

One important function of these classes is to automatically create code in the chosen ZKP language (_e.g._ Zokrates or circom) to create appropriate data-structures for each attribute type, for each state type, and for the transaction. They also create functions to initialize and manipulate these data-structures. For example, when using Zokrates, this would result in the creation of `struct owner_t`, `struct nonce_t`, `struct amount_t`, `struct utxo_t`, and `struct transfer_t`, along with functions `init_owner`, `init_nonce`, `init_amount`, `init_utxo`, and `init_transfer`.

## Details of `State`

A state has the following important properties:

- owner: PublicId
  - the owner of this state whose signature is required for canceling
    this state
    - TODO: we should also allow k-of-n ownership, but the details of
      how to do that need to be worked out
    - Can this be handled externally?
- method: `hash() -> StateHash` returns a hash of the contents of the state
  - The hash function used must be collision resistant, preimage
    resistant, and second preimage resistant.
  - The `nonce` in the `dsl.State` ensures that two different `State`
    instances will not have the same hash even if they represent
    identical data (_i.e._ two `Utxo`s with the same `owner` and
    the same `amount` will still have different hashes)
    - TODO: What is the smallest nonce we can include in a state to guarantee
      uniqueness?
      - Specifically, a GUID or a timestamp wil not provide
        strong guarantees of preimage resistance
    - Does each state contain a timestamp? We should avoid this if possible.
      Generally, we should avoid adding data members to states unless
      absolutely necessary, because each additional byte in a state makes
      the ZKPs more expensive
- At the end of the transaction, the entire contents of each output
  state (including the nonces) need to be sent by the transaction
  creator ("sender") to the corresponding `owner`s (the recipients)

## Details of `Transaction`

At the wallet provider, the Transaction class has the following data members:

- one or more data members representing input states which are going
  to be canceled by this transaction. In the example above, there is
  just one data-member `inputs` which has all the input states because
  they are all of the same type (`Utxo`). However, it is possible to
  have multiple data-members with different state values. Each
  represents a state being canceled.
- output data-members: Similarly, one or more data-members representing
  the `outputs`.
  - whether a state represents an input or an output is deduced from the
    type declaration
- claims: Tuple of names of classes representing the claims being made in this
  transaction. Each claim class will contribute code to the ZKP program
  for this transaction
- method: `hash() -> TransactionHash`
  - Collect together all data members representing input or output states
  - Compute their `StateHash`es
  - Concatenate all these `StateHash`es
  - Hash the result
  - The hash function can be the same as that used for `State.hash`
  - The `StateHash` and `TransactionHash` types can be the same.
- method: `endorsers(creator: PublicId) -> list[PublicId]`
  - a method returning a list of endorsers of this transaction.
    These are the owners of the input states other than the
    (other than the transaction creator). Their signatures
    are needed for the transaction to be valid. 
    - The reason for special treatment for the transaction creator
      is that we don't need a signature for the transaction creator.
      A direct proof of knowledge of the private id is good enough
      for the creator since the creator's private id can be provided
      to the ZKP program as a private input. The same cannot be done
      for the other owners.
  - If there are duplicates among the owners of the different input
    states, then this method will remove duplicates
  - The details of how this is done in the ZKP program efficiently
    needs to be worked out.

- method: `get_zkp_program() -> str`
  - a method returning the (automatically generated) ZKP program
    corresponding to this transaction
  - See section `Proof` for details of what this ZKP program contains
  - the `proof` for a specific transaction instance will be the result
    of running this program with the private data of that transaction

- method: `get_zkp_program_inputs() -> list[str]`
  - a method returning the commandline arguments to be provided to the
    `get_zkp_program()`
    - Includes public as well as private ZKP inputs
    - Question: should this be json instead of `list[str]`?
  - At a minimum, this includes the `inputs`, `outputs`, and `signatures`
    and `creator_private_id` as the private inputs and `input_hashes` and
    `output_hashes` as public inputs
  - Question: does this _have_ to be overridden by any subclass of the
    `Transaction` class? Probably not: so this method can be common and
    moved into the `Transaction` class.

## Details of `Signature`

TODO: we need to figure out what signature scheme we're using

The `signatures` list has the following properties:

- The `proof` will construct the endorsers array and prove that every
  owner in every state exists in the owners array or is the creator
- All signatures will have to be collected via out-of-band means.
  Badal.DSL does not have a way of creating the signature of the
  transaction. Typically, Badal code will output the transaction data
  (inputs and outputs) and the `endorsers()` list. The user has to
  generate/collect the corresponding signatures and input them into
  the system. As a result, the `PrivateId` is never directly used in
  the ZKP program. This allows a transaction creator to collect
  signatures of other parties whose `PrivateId` is not known/revealed
  to the transaction owner.

  The wallet provider will usually have methods to save private ids
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
- assert `HMAC(creator_private_id, 0) == creator`
- construct the endorsers list
- for each owner in each state assert that it in self.endorsers() or
  it is the transaction creator
- For each endorser assert that
  `verify_signature(transaction_hash, self.endorsers()[i],
  signature[i])` returns true. Note: the proof only
  verifies the signature, so it only needs to know the `PublicId`s
  of each owner, not the `PrivateId`.
- assertions related to the chaining pointers if necessary (see
  comment at Notary)


### Code specific to this transaction type:

- Code for each `Claim` in the transaction
  - each claim gets the `transaction` as input and the `Claim`
    definition contains the code to extract the relevant information
    from the `transaction` and assert the appropriate constraint
  - remember, the same `transaction` that is used in the claims
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
