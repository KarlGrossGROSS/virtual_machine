import sys

from architecture import OPS, VMState
from vm_extend import VirtualMachineExtend


class VirtualMachineBreak(VirtualMachineExtend):
    # [init]
    def __init__(self):
        super().__init__()
        self.breaks = {}
        self.watchpoints = {}
        self.handlers |= {
            "b": self._do_add_breakpoint,
            "break": self._do_add_breakpoint,
            "c": self._do_clear_breakpoint,
            "clear": self._do_clear_breakpoint,
            "watchpoint": self._do_add_watchpoint,
            "clearwatchpoint": self._do_clear_watchpoint
        }
    # [/init]

    # [show]
    def show(self):
        super().show()
        if self.breaks or self.watchpoints:
            self.write("-" * 6)
            self.write("breaks")
            for key, instruction in self.breaks.items():
                self.write(f"{key:06x}: {self.disassemble(key, instruction)}")
            self.write("-"*6)
            self.write("watchpoints")
            for key, instruction in self.watchpoints.items():
                self.write(f"{key:06x}: {self.disassemble(key, instruction)}")
            
    # [/show]
    def check_watchpoints(self):
        for wp in self.watchpoints:
            if self.ram[wp] != self.watchpoints[wp]:
                self.watchpoints[wp] = self.ram[wp]
                self.write(f"A watchpoint hit at address {wp}")
                self.interact(self.ip)

    # [run]
    def run(self):
        self.state = VMState.STEPPING

        while self.state != VMState.FINISHED:
            instruction = self.ram[self.ip]
            op, arg0, arg1 = self.decode(instruction)

            if op == OPS["brk"]["code"]:
                original = self.breaks[self.ip]
                op, arg0, arg1 = self.decode(original)
                self.interact(self.ip)
                self.ip += 1
                self.execute(op, arg0, arg1)
                self.check_watchpoints()

            
            else:
                if self.state == VMState.STEPPING:
                    self.interact(self.ip)
                self.ip += 1
                self.execute(op, arg0, arg1)
                self.check_watchpoints()
                
    # [/run]

    def _do_add_watchpoint(self, addr, rest):
        if len(rest)==0:
            if addr in self.watchpoints:
                self.write(f"Watchpoint already set at address: {addr:06x}")
                return True
            self.watchpoints[addr] = self.ram[addr]
            return True
        elif len(rest) ==1:
            formatted_hex = f"{int(rest[0]):06x}"
            result_as_int = int(formatted_hex, 16)
            if result_as_int in self.watchpoints:
                self.write(f"Watchpoint already set at address: {result_as_int:06x}")
                return True
            self.watchpoints[result_as_int] = self.ram[result_as_int]
            return True
    def _do_clear_watchpoint(self, addr, rest):
        if len(rest) == 0:
            if addr in self.watchpoints:
                del self.watchpoints[addr]
                self.write(f"Watchpoint deleted at address: {addr:06x}")
                return True
            else:
                self.write(f"No watchpoint set at address {addr:06x}")
            return True
        elif len(rest) == 1:
            formatted_hex = f"{int(rest[0]):06x}"
            result_as_int = int(formatted_hex, 16)
            if result_as_int in self.watchpoints:
                del self.watchpoints[result_as_int]
                self.write(f"Watchpoint deleted at address: {result_as_int:06x}")
                return True
            else:
                self.write(f"No watchpoint set at address {result_as_int:06x}")
            return True



    # [add]
    def _do_add_breakpoint(self, addr, rest):
        ## 4.2 write breakpoint yourself
        if len(rest) == 0:
            if self.ram[addr] == OPS["brk"]["code"]:
                return
            self.breaks[addr] = self.ram[addr]
            self.ram[addr] = OPS["brk"]["code"]
            return True
        elif len(rest) == 1:
            formatted_hex = f"{int(rest[0]):06x}"
            result_as_int = int(formatted_hex, 16)
            self.write(f"{int(result_as_int)}")
            if self.ram[result_as_int] == OPS["brk"]["code"]:
                self.write("breakpoint encountered")
                return
            self.breaks[result_as_int] = self.ram[result_as_int]
            self.ram[result_as_int] = OPS["brk"]["code"]
            self.write(f"breakpoint added at: { self.ram[result_as_int]}")
            return True

    # [/add]

    # [clear]
    def _do_clear_breakpoint(self, addr, rest):
        ## 4.2 
        if len(rest) == 0:
            if self.ram[addr] != OPS["brk"]["code"]:
                return
            self.ram[addr] = self.breaks[addr]
            del self.breaks[addr]
            return True
            #self.ram[point[0]] = self.breaks[point[0]]
            #del self.breaks[point[0]]
        elif len(rest) == 1:
            formatted_hex = f"{int(rest[0]):06x}"
            result_as_int = int(formatted_hex, 16)
            if self.ram[result_as_int] != OPS["brk"]["code"]:
                return
            self.ram[result_as_int] = self.breaks[result_as_int]
            del self.breaks[result_as_int]
            return True
        
    
        # [/clear]


if __name__ == "__main__":
    VirtualMachineBreak.main()
