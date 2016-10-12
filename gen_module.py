# generate skeleton of module
import optparse
from jinja2 import Template

module_template = """\
from veriloggen import *
from split_to_verilog import *

def mk_{{name}}():
    name = {{name}}

    m = Module(name)
    m.Input('clk')
    m.Input('rst')
    m.Output('dout', width, initval=0)

    return m

if __name__ == '__main__':
    {{name}} = mk_{{name}}()
    #split_to_verilog({{name}})
    verilog = {{name}}.to_verilog()
    print(verilog)

"""


def generate_module(module_name):
    print('generating module:', module_name)
    template = Template(module_template)
    out = template.render(name=module)
    print(out)


if __name__ == '__main__':
    usage = "Usage: %prog  module_name [more_modules ...]"
    parser = optparse.OptionParser(usage=usage)
    # parser.add_option('-t', '--tree',
    #                   dest="out_file",
    #                   default="default.out",
    #                   help='set output file name',
    #                   )
    options, remainder = parser.parse_args()

    if len(remainder) < 1:
        print('ERROR: You have to provide at least one module name!')
        parser.print_help()
        exit(1)

    for module in remainder:
        generate_module(module)
