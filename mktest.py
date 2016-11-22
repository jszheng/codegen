import os
from veriloggen import *


def read_verilog(file_name):
    abs_name = os.path.abspath(file_name)
    dir_name = os.path.dirname(abs_name)
    here = os.path.dirname(os.path.abspath(__file__))
    stubs = from_verilog.read_verilog_module(abs_name, include=[dir_name, here])
    return stubs


def mk_fifo():
    modules = read_verilog('D:/work/async/async_fifo/async_fifo.v')
    fifo = modules['async_fifo']
    return fifo


def mk_test(data_size, addr_size):
    m = Module('tb')

    fifo = mk_fifo()

    m.Parameter('DSIZE', data_size)
    m.Parameter('ASIZE', addr_size)
    ports = m.copy_sim_ports(fifo)
    params = (('DSIZE', data_size), ('ASIZE', addr_size))

    uut = m.Instance(fifo, 'uut', params, ports)

    wclk = ports['wclk']
    rclk = ports['rclk']
    wrst_n = ports['wrst_n']
    rrst_n = ports['rrst_n']
    winc = ports['winc']
    rinc = ports['rinc']
    wfull = ports['wfull']
    rempty = ports['rempty']
    wdata = ports['wdata']
    rdata = ports['rdata']

    simulation.setup_waveform(m, uut)
    simulation.setup_clock(m, wclk, 2)
    simulation.setup_clock(m, rclk, 20)
    simulation.setup_reset(m, wrst_n)
    simulation.setup_reset(m, rrst_n)

    wseq = Seq(m, 'wseq', wclk, wrst_n)
    rseq = Seq(m, 'rseq', rclk, rrst_n)

    wseq.If(winc & ~wfull)(
        wdata(SystemTask('random'))
    )

    rseq.If(rinc & ~rempty)(
        rdata(SystemTask('random'))
    )

    return m

from split_to_verilog import *
if __name__ == '__main__':
    test = mk_test(32, 4)
    verilog = test.to_verilog()
    print(verilog)
    split_to_verilog(test, test.name+'.vc')

    sim = simulation.Simulator(test)
    rslt = sim.run(display=True)
    print(rslt)

    # launch waveform viewer (GTKwave)
    sim.view_waveform() # background=False
    #sim.view_waveform(background=True)