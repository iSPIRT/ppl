
Some Zokrates programs (.zok) and generators for Zok programs here which can be used for ZK proofs.

INSTALLATION of Zokrates: 

On a Linux (Ubuntu 18.04) machine, the curl method from https://github.com/Zokrates/ZoKrates#readme
The version of the Zokrates system (compiler) where the below was tested is version 0.7.7 ( https://github.com/Zokrates/ZoKrates/releases/tag/0.7.7 )

See https://zokrates.github.io/ for Zokrates documentation.


Eg1 : 
	generate_hash_zok.py : A python program that prints a .zok program to output the hash corresponding to 
                               the root of a 'poseidon-hash' tree. There are here two manually written .zok programs
                               that are meant to validate the output of the .zok program generated by generate_hash_zok.py
                               To generate a .zok program for the poseidon tree hash corresponding to a "state" of 50 fields,
                               execute the command :
                                     python generate_hash_zok.py 50

        In the below, generated_pos_14.zok is the output generated by the command  :    python generate_hash_zok.py 14
        In the below, case_14.zok is the manually created .zok program to compute the corresponding poseidon tree hash  
        when the state to be hashed consists of 14 zok fields. We also present the respective witnesses of the output
        corresponding to these two distinct .zok programs for the same 14 field input; and grepping 'out' in the two 
        witness files shows that the poseidon hash tree output for the manual .zok matches the poseidon hash tree output
        for the generated .zok program on the same input.
        

        case_14.zok, witness_14 : Manually written zok program and witness for the zok program on execution of 
                                  the zokrates cli command sequence:
                                  zokrates compile -i case_14.zok
                                  zokrates setup
                                  zokrates compute-witness -a 0 1 2 3 4 5 6 7 8 9 10 11 12 13
                                  zokrates generate-proof
                                  zokrates verify
                                  cp witness witness_14
				  
        gen_pos_14.zok, witness_gen_14 : Generated zok program and corresp witness for the zok program on execution of 
                                  the zokrates cli command sequence:
                                  zokrates compile -i gen_pos_14.zok
                                  zokrates setup
                                  zokrates compute-witness -a 0 1 2 3 4 5 6 7 8 9 10 11 12 13
                                  zokrates generate-proof
                                  zokrates verify
                                  cp witness witness_gen_14
        grepping on "out" in the two witness files witness_14 and witness_gen_14 confirms the same poseidon hash tree output for the same.

        Other such manual-generated .zoks and witnesses are :
          case_41.zok, witness_41, gen_pos_41.zok, witness_gen_41
          case_99.zok, witness_99, gen_pos_99.zok, witness_gen_99