from veriloggen import *
from split_to_verilog import *
import veriloggen.types.bram as bram


def mk_mem_wrapper(height, width, port):
    name = 'Mem' + str(port) + 'p' + str(height) + 'x' + str(width)
    m = StubModule(name)
    m.Input('clk')
    m.Input('rst')

    return m


def mk_reg_array(m, clk, rst, datawidth=32, addrwidth=10, numports=1, nodataflow=False):

    name = 'RegArray' + str(numports) + 'p' + str(1 << addrwidth) + 'x' + str(datawidth)
    return bram.Bram(m, name, clk, rst, datawidth=datawidth, addrwidth=addrwidth, numports=numports,
                     nodataflow=nodataflow)


def mk_top():
    m = Module('TOP')
    clk = m.Input('clk')
    rst = m.Input('rst')

    mem1 = mk_mem_wrapper(128, 64, 1)

    m.Instance(mem1, 'uMem1')
    mk_reg_array(m, clk, rst, datawidth=64, addrwidth=7, numports=1)
    mk_reg_array(m, clk, rst, datawidth=64, addrwidth=7, numports=2)

    return m


if __name__ == '__main__':
    top = mk_top()
    split_to_verilog(top)
