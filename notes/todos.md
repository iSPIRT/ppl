# Todos



**<u>Overall goal is to first create as detailed a CBDC model as feasible</u>**

## Schema

* Cleanup - @dnene
* Complete all validations 
* Create capabilities to add a set of zkps (Nishith)
  * Enhance ZokratesModel class to 
    * Be able to interact with schema for claims etc
    * Be able to hold templates for code generation
    * Be able to interact with runtime for count of parameters (which in turn will lead to code generation)
  * Create ABCs that alternative ZKP models will all collectively implement
* Complete writing DSLs and merge it (Aditya Laghate)
* Figure out wallet operator and Notary Separation
* Allow specification of constant attribute values (eg. for cbdc the UOM is "cbdc_inr" .. **fixed**)



## Journal

* Create a journal module to allow clear communication from notary to journal api.
* This is where all the future concurrency related stuff will get merged

## ZKP

- Zokrates implementation of a stablecoin
  - Hash function
  - Simple transfer (1 input 1 output)
  - Multi-transfer (2 inputs 2 outputs)
  - Work on "generic" implementation
  - PoC for processes to be followed:
    - At the time of ledger creation
    - At the time of schema creation
    - For 2 parties to agree on a ad hoc proof
  - Different schemes:
    - G16
    - Marlin
    - Also different backends: bellman/libsnark/ark
  - Different hash functions:
    - Pedersen
    - Poseidon
    - MiMCHash?
    - SHA256
  - Performance test suite
    - Hashing strings of various lengths
    - Proof for basic 2x2 transfer transaction
    - Proof for 1xN transfer transaction (n=10,50,100,1000,10000)
    - Be able to easily run all the above with different schemes+hashfunctions
  - Implement common API
- Circom implementation of a stablecoin
  - Similar to Zokrates
  - Supported schemes and hash functions will be different
- Common API
  - Understand DSL requirements
  - Define common API based on Zokrates, Circom, and maybe one more
  - Write (failing) tests for the API


