scala_library(
  name='_myapp_lib',
  dependencies=[
    '3rdparty/jvm:avro',
    'src/main/avro:people',
    'src/main/avro:example',
  ],
  sources=globs('*.scala'),
)

jvm_binary(
  name='myapp',
  dependencies=[
    ':_myapp_lib',
  ],
  main='org.foo.bar.Main',
)
