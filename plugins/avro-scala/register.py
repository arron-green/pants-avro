from pants.build_graph.build_file_aliases import BuildFileAliases
from .targets import AvroScala
from .gen import AvroScalaGen
from pants.goal.task_registrar import TaskRegistrar as task


def build_file_aliases():
    return BuildFileAliases(targets={'avro_scala': AvroScala})


def register_goals():
    task(name='avro-scala', action=AvroScalaGen).install('gen')
