def split_to_verilog(node, list_file_name=None):
    import veriloggen.verilog.to_verilog as to_verilog
    from veriloggen.core import module
    import pyverilog.vparser.ast as vast
    from pyverilog.ast_code_generator.codegen import ASTCodeGenerator

    obj = node.to_hook_resolved_obj()

    visitor = to_verilog.VerilogModuleVisitor()
    modules = tuple(obj.get_modules().values())

    run_files = []

    for mod in modules:
        if isinstance(mod, module.StubModule):
            code = mod.get_code()
            filename = mod.name + '.v'
            with open(filename, 'w') as f:
                print("Write file : ", filename)
                f.write("//File : " + filename)
                f.write("\n//This file is auto generated, do not edit!")
                f.write(code)
                run_files.append(filename)
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
                run_files.append(filename)

    if list_file_name is not None:
        with open(list_file_name, 'w') as f:
            for name in run_files:
                f.write(name+"\n")
