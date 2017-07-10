from pants.base.exceptions import TaskError
from pants.task.simple_codegen_task import SimpleCodegenTask
from pants.backend.jvm.targets.scala_jar_dependency import ScalaJarDependency
from pants.backend.jvm.targets.java_library import JavaLibrary
from pants.backend.jvm.tasks.nailgun_task import NailgunTaskBase
from .targets import AvroScala

import logging
logger = logging.getLogger(__name__)


class AvroScalaGen(NailgunTaskBase, SimpleCodegenTask):
    @classmethod
    def product_types(cls):
        return ['scala']

    @classmethod
    def register_options(cls, register):
        cls.register_jvm_tool(register, 'avrohugger-tools',
                              classpath=[
                                ScalaJarDependency(
                                    'com.julianpeeters',
                                    'avrohugger-tools',
                                    '0.16.0')
                              ])
        super(AvroScalaGen, cls).register_options(register)

    @property
    def avrohugger_classpath(self):
        return self.tool_classpath('avrohugger-tools')

    @classmethod
    def prepare(cls, options, round_manager):
        super(AvroScalaGen, cls).prepare(options, round_manager)

    def execute(self):
        super(AvroScalaGen, self).execute()

    def is_gentarget(self, target):
        return isinstance(target, AvroScala)

    def __init__(self, *args, **kwargs):
        super(AvroScalaGen, self).__init__(*args, **kwargs)
        self.set_distribution(jdk=True)
        self.gen_langs = set()
        if self.context.products.isrequired('scala'):
            self.gen_langs.add('scala')

    def _compile_schema(self, args):
        logger.info('AvroScalaGen: invoking avrohugger-tools '
                    'with args %s', args)
        result = self.runjava(classpath=self.avrohugger_classpath,
                              main='avrohugger.tool.Main',
                              args=args,
                              workunit_name='avrohugger-tools')
        logger.info("avrohugger-tools returns %i", result)
        if result != 0:
            raise TaskError('avrohugger-tools returns {}'.format(result))
        return result

    def execute_codegen(self, target, target_workdir):
        if not isinstance(target, AvroScala):
            raise TaskError('Invalid target type "{}" '
                            '(expected AvroScala)'
                            .format(type(target).__name__))

        output_format = target.output_format
        if output_format == 'standard':
            operation = 'generate'
        elif output_format == 'specific':
            operation = 'generate-specific'
        elif output_format == 'scavro':
            operation = 'generate-scavro'
        else:
            raise TaskError('avrohugger unknown output_format %s'
                            % output_format)

        input_files = []
        for src in target.sources_relative_to_buildroot():
            if src.endswith('.avsc') or src.endswith('.avdl'):
                input_files.append(src)
            else:
                raise TaskError('avrohugger unknown file '
                                'type for {}'.format(src))

        if len(input_files) > 0:
            def flatten(l): return [x for y in l for x in y]
            result = self._compile_schema(
                   flatten([[operation, 'schema'], input_files,
                            [target_workdir]]))

            if result != 0:
                raise TaskError('avrohugger-tools ... exited non-zero (%s)'
                                % result)

    @property
    def _copy_target_attributes(self):
        return ['provides']

    def synthetic_target_type(self, target):
        return JavaLibrary
