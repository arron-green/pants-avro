from pants.backend.jvm.targets.jvm_target import JvmTarget
# from pants.base.exceptions import TargetDefinitionException


class JavaAvroLibrary(JvmTarget):
    # _OUTPUT_FORMATS = frozenset(['standard', 'specific', 'scavro'])

    def __init__(self, output_format=None, **kwargs):
        super(JavaAvroLibrary, self).__init__(**kwargs)

        # TODO fix me
        # def check_value_for_arg(arg, value, values):
        #     if value and value not in values:
        #         raise TargetDefinitionException(self, "{} may only be set to {} ('{}' not valid)"
        #                                         .format(arg, ', or '.join(map(repr, values)), value))
        #     return value
        #
        # self._output_format = check_value_for_arg('output_format', output_format, self._OUTPUT_FORMATS)

    # @property
    # def output_format(self):
    #     if self._output_format == 'specific':
    #         return 'generate-specific'
    #     elif self._output_format == 'scavro':
    #         return 'generate-scavro'
    #     else:
    #         return 'generate'
