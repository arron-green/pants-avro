from pants.backend.jvm.targets.jvm_target import JvmTarget
from pants.base.payload import Payload
from pants.base.payload_field import PrimitiveField
from pants.base.exceptions import TargetDefinitionException


import logging
logger = logging.getLogger(__name__)


class AvroJava(JvmTarget):
    def __init__(self, input_type=None, payload=None, **kwargs):
        payload = payload or Payload()
        payload.add_fields({
          'input_type': PrimitiveField(input_type),
        })
        super(AvroJava, self).__init__(payload=payload, **kwargs)
        if input_type not in ('schema', 'protocol'):
            raise TargetDefinitionException(self, 'unknown input_type {}'
                                            .format(input_type))
        self._input_type = input_type

    @property
    def input_type(self):
        return self._input_type
