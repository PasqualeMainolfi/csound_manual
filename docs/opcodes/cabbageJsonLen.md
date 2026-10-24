<!--
id:cabbageJsonLen
category:Cabbage:JSON
-->
# cabbageJsonLen
This opcode returns the size of the value at a dot-notation path in a JSON document: array length or object key count. Missing paths, scalars, and invalid documents yield `0`. See also [cabbageJsonGet](../opcodes/cabbageJsonGet.md) and [cabbageJsonHas](../opcodes/cabbageJsonHas.md).

## Syntax

=== "Modern"
    ``` csound-orc
    len:i = cabbageJsonLen(json:S, path:S)
    len:k = cabbageJsonLen(json:S, path:S)
    ```

### Initialization

* *json:S* – a string holding a valid JSON document
* *path:S* – dot-notation path into the document (`nodes.0.params`, where numeric segments index arrays)
* *len:i* – number of elements/keys, or `0`

### Performance

* *len:k* – as *len:i*, re-evaluated each k-cycle

## Examples

``` csound-orc
instr 1
    doc:S = "{\"gains\":[1, 2.5, 3]}"
    arr:k[] = cabbageJsonGet(doc, "gains")
    n:i = lenarray(arr)
    printf("mixing %d channels\n", 1, n)
endin
```

## Full example

The following instrument exercises the JSON opcodes against a patcher-style state document:

Here is an example of the cabbageJsonLen opcode. It uses the file [cabbageJson.csd](../examples/cabbageJson.csd).

``` csound-csd title="Example of the cabbageJsonLen opcode." linenums="1"
--8<-- "examples/cabbageJson.csd"
```

[Download cabbageJson.csd](https://cabbageaudio.com/examples/cabbageJson.csd)

## Credits

From the [Cabbage documentation](https://cabbageaudio.com/docs/opcodes/cabbagejsonlen/).
