# Zero-Knowledge Proof Systems in Badal

_This is an early-stage, incomplete, and unreviewed draft. Anything can change at any time_

This document assumes that you're familiar with the contents of  [badal/dsl/README.md](../dsl/README.md).

## Introduction

A core mechanism in Badal is that most of the data in a transaction stays private (known only to the entities that participate in the transaction) and only hashes and some other metadata are stored on the ledger. To guarantee validity of all the transactions and prevent double-spends, zero-knowledge proofs are used by the transaction submitters (wallet providers and end users) to provide the appropriate guarantees.

Badal is intended to be a flexible system that supports different various different ZKP protocols (zk-SNARKs vs zk-STARKs vs BulletProofs), ZKP languages/libraries (_e.g._ Zokrates vs circom), proof systems (_e.g._ Groth16 vs Marlin), and and other configurable implementation details of those proof systems (_e.g._ ALTBN_128 vs BLS12_381 curve, or SHA256 hash vs Poseidon hash).

For the rest of this document, we will use the term ZKP parameters to refer to all the different configuration options where multiple choices are possible.

Any one schema in Badal is required to use only one configuration of the ZKP parameters. This is specified once at the time of schema creation and cannot be modified after that. (TODO: figure out what it takes to support modification of ZKP parameters. For example, what happens if a vulnerability is discovered in one of the hash functions we're using? How does a schema recover from this?)

## Building Blocks

### Hash Function

Badal requires the use of a hash function which is collision resistant, preimage resistant, and second preimage resistant. This is used in hashing `State`s to get `StateHash`es. The `State` data is private data which is only saved by the wallet providers or end-users while the `StateHash` is publicly stored on the ledger.

The hash function needs to be ZKP friendly. _i.e._ the time and space requirements for implementing the hash function in the ZKP system picked need to be reasonable. It is likely that which hash functions are acceptable is conditional upon which ZKP language/library and which ZKP system are chosen.


Supported Hash Functions

| Functions | Languages/Libraries | ZKP Systems | Comments                                                    |
|-----------|---------------------|-------------|-------------------------------------------------------------|
| SHA256    | Zokrates, ??        | All??       | Used in ZCash with an optimized circuit but still expensive |
|-----------+---------------------+-------------+-------------------------------------------------------------|
| Pedersen  | ??                  | ??          | ??                                                          |
| Poseidon  | ??                  | ??          | ??                                                          |
| MiMCHash  | ??                  | ??          | ??                                                          |

TODO: Fill in the `??` in this table. Also, add more rows?

### Digital Signatures, Public ID, Private ID

Badal uses two different types of digital signatures: standard digital signatures and ZKP digital signatures.

A standard digital signature is used by a Notary to sign a transaction
being appended to the ledger. In this case, the "message" is the
public fields of transaction (i.e. the `StateHash` values and other
public fields) to be signed by using the Public/Private ID of the
Notary. The message, the signature, and the Public ID of the notary
are publicly known.

A ZKP digital signature is used by a wallet or entity to provide a ZKP
to the Notary that a transaction is approved by the entity. Usually,
this would involve proof of knowledge of the Private ID associated
with the Public ID of the wallet or entity. (Question: it is possible
to have a different system?)

In both cases, picking a digital signature system automatically
determines the formats of the Public and Private IDs

#### Standard digital signature system

Every Notary has a well known Public ID and a secret Private ID. All
transactions appended to a ledger by a notary are digitally signed by
the Notary using its Private ID. 

The system must satisfy the standard guarantees of digital signatures:

- It should be possible to verify the validity of a signature given
  just the document and the Public Id
- It should not be possible to sign a document without knowing the Private ID
- It should not be possible to extract the Private Id from a large set
  of messages, signatures for a given Public Id
- It must be resistant to an existential forgery attack.

Note: this digital signature system does not have to be ZKP friendly

TODO: Decide which system(s) will be supported by Badal.

#### ZKP digital signature system

In Badal, a `PublicId` is used in `State`s to refer to entities or
wallets. Note: although it is called a `PublicId`, usually it will be
a part of the _private_ information in a state/transaction which is
known to all the transaction participants but is not put on the
ledger.

Every transaction in Badal has a set of "owners", referred to by their
Public IDs, and for a transaction to be considered valid, we need
proof that each owner approves of this transaction.

_Discussion_: In a ZKP system it is possible for a transaction creator
to signal their own approval for the transaction without actually
using a standard digital signature system. The ZKP that the
transaction creator submits to the Notary along with the transaction
can contain a proof of knowledge of the Private ID of the transaction
creator. This can be done directly by providing the Private ID as one
of the private inputs to the ZKP program and in the program proving
that this Private Id is connected to the Public Id of the transaction
creator. (For example, this could be done by `assert HMAC(private_id,
0) == public_id`.)

However, this process fails when a transaction has multiple owners
whose approval needs to be proven. It is not possible for the Private
IDs of the other owners to be provided as private inputs to the ZKP
program (because then they would become known to the transaction
creator). To get around this problem, the transaction creator creates
the `transaction_core` data structure, and sends it to the other
owners for their signatures. Each owner signs the `transaction_core`
and sends the signature back to the transaction creator. The
`transaction_creator` collects all these signatures and and attaches
them along with the transaction as public inputs when submitting it to
the Notary. In addition, the ZKP program contains code to verify that
each of these signatures is a valid signature (this step does not require
knowledge of the Private IDs).

Should the transaction creator provide a "direct proof" as described
in the first paragraph, or should the transaction owner be treated as
just another owner and its signature included in the list of
signatures that are public inputs? The advantage of the former is that
it would be more efficient than the latter. The advantage of the latter is
consistency and simplicity of the code?

TODO: Decide whether the transaction owner will use a "direct proof"
or a signature. Remember, it is possible that single-owner
transactions the most common case in many schemas and hence it might
be worth optimizing this case.

The ZKP digital signature system (used for non-transaction creator
owners) must satisfy all the same properties as those for the standard
digital signature described in the previous section. In addition it
should also satisfy this:

- The system must be ZKP friendly

Due to this requirement is it possible that the ZKP digital signature
system is used is not the same as the standard digital signature
system.

If we're using the "direct proof" method the transaction creator then it has a different set of requirements. Specifically, this method is equivalent to having a HMAC keyed on the Private ID, with the following properties:

- It should be collision resistant and preimage resistant
- It should be ZKP friendly

TODO: If we are using the "direct proof" method, then decide which
HMAC is used for this

## ZKP Protocols 

At this time, the following three are the most common ZKP protocols
with practical implementations: zk-SNARKs, zk-STARKs, and
BulletProofs. (TODO: keep adding to this list. Should Aurora be here?)

As per [this
article](https://ethereum.stackexchange.com/questions/59145/zk-snarks-vs-zk-starks-vs-bulletproofs-updated),
it appears only zk-SNARKs provide the performance required by Badal. Specifically, zk-STARKs proof sizes are too large (~45KB) and BulletProofs require 1+s to verify proofs. 

TODO: update this as and when new information becomes available.

TODO: decide whether BulletProofs are really unacceptable?

Decision: For now, we only support zk-SNARKs.

## ZKP Languages / Libraries

The following are high level languages or libraries that can be used
to quickly and easily write ZKP programs:

- [Zokrates](https://zokrates.github.io/)
- [circom](https://docs.circom.io/)
- [snarkjs](https://github.com/iden3/snarkjs)
- [arkworks](https://github.com/arkworks-rs)
- Rejected: [Cairo](https://www.cairo-lang.org/): license is not open source

Note: all the languages/libraries we support must have an appropriate open source licence.

Decision: We will certainly be supporting Zokrates. Circom also looks promising.

TODO: evaluate snarkjs and arkworks for suitability

### Low level zk-SNARK libraries?

Should we be looking at low level zk-SNARK libraries? Ease of creating new schemas is one of the design goals, and that includes ease of writing ZKP programs. That seems to argue against lower level libraries.

Potential low-level libraries to look at, if we choose to do so: [Libsnark](https://github.com/scipr-lab/libsnark), [Bellman](https://github.com/zkcrypto/bellman), [Gnark](https://github.com/ConsenSys/gnark). 

## ZKP Protcols

This decision will be conditional upon the choice of the ZKP language/library.

Zokrates supports: Groth16, GM17, Marlin, PGHR13. 

Circom supports: Groth16, PLONK. 

[Groth16 seems to be fastest](https://github.com/scipr-lab/libsnark/blob/master/libsnark/zk_proof_systems/ppzksnark/README.md). But [Groth16 has the strongest cryptographic assumption](https://eprint.iacr.org/2016/260.pdf), meaning. Most widely used cryptographic assumptions in non-ZKP systems are Hardness of Factoring (RSA) and Discrete Log (El-gamal encryption, TLS) but Groth uses a stronger assumption, relatively nonstandard.

Of this PGHR13 is primarily for historical reasons, because it is the first paper and easy to understand? (TODO: confirm this?).

Marlin and PLONK have the big advantage that is it "Universal" and would thus not require a per ZKP program setup phase. But ar they too new?

TODO: Create a comprehensive table of the assumptions, advantages, and
disadvantages of each system

TODO: What are the advantages and disadvantages of GM17?

TODO: Decide if Marlin is safe enough to use. Decide how to decide this.

TODO: Decide if PLONK is safe enough to use. Decide how to decide this.

TODO: Is PLONK a zk-SNARK or something different?

### Notes on cryptographic assumptions

TODO: How should we decide which cryptographic assumptions are acceptable for Badal and which ones aren't?

Should we decide based on ‘oldest and most widely used’ assumption with the largest security-parameter bit length? Or should be do it based on which assumption has had the largest amount of $$ riding on it so far?

Hardness of Factoring: So use RSA with 512 bits security-parameter? But I think the ‘default’ libsnark field is 254 bits and cannot be used for proof of pre-image of RSA public key with 512 bit fields.. This suggests that if we use non-default higher bitlength fields within libsnark the proof overheads may get very high?

There probably are no practical ZKP systems whose underlying cryptographic assumption is Hardness of Factoring 

Discrete Log: El-gamal encryption and TLS security relies on this. Not sure 

## Other ZKP Parameters.

TODO: Figure out the pros and cons of using different curves.

## Operational Considerations

TODO: For each combination of ZKP parameters we need to figure out
what is the impact on processes to be followed at various stages in
the Badal lifecycle

These are the important milestones in the Badal lifecycle:

- Initializing Badal
- Adding a notary
- Adding ledger
- Adding a schema
- Submitting a transaction
- Creating an _ad hoc_ ZKP program and proof

For example in Zokrates with Groth16:

- Initializing Badal: At this time we would need a problem/Circuit
  independent Trusted Setup (_i.e._ the perpetual powers of tau
  ceremony). Would this require an MPC computation that could be
  performed by hundreds of finance ministry personnel?
- Adding a notary: ??
- Adding a ledger: ??
- Add a schema: TODO: Trusted setup would need to be repeated for each
  ZKP Program in the schema? How will this be done exactly? How are
  variable number of inputs/outputs handled? Will the trusted setup
  have to be repeated for each unique combination, at runtime?
- Submitting a transaction: Nothing special?
- Ad hoc proof: TODO: Trusted setup would be repeated? Who runs it?
  How are the prover key and verifier key distributed?

TODO: repeat with: Zokrates+Marlin, circom+Groth16, circom+PLONK.





