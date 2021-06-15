# Outline of a possible CBDC + Public Private Partitioned Ledger platform

-- Dhananjay Nene

Status: (early draft) 

v0.1 1/6/2021

As we have been going through the various discussions around CBDC some characteristics of potential use cases are emerging which can be covered through specific platform features of CBDC. Given the inter-dependencies between CBDC and other economic activities for the purposes of being able to support smart contracts, the platform itself has a broader set of capabilities that can support much more than CBDC alone. 

## Imperatives

### Financial and Digital Inclusion:

One of the biggest difficulties with cash is that it is physically disconnected from the rest of the electronic ecosystem. Thus it takes formal procedures to create business constructs such as accounts, and then at some stage physically deposit and withdraw cash. Digital currency by its very nature of existence is accessible to the electronic ecosystem, thus substantially reducing the barriers of making it interact with the rest of the ecosystem. 

Note that inclusivity is not the same as inclusion. Former is the enabler. While the platform may play a significant role in catalysing inclusion, it could take more than the platform alone to do so. There are two very important elements here are 

1. The ease with which how initial KYC is done when issuing Digital Currency wallets
2. The form factor of digital currency and how it is accessed. While for corporate accounts, digital currency could reside purely in software applications, for personal accounts, it could reside on smartphones and hardware based smart cards. The form factors are important from a psychological perspective for digital currency to be omnipresent since one form does not necessarily suit all use cases and audiences. Access and usability is important since the ability to spend or collect money *easily* when required is extremely important. While on software or smartphones this could be significantly and easily enhanced over time, it will be important to design it appropriately to cover a wide variety of use cases.

The platform then connects up the digital currency to all the other capabilities that are there. Thus at this stage currency becomes easily inclusive. Inclusion however is also a function of the apps that get build on top of it. An important consideration is to figure out what are the limitations to inclusion and can the platform address it in some form. Also that the platform is capable of supporting necessary private innovation to improve inclusion. The details of matters related to form factor, usability design, and business and technological innovation is left beyond the scope of this particular document but very relevant to the topic as a whole.

### Observability of economic flow:

Economic activity forms a positive spiral with information about the economic activity. The more accurate and timely information about subsets of economic activity are available, the better these can be fed into more productive economic activities once again. Thus whether at a micro (individual) or a macro (national) level, availability of such information in time can act as a boost to economic activity and a driver to make more sound investment decisions. 

There is clearly a tension here in terms of privacy. However if the platform can support much higher observability of the economic activities without compromising on privacy, it would clearly be a significant contribution towards improved economic activity. This amongst many things could include 

* Ability to access consent based money and goods flow records of MSMEs which can help drive better lending decisions towards the deserving.
* Ability to leverage informal community power structures to support more reasons to do funds transfers than payments alone (eg peer to peer lending) which could in turn help observe say hypothetically at a village level how much money is flowing into or out of a village and for what reasons. (This is assuming some kind of anonymous aggregate tracking is implemented independent of that necessary for regulatory requirements)

There are broader advantages to observability of economic flow in terms of being able to feed the macro economic system with more accurate aggregate and timely information. This could be either in terms of quantities (eg number of invoices issued from textile sector) or amounts, if the latter becomes feasible under the appropriate privacy regime. Also, tracking M0, M1, M2, M3, M4 can all be tracked better.

### Automation of economic activity with concomitant assurance of such automation

Economic activity can be made much smoother if relevant activities can be fully or semi automated under prescribed conditions. eg. initiating payment or issuance of an IOU upon receipt of goods. This can be made feasible using this platform by implementation of smart contracts. While automation and productivity enhancement is an immediately visible capability, the bigger capability is in terms of the psychological assurance of a platform helping support good behaviour and flagging bad behaviour (eg repayment of loans) in realtime which can greatly improve business morale, willingness to engage with more counterparties and in general smoother business activities.

### Integration with existing ecosystem to encourage steady migration and early leveraging of low hanging fruit

The envisaged system does not necessarily replace any pre-existing systems, but instead offers a convenient path for existing systems such a core banking, accounting or ERPs to become participants into the distributed ledger. Such participation early on could be one way publishing, but eventually could feed back information on the ledger back into the main systems. This sort of becomes a distributed, privacy maintaining bus.

## Structure of the platform

It is at this point imagined that the platform will be a combination of public and private/partitioned ledgers. The public data will be managed by a set of notaries who will perform the necessary activities to inject sufficient trust into the platform and to be able to run the smart contracts, even while retaining only partial visibility into the underlying data. The private data will be maintained by the wallet providers. 

The notaries will know how to address an interact with all wallet providers and within themselves form a federated, distributed cluster of systems keeping multiple copies of the public data in a chain (blocks or not). 

In general every transaction will identify the necessary wallets (and thus wallet providers) participating in the transaction. The initiating wallet provider (for one of the wallets) will interact with a notary (who could be randomly chosen since they will all be interchangeable) to submit a transaction request. The notary will ensure all wallet providers agree to the same set of data, and all necessary validations based on the underlying schema, regulations, and outstanding contracts if any are performed, and only if all tests are cleared will forward the transaction to at least two other (this could change) notaries (thus supporting digital persistence and integrity of the public information), trigger any further events as necessary, perform any smart contract activities if found appropriate and report the successful transaction back to the wallet providers. Through eventual consistency a consistent view of the public ledger will be shared across all notaries.

## Main parties

### Entity: 

Entities are legal persons. Human beings, corporations, trusts, associations etc which participate in economic activities. Each entity will have a globally unique identifier. This could be correlated with say the Aadhaar id etc for KYC purposes.

### Wallet providers:

Wallet providers will be agencies which maintain and operate a wallet on user's behalf. These could be banks, nbfcs, micro finance agencies, conventionally understood wallet providers such as PayTM etc. The responsibility of a wallet provider will be to keep detailed record of the transactions and interact with the ecosystem for appropriate purposes such as executing smart contracts. Wallet providers will not be able to update wallet transactions by themselves. Such transactions should always be initiated by a user or should be a consequence of a smart contract. There will be two types of wallet providers - a) Third party wallet providers or b) Self hosted wallet provider. The latter will allow entities higher level of control and privacy over the transactions, but this could result in transaction/aggregate limits on self hosted wallet providers for purposes of AML, Transaction Monitoring etc. The primary intent of self hosted wallets is to allow entities to interact with other peers while keeping direct control on the value/information being stored (think of it as a wallet one carries in his pocket)

### Notaries:

Notaries are a federated group of systems who validate state creation and transactions, and who while not storing all the data will store a fingerprint of every transaction as a chain of transactions. They can assert existence of transactions based on publicly available information, and if someone has full data about the transaction, they can assert its validity. While detailed data will be stored only by the concerned wallet providers participating in a transaction, notaries will inject necessary trust to ensure that the wallet providers cannot subsequently modify attributes of the transaction. Notaries can also be used to implement a full permissioned but publicly visible chain, if the data stored is not sensitive or private.

## Important domain model constructs

### Wallets:

Wallets will be repository of value and/or information. Wallets could contain one or more types of value/information. Each wallet will be owned by one or more entities (in case of joint wallets). Each wallet will have a globally unique identifier. Wallets will contain value stores. In general wallet creation should be cheap and easy so that segmentation and participation in smart contracts would be easy. However wallet providers should be able to collaborate in a manner so that any total limits across wallets can be enforced. Easy wallet creation can also help tagging separate wallets eg. for intent or purpose which could allow additional validations against expenditure from or receipts into such wallets. Also meta information around wallets could help influence drive different levels of observability for economic activity and monitoring for regulatory purposes. Since the system except for regulatory purposes should be consent driven, tagging consents with wallets would be far easier than tagging individual transactions.

### Value store:

Value stores are information records which are owned by some wallet and have some associated value. Examples of states are IOUs, einvoices, eWay bills, etc. 

### Transaction:

A transaction will be a record of atomic collection of changes to states of various value stores

### References:

References are static or dynamic pieces of information cross referenced by either a state or a smart contract. References could be value stores themselves. A value store may refer to one more references. References may have their own event transitions which are tracked by the system, and may result in smart contracts on other states dependent on such references getting triggered. An example of a dynamic reference could be stock price, or commodity price which will have to be discovered at a future point in time. At this point in time it is thought that reference would be some kind of a unique URL identifying the reference, and perhaps a resolver URL for dynamic references. References unless they are value stores will not be associated with a wallet

### IOU:

IOUs are value stores and records of a liability from the issuing wallet to the receiving wallet for a given amount of units. The owner shall be the receiving wallet id. These create and maintain a record of many of the assets and liabilities as a part of the overall economic activity. They could have a number of additional attributes such as but not limited to

* *Issued*: Issue time
* *Callable*: Does it require recipient explicitly calling for payment 
* *Due*: Timestamp when it becomes due
* *Transferable*: Can the current lender transfer it to another lender without a borrower's consent
* *Unit of Measurement* : eg. I owe someone else 5 gms of gold. For bank accounts etc it will be the central bank currency

### Smart Contracts: 

Smart contracts are pieces of computer code that are associated with events or time which trigger some activity on associated references. Thus a smart contract could be programmed to pay back certain amount of money when the IOU becomes due and is not callable. Smart Contracts will perform all pre-authorisations necessary at creation time and will have a delegated capability to perform value transfer (or any other activities) in an unattended or automated way.

### Digital Currency/Notes:

These are a special version of IOUs where the issuer is the central bank of the country. These notes will not be callable, will never become due and will be transferable, and will be denominated in central bank currency. (eg. unit of measurement would be a Rupee)

### Value cards:

These would be hardware based cards (or smartphone/computer based data records + associated app) which securely store interact with remote value stores, in a wallet that is directly associated with the card. As envisaged at the moment this would need a rudimentary LCD display, basic Near Field Communication capabilities, and Yes/No/Cancel buttons. The hardware would allow appropriate records to be digitally signed and transferred to other cards. These would predominantly be reactive, and at least one out of multiple wallets in a transaction will need to be hosted by a smart phone / computer to have the necessary hardware to initiate the overall transaction. It is thought that in most cases at least one of the value cards will have active internet connectivity. Transactions can be conducted in absence of internet connectivity but will not be treated and validated until the designated value card gets some form of internet connectivity. 

## Additional Notes (Much of this will be detailed further .. this is all work in progress):

### 1. Schema and structure of ledger for Issuance of and transferring of digital currency and CASA operations

* *Create value store for 1,00,000*

> | State ID | State Type | IOU Type | From Wallet ID                            | To Wallet ID | UOM  | Amount |
> | -------- | ---------- | -------- | ----------------------------------------- | ------------ | ---- | ------ |
> | S1       | IOU        | DC       | RBI1 *(Special Wallet with Magic Powers)* | RBI1         | INR  | 100000 |
>
> 
>
> | Transaction ID | Dropped States | Created States |
> | -------------- | -------------- | -------------- |
> | T1             |                | S1             |

* *Transfer 10,000 to a bank Bank1*

> | State ID | State Type | IOU Type | From Wallet ID                            | To Wallet ID | UOM  | Amount |
> | -------- | ---------- | -------- | ----------------------------------------- | ------------ | ---- | ------ |
> | S2       | IOU        | DC       | RBI1 *(Special Wallet with Magic Powers)* | RBI1         | INR  | 90000  |
> | S3       | IOU        | DC       | RBI1                                      | B1DC         | INR  | 10000  |
>
> 
>
> | Transaction ID | Dropped States | Created States |
> | -------------- | -------------- | -------------- |
> | T2             | S1             | S2, S3         |

* *User deposits 20,000 paper currency and opens an account with B1 for 18000 Rs also transfers 2000 of digital currency to his personal wallet on card*

  

> | State ID | State Type | IOU Type | From Wallet ID | To Wallet ID | UOM  | Amount |
> | -------- | ---------- | -------- | -------------- | ------------ | ---- | ------ |
> | S4       | IOU        | BA       | B101           | U1B1         | INR  | 18000  |
> | S5       | IOU        | DC       | RBI1           | U1P1         | INR  | 2000   |
> | S6       | IOU        | DC       | RBI1           | B1DC         | INR  | 8000   |
>
> 
>
> | Transaction ID | Dropped States | Created States |
> | -------------- | -------------- | -------------- |
> | T3             | S3             | S4, S5, S6     |

* User U1 pays User U2 1000 Rs digital currency and 4000 Rs of bank account deposit. 

> | State ID | State Type | IOU Type | From Wallet ID | To Wallet ID | UOM  | Amount |
> | -------- | ---------- | -------- | -------------- | ------------ | ---- | ------ |
> | S7       | IOU        | BA       | B101           | U1B1         | INR  | 14000  |
> | S8       | IOU        | DC       | B101           | U2B1         | INR  | 4000   |
> | S9       | IOU        | DC       | RBI1           | U1P1         | INR  | 1000   |
> | S10      | IOU        | DC       | RBI1           | U2P1         | INR  | 1000   |
>
> 
>
> | Transaction ID | Dropped States | Created States  |
> | -------------- | -------------- | --------------- |
> | T4             | S4, S5         | S7, S8, S9, S10 |

### 2. Unified payments

Since digital currency on a card in physical possession, bank accounts, credit card accounts, BNPL accounts, etc etc can all be represented by a combination of a IOU and a transaction on the ledger, payments become a lot more simplified since irrespective of the type of source or destination wallet, the nature of payment always remains the same, move some value from the source wallet to the destination wallet. 

### 3. Sample Smart Contract

This textual description is a place holder for a much more detailed explanation in data terms how exactly a smart contract could work. 

For simplicity it is assumed that a PO / Invoice consists of only 1 item here. 

A PO might specify an order which says the buyer B1 wishes to order an item of goods G1 of say 10 units at Rs 100 each for a total of 1000 Rs from Seller S1. The PO further specifies that any goods received but not returned within 5 days of receipt will result in an automatic creation of an IOU for the amount (1000 Rs), and the buyer supplies their wallet id and performs the necessary pre-authentication to create an IOU and eventually make the payment later on expiry of the IOU. 

Assuming that the eWay bill has a reference to the PO number (or eWay -> Invoice -> PO Number) the system can now await the creation of the eWay bill, track it to its end state, and then wait another 5 days to see if the goods are being returned. If these goods are not returned, the system will initiate an IOU between the two parties. The seller could choose to finance/factor the IOU or await the payment after 45 days. The IOU is a authenticated collateral for such a transaction. On completion of 45 days, the system could initiate the auto transfer (given it has the pre-authorisation to do so) assuming there are sufficient funds in the source wallet. (This could either be digital cash or bank balance .. not material here). If there are insufficient funds, the system could first raise a credit event which could alert a number of credit monitoring sources. Further the system could make further transactions for the buyer harder by making it harder for him to conduct the business due to negatively impacted payment or collection capabilities or some other penalties until the buyer does settle the IOU. This system of additional inconveniences needs to be further explored. 

In case of retail situation, one could replace the IOU with a credit card EMI charge (the pre-authorisation having been already received on dispatch of goods) or appropriate transaction on a BNPL card.

### 4. Supporting of data requests

#### 4.1 Authentication

Any party having full access to the detailed data can request a authentication of the existence of the transaction by providing the necessary information (eg could be public attributes plus a hash of all other information) and any notary could revert with authentication of the same

#### 4.2 Data requests

Any party requiring access to private data after the transaction has been processed, can create a request for such information which would first need to get routed to the appropriate wallet provider(s), who would authenticate such a request. In many cases the wallet provider itself will be able to revert with most of the data (since each wallet provider retains a copy of the transaction) which can then be submitted for authentication to the notary. It could also be feasible if necessary for the source wallet provider to sign a request and then route it to counterparty wallet providers, though given that notaries can authenticate such data, it may no longer be necessary. Data requests could be useful for processes such as loan approvals etc. Further additional information such as number of wallets etc could be validated by notaries themselves based on a signed request of an entity given that notaries will have visibility into existence of all such wallets. This information could be useful to banks, NBFCs, MFAs etc etc.







