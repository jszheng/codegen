from veriloggen import *
from split_to_verilog import *
import math


def cal_addr_width(height):
    addr_width = int(math.log(height, 2))
    length = 2 ** addr_width
    if height > length:
        addr_width += 1
    return addr_width


def mk_rf_behav(height, width,
                word_width=None,
                pipeme_pipelined=False,
                q_pipelined=False):
    addr_width = cal_addr_width(height)

    if word_width is not None:
        # check
        num_word = int(width / word_width)
        if (num_word * word_width) != width:
            raise ValueError("RAM width must multiple of word_width")
    else:
        num_word = width

    name = 'sram_bfm2pa' + str(height) + 'x' + str(width)
    if word_width is not None:
        name += 'wm' + str(num_word)
    if pipeme_pipelined:
        assert (q_pipelined)
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

    # Storage
    data = m.Reg('data', width, height)

    seqw = Seq(m, 'seq_write', clka, rsta)
    seqr = Seq(m, 'seq_read', clkb, rstb)

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

    data_read = m.RegLike(qb, 'data_read')
    seqr.If(meb)(
        data_read(data[adrb])
    )

    if q_pipelined:
        rdataq = m.RegLike(qb, 'rdataq')
        if pipeme_pipelined:
            pipemebq = m.RegLike(pipemeb, 'PIPEMEB_q')
            mebq = m.RegLike(meb, 'MEB_q')

            seqr(
                pipemebq(pipemeb)

            )
            seqr.If(mebq & pipemebq)(
                rdataq(data_read)
            )
        else:
            seqr.If(pipemeb)(
                rdataq(data_read)
            )
        m.Assign(qb(rdataq))
    else:
        m.Assign(qb(data_read))

    return m


def mk_pdp_behav(height, width,
                 word_width=None,
                 pipeme_pipelined=False,
                 q_pipelined=False):
    addr_width = cal_addr_width(height)

    if word_width is not None:
        # check
        num_word = int(width / word_width)
        if (num_word * word_width) != width:
            raise ValueError("RAM width must multiple of word_width")
    else:
        num_word = width

    name = 'sram_bfm2ps' + str(height) + 'x' + str(width)
    if word_width is not None:
        name += 'wm' + str(num_word)
    if pipeme_pipelined:
        assert (q_pipelined)
        name += '_pp'
    if q_pipelined:
        name += '_po'

    m = Module(name)

    # Write Port
    clk = m.Input('CLK')
    rst = m.Input('RST')

    adra = m.Input('ADRA', addr_width)
    da = m.Input('DA', width)
    wea = m.Input('WEA')
    if word_width is not None:
        wema = m.Input('WEMA', num_word)
    else:
        wema = None
    mea = m.Input('MEA')

    # Read Port
    adrb = m.Input('ADRB', addr_width)
    meb = m.Input('MEB')
    pipemeb = m.Input('PIPEMEB')
    qb = m.Output('QB', width)

    # Storage
    data = m.Reg('data', width, height)

    seqw = Seq(m, 'seq_write', clk, rst)
    seqr = Seq(m, 'seq_read', clk, rst)

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

    data_read = m.RegLike(qb, 'data_read')
    seqr.If(meb)(
        data_read(data[adrb])
    )

    if q_pipelined:
        rdataq = m.RegLike(qb, 'rdataq')
        if pipeme_pipelined:
            pipemebq = m.RegLike(pipemeb, 'PIPEMEB_q')

            seqr(
                pipemebq(pipemeb)

            )
            seqr.If(pipemebq)(
                rdataq(data_read)
            )
        else:
            seqr.If(pipemeb)(
                rdataq(data_read)
            )
        m.Assign(qb(rdataq))
    else:
        m.Assign(qb(data_read))

    return m


def mk_1p_behav(height, width,
                word_width=None,
                pipeme_pipelined=False,
                q_pipelined=False):
    addr_width = cal_addr_width(height)

    if word_width is not None:
        # check
        num_word = int(width / word_width)
        if (num_word * word_width) != width:
            raise ValueError("RAM width must multiple of word_width")
    else:
        num_word = width

    name = 'sram_bfm1p' + str(height) + 'x' + str(width)
    if word_width is not None:
        name += 'wm' + str(num_word)
    if pipeme_pipelined:
        assert (q_pipelined)
        name += '_pp'
    if q_pipelined:
        name += '_po'

    m = Module(name)

    # Write Port
    clk = m.Input('CLK')
    rst = m.Input('RST')
    adr = m.Input('ADR', addr_width)
    d = m.Input('D', width)
    we = m.Input('WE')
    if word_width is not None:
        wem = m.Input('WEM', num_word)
    else:
        wem = None
    me = m.Input('ME')
    pipeme = m.Input('PIPEME')
    q = m.Output('Q', width)

    # Storage
    data = m.Reg('data', width, height)

    seqw = Seq(m, 'seq_write', clk, rst)
    seqr = Seq(m, 'seq_read', clk, rst)

    if word_width is not None:  # Write with Word Mask
        i = m.Integer('i')
        seqw.If(me & we)(
            For(i(0), i < width, i(i + 1))(
                If(wem[i / word_width])(
                    data[adr][i](d[i])
                )
            )
        )
    else:  # Write Whole Data
        seqw.If(me & we)(
            data[adr](d)
        )

    data_read = m.RegLike(q, 'data_read')
    seqr.If(me)(
        data_read(data[adr])
    )

    if q_pipelined:
        rdataq = m.RegLike(q, 'rdataq')
        if pipeme_pipelined:
            pipemeq = m.RegLike(pipeme, 'PIPEME_q')

            seqr(
                pipemeq(pipeme)

            )
            seqr.If(pipemeq)(
                rdataq(data_read)
            )
        else:
            seqr.If(pipeme)(
                rdataq(data_read)
            )
        m.Assign(q(rdataq))
    else:
        m.Assign(q(data_read))

    return m


if __name__ == '__main__':
    for po in [False, True]:
        for pp in [False, True]:
            if not po:
                pp = False
            ram = mk_1p_behav(128, 32, q_pipelined=po, pipeme_pipelined=pp)
            split_to_verilog(ram)
            ram = mk_1p_behav(128, 32, 8, q_pipelined=po, pipeme_pipelined=pp)
            split_to_verilog(ram)
