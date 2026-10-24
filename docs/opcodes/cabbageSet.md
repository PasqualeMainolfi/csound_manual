<!--
id:cabbageSet
category:Cabbage:Widgets
-->
# cabbageSet
This opcode sets a widget property, i.e,`colour.fill`, `visible`, `opacity`, etc. It can run at init-time or k-time. The k-time variant must use a trigger to initiate the update (see below).

## Syntax

=== "Modern"
    ``` csound-orc
    cabbageSet:i(SChannel, SProperty, iValue)
    cabbageSet:i(SChannel, SProperty, iValue[])
    cabbageSet:i(SChannel, SProperty, SValue)
    cabbageSet:k(kTrig, SChannel, SProperty, SValue)
    cabbageSet:k(kTrig, SChannel, SProperty, kValue)
    cabbageSet:k(kTrig, SChannel, SProperty, kValue[])
    ```

### Initialization

* *SChannel* – the name of the channel to query
* *SProperty* - the property you wish to update. If the property is part of a JSON object, such as `"bounds:{"left":0}` you can use dot notation, i.e., "bounds.left"
* *iValue / iValue[]* - a value to set the widget property to

### Performance

* *kValue / kValue[]* - a value to set the widget property to
* *SValue* - a string value to set the widget property to
* *kTrig* - used to trigger updates at k-rate

> The k-rate variant of cabbageSet must use a k-rate trigger to initiate updates. This is to prevent the UI from being saturated with changes. If you need continuous updates, use a metro() opcode, for example: cabbageSet metro(5) ...

> However, even when sending frequent updates, such as 20 changes per second, the frontend may only process a subset of them. This is because the UI runs at a much slower frame rate than the audio thread.

## Examples

Here is an example of the cabbageSet opcode. It uses the file [cabbageSet.csd](../examples/cabbageSet.csd).

``` csound-csd title="Example of the cabbageSet opcode." linenums="1"
--8<-- "examples/cabbageSet.csd"
```

[Download cabbageSet.csd](https://cabbageaudio.com/examples/cabbageSet.csd)

## Credits

From the [Cabbage documentation](https://cabbageaudio.com/docs/opcodes/cabbageset/).
