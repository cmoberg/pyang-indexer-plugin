
from pyang import plugin, statements

def pyang_plugin_init():
    plugin.register_plugin(IndexerPlugin())

class IndexerPlugin(plugin.PyangPlugin):
    def add_output_format(self, fmts):
        self.multiple_modules = True
        fmts['yang-catalog-index'] = self

    def setup_fmt(self, ctx):
        ctx.implicit_errors = False

    def emit(self, ctx, modules, fd):
        emit_index(ctx, modules, fd)

def emit_index(ctx, modules, fd):
	print "create table yindex(module, path, statement, argument);"
	for module in modules:
		for child in module.i_children:
			statements.iterate_i_children(child, printer)

def printer(stmt):
	module = stmt.main_module()
	path = statements.mk_path_str(stmt)
	print "insert into yindex values('%s', '%s', '%s', '%s');" % (module.arg, path, stmt.keyword, stmt.arg)
	# print "###", module.arg, path, stmt.keyword, stmt.arg
