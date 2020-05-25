import os
import subprocess as sp
import unittest



def run_unit_tests():
    os.chdir(os.getcwd() + "/../microservices/db/unittest")
    sp.call("python3 -m pip install -r ../requirements.txt", shell=True)
    sp.call("python3 -m unittest discover -s . -p '*_test.py'",shell=True)
    os.chdir(os.getcwd() + "/../../dispatcher/unittest")
    sp.call("python3 -m pip install -r ../requirements.txt", shell=True)
    sp.call("python3 -m unittest discover -s . -p '*_test.py'",shell=True)
    os.chdir(os.getcwd() + "/../../video-deleter/unittest")
    sp.call("python3 -m pip install -r ../requirements.txt", shell=True)
    sp.call("python3 -m unittest discover -s . -p '*_test.py'",shell=True)
    os.chdir(os.getcwd() + "/../../video-download/unittest")
    sp.call("python3 -m pip install -r ../requirements.txt", shell=True)
    sp.call("python3 -m unittest discover -s . -p '*_test.py'",shell=True)
    return True



if __name__ == "__main__":
    run_unit_tests()


