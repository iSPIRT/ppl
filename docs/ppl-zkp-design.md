# ZKP Designs for Transactions

-- Navin Kabra

_Status: v0.02. This is an early, unreviewed draft, and the entire design is subject to change. This version assumes that as far as wallet providers are concerned the "notary" appears as a single/centralized entity. If there is any decentralization of the notary, either for availability or for trust purposes, that is assumed to be hidden behind an API_

## UTXO based design

We assume that a wallet can handle states of different types of UOMs.


### Wallet

A wallet consists of:

- WalletID
- PublicKey

(Note: we could replace PublicKey with a list, allowing for multiple owners with 1-of-N or k-of-N semantics. For simplicity, this functionality not described here, but the changes for this would be minimal.)

### State

A state consists of:

- StateID (unique across the system)
- WalletID
- Amount
- UOM
- StateHash

The StateHash is simply a hash of the StateID+WalletID+Amount+UOM. 

A state represents an `amount` of `UOM` that has been deposited into a wallet. A state can be _active_ or _dropped_. An active state is a UTXO—indicating that the amount represented by it has not yet been used in another transaction, so is a valid candidate to be an input for a future transaction. A dropped state is one which has been used in a transaction, and hence cannot be used again.

Any transaction consists of taking one or more active states (from one or more wallets), dropping them, and redistributing the total UOM from the input states into one or more newly created output states which will now be active states.

In the rest of this document we use the words _spent_ and _unspent_ as synonyms for active and dropped states, because it makes the examples easier to understand, but keep in mind that a sleeve can hold non-currency values in which case spent and unspent words would be misleading.


### Simple Transaction

We will go through an example transaction with just one UOM, two inputs and two outputs.

#### Sender steps

In this case, the owner creates a transaction core data structure as follows:

**TxCore**

- Input states
  - SIn1: SIn1ID, SIn1WalletID, SIn1Amount, SIn1UOM, SIn1Hash
  - SIn2: SIn2ID, SIn2WalletID, SIn2Amount, SIn2UOM, SIn2Hash
- Output states
  - SOut1: SOut1ID, SOut1WalletID, SOut1Amount, SOut1UOM, SInSOut1Hash
  - SOut2: SOut2ID, SOut2WalletID, SOut2Amount, SOut2UOM, SInSOut1Hash
- TxCoreHash = Hash(SIn1Hash + SIn2Hash + SOut1Hash + SOut2Hash)

Note: this transaction core data structure is known and visible only to the owner. At no point are the WalletIDs and Amounts of any of the states revealed to any of the notaries or on the public chain. The details of SOut1 and SOut2 will be sent to the receivers by the sender using some other communication method.

Based on this, the sender creates a transaction packet consisting of this information:

**Transaction Packet**

- TxCoreHash
- SIn1ID, SIn1Hash, TxCoreHash, SIn1Proof
- SIn1ID, SIn1Hash, TxCoreHash, SIn1Proof
- SOut1ID, SOut1Hash
- SOut2Id, SOut2Hash
- TxProof

Here, SIn1Proof is a zero knowledge proof of the following:

- SIn1Hash is a valid hash of the contents of SIn1
- Proof of knowledge of the PrivateKey matching the PublicKey in SIn1Wallet. (Note: this part needs to be fleshed out a bit more.)

Similarly for SIn2Proof.

TxProof is a zero knowledge proof of the following:

- SIn1Amount + SIn2Amount = SOut1Amount + SOut2Amount
- SOut1Amount >= 0
- SOut2Amount >= 0
- TxCoreHash = Hash(SIn1Hash + SIn2Hash + SOut1Hash + SOut2Hash)

(Note: in reality, the first line of TxProof will be more complicated than this because it has to account for the fact that there might be different UOMs involved, and the input totals for each UOM must add up to the output totals for that UOM.)

The transaction packet created above is sent to the Notary. (Note: the transaction core data structure is not sent to the notary. Only the transaction packet.)

#### Notary steps

Notary first verifies that the inputs: by checking that each one represents an unspent state and that the sender has permission to spend this input. Then Notary verifies the integrity of the full transaction by checking that the total of the output amounts matches the total of the input amounts.

First, Notary confirms that SIn1ID does not appear as an input of any past valid transaction. The system guarantees that if any state is dropped, the corresponding StateID would show up as the input of some transaction that _must_ be sent to Notary and saved in the public ledger before the transaction is considered final. This check guarantees SIn1ID cannot be double spent.

Next, Notary finds the past transaction that contains SIn1ID as one of its outputs. The system guarantees that one and only one such transaction will exist and it will be present in the public ledger. Let's call this transaction TxIn1. 

Now Notary verifies that SIn1Hash matches the corresponding StateHash in the outputs of TxIn1. Note: this guarantees that SIn1WalletID, SIn1Amount, and SIn1UOM (which Notary does not know) also match.

Notary repeats this for each of the inputs.

Finally, Notary verifies the TxProof.

At this point, Notary is convinced that the transaction is valid, and writes the transaction packet to its public ledger along with its own signature and the transaction is considered complete.

#### Closing the loop


At this point, the transaction initiator sends the details of SOut1 and SOut2 (amounts, WalletIDs, and UOMs) to the receivers using some other communication method. The receivers can check the public ledger and confirm that the SOut1Hash and SOut2Hash values match the expected values, ensuring that they have indeeded received the claimed amounts.

At no point are the WalletIDs and Amounts of any of the states revealed to any of the notaries or on the public chain.

### Complex Transaction

TODO:

1. Sketch out a transaction in which there are multiple UOMs involved
2. Sketch out a transaction in which the inputs are from different owners

The basic idea is to think of this transaction as having an initiator who puts together the "deal" (which is essentially an agreement about what inputs are provided by whom and what outputs are sent to whom). Then the initiator secures permission for this deal from all the owners of the input states. Once all the permissions are secured, the initiator then finalizes this transaction on the public ledger. 

The rest of design is still being worked on.
