#!/usr/bin/env python

import sys
max_poseidon_arity = 6

#Zok program that given an N-field input OrigInp will generate 
#a tree in which the N OrigInp fileds form the leaf-layer
#and each parent is a poseidon hash. The arity of each poseidon 
#hash is governed by the HashSeq array, which is computed 
#quite simply in the prepare_zok_args function

hashgen_zok = """
import "hashes/poseidon/poseidon" as poseidon 
import "utils/casts/u32_to_field" as u32_to_field
import "utils/casts/field_to_u32" as field_to_u32


const u32 N = %s 
const u32 INTERNAL_NODES = %s
const u32[INTERNAL_NODES] HashSeq = %s

def main(field[N] OrigInp) -> field:
    u32 HeapSz = INTERNAL_NODES+N
    field[HeapSz] Heap = [0; HeapSz]
    //Initialize to 0 field

    u32 j = 0
    for u32 i in 0..N do
       j = (HeapSz-1)-i
       Heap[j]=OrigInp[(N-1)-i]
    endfor
    //The last N nodes of the Heap field array are set to the input fields

    u32 leftChildOffset = HeapSz
    u32 parent = INTERNAL_NODES
    for u32 i in 0..INTERNAL_NODES do
       parent = parent-1
       leftChildOffset = leftChildOffset-HashSeq[i]
       Heap[parent] = poseidon(Heap[leftChildOffset..leftChildOffset+HashSeq[i]])
    endfor
    return Heap[0]
"""

#function that takes the number of fields in the transaction that
#needs to be hashed and generates an appropriate Zok program from 
#hashgen_zok. 
def print_zok_program(NumInputs) :
    levelSz=NumInputs
    if levelSz <= max_poseidon_arity:
        hash_seq = [levelSz]
    else: 
        hash_seq = []
        while levelSz > 1:
            if levelSz%max_poseidon_arity==0:
                nextLevelSz = levelSz//max_poseidon_arity
                hash_seq += [max_poseidon_arity]*nextLevelSz
            else:
                nextLevelSz = levelSz//max_poseidon_arity+1
                hash_seq += [max_poseidon_arity]*(levelSz//max_poseidon_arity)+[levelSz%max_poseidon_arity]
            levelSz = nextLevelSz
    #print(levelSz)
    #print(hash_seq)
    print(hashgen_zok%(str(NumInputs),str(len(hash_seq)),str(hash_seq)))



if __name__ == '__main__':
  print_zok_program(int(sys.argv[1])) 




