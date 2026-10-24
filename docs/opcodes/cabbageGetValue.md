<!--
id:cabbageGetValue
category:Cabbage:Widgets
-->
# cabbageGetValue
This opcode queries the current value of a widget. It can run at init-time or k-time and includes an optional output argument that triggers a value of 1 for one k-cycle whenever the widget value is updated or changed. The value and trigger can either be returned as two separate variables, or as a single [built-in trigger struct](https://cabbageaudio.com/docs/using/csound7/#built-in-trigger-structs) variable.

## Syntax

=== "Modern"
    ``` csound-orc
    value:i = cabbageGetValue(SChannel)
    value:k = cabbageGetValue(SChannel)
    value:S = cabbageGetValue(SChannel)
    value:k, trig:k = cabbageGetValue(SChannel)
    value:S, trig:k = cabbageGetValue(SChannel)
    res:CabbageNumTrig = cabbageGetValue(SChannel)
    res:CabbageStrTrig = cabbageGetValue(SChannel)
    ```

### Initialization

* *SChannel* – the name of the channel to query
* *iValue* - the current value of the widget at i-time

### Performance

* *kValue* - the current value of the widget at k-time
* *SValue* - the current value of the widget at i/k-time. The trigger version of `cabbageGetValue` for strings works at k-rate, the non trigger version is i-time only.
* *kTrig* - a trigger signal that will return 1 for a single k-cycle whenever the value has been updated/changed
* *res:CabbageNumTrig* - numeric channels. `res.val` mirrors *kValue* and `res.trig` mirrors *kTrig*. Runs at init-time and k-time.
* *res:CabbageStrTrig* - string channels. `res.val` holds the latest string and `res.trig` fires 1 for a single k-cycle whenever the string changes. k-rate only; on the first pass the trigger is primed to 0, so only subsequent changes fire.

## Examples

Here is an example of the cabbageGetValue opcode. It uses the file [cabbageGetValue.csd](../examples/cabbageGetValue.csd).

``` csound-csd title="Example of the cabbageGetValue opcode." linenums="1"
--8<-- "examples/cabbageGetValue.csd"
```

[Download cabbageGetValue.csd](https://cabbageaudio.com/examples/cabbageGetValue.csd)

## Credits

From the [Cabbage documentation](https://cabbageaudio.com/docs/opcodes/cabbagegetvalue/).
