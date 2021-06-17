# ppl

## Setup / Installation

Install the packages listed in requirements.txt. For example, using:

    pip install -r requirements.txt

Install qaptools

    git clone git@github.com:Charterhouse/qaptools.git
    cd qaptools
    git submodule init
    git submodule update
    mkdir build
    cd build
    cmake ..
    make    

Note: you might have to install cmake to do this. Note the location of
the build directory.

Run the tests:

    cd tests
    cp config_example.py config.py
    # edit the file and set the correct values for
    # the path of the python executable and the
    # QAPTOOLS_BIN directory (pointing to the build directory)
    # created above

    cd ..
    python -m unittest tests.pysnark_test
