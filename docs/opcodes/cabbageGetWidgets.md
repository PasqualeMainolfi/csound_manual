<!--
id:cabbageGetWidgets
category:Cabbage:Widgets
-->
# cabbageGetWidgets
Returns a string array containing the IDs of all widgets currently loaded in the instrument. This opcode works at i-time only. Each entry in the returned array corresponds to a widget’s top-level `id` field, or falls back to `channels[0].id` if no top-level `id` is present. This opcodes runs at i-time only.

## Syntax

=== "Modern"
    ``` csound-orc
    SWidgetIds[] = cabbageGetWidgets()
    ```

## Initialization

- `SWidgetIds[]` – a string array of widget IDs, one entry per widget in the current Cabbage layout.

## Examples

Here is an example of the cabbageGetWidgets opcode. It uses the file [cabbageGetWidgets.csd](../examples/cabbageGetWidgets.csd).

``` csound-csd title="Example of the cabbageGetWidgets opcode." linenums="1"
--8<-- "examples/cabbageGetWidgets.csd"
```

[Download cabbageGetWidgets.csd](https://cabbageaudio.com/examples/cabbageGetWidgets.csd)

## Notes

- This opcode is i-time only; call it from an instrument that runs at initialisation, or from a always-on instrument (`i1 0 z`).
- The form widget is included in the returned array.
- If a widget has no `id` field and no `channels[0].id`, an empty string is returned for that entry.
- Combine with `cabbageGet` or `cabbageHasKey` to dynamically inspect widget properties at startup.

## Credits

From the [Cabbage documentation](https://cabbageaudio.com/docs/opcodes/cabbagegetwidgets/).
