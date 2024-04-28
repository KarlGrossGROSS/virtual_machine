# exercise 1

## test_x.py: a file testing all functions for exercise 1

we import assembler.py file to test how the object and its function turn assembly code to machine code (hexadecimal) and vm to test if it produces correct output and executes all instructions correctly. All 11 instructions are written and used in one file. There was no need to create multiple ones. As discussed with Mr. Konstantinos in person in an office hour, we figured out that importing functions and files from other folders does not work on my machine, which is a MacOS. Mr. Konstantinos told me I should put everything I want to test in one file, exercise 1, and that I should mention this issue here and he will remember my case. Thank you!

# tests:

## test_one(): 
This tests whether the assembler.py generates hexadecimal code correctly using assembly code as input. As input for the instance "a" of Assembler() we read assembly code from "testing_assembly.as" and call it on function assemble(). We compare this output with an expected one we calculated manually in file "expected_output.mx".

## test_vm(): 
To test the VirtualMachine(), we take the output of assemble() function in the Assembler() instance, which is hexadecimal code, and give it to the VirtualMachine. It should run the instructions and calculate the output. We compare this output with the output claculated manually in file "777.mx".

## test_out_of_memory():
Here we test that for a given RAM capacity in VirtualMachine, if this capacity was exceeded, the programm shall raise an AssertionError. When initializing (using vm.initialize(program)) a VirtualMachine(), there is an assert checking whether the given program has at most the length of its RAM or not. We test this by providing "out_of_memory.mx" as our program, which has much more lines of code than what the VM can hold (more than 255). Thus, the program should crash. However, for our test to proceed correctly, we use the "try" and "except" block to catch the AssertionError in vm.py. The Except block changes the value of actual to AssertionError! If there was no AssertionError raised, which should be the case, the test will fail, as the actual value is None and the expected value is an AssertionError. 

## test_instruction_not_found(): 
Here we test if the program will behave as expected if we provided it with a code with unknown instructions. The program in this case should crash. "instruction_not_found_error.mx" contains instructions that are unkown specifically in lines 2, 5, 10. We read this file and give it as input to the VirtualMachine. If we run the VM with this program, two types of errors might occur (depending on the program we are testing), AssertionError or IndexError. Using the try and except block method as in the test before will ensure that our test itself does not crash due to the self-made error that occured. *Note: In the try block, the except AssertionError is not necessary for this case in our implementation, however it might be for the future, as it can occur in the else-condition in the run(self) function in vm.py.

## Terminal:
to run all these tests in Terminal on Mac, we import pytest in the file test_x.py. In terminal on macos, we navigate to the Folder, where our test is. We then type the command: pytest. This will run all files that start with "test_" in this case only "test_x". The interface then shows all details concerning the passed and failed tests.

# Test coverage: To test the coverage of the test, one has to install the following in his terminal fist: "pip install pytest-cov"
Afterwards, navigate to the folder exercise 1 and type "coverage report -m" then enter. One can see that the coverage indicates the following: In the first column there is the name of the files that have been tested plus the testing file itself. In column 2 there's the number of statements that we covered in our test. Then, in column 3, the missing statements that were not covered. The coverage percentage for every file is shown in column 4, whereas column 5 denotes the lines that were not covered for each file. In the last row, one can see the TOTAL of each column of the first 4 columns.


# VM Instruction Disassembler

## Overview
This Python script serves as a disassembler for a simple virtual machine (VM). It converts VM instructions, written in hexadecimal format in a `.mx` file, into readable assembly language commands and writes them to an `.as` file.

## Features
- **Support for Various Instructions**: Handles instructions such as `hlt`, `ldc`, `ldr`, `cpy`, and more.
- **Direct Mapping**: Translates VM instruction codes to corresponding assembly mnemonics.
- **Command-Line Interface**: Easy execution from the command line.

## Instruction Set
The script recognizes the following VM instructions:
- `hlt` - Halt program
- `ldc` - Load value into a register
- `ldr` - Load from one register to another
- `cpy` - Copy between registers
- `str` - Store register value in memory
- `add` - Add register values
- `sub` - Subtract register values
- `beq` - Branch if equal
- `bne` - Branch if not equal
- `prr` - Print register value
- `prm` - Print memory at register


## Example
Input (input.mx):
```bash
000102
000203
```


Output (output.as):
```bash

ldc R1, @002
ldr R2, R3
```




## Usage
Ensure you have two files:
1. An input file (`input.mx`) with VM instructions in hexadecimal.
2. An output file (`output.as`) for the assembly code.

Run the script in the command line:
```bash
python disassembler.py input.mx output.as
```





# vm.py 

This README provides an overview and description of the virtual machine implemented in the given Python code. The virtual machine operates with a simple architecture and executes a program defined in a custom assembly-like language.

## Table of Contents
1. [Overview](#overview)
2. [Initialization](#initialization)
3. [Instruction Fetching](#instruction-fetching)
4. [Program Execution](#program-execution)
5. [Instructions](#instructions)
6. [Command-Line Usage](#command-line-usage)

## Overview

The virtual machine is designed to execute programs represented in a custom assembly language. It utilizes a simple architecture with a specified number of registers (`NUM_REG`) and RAM size (`RAM_LEN`). The program is loaded into memory, and the virtual machine processes each instruction sequentially.

## Initialization

The virtual machine is initialized with an empty program, and the default prompt is set to ">>". The `initialize` method sets up the initial state, including registers and RAM.

## Instruction Fetching

The `fetch` method retrieves the next instruction from memory pointed to by the instruction pointer (`ip`). The instruction is then decoded into its components: operation (`op`), and two arguments (`arg0` and `arg1`).

## Program Execution

The `run` method is responsible for executing the loaded program. It iterates through the instructions, performs the specified operations, and updates the state of registers and memory accordingly. The program terminates when a halt instruction (`OPS["hlt"]`) is encountered.

## Instructions

The virtual machine supports a set of instructions, each identified by a unique code. Notable instructions include loading values (`ldc`), loading from memory (`ldr`), copying registers (`cpy`), storing to memory (`str`), arithmetic operations (`add`, `sub`), conditional branching (`beq`, `bne`), printing register values (`prr`), printing memory values (`prm`), incrementing (`inc`), decrementing (`dec`), swapping registers (`swp`), and conditional branching based on a register value if said value is bigger or equal to 0(`bt0`) This last one was implemented to overcome the challenge in task 3.3, where we had to swap in array i place with only four registers. We discovered that our solution could only work with an odd and even number of integers in the array alike, if we implemented a function that checks if, the difference of the two register pointers is bigger or equalt to 0(for even numbers) or equal to 0(for odd numbers).

## Command-Line Usage

The virtual machine is designed to be run from the command line. The program expects two arguments: the input file containing the program and the output file to write the results. If "-" is provided as an argument, the program reads from stdin or writes to stdout, respectively.

Example usage:
```bash
python virtual_machine.py input_file.mx output_file.txt
```

## architecture.py

### Overview
This Python script represents a simple virtual machine. The machine has a specified number of registers (`NUM_REG`) and words in RAM (`RAM_LEN`). It supports various operations defined by opcode mappings (`OPS`). Each operation has a corresponding code, and the format (`fmt`) indicates the operand format.

### Configuration
- `NUM_REG`: Number of registers in the virtual machine.
- `RAM_LEN`: Number of words in RAM.

### Operations (OPS)
- `hlt`: Halt program
- `ldc`: Load value
- `ldr`: Load register
- `cpy`: Copy register
- `str`: Store register
- `add`: Add
- `sub`: Subtract
- `beq`: Branch if equal
- `bne`: Branch if not equal
- `prr`: Print register
- `prm`: Print memory
- `inc`: Increase register by 1 (as intended in task 3.1)
- `dec`: Decrease register by 1 (as intended in task 3.1)
- `swp`: Swap two values        (as intended in task 3.2)
- `bs0`: Branch if smaller or equal to 0 (added to complete exercise 3.3)

### Opcode Configuration
- `OP_MASK`: Select a single byte for operation.
- `OP_SHIFT`: Shift up by one byte for operation.
- `OP_WIDTH`: Width of the operation when printing.

## arrays.py
This file was left intact

## example_3_1.as


### Instructions

1. **Load Constants**: The program loads the constant values `3` and `4` into registers `R0` and `R1`, respectively.
    - `ldc R0 3`: Load the constant `3` into register `R0`.
    - `ldc R1 4`: Load the constant `4` into register `R1`.

2. **Print Registers**: The program prints the values stored in registers `R0` and `R1`.
    - `prr R0`: Print the value in register `R0`.
    - `prr R1`: Print the value in register `R1`.

3. **Increment and Decrement**: The program increments the value in `R0` and decrements the value in `R1`.
    - `inc R0`: Increment the value in register `R0`.
    - `dec R1`: Decrement the value in register `R1`.

4. **Print Registers Again**: The updated values in registers `R0` and `R1` are printed.
    - `prr R0`: Print the updated value in register `R0`.
    - `prr R1`: Print the updated value in register `R1`.

5. **Halt**: The program halts its execution.
    - `hlt`: Halt the program.

### Execution
The program, when executed on a virtual machine, will produce the following output:

```
3
4
4
3
```

### Usage
This program is used as an example of the inc and dec funtion

### example_3_2.as

Explanation:
1. `ldc R0 3`: Load the constant value 3 into register R0.
2. `ldc R1 4`: Load the constant value 4 into register R1.
3. `prr R0`: Print the value in register R0.
4. `prr R1`: Print the value in register R1.
5. `swp R0 R1`: Swap the values in registers R0 and R1.
6. `prr R0`: Print the updated value in register R0.
7. `prr R1`: Print the updated value in register R1.
8. `hlt`: Halt the program.

```assembly
ldc R0 3    ; Load the constant value 3 into register R0
ldc R1 4    ; Load the constant value 4 into register R1
prr R0      ; Print the value in register R0
prr R1      ; Print the value in register R1
swp R0 R1   ; Swap the values in registers R0 and R1
prr R0      ; Print the updated value in register R0
prr R1      ; Print the updated value in register R1
hlt         ; Halt the program
```

### Usage
The program prints the initial values of R0 and R1, swaps their values, and then prints the updated values before halting. The output will show the progression of values in R0 and R1 during the execution.

### example_3_3.as


This assembly code is designed to count up to 3 and perform an in-place array reversal. The program uses a simple assembly language with a set of instructions and registers.

## Registers:

- **R0:** Loop index.
- **R1:** Loop limit.
- **R2:** Array index.
- **R3:** Temporary register.

## Instructions:

- **ldc:** Load constant value into a register.
- **str:** Store the value of a register into memory.
- **add:** Add two registers.
- **sub:** Subtract one register from another.
- **bne:** Branch if not equal (conditional jump).
- **dec:** Decrease the value of a register by 1.
- **ldr:** Load the value from memory into a register.
- **cpy:** Copy the value of one register into another.
- **inc:** Increase the value of a register by 1.
- **bt0:** Branch if the value in a register is equal or bigger to 0 (conditional jump).

## Program Execution:

1. Load constants into R0, R1, and R2 (initializing loop variables and array index).
2. Start a loop:
   - Store the loop index (R0) into the array at the current index (R2).
   - Increment loop index (R0).
   - Increment array index (R2).
   - Calculate the remaining loop iterations (R1 - R0) and check if it's not equal to zero. If true, repeat the loop.
3. Decrease the loop limit (R1).
4. Load constants into R2 and R3 (re-initializing array index and temporary register).
5. Start a second loop:
   - Load values from the array at indices R2 and R3 into R0 and R1, respectively.
   - Store the values of R0 and R1 back into the array at indices R3 and R2, respectively (performing the swap).
   - Increment array index (R2) and decrease the temporary register (R3).
   - Calculate the remaining loop iterations (R1 - R3) and check if it's not equal or bigger than zero. If true, repeat the loop.
6. Halt the program.

## Data Section:

- The program includes a data section with an array labeled "array" initialized with the value 10.

## Running the Program:

- Load this assembly code into your assembler and assemble it.
- Run the resulting machine code using your virtual machine.
- The program should reverse the contents of the array and halt.

This README provides a high-level overview of the assembly code's functionality. Be sure to consult the specific documentation of your assembler and virtual machine for detailed usage instructions.

# vm_break

This Python program further extends the virtual machine by incorporating the ability to set breakpoints and watchpoints during program execution. Breakpoints interrupt program flow at specific addresses, allowing for interactive inspection, while watchpoints trigger when the value at a specified memory address changes.

## Usage

To use the extended virtual machine with breakpoints and watchpoints, follow these steps:

1. **Import Necessary Modules:**

    ```python
    import sys
    from architecture import OPS, VMState
    from vm_extend import VirtualMachineExtend
    ```

2. **Initialize the Extended Virtual Machine with Breakpoints and Watchpoints:**

    Create an instance of `VirtualMachineBreak`, which inherits from `VirtualMachineExtend`. This class includes additional commands for managing breakpoints and watchpoints.

    ```python
    vm = VirtualMachineBreak()
    ```

3. **Set Breakpoints and Watchpoints:**

    Use commands such as `b` or `break` to set breakpoints at specific addresses, and `watchpoint` to set watchpoints.

    ```python
    b 0x000012   # Set breakpoint at address 0x000012
    watchpoint 0x00001A  # Set watchpoint at address 0x00001A
    ```

4. **Run the Virtual Machine:**

    Execute the virtual machine using the `run` method, which incorporates breakpoint and watchpoint handling.

    ```python
    vm.run()
    ```

5. **Interact and Explore:**

    During execution, the virtual machine will pause at breakpoints and watchpoints, allowing interactive exploration using the `interact` method.

6. **Additional Commands:**

    - `c` or `clear`: Clear breakpoints or watchpoints at specific addresses.
    - `show`: Display information about breakpoints and watchpoints.

    For all the command it's just necessary to type the first letters of the command to execute it!

## Example

```python
if __name__ == "__main__":
    vm = VirtualMachineBreak()
    vm.run()
```

## Breakpoints and Watchpoints Commands

- **Set Breakpoint (b or break):** Set a breakpoint at a specific address.

    ```python
    b 2   # Set breakpoint at address 2
    ```

- **Clear Breakpoint (c or clear):** Clear a breakpoint at a specific address.

    ```python
    c 2   # Clear breakpoint at address 2
    ```

- **Set Watchpoint (watchpoint):** Set a watchpoint at a specific address.

    ```python
    watchpoint 5   # Set watchpoint at address 5
    ```

- **Clear Watchpoint (clearwatchpoint):** Clear a watchpoint at a specific address.

    ```python
    clearwatchpoint 5   # Clear watchpoint at address 5
    ```
The program will convert the address in the right format so the program can find and execute the operation properly

- **Show (show):** Display information about breakpoints and watchpoints.

    ```python
    show   # Display information about breakpoints and watchpoints
    ```


# vm_extend.py


## Usage

To use the extended virtual machine with interactive features, follow these steps:

1. **Import Necessary Modules:**

    ```python
    import sys
    from architecture import VMState
    from vm_step import VirtualMachineStep
    ```

2. **Initialize the Extended Virtual Machine:**

    Create an instance of `VirtualMachineExtend` with optional reader and writer configurations. The default reader is `input`, and the default writer is `sys.stdout`.

    ```python
    vm = VirtualMachineExtend(reader=input, writer=sys.stdout)
    ```

3. **Interact with the Virtual Machine:**

    Use the `interact` method to enter interactive mode, enabling you to input commands and explore the virtual machine's state.

    ```python
    vm.interact(start_address)
    ```

    - Enter commands when prompted. Available commands include:
        - `d` or `dis`: Disassemble instructions at the current address.
        - `i` or `ip`: Display the current instruction pointer (IP).
        - `m` or `memory`: View memory contents. You can specify a range of addresses.
        - `q` or `quit`: Quit the virtual machine.
        - `r` or `run`: Run the virtual machine.
        - `s` or `step`: Step through the program one instruction at a time.
    The commands are also understood if the first letters of the command are typed!

4. **Explore and Analyze:**

    Utilize the interactive mode to explore the virtual machine's state, inspect memory, and analyze program execution. The extended functionality provides a more detailed understanding of the machine's behavior.

## Example

```python
if __name__ == "__main__":
    vm = VirtualMachineExtend(reader=input, writer=sys.stdout)
    vm.interact(start_address)
```

## Interactive Commands

- **Disassemble (d or dis):** Disassembles instructions at the current address.

- **Instruction Pointer (i or ip):** Displays the current instruction pointer (IP).

- **Memory (m or memory):** Views memory contents. You can specify a range of addresses or one address.

- **Quit (q or quit):** Quits the virtual machine.

- **Run (r or run):** Runs the virtual machine.

- **Step (s or step):** Steps through the program one instruction at a time.

- **Breakpoint Commands:** Additional commands for setting and clearing breakpoints.
