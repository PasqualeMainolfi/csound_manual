<!--
id:cabbageGet
category:Cabbage:Widgets
-->
# cabbageGet
This opcode queries the current value of a widget property, i.e,`colour`, `bounds.top`, `height`, etc. It can run at init-time or k-time and includes an optional output argument that triggers a value of 1 for one k-cycle whenever the widget value is updated or changed. String results can also be returned as a single [built-in trigger struct](https://cabbageaudio.com/docs/using/csound7/#built-in-trigger-structs) variable.

## Syntax

=== "Modern"
    ``` csound-orc
    value:k = cabbageGet(SChannel, SProperty)
    value:i = cabbageGet(SChannel, SProperty)
    value:S = cabbageGet(SChannel, SProperty)
    value:k, kTrig = cabbageGet(SChannel, SProperty)
    value:S, kTrig = cabbageGet(SChannel, SProperty)
    res:CabbageStrTrig = cabbageGet(SChannel, SProperty)
    ```

### Initialization

- *SChannel* – the name of the channel to query
- *SProperty* - the property you wish to access. If the property is part of a JSON object, such as `"bounds:{"left":0}` you can use dot notation, i.e., “bounds.left”
- *iValue* - the current value of the widget at init-time

### Performance

- *kValue* - the current value of the widget property
- *SValue* - the current string value of the widget property
- *kTrig* - a trigger signal that will return 1 for a single k-cycle whenever the value has been updated/changed
- *res:CabbageStrTrig* - `res.val` mirrors *SValue* and `res.trig` mirrors *kTrig*. k-rate only; the trigger fires when the property value changes.

## Examples

Here is an example of the cabbageGet opcode. It uses the file [cabbageGet.csd](../examples/cabbageGet.csd).

``` csound-csd title="Example of the cabbageGet opcode." linenums="1"
--8<-- "examples/cabbageGet.csd"
```

[Download cabbageGet.csd](https://cabbageaudio.com/examples/cabbageGet.csd)

## Credits

From the [Cabbage documentation](https://cabbageaudio.com/docs/opcodes/cabbageget/).
