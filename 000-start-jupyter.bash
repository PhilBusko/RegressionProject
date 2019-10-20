#!/bin/bash

source $HOME/myData/BASH
source $HOME/myData/CONDA

condaStart
condaEnv pycpu

#mongod --dbpath data-final &
#sleep 30

jupyter notebook
condaStop

exit 0
