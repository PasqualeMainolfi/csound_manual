<!--
id:cabbageDump
category:Cabbage:Widgets
-->
# cabbageDump
This opcode will print the JSON representation of a widget to the Csound console. This can be useful for debugging widgets.

## Syntax

=== "Modern"
    ``` csound-orc
    cabbageDump:i(SChannel, iIndent)
    cabbageDump:k(kTrig, SChannel, iIndent)
    ```

### Initialization

- *SChannel* – the name of the channel to query
- *iIndent* - If *iIndent* is nonnegative, then array elements and object members will be pretty-printed with that indent level. An indent level of 0 will only insert newlines. -1 selects the most compact representation. The default level is 4.

### Performance

- *kTrig* - a trigger signal that will cause the widget’s JSON representation to be printed to the console.

## Examples

Here is an example of the cabbageDump opcode. It uses the file [cabbageDump.csd](../examples/cabbageDump.csd).

``` csound-csd title="Example of the cabbageDump opcode." linenums="1"
--8<-- "examples/cabbageDump.csd"
```

[Download cabbageDump.csd](https://cabbageaudio.com/examples/cabbageDump.csd)

## Credits

From the [Cabbage documentation](https://cabbageaudio.com/docs/opcodes/cabbagedump/).
