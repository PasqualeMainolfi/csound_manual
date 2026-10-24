<!--
id:cabbageJsonHas
category:Cabbage:JSON
-->
# cabbageJsonHas
This opcode checks whether a dot-notation path exists in a JSON document (`nodes.0.params.rate`, where numeric segments index arrays). Unlike a query that returns an empty value, it distinguishes “missing” from “present but null/zero”. See also [cabbageJsonType](../opcodes/cabbageJsonType.md) and [cabbageJsonGet](../opcodes/cabbageJsonGet.md).

## Syntax

=== "Modern"
    ``` csound-orc
    has:i = cabbageJsonHas(json:S, path:S)
    has:k = cabbageJsonHas(json:S, path:S)
    ```

### Initialization

- *json:S* – a string holding a valid JSON document
- *path:S* – dot-notation path into the document
- *has:i* – `1` when the path exists (even if its value is `null`), else `0`

### Performance

- *has:k* – as *has:i*, re-evaluated each k-cycle

## Examples
``` csound-orc
instr 1
    doc:S = "{\"params\":{\"rate\":2.5}}"
    if cabbageJsonHas(doc, "params.rate") == 1 then
        rate:k = cabbageJsonGet(doc, "params.rate")
    endif
endin
```

## Full example

The following instrument exercises the JSON opcodes against a patcher-style state document:

Here is an example of the cabbageJsonHas opcode. It uses the file [cabbageJson.csd](../examples/cabbageJson.csd).

``` csound-csd title="Example of the cabbageJsonHas opcode." linenums="1"
--8<-- "examples/cabbageJson.csd"
```

[Download cabbageJson.csd](https://cabbageaudio.com/examples/cabbageJson.csd)

## Credits

From the [Cabbage documentation](https://cabbageaudio.com/docs/opcodes/cabbagejsonhas/).
