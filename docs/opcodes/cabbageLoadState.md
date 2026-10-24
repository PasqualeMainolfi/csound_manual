<!--
id:cabbageLoadState
category:Cabbage:Files and State
-->
# cabbageLoadState
This opcode loads widget values from a previously saved JSON state file created by the `cabbageSaveState` opcode. All matching widget channels will be updated with their saved values. Unlike Cabbage 2, all widget state is saved and restored, not only the current parameter values. This opcode works at i-time only. Therefore it's best used in an instrument that is called when you want to load state.

## Syntax

=== "Modern"
    ``` csound-orc
    cabbageLoadState:i(SFilePath)
    ```

### Initialization

* *SFilePath* – the absolute file path to the state file to load (e.g., "/Users/username/Documents/mypreset.json" or "C:\\Users\\username\\Documents\\mypreset.json"). The file must exist and contain valid JSON data. Relative paths are not supported.

> **Note**
>
> Only widgets with channels that match those in the saved state file will be updated. Widgets not present in the state file will retain their current values. To load different presets, use Csound's string formatting to dynamically generate filenames, for example: `sprintf("/path/to/presets/preset_%d.json", iPresetNumber)`

## Examples

``` csound-orc
instr LoadState
    filename:S = sprintf("%s/myPreset.json", chnget:S("CSD_PATH"))
    cabbageLoadState(filename)
endin
```

To create the state file loaded here, see [cabbageSaveState](../opcodes/cabbageSaveState.md). For a full example, see [Saving and Loading State](https://cabbageaudio.com/docs/using/saving-and-loading-state/).

## Full example

Here is an example of the cabbageLoadState opcode. It uses the file [cabbageState.csd](../examples/cabbageState.csd).

``` csound-csd title="Example of the cabbageLoadState opcode." linenums="1"
--8<-- "examples/cabbageState.csd"
```

[Download cabbageState.csd](https://cabbageaudio.com/examples/cabbageState.csd)

## See also

- [cabbageSaveState](../opcodes/cabbageSaveState.md)
- [Saving and Loading State](https://cabbageaudio.com/docs/using/saving-and-loading-state/)

## Credits

From the [Cabbage documentation](https://cabbageaudio.com/docs/opcodes/cabbageloadstate/).
