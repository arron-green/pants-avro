# Pants Build avro codegen POC

This was a quick hack to support avro case classes generation

Currently only supports scala with generate-specific (hardcoded)

ideally i would like to support other options that [avrohugger](https://github.com/julianpeeters/avrohugger) supports

# Run the example

```
./pants binary .::
./pants run.jvm src/main/scala/org/foo/bar:myapp
```

