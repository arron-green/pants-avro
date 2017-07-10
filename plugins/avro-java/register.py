from pants.build_graph.build_file_aliases import BuildFileAliases
from .targets import AvroJava
from .gen import AvroJavaGen
from pants.goal.task_registrar import TaskRegistrar as task


def build_file_aliases():
    return BuildFileAliases(targets={'avro_java': AvroJava})


def register_goals():
    task(name='avro-java', action=AvroJavaGen).install('gen')
