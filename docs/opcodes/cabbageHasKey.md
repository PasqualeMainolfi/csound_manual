<!--
id:cabbageHasKey
category:Cabbage:Widgets
-->
# cabbageHasKey
This opcode checks whether a named widget has a given property key. It supports dot-notation for nested JSON properties (e.g., `"bounds.left"`). Returns 1 if the key exists, 0 otherwise. It can run at init-time or k-time.

## Syntax

=== "Modern"
    ``` csound-orc
    hasKey:i = cabbageHasKey(SChannel, SProperty)
    hasKey:k = cabbageHasKey(SChannel, SProperty)
    ```

### Initialization

* *SChannel* – the name of the widget channel to query
* *SProperty* – the property key to check. Supports dot-notation for nested properties, e.g., `"bounds.left"`
* *hasKey* – 1 if the property exists on the widget, 0 otherwise

### Performance

* *hasKey* – 1 if the property exists on the widget, 0 otherwise (evaluated each k-cycle)

## Examples

Here is an example of the cabbageHasKey opcode. It uses the file [cabbageHasKey.csd](../examples/cabbageHasKey.csd).

``` csound-csd title="Example of the cabbageHasKey opcode." linenums="1"
--8<-- "examples/cabbageHasKey.csd"
```

[Download cabbageHasKey.csd](https://cabbageaudio.com/examples/cabbageHasKey.csd)

## Notes

- If the specified channel does not match any widget, 0 is returned.
- Dot-notation traverses nested JSON objects, so `"bounds.left"` checks that both `bounds` and `left` within it exist.

## Credits

From the [Cabbage documentation](https://cabbageaudio.com/docs/opcodes/cabbagehaskey/).
