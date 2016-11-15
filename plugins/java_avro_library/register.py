from pants.build_graph.build_file_aliases import BuildFileAliases
from java_avro_library.targets.java_avro_library import JavaAvroLibrary
from java_avro_library.tasks.apache_avro_gen import ApacheAvroGen
from pants.goal.task_registrar import TaskRegistrar as task


def build_file_aliases():
    return BuildFileAliases(
            targets={
                'java_avro_library': JavaAvroLibrary,
                },
            )


def register_goals():
    task(name='avro', action=ApacheAvroGen).install('gen')

