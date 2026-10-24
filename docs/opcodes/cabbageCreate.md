<!--
id:cabbageCreate
category:Cabbage:Widgets
-->
# cabbageCreate
This opcode will create a new widget based on a JSON object. Note that widgets generated in this way cannot be registered as parameters. This means they cannot be automated by the host. Note this opcode only runs at i-time.

## Syntax

=== "Modern"
    ``` csound-orc
    cabbageCreate:i(SJson)
    ```

### Initialization

* *SJson* – a well-formed JSON string. This will typically look like a JSON object from the Cabbage section JSON array.

> **Note**
>
> You need to provide a channel and a valid type when creating the string.

## Examples

Here is an example of the cabbageCreate opcode. It uses the file [cabbageCreate.csd](../examples/cabbageCreate.csd).

``` csound-csd title="Example of the cabbageCreate opcode." linenums="1"
--8<-- "examples/cabbageCreate.csd"
```

[Download cabbageCreate.csd](https://cabbageaudio.com/examples/cabbageCreate.csd)

### Extended example

A larger step-sequencer built on the same `cabbageCreate` technique:

Here is an example of the cabbageCreate opcode. It uses the file [GridSequencer.csd](../examples/GridSequencer.csd).

``` csound-csd title="Example of the cabbageCreate opcode." linenums="1"
--8<-- "examples/GridSequencer.csd"
```

[Download GridSequencer.csd](https://cabbageaudio.com/examples/GridSequencer.csd)

## Credits

From the [Cabbage documentation](https://cabbageaudio.com/docs/opcodes/cabbagecreate/).
