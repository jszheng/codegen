from veriloggen import *
from split_to_verilog import *
import math


def cal_addr_width(height):
    addr_width = int(math.log(height, 2))
    length = 2 ** addr_width
    if height > length:
        addr_width += 1
    return addr_width


def mk_ram1p_behav(height, width,
                   word_width=None,
                   with_ls=False,
                   with_ds=False):
    addr_width = cal_addr_width(height)

    if word_width is not None:
        # check
        num_word = int(width / word_width)
        if (num_word * word_width) != width:
            raise ValueError("RAM width must multiple of word_width")
    else:
        num_word = width

    name = 'sram1p' + str(height) + 'x' + str(width)
    if word_width is not None:
        name += 'wm' + str(num_word)

    m = Module(name)

    clk = m.Input('CLK')
    adr = m.Input('ADR', addr_width)
    di = m.Input('D', width)
    we = m.Input('WE')
    me = m.Input('ME')
    if word_width is not None:
        wem = m.Input('WEM', num_word)
    else:
        wem = None
    if with_ls:
        ls = m.Input('LS')
    else:
        ls = None
    if with_ds:
        ds = m.Input('DS')
        sd = m.Input('SD')
    else:
        ds = None
        sd = None

    qo = m.OutputReg('Q', width)

    me_latched = m.Reg('MElatched')
    flag_clk_valid = m.Reg('flag_clk_valid')
    mes_all_valid = m.Reg('mes_all_valid')
    adr_valid = m.Wire('ADR_valid')

    # Storage
    data = m.Reg('mem_core_array', width, height)

    pwr_dwn = m.Reg('pwr_dwn')
    m.Initial(pwr_dwn(Int("1'b0")))

    t_report = m.Task('report_unknown')
    signal = t_report.Input('signal', 40)
    t_report.Body(
        If(Eql(pwr_dwn, 0) | (Eql(pwr_dwn, 1) & ((signal == "DS") | (signal == 'SD'))))(
            If((SystemTask('realtime') != 0) & mes_all_valid)(
                SystemTask('display', "<<VIRL_MEM_ERR:%0s unknown>> at time=%t; instance=%m (RAM1P)", signal,
                           SystemTask('realtime'))

            )
        )
    )

    t_corrupt = m.Task('corrupt_all_loc')
    rang_ok = t_corrupt.Input('flag_range_ok')
    adr_idx = t_corrupt.Integer('addr_index')
    t_corrupt.Body(
        If(rang_ok == 1)(
            For(adr_idx(0), adr_idx < height, adr_idx(adr_idx + 1))(
                data[adr_idx](IntX(width))
            )
        )
    )

    t_write = m.Task('WritePort')
    t_write.Body(

    )

    t_read = m.Task('ReadPort')
    t_read.Body(

    )

    m.Initial(
        flag_clk_valid(0),
        mes_all_valid(0)
    )

    m.Assign(adr_valid(Uxor(adr) == IntX(1)))

    m.Always(Negedge(clk))(
        If(NotEql(clk, IntX(1)) & NotEql(clk, IntZ(1)))(
            flag_clk_valid(Int(1, 1), blk=True)
        ).Else(
            t_report.call("CLK"),
            flag_clk_valid(Int(0, 1), blk=True),
            qo(IntX(width), blk=True),
            t_corrupt.call(1)
        )
    )

    m.Always(Posedge(clk))(
        me_latched(me, blk=True),
        If(NotEql(sd, 0) | Eql(ds, 1) | (Eql(ds, 0) & Eql(ls, 1) & NotEql(me_latched, IntX(1))))(
            me_latched(0, blk=True)
        ),
        If(Eql(ls, IntX(1)) & NotEql(me_latched, 0))(
            t_report.call("LS"),
            t_corrupt.call(1),
            qo(IntX(width), blk=True)
        ).Elif(Eql(ds, IntX(1)))(
            t_corrupt.call(1),
            qo(IntX(width), blk=True)
        ).Else(
            If(flag_clk_valid)(
                If(Eql(clk, 1))(
                    If(Eql(me_latched, 1))(
                        If(Eql(we, 1))(
                            t_write.call()
                        ).Elif(Eql(we, 0))(
                            t_read.call()
                        ).Else(
                            t_report.call('WE')

                        )
                    )
                )
            )
        )
    )

    return m


if __name__ == '__main__':
    ram = mk_ram1p_behav(32768, 64, 1, True, True)
    print(ram.to_verilog())
