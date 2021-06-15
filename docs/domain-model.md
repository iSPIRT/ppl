# CBDC Domain Model



-- Dhananjay Nene 

[TOC]



- v1.0 25/4/2021



## Objective

This document proposes a domain model to further discussions on what are the essential domain elements of a CBDC for India. It is too early to be even remotely considered a proposal, is merely a first draft for the sake of being able to start and catalyse the thinking process around the same. 

By domain model I specifically refer to important abstractions that could make sense to practitioners of the domain (eg central bankers or transaction bankers). It eschews both the usability aspects (the fine details but not the major components of how the users interact with the domain) and the techonology implementation issues .. leaving both to be worked through later once the domain model is considered somewhat satisfactory. It does not avoid the specific discussion of either but prefers not to go into any significant details with them. 

One of the important aspects of the CBDC domain is that while it can be guided by existing domain experts, it is also an emergent domain, thus while it can treat the existing physical currency domain as a reference, it will need to explore a lot of new thoughts and ideas with respect to how this domain could evolve especially given the difference in characteristics of electronic vs physical renderings of a currency. 



## Background

### Currency

Currencies have evolved from having inherent value (metal coins) to proxy value (gold backed paper notes) to sovereign promise value (contemporary fiat currencies) to scarcity based electronic manifestations (crypto). Since a CBDC is essentially likely to complement a fiat currency, that is the reference meaning used generally though crypto will be relied upon quite a bit because of the significant technological innovations that have already been deployed in making them usable. 

This document refers to a candidate model for CBDC Rupee where in the future the physical, contemporary banking system electronic rupee and a digital currency manifestation will all be easily interchangeable versions of each other. The specifics of such an interchange are beyond the scope of this dicussion. 



### IOUs and Money Multiplier

While not particularly meaningful, contemporary physical currencies are in literal terms IOUs (I Owe You) issued by the central bank. However when such currencies circulate through the economy, injection of some amount of additional currency results in an increase in income that is substantially higher than the amount of currency injected, a factor often referred to as the money multiplier. Some part of this additional income is due to the creation of additional IOUs in the system between private parties, which encourages amplification of economic activity.



### IOUs as a record of economic activity

While this document does not conflate IOU with currency (only an IOU issued by the central bank is a currency), it does assert that recording IOU creations and closure along with currency transfers create a better representation of the economic activity. Importantly, in addition, by bringing in IOUs into the fold of a CBDC system (emphasis on system), it encourages traceable settlements of such IOUs using currency and in fact also allows such settlements to be automated or programmatically managed.



## Participants in CBDC

Any CBDC system will obviously eventually encourage participation and interaction with it from everyone who does economic activity using such a currency, but it is important to understand the more important roles. While there are many important players today, in an electronic version, more could need to be identified.

### Central Bank

In India this would be RBI. This is the bank which issues at will new currency into the system, and can choose to extinguish whatever currency it has access to as well at any point in time. While RBI serves a lot of additional responsibilities, for the purposes of this documents, this will be the primary role it will play in addition to those related to creation and governance of such a CBDC system. 

### Wallet Providers

Banks today collect deposits, disburse loans, and perform electronic money transfers apart from many other activities. Given that the nature of a digital currency is somewhat different (eg. it is easily cloneable unlike physical currency), and the significant importance of banks, an evolution of the currency will likely continue to see banks playing a significant role. NBFCs and Digital Wallet Systems also play roughly similar roles. They are indeed different from banks, but for the purpose of this document (given the high level) they are clubbed together under wallet providers 

### Entities (Legal Persons, People, Associations, Trusts, Companies etc)

These are the users of the digital currency or for that matter even peer to peer IOUs

### Notaries

This is a new role which will be detailed further. Suffice to say at this stage, any currency transfer is valid only once it is successfully notarised by the notary also participating in the digital record of the transfer. For purposes of healthy competition, redundancy and scalability, there will be a number of different notaries, who will be federated with some central management to ensure system level sanity and integrity. While banks could play the role of notaries, for the purposes of this dicussion notary is an independent role, and a lot of the contemporary payments processing responsibilities are transitioned from banks to notaries.

## Important artifacts in the CBDC system

Apart from the participants the following are some of the important conceptual elements of the CBDC system

### Wallets

Wallets are the logical equivalents of accounts, except that they have a broader scope. They need not be held with a bank or a NBFC etc. Every entity can create as many wallets as it wishes. Some of it may be entirely self created and operated (eg. digital equivalent of the leather wallet I carry in my back pocket). Some others would be created in collaboration with wallet providers. Any transactions that are done using a wallet that is maintained by a wallet provider will require the wallet provider to participate in the same as well (not clear at this stage if the participation is immediate or could be in the future as well). Wallets shall be repository of value .. either as digital currency or assets in form of IOUs, whereas they can also reflect liabilities as issued IOUs. There will be at least one special wallet .. which is the wallet into which fiat currency is brought to life and is extinguished from. This wallet shall be controlled and managed by the central bank. And any IOUs issued from this wallet into other wallet shall effectively form the currency holding of the owning wallet. 

From a system perspective wallets can be associated with constraints/metadata such as reporting, transaction amounts, signing authorities etc etc

### IOU

An IOU is an acknowledgement of liability by an issuer to a recipient. It could just be authored by the issuer alone. It will have a few more characteristics such as (question marks at end indicate optional fields)

- Issuing wallet and receiving wallet
- Unique id and issuing timestamp (for obvious reasons)
- Callable? - An IOU can be attempted to be autoconverted into currency holdings or can be explicitly done so only when the owning wallet explicitly calls for it
- Due? - can be any timestamp at or after issuing timestamp. An IOU can be attempted to be converted into currency only at or after due timestamp. An absent due value indicates the IOU is due at any time but must be explicitly converted only when called, no autoconversion allowed.
- Expires? - An IOU will be worthless if it has a expiry and the expiry timestamp is in the past and can no longer be converted. 
- Transferable - A transferable IOU can be transferred by the owner to another party (just like endorsing a cheque if it is allowed to be transferable). By default all currency IOUs will be transferrable

Note that IOUs can be strictly bilateral and do not require another party to attest the same. Offline payments will be initiated as a bilateral IOU which can be converted to value when appropriate connectivity is established. An IOU needs to be signed at least by the issuer

### Transactions

Transactions are essentially transfers of IOU from one wallet into another. Sometimes they just might record IOUs getting created. The underlying IOUs obviously need to be transferrable. A transaction may combine multiple IOUs into one or split one into many (or in extreme cases do both simultaneously). Transactions need to be signed by either the payer(s) and/or the payee(s) and in addition have to submitted to the notaries who will verify and then appropriate log the same as necessary into an immutable system of record. The exact scope of permissions around such a system and considerations around access control/privacy/surveillance of such a system of record. Obviously blockchain will be used as one of the references to evolve such a system, but its too premature to conceptualise such a design in any level of detail

