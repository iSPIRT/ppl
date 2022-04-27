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
* 