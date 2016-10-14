from veriloggen import *
from split_to_verilog import *
import veriloggen.types.bram as bram
import math


def cal_addr_width(height):
    addr_width = int(math.log(height, 2))
    length = 2 ** addr_width
    if height > length:
        addr_width += 1
    return addr_width


def mk_mem2p(height, width,
             word_width=None,
             input_pipelined=False,
             pipeme_pipelined=False,
             q_pipelined=False,
             with_ls=False,
             with_ds=False):
    print('height=', height, ' width=', width,
          ' word=', word_width,
          ' pi=', input_pipelined,
          ' pp=', pipeme_pipelined,
          ' po=', q_pipelined)
    # check address width
    addr_width = cal_addr_width(height)

    if word_width is not None:
        # check
        num_word = int(width / word_width)
        if (num_word * word_width) != width:
            raise ValueError("RAM width must multiple of word_width")
    else:
        num_word = width

    name = 'Mem2p' + str(height) + 'x' + str(width)
    if word_width is not None:
        name += 'wm' + str(num_word)
    if input_pipelined:
        name += '_pi'
    if pipeme_pipelined:
        name += '_pp'
    if q_pipelined:
        name += '_po'
    m = Module(name)

    # Write Port
    clka = m.Input('CLKA')
    rsta = m.Input('RSTA')
    adra = m.Input('ADRA', addr_width)
    da = m.Input('DA', width)
    wea = m.Input('WEA')
    if word_width is not None:
        wema = m.Input('WEMA', num_word)
    else:
        wema = None
    mea = m.Input('MEA')

    # Read Port
    clkb = m.Input('CLKB')
    rstb = m.Input('RSTB')
    adrb = m.Input('ADRB', addr_width)
    meb = m.Input('MEB')
    pipemeb = m.Input('PIPEMEB')
    qb = m.Output('QB', width)

    # LS and DS are not able to modeling in here
    # Just to show the port
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

    data = m.Reg('data', width, height)

    seqw = Seq(m, 'seq_write', clka, rsta)
    seqr = Seq(m, 'seq_read', clkb, rstb)

    final_data = m.Wire('final_data', width)

    if input_pipelined:
        meaq = m.RegLike(mea, 'MEA_q')
        weaq = m.RegLike(wea, 'WEA_q')
        adraq = m.RegLike(adra, 'ADRA_q')
        daq = m.RegLike(da, 'DA_q')

        adrbq = m.RegLike(adra, 'ADRB_q')
        mebq = m.RegLike(meb, 'MEB_q')

        read_data = m.Wire('read_data', width)

        seqw(
            meaq(mea),
            weaq(wea),
            adraq(adra),
            daq(da)
        )

        seqr(
            mebq(meb),
        )
        seqr.If(meb)(
            adrbq(adrb)
        )

        if word_width is not None:  # Write with Word Mask
            i = m.Integer('i')
            wemaq = m.RegLike(wema, 'WEMA_q')
            seqw(
                wemaq(wema)
            )
            seqw.If(meaq & weaq)(
                For(i(0), i < width, i(i + 1))(
                    If(wemaq[i / word_width])(
                        data[adraq][i](daq[i])
                    )
                )
            )
        else:  # Write Whole Data
            seqw.If(meaq & weaq)(
                data[adraq](daq)
            )

        m.Assign(read_data(data[adrbq]))  # read out data

        read_data_latched = m.Reg('read_data_latched', width)

        seqr.If(mebq)(
            read_data_latched(read_data)
        )

        m.Assign(final_data(Cond(mebq, read_data, read_data_latched)))
    else:
        if word_width is not None:  # Write with Word Mask
            i = m.Integer('i')
            seqw.If(mea & wea)(
                For(i(0), i < width, i(i + 1))(
                    If(wema[i / word_width])(
                        data[adra][i](da[i])
                    )
                )
            )
        else:  # Write Whole Data
            seqw.If(mea & wea)(
                data[adra](da)
            )

        m.Assign(final_data(data[adrb]))  # read out data

    if q_pipelined:
        final_d1 = m.RegLike(qb, 'final_data_d1')
        pipemebq = m.RegLike(pipemeb, 'PIPEMEB_q')
        seqr(
            pipemebq(pipemeb)
        )

        if pipeme_pipelined:
            seqr.If(pipemebq)(
                final_d1(final_data)
            )
        else:
            seqr.If(pipemeb)(
                final_d1(final_data)
            )
        m.Assign(qb(final_d1))
    else:
        m.Assign(qb(final_data))

    return m


def mk_reg_array(height, width):
    # check address width
    addr_width = cal_addr_width(height)

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

    uniq_id = 0
    for pi in [False, True]:
        for pp in [False, True]:
            for po in [False, True]:
                mem = mk_mem2p(128, 64, input_pipelined=pi, pipeme_pipelined=pp, q_pipelined=po)
                name = 'uMem' + str(uniq_id)
                m.Instance(mem, name)
                uniq_id += 1
                mem = mk_mem2p(128, 64, word_width=8, input_pipelined=pi, pipeme_pipelined=pp, q_pipelined=po)
                name = 'uMem' + str(uniq_id)
                m.Instance(mem, name)
                uniq_id += 1

    return m


if __name__ == '__main__':
    top = mk_top()
    split_to_verilog(top)
    regary = mk_reg_array(128, 64)
    split_to_verilog(regary)
