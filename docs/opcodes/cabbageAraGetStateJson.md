<!--
id:cabbageAraGetStateJson
category:Cabbage:ARA
-->
# cabbageAraGetStateJson
Returns the complete ARA data pool as a JSON string. Useful for passing ARA state directly to a web frontend or other JSON consumers.

## Syntax

=== "Modern"
    ``` csound-orc
    json:S = cabbageAraGetStateJson()                  ; i-rate: dump once on init
    json:S = cabbageAraGetStateJson(kTrig)             ; k-rate: dump on trigger
    ```

## Description

`cabbageAraGetStateJson` serializes the entire ARA document model state into a JSON string. The JSON contains all sections that `cabbageAraDump` prints in detailed mode, but as a structured string rather than formatted text.

The **i-rate** version returns the JSON once when the instrument initializes.

The **k-rate** version takes a trigger signal and returns a fresh JSON string each time the trigger transitions from zero to nonzero.

### JSON Structure

``` json
{
  "currentIndex": 0,
  "update": 12,
  "lastEvent": "notifySelection",
  "sourceCount": 1,
  "sources": [
    {
      "name": "cleanGuitar.wav",
      "channels": 1,
      "sampleRate": 44100,
      "sampleCount": 3226747,
      "duration": 73.169,
      "regionStartInSamples": 0,
      "regionDurationInSamples": 3226747,
      "regionStart": 0.0,
      "regionDuration": 73.169
    }
  ],
  "playbackRegionCount": 1,
  "playbackRegions": [
    {
      "name": "cleanGuitar.wav",
      "regionSequenceName": "cleanGuitar",
      "playbackStart": 0.0,
      "playbackDuration": 73.169,
      "regionStartInSamples": 0,
      "regionDurationInSamples": 3226747,
      "colorR": 0.0,
      "colorG": 0.0,
      "colorB": 1.0
    }
  ],
  "musicalContextCount": 1,
  "musicalContexts": [ ... ],
  "regionSequenceCount": 1,
  "regionSequences": [ ... ],
  "audioModificationCount": 1,
  "audioModifications": [ ... ],
  "editorView": {
    "selectedRegions": [ ... ],
    "hiddenSequenceCount": 0,
    "timeRangeStart": 0.0,
    "timeRangeDuration": 73.169
  }
}
```

## Examples
``` csound-orc
; Get JSON once at init
instr 1
  json:S = cabbageAraGetStateJson()
  printfi("JSON: %s\n", 1, json)
endin

; Get JSON on each ARA update
instr 2
  trig:k = cabbageAraGetUpdate()
  json:S = cabbageAraGetStateJson(trig)
endin

; Write JSON to stdout
instr 3
  trig:k = cabbageAraGetUpdate()
  if trig > 0 then
    json:S = cabbageAraGetStateJson(kTrig)
    printf(json, trig);
  endif
endin
```

## See also
- [cabbageAraDump](../opcodes/cabbageAraDump.md)
- [cabbageAraGet](../opcodes/cabbageAraGet.md)
- [cabbageAraGetUpdate](../opcodes/cabbageAraGetUpdate.md)

## Credits

From the [Cabbage documentation](https://cabbageaudio.com/docs/opcodes/cabbagearagetstatejson/).
