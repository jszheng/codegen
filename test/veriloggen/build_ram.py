from veriloggen import *
from split_to_verilog import *
import veriloggen.types.bram as bram
import math


def mk_mem_wrapper(height, width, port):
    # check address width
    addr_width = int(math.log(height, 2))
    length = 2 ** addr_width
    if height > length:
        addr_width += 1

    name = 'Mem' + str(port) + 'p' + str(height) + 'x' + str(width)

    m = Module(name)
    m.Input('CLK')
    m.Input('D', width)
    m.Input('ADR', addr_width)
    m.Input('WE')
    m.Input('ME')
    m.Input('RME')
    m.Input('RM', int(width / 8))
    m.Input('LS')
    m.Output('Q', width)

    return m


def mk_reg_array(height, width):
    # check address width
    addr_width = int(math.log(height, 2))
    length = 2 ** addr_width
    if height > length:
        addr_width += 1

    name = 'RegArray' + str(height) + 'x' + str(width)

    m = Module(name)
    clk = m.Input('CLK')
    d = m.Input('D', width)
    wadr = m.Input('WADR', addr_width)
    radr = m.Input('RADR', addr_width)
    we = m.Input('WE')
    q = m.Output('Q', width)

    mem = m.Reg('MEM', width, height)

    m.Always(Posedge(clk))(
        If(we)(
            mem[wadr](d)
        )
    )

    m.Assign(q(mem[radr]))
    return m


def mk_top():
    m = Module('TOP')
    clk = m.Input('clk')
    rst = m.Input('rst')

    mem1 = mk_mem_wrapper(128, 64, 1)
    # regary = mk_reg_array(128, 64)

    m.Instance(mem1, 'uMem1')
    # m.Instance(regary, 'uRegArray')

    return m


if __name__ == '__main__':
    top = mk_top()
    split_to_verilog(top)
    regary = mk_reg_array(128, 64)
    split_to_verilog(regary)
