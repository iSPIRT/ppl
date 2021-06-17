# Code for FAILED attempts at use of libsnark and qaptools backends as
# a python library. This is checked in because we might want to give
# it another shot at a later time. Search for XXX to see the specific
# points where there was a failure

from contextlib import contextmanager
import logging
import os
from pathlib import Path
from shutil import copy
import sys
import tempfile
import unittest

from pysnark import runtime as pysnark_runtime
from pysnark.qaptools import backend as qaptools_backend
from pysnark.libsnark import backend as libsnark_backend

logger = logging.getLogger("snark_test")


@pysnark_runtime.snark
def cube(x):
    return x*x*x


@contextmanager
def cd(path):
    old_dir = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old_dir)


@unittest.skip('This does not work at all')
class QAPToolsTest(unittest.TestCase):
    '''Using the qaptools backend'''
    def test_threephase_xcube(self):
        # Unfortunately pysnark litters the current directory
        # with hardcoded filenames, so we create
        # temporary directories and cd there
        pysnark_runtime.backend = qaptools_backend
        with tempfile.TemporaryDirectory() as temp_root:
            # To make sure that we understand the usage of the
            # different files properly, we use 3 different directories:
            # master_dir for one-time keypair generation
            # prover_dir for the proof and verifier_dir for verification
            root_dir = Path(temp_root)
            master_dir = root_dir/'generator_dir'
            prover_dir = root_dir/'prover_dir'
            verifier_dir = root_dir/'verifier_dir'
            master_dir.mkdir()
            prover_dir.mkdir()
            verifier_dir.mkdir()
            
            m2p_files = ('pysnark_schedule', 'pysnark_masterek',
                         'pysnark_ek_main', 'pysnark_eqs_main',
                         'pysnark_masterpk')
            m2v_files = ('pysnark_schedule', 'pysnark_masterpk',
                         'pysnark_vk_main')
            p2v_files = ('pysnark_proof', 'pysnark_values')
            masteronly_files = ('pysnark_mastersk',)
          
            with cd(master_dir):
                # phase 1, generate
                # make sure the files don't already exist
                for file in m2p_files + m2v_files:
                    assert(not Path(file).exists())
                 
                out = cube(3)
                pysnark_runtime.backend.prove()

                assert(Path('pysnark_mastersk').exists())
                # must delete this file: this is the master secret key

                # send these files to prover
                for file in m2p_files:
                    copy(Path(file), prover_dir/file)

                # send these files to verifier
                for file in m2v_files:
                    copy(Path(file), verifier_dir/file)

            with cd(prover_dir):
                # phase 2, proof
                for file in p2v_files:
                    assert(not Path(file).exists())

                # XXX: the `prove` call below fails for reasons I
                # don't completely understand. Do we need to re-run
                # the computation here? Do we need to reinitialize the
                # backend? Couldn't find a combination that worked
                pysnark_runtime.backend.init()
                out = cube(3)

                pysnark_runtime.backend.prove()

                for file in masteronly_files:
                    # make sure that a new keypair did not get generated
                    assert(not Path(file).exists())

                for file in p2v_files:
                    copy(Path(file), verifier_dir/file)

            with cd(verifier_dir):
                # phase 3, verification
                libsnark = pysnark_runtime.backend.runqapver.run()
                # this gives an exception if verification failes


@unittest.skip("Broken because of shared data between master and verifier")
class LibSnarkTest(unittest.TestCase):
    '''Using the libsnark backend

    This is libsnark, non-groth version

    This test passes, but it is broken because verifier does not have
    a readymade function to read either pysnark_vk or pysnark_log to
    get the vk, pubvals, proof values needed for verification
    '''
    def test_threephase_xcube(self):
        # Unfortunately pysnark litters the current directory
        # with hardcoded filenames, so we create
        # temporary directories and cd there
        #
        with tempfile.TemporaryDirectory() as temp_root:
            # To make sure that we understand the usage of the
            # different files properly, we use 3 different directories:
            # master_dir for one-time keypair generation
            # prover_dir for the proof and verifier_dir for verification
            root_dir = Path(temp_root)
            generator_dir = root_dir / 'generator_dir'
            prover_dir = root_dir / 'prover_dir'
            verifier_dir = root_dir / 'verifier_dir'
            generator_dir.mkdir()
            prover_dir.mkdir()
            verifier_dir.mkdir()
          
            with cd(generator_dir):
                # phase 1, generate
                # create the keypair and write pysnark_ek and pysnark_vk
                # pysnark_ek contains both, proving key and verification key
                # pysnark_vk contains the verification key

                # do the computation
                out = cube(3)
             
                # this does the keypair generation
                pysnark_runtime.backend.prove(
                    do_keygen=True, do_write=False, do_print=False)
                assert(Path('pysnark_ek').exists())
                assert(Path('pysnark_vk').exists())
                assert(not Path('pysnark_log').exists())
             
                # copy the keypair to the prover 
                copy(Path('pysnark_ek'), prover_dir / 'pysnark_ek')
             
                # copy the verification key to the verifier
                copy(Path('pysnark_vk'), verifier_dir / 'pysnark_vk')
             
            with cd(prover_dir):
                # phase 2, proof
                assert(Path('pysnark_ek').exists())
                assert(not Path('pysnark_vk').exists())
                assert(not Path('pysnark_log').exists())
                vk, proof, pubvals = pysnark_runtime.backend.prove(
                    do_keygen=False,
                    do_write=True,
                    do_print=False)
                assert(Path('pysnark_log').exists())
                # copy the proof to verifier dir
                copy(Path('pysnark_log'), verifier_dir / 'pysnark_log')

            with cd(verifier_dir):
                # phase 3, verification
                # This is broken
                # Ideally we should be able to read the
                # verifier key from pysnark_vk and the pubvals and proof
                # from pysnark_log
                # But pysnark doesn't give us functions to do either
                # So we are just going to fake it here until
                # (or we have to hack it at some point in the future)
                # 
                # For now we directly take vk, pubvals, proof
                # variables from prover
                #
                # I tried writing the vk, pubvals, and proof into
                # files using vk.str(), pubvals.str(), and proof.str()
                # and then later reading them in and re-instantiating
                # them using the `fromstr` method on the 3 relevant
                # classes. But that did not work reliably. It would work
                # sometimes, give segmentation violations sometimes, and
                # would go into an infinite loop sometimes.
                libsnark = pysnark_runtime.backend.libsnark
                verifier = libsnark.zk_verifier_strong_IC
                assert(verifier(vk, pubvals, proof))

if __name__ == '__main__':
    unittest.main()
