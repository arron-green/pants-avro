from pants.base.exceptions import TaskError
from pants.task.simple_codegen_task import SimpleCodegenTask
from pants.java.jar.jar_dependency import JarDependency
from pants.backend.jvm.targets.java_library import JavaLibrary
from pants.backend.jvm.tasks.nailgun_task import NailgunTaskBase
from .targets import AvroJava

import logging
logger = logging.getLogger(__name__)


class AvroJavaGen(NailgunTaskBase, SimpleCodegenTask):
    @classmethod
    def product_types(cls):
        return ['java']

    @classmethod
    def register_options(cls, register):
        cls.register_jvm_tool(register, 'avro-tools',
                              classpath=[
                                  JarDependency(org="org.apache.avro",
                                                name="avro-tools",
                                                rev="1.8.2")
                              ])
        super(AvroJavaGen, cls).register_options(register)

    @property
    def avrotools_classpath(self):
        return self.tool_classpath('avro-tools')

    @classmethod
    def prepare(cls, options, round_manager):
        super(AvroJavaGen, cls).prepare(options, round_manager)

    def execute(self):
        super(AvroJavaGen, self).execute()

    def is_gentarget(self, target):
        return isinstance(target, AvroJava)

    def __init__(self, *args, **kwargs):
        super(AvroJavaGen, self).__init__(*args, **kwargs)
        self.set_distribution(jdk=True)
        self.gen_langs = set()
        if self.context.products.isrequired('java'):
            self.gen_langs.add('java')

    def _compile_schema(self, args):
        logger.info('AvroJavaGen: invoking avro-tools '
                    'with args %s', args)
        result = self.runjava(classpath=self.avrotools_classpath,
                              main='org.apache.avro.tool.Main',
                              args=args,
                              workunit_name='avro-tools')
        logger.info("avro-tools returns %i", result)
        if result != 0:
            raise TaskError('avro-tools returns {}'.format(result))
        return result

    def execute_codegen(self, target, target_workdir):
        if not isinstance(target, AvroJava):
            raise TaskError('Invalid target type "{}" '
                            '(expected AvroJava)'
                            .format(type(target).__name__))

        input_files = []
        for src in target.sources_relative_to_buildroot():
            if src.endswith('.avsc'):
                input_files.append(src)
            else:
                raise TaskError('avro-tools unknown file '
                                'type for {}'.format(src))

        if len(input_files) > 0:
            def flatten(l): return [x for y in l for x in y]
            result = self._compile_schema(
                    flatten([["compile", target.input_type], input_files,
                             [target_workdir]]))

            if result != 0:
                raise TaskError('avro-tools ... exited non-zero (%s)'
                                % result)

    @property
    def _copy_target_attributes(self):
        return ['provides']

    def synthetic_target_type(self, target):
        return JavaLibrary
