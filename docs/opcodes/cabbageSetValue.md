<!--
id:cabbageSetValue
category:Cabbage:Widgets
-->
# cabbageSetValue
This opcode sets the current value of a widget and can be executed at either init-time or k-time. When called, it immediately writes the incoming value to a Csound channel and also places the value into a FIFO queue, which the frontend reads to update the UI.

Because the frontend operates at a much lower frame rate than the audio thread, it cannot process every value update. While all updates are written to the underlying Csound channel, many intermediate values will not make it into the FIFO queue and therefore will not be seen by the frontend. However, the most recent value will always make it through, ensuring the UI remains in sync with the latest state.

## Syntax

=== "Modern"
    ``` csound-orc
    cabbageSetValue:k(SChannel, kValue [, kTrigger]) 
    cabbageSetValue:i(SChannel, iValue) 
    ```

### Initialization

* *SChannel* – the name of the channel to query
* *iValue* - the value to set the widget to

### Performance

* *kValue* - the value to set the widget to
* *kTrigger* - a signal used to trigger a value update

## Examples

Here is an example of the cabbageSetValue opcode. It uses the file [cabbageSetValue.csd](../examples/cabbageSetValue.csd).

``` csound-csd title="Example of the cabbageSetValue opcode." linenums="1"
--8<-- "examples/cabbageSetValue.csd"
```

[Download cabbageSetValue.csd](https://cabbageaudio.com/examples/cabbageSetValue.csd)

## Credits

From the [Cabbage documentation](https://cabbageaudio.com/docs/opcodes/cabbagesetvalue/).
