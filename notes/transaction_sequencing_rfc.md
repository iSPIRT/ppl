# Wallet-Managed Chaining of Transactions

1.  [Example use case](#org2b36a43)
2.  [Algorithm Overview](#org46075b4)
3.  [Implementation Details](#org5730d30)
4.  [DoS Prevention](#orgaee08f0)
5.  [Enforcing a total order](#orge5163d8)
6.  [Performance Optimizations](#orgfd5db09)
7.  [Outstanding Questions](#orgc6c2885)

This is a Request for Comments on a proposal for a wallet to manage the chaining/sequencing of all the transactions it is involved in. This will make it easier  to implement aggregate proofs involving those wallets.


<a id="org2b36a43"></a>

# Example use case

A wallet needs to prove that none of the incoming payments out of the last 100 exceeded ₹20000. To be able to do that using Badal, the most important problem to be solved is to actually guarantee that none of the transactions were skipped while constructing this proof. Doing so requires some way of sequencing or chaining the transactions but this needs to be done without leaking any extra information to either the counterparties in the individual transactions or to the Notary.


<a id="org46075b4"></a>

# Algorithm Overview

This can be solved by having each wallet publish a sequence of states on the ledger with consecutive sequence numbers and later each actual transaction involving this wallet references (and thus cancels) one of these states. This associates a per-wallet sequence number for each transaction in the system with the following guarantees:

-   For each wallet, every transaction involving that wallet cancels exactly one sequence sequence number state of that wallet
-   The same sequence number of a wallet cannot be canceled by two different transactions
-   If a transaction involves N wallets it will cancel exactly N different sequence states (one for each wallet)

Now, an aggregate proof would be as follows:

1.  Start with sequence number S
2.  Use the private data of the N<sup>th</sup> transaction, prove that the sequence state canceled as a part of this transaction contains the sequence number S
3.  Incorporate the data of this transaction in the aggregate computation
4.  Increment S
5.  Repeat these steps with the next transaction

Step 3 computes the aggregate and step 4 ensures that none of the transactions can be skipped (otherwise the proof will fail).


<a id="org5730d30"></a>

# Implementation Details

We define a new `State` called a `SequenceState`. This state contains a sequence number and wallet id. We define a new `Transaction` called `ExtendSequence` which creates a new `SequenceState` (containing a new sequence number), and references the previous `SequenceState`. The proof for this transaction proves that the sequence number in this state is 1 more than the sequence number in the previous `SequenceState` referenced.

The previous `SequenceState` is not _canceled_ by this transaction. It still remains active. (It will actually get canceled by the actual transaction later on.)

When a regular transaction is created, the transaction creator ensures that the `inputs` of the transaction contain all the regular inputs (e.g. `Utxo` being canceled in case of a `Transfer` transaction) but in addition contains the `SequenceState`s for each wallet included in the transaction. To do this, the transaction creator has to contact each wallet involved in the transaction and ask them to provide them `StateHash` of the appropriate `SequenceState` for this transaction.

Note: this needs to be done for wallets of the owners of the `input` states as well as the `output` states. This is to ensure that aggregate proofs can include transactions in which a wallet has appeared as an output as well as an input. (_i.e._ to prove that balance in a wallet has always been above 10000 we need to include transfers in as well as transfers out of this wallet)

Each wallet needs to ensure that the `SequenceState`s assigned to the transactions are actually in sequence. 

<a id="orgaee08f0"></a>

# DoS Prevention

It is possible that a transaction creator asks a wallet for a `SequenceState` for a new transaction and later never actually publishes that transaction to the ledger (either due to an error or out of malice). This would result in gap in that wallet's transaction sequence and it would never be able to generate any aggregate proof involving that sequence number.

A simple fix to this is that a after a wallet has assigned a `SequenceState` for a specific transaction, it waits for a predefined timeout period, and if the transaction does not appear on the ledger during that period, it publishes a new dummy transaction which simply cancels that `SequenceState`. As a result, the gap in the sequence numbers for that wallet gets filled. Now, if the creator of the earlier transaction tries to publish the transaction (which had gotten delayed for whatever reason) it will fail (because it is trying to cancel a `SequenceState` that has already been canceled). At this point, to be able to actually complete this transaction, the transaction creator would have to request a new sequence number from the wallet. 


<a id="orge5163d8"></a>

# Enforcing a total order

We need to ensure that a wallet cannot play tricks by creating two difference `SequenceState`s with sequence number N+1. To do this we make a slight change in the protocol for a Notary.

In the `inputs` of a regular transaction, we tag each input with either `canceled` or `chained`. When validating a transaction a Notary ensure that each state can only be `canceled` once in the system and can be `chained` only once. This means that at the time of creating a transaction, the Notary ensures that each `canceled` input state has not appeared as a `canceled` input state in any previous transaction and that each `chained` input state has not appeared as a `chained` input state in any previous transaction. 

A `ExtendSequence` transaction contains exactly one input state of type `chained`. By contrast, all the `inputs` in a regular transaction are of type `canceled`. (_i.e._ the regular inputs as well as the sequencing inputs.)

<a id="orgfd5db09"></a>

# Performance Optimizations

A naive implementation of this protocol would significantly increase the latency of transaction because after the transaction creator sends messages to the other wallets each of them would publish a new `ExtendSequence` transaction on the ledger and then send the corresponding `SequenceState` to the transaction creator.

A suggested optimization for this is that wallets can pre-create and cache a number of `SequenceState`s. Depending on the expected volume of transactions some wallets might pre-create a small number of `SequenceState`s while others might create a much larger. We can even have a design in which a single `ExtendSequence` transaction can create a block of many sequence numbers further improving the performance.

Wallets can then assign any of the cached `SequenceState`s when they receive transaction requests. It is possible that the transactions might not get confirmed on the ledger in exactly the same order in which the `SequenceState`s were assigned: thus, due to the asynchronous nature of this process, the transaction assigned sequence number 432 might get published on the ledger before the one assigned 431. However, this is not a problem: creation of a regular transaction does not enforce the sequencing (only creation of a `ExtendSequence` transaction does that and those transactions always happen in sequence). And later, during an aggregate proof, the transactions can be processed in order of sequence number, they don't have to be processed in order they were confirmed on the ledger. 


<a id="orgc6c2885"></a>

# Outstanding Questions

-   How does a wallet <span class="underline">prove</span> that the <span class="underline">latest</span> transaction has been included in the proof? In the proposal above, we have handwaved this question by proving that the last transaction in the sequence has a recent timestamp. That might be enough for most use cases, because most aggregate proofs are for a period in the past and do not require up-to-the-minute data (_i.e._ when applying for a bank loan, your financial records until the last month are good enough). Will we need a stronger guarantee, and if yes, how would we solve it?
-   Do we allow a state that has been `canceled` to later be included in a transaction as a `chained` input state? Why or why not?

