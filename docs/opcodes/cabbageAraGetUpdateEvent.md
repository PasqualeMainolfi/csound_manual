<!--
id:cabbageAraGetUpdateEvent
category:Cabbage:ARA
-->
# cabbageAraGetUpdateEvent
Returns the type of the most recent ARA lifecycle event together with a trigger that is `1` for a single k-cycle whenever the ARA model data changes.

## Syntax

=== "Modern"
    ``` csound-orc
    event:S, trig:k = cabbageAraGetUpdateEvent()
    res:CabbageStrTrig = cabbageAraGetUpdateEvent()
    ```

### Performance

- *SEvent* — the name of the most recent ARA event as a string, for example `"audioSourceAddedToDocument"` or `"regionSequencePropertiesUpdated"` (k-rate)
- *kTrig* — fires `1` for a single k-cycle whenever the shared ARA document model data has been refreshed; `0` otherwise
- *res:CabbageStrTrig* — the [built-in trigger struct](https://cabbageaudio.com/docs/using/csound7/#built-in-trigger-structs) form: `res.val` holds *SEvent* and `res.trig` mirrors *kTrig*

## Description

This opcode pairs the edge trigger of [cabbageAraGetUpdate](../opcodes/cabbageAraGetUpdate.md) with the name of the event that caused it. The trigger fires on every refresh of the shared ARA document model, while *SEvent* tells you which lifecycle change produced it. Typical event names include:

- `audioSourceAddedToDocument`, `audioSourceRemovedFromDocument`
- `audioSourcePropertiesUpdated`, `audioModificationPropertiesUpdated`
- `playbackRegionAddedToRegionSequence`, `playbackRegionRemovedFromRegionSequence`
- `musicalContextAddedToDocument`, `regionSequenceAddedToDocument`
- `documentPropertiesUpdated`, `beginEditing`, `endEditing`
- `documentWillDestroy`

The same information is available through `cabbageAraGet "lastEvent"`; this opcode simply returns it directly, so no second query is needed inside the triggered block.

Only instruments running inside a host with ARA support see non-empty events. Outside an ARA session the string stays empty and the trigger never fires.

## Examples
``` csound-orc
instr 1
  event:CabbageStrTrig = cabbageAraGetUpdateEvent()
  printf("ARA event: %s\n", event.trig, event.val)
endin
```

The struct form compiles the two outputs into a single variable:

``` csound-orc
instr 1
  res:CabbageStrTrig  = cabbageAraGetUpdateEvent()
  printf("ARA event: %s\n", res.trig, res.val)
endin
```

## See also
- [cabbageAraGetUpdate](../opcodes/cabbageAraGetUpdate.md)
- [cabbageAraGet](../opcodes/cabbageAraGet.md)
- [cabbageAraDump](../opcodes/cabbageAraDump.md)

## Credits

From the [Cabbage documentation](https://cabbageaudio.com/docs/opcodes/cabbagearagetupdateevent/).
