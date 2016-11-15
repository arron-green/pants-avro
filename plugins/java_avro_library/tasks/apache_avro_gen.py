from twitter.common.collections import OrderedSet
from pants.base.exceptions import TaskError
from pants.backend.codegen.tasks.simple_codegen_task import SimpleCodegenTask
from pants.backend.jvm.targets.java_library import JavaLibrary
from pants.backend.jvm.tasks.nailgun_task import NailgunTaskBase
from java_avro_library.targets.java_avro_library import JavaAvroLibrary


class ApacheAvroGen(NailgunTaskBase, SimpleCodegenTask):
    def __init__(self, *args, **kwargs):
        super(ApacheAvroGen, self).__init__(*args, **kwargs)

    def synthetic_target_type(self, target):
        return JavaLibrary

    def is_gentarget(self, target):
        return isinstance(target, JavaAvroLibrary)

    @classmethod
    def register_options(cls, register):
        super(ApacheAvroGen, cls).register_options(register)
        # TODO add support for avro-tools
        # cls.register_jvm_tool(register, 'avro-tools')
        cls.register_jvm_tool(register, 'avrohugger-tools')

    def format_args_for_target(self, target, target_workdir):
        sources = OrderedSet(target.sources_relative_to_buildroot())
        # NOTE hard coded generate-specific for now
        # TODO allow options to be passed in from target
        args = ['generate-specific', 'schema']
        for s in sources:
            args.append(s)
        args.append(target_workdir)
        return args

    def execute_codegen(self, target, target_workdir):
        # TODO add support for avro-tools
        # avrotools_res = self.runjava(classpath=self.tool_classpath('avro-tools'),
        #                              main='org.apache.avro.tool.Main',
        #                              args=[])
        fmtdargs = self.format_args_for_target(target, target_workdir)
        result = self.runjava(classpath=self.tool_classpath('avrohugger-tools'),
                              main='avrohugger.tool.Main',
                              args=fmtdargs)
        if result != 0:
            raise TaskError('avro-tools returned non 0')
