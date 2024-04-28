import sys

from architecture import VMState
from vm_step import VirtualMachineStep
COLUMNS = 4


class VirtualMachineExtend(VirtualMachineStep):
    # [init]
    def __init__(self, reader=input, writer=sys.stdout):
        super().__init__(reader, writer)
        self.handlers = {
            "d": self._do_disassemble,
            "dis": self._do_disassemble,
            "i": self._do_ip,
            "ip": self._do_ip,
            "m": self._do_memory,
            "memory": self._do_memory,
            "q": self._do_quit,
            "quit": self._do_quit,
            "r": self._do_run,
            "run": self._do_run,
            "s": self._do_step,
            "step": self._do_step,
        }
    # [/init]

    def find_do(self, prefix, pattern=""):
        for name, func in self.handlers.items():
            #if name.startswith(prefix) and pattern in name:
            #    ops.append((name, func))
            if name.startswith(pattern):
                return name
        return None

    # [interact]
    def interact(self, addr):
        ## 4.3 and 4.2
        prompt = "".join(sorted({key[0] for key in self.handlers}))
        interacting = True
        while interacting:
            try:
                command = self.read(f"{addr:06x} [{prompt}]> ").split()
                command[0] = self.find_do("_do_", command[0])
                if not command[0]:
                    continue
                elif command[0] not in self.handlers:
                    self.write(f"Unknown command {command}")
                
                elif self.handlers[command[0]] == self._do_memory:
                    interacting = self.handlers[command[0]](self.ip, command[1:])
                
                elif command[0] in ["break", "clear", "b", "c"]:
                    interacting = self.handlers[command[0]](self.ip, command[1:])
                
                elif command[0] in ["watchpoint", "clearwatchpoint"]:
                    interacting = self.handlers[command[0]](self.ip, command[1:])

                
                # elif self.handlers[command[0]] == self._do_add_breakpoint:
                #     interacting = self.handlers[command[0]](self.ip, command[1:])

                else: 
                    self.handlers[command[0]] != self._do_memory
                    interacting = self.handlers[command[0]](self.ip)

            except EOFError:
                self.state = VMState.FINISHED
                interacting = False
    # [/interact]

    def _do_disassemble(self, addr, rest=None):
        self.write(self.disassemble(addr, self.ram[addr]))
        return True

    def _do_ip(self, addr, rest=None):
        self.write(f"{self.ip:06x}")
        return True


    def _do_memory(self, addr, rest=None):
        if len(rest)==0:
            self.show()
            return True
        if len(rest) == 1:
            self.write(f"{self.ram[int(rest[0])]:06x}")
        elif len(rest) ==2:
            for addr in range(int(rest[0]), int(rest[1])+1):
                 self.write(f"{self.ram[addr]:06x}")
    
        #top = max(i for (i, m) in enumerate(self.ram) if m != 0)
        
        # addr1 = int(self.read("Start address: ").strip(), 16)
        # addr2 = self.read("End address: ").strip()
        # if addr2 == 'None':
        #     self.write(f"{self.ram[addr1]:06x}")
        # else:
        #     addr2 = int(addr2, 16)
        #     assert addr1<=addr2<=len(self.ram)
        #     for addr in range(addr1, addr2+1):
        #         self.write(f"{self.ram[addr]:06x}")
        # # Show memory
        # base = 0
        # while base <= top:
        #     output = f"{base:06x}: "
        #     for i in range(COLUMNS):
        #         output += f"  {self.ram[base + i]:06x}"
        #     self.write(output)
        #     base += COLUMNS
        return True

    def _do_quit(self, addr):
        self.state = VMState.FINISHED
        return False

    def _do_run(self, addr):
        if not self.breaks:
            self.state = VMState.RUNNING
        else:
            self.state = VMState.RUN_TO_BREAKPOINT
        return False

    # [step]
    def _do_step(self, addr):
        self.state = VMState.STEPPING
        return False
    # [/step]


if __name__ == "__main__":
    VirtualMachineExtend.main()
