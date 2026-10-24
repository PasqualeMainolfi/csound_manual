<!--
id:cabbageJsonGet
category:Cabbage:JSON
-->
# cabbageJsonGet
This opcode queries a JSON document using dot-notation paths (`nodes.0.params.rate`, where numeric segments index arrays). The output variable determines the expected type: assign to a string, number, or array and the matching overload runs. Invalid documents, missing paths, and type mismatches degrade gracefully to empty/zero values — use [cabbageJsonType](../opcodes/cabbageJsonType.md) and [cabbageJsonHas](../opcodes/cabbageJsonHas.md) when the distinction matters.

## Syntax

=== "Modern"
    ``` csound-orc
    val:S = cabbageJsonGet(json:S, path:S)
    val:k = cabbageJsonGet(json:S, path:S)
    val:i = cabbageJsonGet(json:S, path:S)
    val:S, trig:k = cabbageJsonGet(json:S, path:S)
    res:CabbageStrTrig = cabbageJsonGet(json:S, path:S)
    arr:S[] = cabbageJsonGet(json:S, path:S)
    arr:k[] = cabbageJsonGet(json:S, path:S)
    ```

### Initialization

- *json:S* – a string holding a valid JSON document
- *path:S* – dot-notation path into the document
- *val:S* – strings come back verbatim; numbers, booleans, and containers come back as compact JSON; missing paths yield `""`
- *val:i* – numbers direct; numeric strings parsed (`"42"` → `42`); booleans → `1`/`0`; anything else → `0`
- *arr:S*, *arr:k* – per-element rules as above (i-time only); missing paths and non-arrays yield empty arrays

### Performance

- *val:k* – as *val:i*, re-evaluated each k-cycle (the document is re-parsed only when the input text changes)
- *val:S* – as i-time; the document is re-parsed only when the input text changes
- *trig:k* – fires `1` for a single k-cycle whenever the result string changes
- *res:CabbageStrTrig* – the [built-in trigger struct](https://cabbageaudio.com/docs/using/csound7/#built-in-trigger-structs) form: `res.val` mirrors *val:S* and `res.trig` fires `1` for a single k-cycle whenever the result string changes. k-rate only.

## Examples
``` csound-orc
instr 1
    doc:S = "{\"nodes\":[{\"id\":\"n1\",\"params\":{\"freq\":440}}]}"
    id:S = cabbageJsonGet(doc, "nodes.0.id")
    freq:k = cabbageJsonGet(doc, "nodes.0.params.freq")
    printf("node %s runs at %f Hz\n", 1, id, freq)

    ; trigger struct form: fires when the fetched string changes
    res:CabbageStrTrig cabbageJsonGet(doc, "nodes.0.id")
    if res.trig == 1 then
        printf("id changed to %s\n", 1, res.val)
    endif
endin
```

## Full example

The following instrument exercises the JSON opcodes against a patcher-style state document:

Here is an example of the cabbageJsonGet opcode. It uses the file [cabbageJson.csd](../examples/cabbageJson.csd).

``` csound-csd title="Example of the cabbageJsonGet opcode." linenums="1"
--8<-- "examples/cabbageJson.csd"
```

[Download cabbageJson.csd](https://cabbageaudio.com/examples/cabbageJson.csd)

## Credits

From the [Cabbage documentation](https://cabbageaudio.com/docs/opcodes/cabbagejsonget/).
