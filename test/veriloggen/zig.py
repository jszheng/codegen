from veriloggen import *
from split_to_verilog import *
from sram_bfm import *


def mk_zig(width=32, xsize=8, ysize=4):
    name = 'zig'

    m = Module(name)
    clk = m.Input('clk')
    rst = m.Input('rst')

    dout = list(range(ysize))
    for y in range(ysize):
        dout[y] = list(range(xsize))
        for x in range(xsize):
            dout[y].append(m.OutputReg('dout_%d_%d' % (y, x), width, initval=0))
    #dout1 = [[m.OutputReg('dout1_%d_%d' % (y, x)) for x in range(xsize)] for y in range(ysize)]

    buf_size = 256
    ysram = mk_pdp_behav(buf_size, width, q_pipelined=True)
    ybuf_array = [m.Instance(ysram, "ybuf_%d" % y) for y in range(ysize)]

    # Controller

    return m


def mk_test():
    m = Module('test')

    mdut = mk_zig()

    # dut_ports = dut.io_variable
    #
    # for key, value in dut_ports.items():
    #     print(key, type(value))
    # return m

    dut = m.Instance(mdut, 'DUT')

    clk = mdut.find_identifier('clk')
    rst = mdut.find_identifier('rst')

    dut.set_port('clk', clk)
    dut.set_port('rst', rst)

    simulation.setup_waveform(m, dut, m.get_vars())
    simulation.setup_clock(m, clk, hperiod=5)
    simulation.setup_reset(m, rst, m.make_reset(), period=100)

    return m

if __name__ == '__main__':
    test = mk_test()
    # split_to_verilog(zig)
    verilog = test.to_verilog()
    print(verilog)
