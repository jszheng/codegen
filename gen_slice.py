from veriloggen import *


def mk_sub1():
    m = Module('sub1')
    adr = m.Input('ADR', 40)
    return m


def mk_sub2():
    m = Module('sub2')
    dat = m.Input('DAT', 30)
    return m


def mk_top():
    m = Module('top')
    adr = m.Input('ADR', 36)
    dat = m.Input('DAT', 36)

    sub1 = mk_sub1()
    sub2 = mk_sub2()

    ins1 = m.Instance(sub1, 'inst_sub1', ports=(('ADR', Cat(Int(0, 4), adr)), ) )
    #ins2 = m.Instance(sub2, 'inst_sub2', ports=(('DAT', dat[0:-1]), ) )
    ins2 = m.Instance(sub2, 'inst_sub2', ports=(('DAT', dat[0:29]), ) )

    return m

if __name__ == '__main__':
    top = mk_top()
    print(top.to_verilog())