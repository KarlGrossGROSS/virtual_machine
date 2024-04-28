#!/usr/bin/env python3

import pytest
import sys
import os


from assembler import *
from vm import *



def test_one(): #do I have to create a seperate file for the actual output? or can I just compare the output of assembly program directly with the file I wrote expected output?
    with open ("expected_output.mx", "r") as hexadecimal:
        f = hexadecimal.readlines()
    with open("testing_assembly.as", "r") as assembler:
        m = assembler.readlines()
    a = Assembler()
    expected = [i.rstrip("\n") for i in f]
    actual = a.assemble(m)
    assert actual == expected, "Assembler class produces different output/hexadecimal numbers"

def test_vm(): #if I should create a new file for the output of assembly as noted in test_one, you should use it here instead of expected_output
    with open ("expected_output.mx", "r") as vm_in:
        f = vm_in.readlines()
    f = [i.rstrip("\n") for i in f]
    f = [int(i, 16) for i in f]
    with open ("777.mx", "r") as vm_expected:
        c = vm_expected.readlines()
    c = [i.rstrip("\n") for i in c]
    vm = VirtualMachine()
    vm.initialize(f)
    vm.run()
    with open("actual_output_vm.mx", "w+") as vm_out:
        vm.show(vm_out)
    with open("actual_output_vm.mx", "r") as vm_out:
        actual = vm_out.readlines()
    actual = [i.rstrip("\n") for i in actual]
    print(actual)
    expected = c
    assert actual == expected, "test_vm does not work correctly"

def test_out_of_memory():
    #out_of_memory.mx
    with open ("out_of_memory.mx", "r") as vm_in:
        f = vm_in.readlines()
    f = [i.rstrip("\n") for i in f]
    f = [int(i, 16) for i in f]
    vm = VirtualMachine()
    actual = None
    
    try: #try block is for catching AssertionError in vm.py, else it will be skipped and actual remains with value None
        vm.initialize(f) 
    except AssertionError:
        actual = AssertionError

    expected = AssertionError
    assert actual == expected, "AssertionError not raised for out_of_memory input"



def test_instruction_not_found(): # I am not sure about catching assertion and IndexError together!
    #instruction_not_found_error.mx, error is in line 2 register 9, in the middle!, line 5: 010304, line10: 0b0009
    with open ("instruction_not_found_error.mx", "r") as vm_in:
        f = vm_in.readlines()
    f = [i.rstrip("\n") for i in f]
    f = [int(i, 16) for i in f]
    vm = VirtualMachine()
    vm.initialize(f)
    actual = None
    try: #try block is for catching AssertionError in vm.py, else it will be skipped and actual remains with value None
        vm.run()    
    except AssertionError:
        actual = AssertionError
        expected = AssertionError
    except IndexError: #if register nr. is too large, small, not existent!
        actual = IndexError
        expected = IndexError
    
    assert actual == expected, f"{actual} not raised for instruction_not_found_error"
    
#if __name__=='__main__':
#    test_one()
#    test_vm()

#for test coverage type this: coverage run -m pytest
#coverage report -m

