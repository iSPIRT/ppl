# ZKP Designs for Transactions

-- Navin Kabra

_Status: This is an early, unreviewed draft. It is likely to have errors._

## UTXO based design

We assume that a wallet consists of multiple sleeves. Each sleeve holds value stores of only one type of IOUType and UOM.



### Sleeve

A sleeve consists of:

- WalletID
- SleeveID
- IOUType
- UOM (Unit of Measurement)
- PublicKey
- NotaryID (the primary notary for this wallet)

(Note: we could replace PublicKey with a list, allowing for multiple owners with 1-of-N or k-of-N semantics. For simplicity, this functionality not described here, but the changes for this would be minimal.)

A sleeve stores fungible IOUs (of one type) for one owner. There is one primary notary associated with this sleeve. This notary is responsible for preventing double spends and generally verifying the integrity of the sleeve and associated transctions.

### State

A state consists of:

- StateID (unique across the system)
- SleeveID
- Amount
- StateHash

The StateHash is simply a hash of the StateID+SleeveID+Amount. 

A state represents an amount of `UOM` that has been deposited into a sleeve. A state can be _active_ or _dropped_. An active state is a UTXO—indicating that the amount represented by it has not yet been used in another transaction, so is a valid candidate to be an input for a future transaction. A dropped state is one which has been used in a transaction, and hence cannot be used again.

Any transaction consists of taking one or more active states, dropping them, and redistributing the total UOM from the input states into one or more newly created output states which will now be active states.

In the rest of this document we use the words _spent_ and _unspent_ as synonyms for active and dropped states, because it makes the examples easier to understand, but keep in mind that a sleeve can hold non-currency values in which case spent and unspent words would be misleading.


### Simple Transaction

A simple transaction is one in which all the input states belong to the same owner (called the _sender_ in this example) and the primary notary for all of them is the same. The output states can belong to different owners (referred to as _receivers_).

We will go through an example transaction with two inputs and two outputs. 

#### Sender steps

In this case, the owner creates a transaction core data structure as follows:

- Input states
  - SIn1: SIn1ID, SIn1SleeveID, SIn1Amount, SIn1Hash
  - SIn2: SIn2ID, SIn2SleeveID, SIn2Amount, SIn2Hash
- Output states
  - SOut1: SOut1ID, SOut1SleeveID, SOut1Amount, SOut1Hash
  - SOut2: SOut2ID, SOut2SleeveID, SOut2Amount, SOut2Hash
- TxCoreHash = Hash(SIn1Hash + SIn2Hash + SOut1Hash + SOut2Hash)

Note: this transaction core data structure is known and visible only to the owner. At no point are the SleeveIDs and Amounts of any of the states revealed to any of the notaries or on the public chain. The details of SOut1 and SOut2 will be sent to the receivers by the sender using some other communication method.

Based on this, the sender creates a transaction packet consisting of
this information:

- TxCoreHash
- SIn1ID, SIn1Hash, TxCoreHash, SIn1Proof
- SIn1ID, SIn1Hash, TxCoreHash, SIn1Proof
- SOut1ID, SOut1Hash
- SOut2Id, SOut2Hash
- TxProof

Here, SIn1Proof is a zero knowledge proof of the following:

- SIn1Hash is a valid hash of the contents of SIn1
- Proof of knowledge of the PrivateKey matching the PublicKey in SIn1Sleeve

Similarly for SIn2Proof.

TxProof is a zero knowledge proof of the following:

- SIn1Amount + SIn2Amount = SOut1Amount + SOut2Amount
- SOut1Amount >= 0
- SOut2Amount >= 0
- TxCoreHash = Hash(SIn1Hash + SIn2Hash + SOut1Hash + SOut2Hash)

Remember that for a simple transaction, all the input sleeves have the same primary notary. Let's call it NotaryIn. The transaction packet created above is sent to NotaryIn. (Note: the transaction core data structure is not sent to the notary. Only the transaction packet.)

#### NotaryIn steps

NotaryIn first verifies that the inputs: by checking that each one represents an unspent state and that the sender has permission to spend this input. Then NotaryIn verifies the integrity of the full transaction by checking that the total of the output amounts matches the total of the input amounts.

First, NotaryIn confirms that SIn1ID does not appear as an input of any past valid transaction. The system guarantees that if any state is dropped, the corresponding StateID would show up as the input of some transaction that _must_ be sent to NotaryIn and saved in its copy of the public ledger before the transaction is considered final. This check guarantees SIn1ID cannot be double spent.

Next, NotaryIn finds the past transaction that contains SIn1ID as one of its outputs. The system guarantees that one and only one such transaction will exist and it will be present in NotaryIn's copy of the public ledger. Let's call this transaction TxIn1. 

Now NotaryIn verifies that SIn1Hash matches the corresponding StateHash in the outputs of TxIn1. Note: this guarantees that SIn1SleeveID, and SIn1Amount (which NotaryIn does not know) also match.

NotaryIn repeats this for each of the inputs.

Finally, NotaryIn verifies the TxProof.

At this point, NotaryIn is convinced that the transaction is valid, and writes the transaction packet to its public ledger along with its own signature and the transaction is considered complete.

#### Closing the loop


After this, NotaryIn sends this transaction to NotaryOut1 and NotaryOut2, the primary notaries corresponding to SOut1SleeveID and SOut2SleeveID and the transaction gets recorded on their public ledgers. This ensures that the newly created UTXOs are available to the new owner.

In addition, the details of SOut1 and SOut2 (amounts) will be sent to the receivers by the initiator using some other communication method. At no point are the SleeveIDs and Amounts of any of the states revealed to any of the notaries or on the public chain.

### Complex Transaction

A transaction in which the inputs come from different owners, or the inputs are from the same owner but the sleeves/wallets have different primary notaries is more complicated and needs to be treated differently since it becomes a distributed transaction.

The basic idea is to think of this transaction as having an initiator who puts together the "deal" (which is essentially an agreement about what inputs are provided by whom and what outputs are sent to whom). Then the initiator secures permission for this deal from all the owners of the input states. Once all the permissions are secured, the initiator then finalizes this transaction on the public ledger. 

The rest of design is still being worked on.

## Account/Balance based design

This design is still being worked on.
