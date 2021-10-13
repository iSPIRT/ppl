from contextlib import contextmanager
import logging
import os
from pathlib import Path
from shutil import copy
import subprocess
import tempfile
import unittest

from . import config

logger = logging.getLogger("snark_test")


@contextmanager
def cd(path):
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)


class QAPToolsTest(unittest.TestCase):
    '''Simple snark implementation Using the qaptools backend

    Unfortunately, pysnark doesn't really insulate us
    from the internals of the backends, so the usage
    is different for each backend.

    Also, pysnark appears to be designed purely as a command line
    utility that uses hardcoded filenames. A couple of attempts to use
    it as a library failed (see pysnark_aslib_broken_test.py for
    details). So that's what we're doing.
    '''
    def setUp(self):
        self.env = {'QAPTOOLS_BIN': config.QAPTOOLS_BIN,
                    'PYSNARK_BACKEND': 'qaptools'}


    def do_three_phases(self, codefile, *args):
        '''Run the master/generator, prover, and verifier for codefile

        The prover is run for "codefile *args"
        Note: codefile must be a string representing a file
        that exists in the same directory as this test.
        '''
        # Unfortunately pysnark litters the current directory
        # with hardcoded filenames, so we do this in
        # a temporary directory

        print(" # phase 0, codefile ",codefile,"args",args)
        codepath = Path(__file__).parent/codefile
        with tempfile.TemporaryDirectory() as temp_root:
            # To make sure the master, prover, and verifier
            # are insulated from each other, we create 3 different
            # for them
            # master_dir for one-time keypair generation
            # prover_dir for the proof and verifier_dir for verification
            root_dir = Path(temp_root)
            master_dir = root_dir/'master_dir'
            prover_dir = root_dir/'prover_dir'
            verifier_dir = root_dir/'verifier_dir'
            master_dir.mkdir()
            prover_dir.mkdir()
            verifier_dir.mkdir()

            # copy codefile to master and prover
            copy(codepath, master_dir/codefile)
            copy(codepath, prover_dir/codefile)

            # files created by master to be sent to prover
            m2p_files = ('pysnark_schedule', 'pysnark_masterek',
                         'pysnark_ek_main', 'pysnark_eqs_main',
                         'pysnark_masterpk')
            # files created by master to be sent to verifier
            m2v_files = ('pysnark_schedule', 'pysnark_masterpk',
                         'pysnark_vk_main')
            # files created by prover to be sent to verifier
            p2v_files = ('pysnark_proof', 'pysnark_values')

            # files that should never exist anywhere other than master
            masteronly_files = ('pysnark_mastersk',)

            # phase 1, master: generate keypair
            with cd(master_dir):
                print(" # phase 1, master: generate keypair")
                # make sure the files don't already exist
                for file in m2p_files + m2v_files:
                    assert(not Path(file).exists())

                subprocess.run((config.PYSNARK_PYTHON, codefile) + args,
                               check=True, env=self.env)
                assert(Path('pysnark_mastersk').exists())
                # master secret key: should be deleted

                # send these files to prover
                for file in m2p_files:
                    copy(Path(file), prover_dir/file)

                # send these files to verifier
                for file in m2v_files:
                    copy(Path(file), verifier_dir/file)

            with cd(prover_dir):
                # phase 2, proof
                print(" # phase 2, proof")
                for file in p2v_files + masteronly_files:
                    assert(not Path(file).exists())

                subprocess.run((config.PYSNARK_PYTHON, codefile) + args,
                               check=True, env=self.env)
                for file in masteronly_files:
                    # make sure that a new keypair did not get generated
                    assert(not Path(file).exists())

                for file in p2v_files:
                    copy(Path(file), verifier_dir/file)

            with cd(verifier_dir):
                # phase 3, verification
                print(" # phase 3, verification")
                subprocess.run((config.PYSNARK_PYTHON, '-m',
                                'pysnark.qaptools.runqapver',
                                codefile) + args,
                               check=True, env=self.env)
                # this should give an exception if verification fails
            print(" # Done")

    def test_trivial(self):
        '''A trivial test that simply computes a cube

        Input and output are both public. This is just to test
        The basic functionality
        '''
        self.do_three_phases('zkcube.py', '3')

    def test_hash(self):
        '''A minimal test with a witness

        Given a public hash value, prover uses a private input to computes
        the hash_value and checks that it matches the public value
        '''

        # successful computation
        self.do_three_phases('zkhash.py',
                             '12159113912127441302481669165612839028677601711152277646610726095099155477934',
                             '42')
        
        # also confirm that 41 is not the ultimate answer
        with self.assertRaises(Exception):
            self.do_three_phases(
               'zkhash.py',
               '12159113912127441302481669165612839028677601711152277646610726095099155477934',
               '41')

    def test_sumcheck(self):
        '''A test that checks if the first arg ('claim) is <= sum of second and third args
           Second and Third argument will be private in real app
        The basic functionality
        '''
        self.do_three_phases('zksumcheck.py', '100','27','73')
        with self.assertRaises(Exception):
            self.do_three_phases('zksumcheck.py', '101','27','73')

if __name__ == '__main__':
    unittest.main()
