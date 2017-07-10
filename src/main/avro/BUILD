avro_scala(
    name='people',
    sources=['people.avdl'],
    output_format='specific', # or 'standard' or 'scavro'
    dependencies=[
      '3rdparty/jvm/apache/avro',
    ],
)

avro_scala(
    name='example',
    sources=['example.avsc'],
    output_format='specific', # or 'standard' or 'scavro'
    dependencies=[
      '3rdparty/jvm/apache/avro',
    ],
)

avro_java(
    name='example-java',
    sources=['example.avsc'],
    input_type='schema', # or 'protocol'
    dependencies=[
      '3rdparty/jvm/apache/avro',
    ],
)
