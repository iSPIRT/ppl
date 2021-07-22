# Design Discussions and Rationales

This document has sections exploring the major design alternatives, including summaries of the trade-offs, links to references with more information, and implications for PPL if any.

As and when we actually take decisions, this will be updated with the rationale for our choice.

## UTXO Model vs Account Model

The two important models of organizing the information on a blockchain: the UTXO model used by Bitcoin and the account model used by Ethereum. [This article][horizen] gives a good overview of both, what the UTXO and account models are, and the architectural tradeoffs involved.

In the UTXO model, each transaction has one or more inputs which indicate which specific coins are being spent (they have to be unspent outputs of earlier transactions, hence the name unspent transaction outputs) and has one or more outputs indicating how many coins are being given to which addresses. Once this transaction is confirmed, the outputs of the transactions become new UTXOs and the inputs are no longer UTXOs because they are no longer unspent. Note that the total amount owned by any particular address is not stored/maintained by the blockchain, and is not needed to validate any transaction—just ensuring that the inputs are unspent is good enough. Clients who want to know their total balance need to compute and maintain the balance themselves. 

In the account model, the system maintains the current balance in each account. Each transaction indicates the amounts to be deducted from the input accounts and amounts to be added to the output accounts. The validation of a transaction involves checking that the input accounts have balances that are larger than the amounts being deducted. Note that the system does not keep track of individual coins—if two different transactions deposit 10 ether each in the same account giving a balance of 20, and then 10 ether is spent, there is no way to know whether this 10 came from the first transaction or the second. 

One important note: in the account model, a transaction of the type "send 10 eth to account x" could be sent multiple times to the blockchain and would result in multiple withdrawls unless we take care to prevent this kind of a double spend. (This is not possible in the UTXO model since one UTXO can only be spent once.) Ethereum solves this problem by maintaining a "nonce" as the part of the state of each account. This nonce is essentially a transaction counter which is incremented with every transaction. When a transaction is submitted to the blockchain, it needs to include this nonce, and the miner ensures that the nonce in the transaction matches the current nonce in the account. This point will become important for scalability later.

Architectural impact of UTXO vs account model:

-   **Privacy**: The UTXO and account models give different types of privacy. 
    
    In the UTXO model, if a user creates new address every time a UTXO
    is spent, it would be difficult to link accounts to each other. This
    is something that can be done easily in a UTXO system. Doing
    something similar in an account based system would require much more
    work. Thus, UTXO model allows more privacy via lower linkability to
    transactions.
    
    On the other hand, in UTXO, following the movement of a particular
    set of coins through the system is easy. In an account model, this
    can't be done for more than one step since the individual coins
    don't have an independent existence. Thus, the account model
    provides more privacy via fungibility.
    
    Depending on the application context, one or the other might be more
    desirable.

-   **Scalability**: The UTXO model allows more parallelization of
    transactions because two different transactions for the same account
    can go ahead independently of each other as long as they use
    different UTXOs for inputs. By contrast, the account model, through
    the use of the transaction nonce forces serialization of all the
    transactions on one account. This increases the effort required to
    increase transaction throughput via parallelization and sharding.
    
    However, the account model has a different scalability advantage
    over the UTXO model. The account model only needs to keep track of
    the final balance of each account, and not each and every individual
    UTXO. As a result the total size of the state that needs to be
    maintained by a node is much smaller. This not only reduces the
    memory requirement of any one node, but also reduces the time
    required for a new node joining the system to sync up with the
    current state of the blockchain.

-   **Ease of Programming**: The account model is closer to how people
    think in the real world, and as a result it is easier to write
    programs and smart contracts for.

-   **Light Clients**: If additional capabilities are layered on top of
    the blockchain (for example, the Lightning network on top of
    Bitcoin), then the use of UTXO model makes certain kinds of layers
    easier while the account model makes other kinds of layers easier to
    construct.
    
    Consider an example from the Lightning Network. Here, Alice and Bob
    can maintain a running balance between them by Alice creating
    off-chain transactions based on a UTXO and sending the signed
    transaction to Bob. Bob submit this transaction to the blockchain.
    Instead, when another small payment needs to be made, Alice creates
    updated transaction against the same UTXO, consisting of the sum of
    the payments so far. This new transaction replaces the previous
    transaction. When Bob wants to settle the accounts, he submits just
    the last transaction to the blockchain. 
    
    Due to the nonces, this kind of a scheme is not easy to implement in
    the account model. 
    
    By contrast, the account model makes it easier to implement light
    clients which need to provide services related to just one account.
    In case of the account model, it is easy to just fetch the current
    state related to that one account without having to fetch the entire
    state. (For example, in Ethereum, the Merkle Patricia Tree allows
    verifiable fetching of the data of one account by just going down
    one path of the tree.) In the UTXO model, to be able to do something
    like this effectively, a client would need to watch and analyze all
    the transactions on the blockchain.

To understand these issues in more detail, read the [Horizen article][horizen] (referenced earlier) as well as the [original design rationale][ethrationale] published by Ethereum itself. 

Does a hybrid model make sense?

It is possible that building a UTXO model at the base, and layering an account model on top of it might give the best of both worlds. The [Horizen article][horizen] points out that [QTUM][qtum] implements such a hybrid model. 


[horizen]: https://academy.horizen.io/technology/expert/utxo-vs-account-model/
[ethrationale]: https://eth.wiki/en/fundamentals/design-rationale
[qtum]: https://blog.qtum.org/qtums-utxo-design-decision-d3cb415a3a6e?gi=d822a092f221
