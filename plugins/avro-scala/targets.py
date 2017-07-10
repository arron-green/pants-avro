from pants.backend.jvm.targets.jvm_target import JvmTarget
from pants.base.payload import Payload
from pants.base.payload_field import PrimitiveField
from pants.base.exceptions import TargetDefinitionException


import logging
logger = logging.getLogger(__name__)


class AvroScala(JvmTarget):
    def __init__(self, output_format=None, payload=None, **kwargs):
        payload = payload or Payload()
        payload.add_fields({
          'output_format': PrimitiveField(output_format),
        })
        super(AvroScala, self).__init__(payload=payload, **kwargs)
        self.add_labels('codegen', 'avro')

        if output_format not in ('standard', 'specific', 'scavro'):
            raise TargetDefinitionException(self, 'unknown output_format {}'
                                            .format(output_format))
        self._output_format = output_format

    @property
    def output_format(self):
        return self._output_format
