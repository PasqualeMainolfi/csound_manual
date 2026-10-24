<!--
id:cabbageJsonType
category:Cabbage:JSON
-->
# cabbageJsonType
This opcode reports the JSON type of the value at a dot-notation path, so the orchestra can branch before querying. It is the typesafe companion to [cabbageJsonGet](../opcodes/cabbageJsonGet.md): use it when an empty string or zero is ambiguous (missing vs. present-but-empty, `"123"` vs. `123`).

## Syntax

=== "Modern"
    ``` csound-orc
    type:S = cabbageJsonType(json:S, path:S)
    ```

### Initialization

- *json:S* – a string holding a valid JSON document
- *path:S* – dot-notation path into the document, where numeric segments index arrays
- *type:S* – one of `"string"`, `"number"`, `"boolean"`, `"array"`, `"object"`, `"null"`, or `"missing"` (invalid documents report `"missing"` for every path)

### Performance

- Works at k-rate; the document is re-parsed only when the input text changes

## Examples
``` csound-orc
instr 1
    doc:S = "{\"freq\":\"440\"}"
    type:S = cabbageJsonType(doc, "freq")
    if strcmp(type, "string") == 0 then
        prints("frequency arrived as text, parsing...\n")
    endif
    freq:k = cabbageJsonGet(doc, "freq")
endin
```

## Full example

The following instrument exercises the JSON opcodes against a patcher-style state document:

Here is an example of the cabbageJsonType opcode. It uses the file [cabbageJson.csd](../examples/cabbageJson.csd).

``` csound-csd title="Example of the cabbageJsonType opcode." linenums="1"
--8<-- "examples/cabbageJson.csd"
```

[Download cabbageJson.csd](https://cabbageaudio.com/examples/cabbageJson.csd)

## Credits

From the [Cabbage documentation](https://cabbageaudio.com/docs/opcodes/cabbagejsontype/).
