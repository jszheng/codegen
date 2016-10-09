def split_to_verilog(node):
    import veriloggen.verilog.to_verilog as to_verilog
    from veriloggen.core import module
    import pyverilog.vparser.ast as vast
    from pyverilog.ast_code_generator.codegen import ASTCodeGenerator

    obj = node.to_hook_resolved_obj()

    visitor = to_verilog.VerilogModuleVisitor()
    modules = tuple(obj.get_modules().values())

    for mod in modules:
        if isinstance(mod, module.StubModule):
            code = mod.get_code()
            filename = mod.name + '.v'
            with open(filename, 'w') as f:
                print("Write file : ", filename)
                f.write("//File : " + filename)
                f.write("\n//This file is auto generated, do not edit!")
                f.write(code)
        else:
            m = visitor.visit(mod)
            filename = m.name + '.v'
            description = vast.Description([m])
            source = vast.Source(filename, description)
            codegen = ASTCodeGenerator()
            main = codegen.visit(source)
            with open(filename, 'w') as f:
                print("Write file : ", filename)
                f.write("//File : " + filename)
                f.write("\n//This file is auto generated, do not edit!")
                f.write(main)
