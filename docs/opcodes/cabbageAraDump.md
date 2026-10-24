<!--
id:cabbageAraDump
category:Cabbage:ARA
-->
# cabbageAraDump
Prints a formatted dump of the entire ARA data pool to the Csound output. Useful for debugging and understanding the state of the ARA document model. Supports two output modes: detailed property dump and ASCII timeline view.

## Syntax

=== "Modern"
    ``` csound-orc
    cabbageAraDump()                             ; i-rate: dump once on init
    cabbageAraDump(kTrig)                        ; k-rate: dump on trigger
    ```

## Description

`cabbageAraDump` is a diagnostic opcode that prints the complete ARA state to the Csound output window.

**Parameters:**

| Parameter | Description |
|-----------|-------------|
| `kTrig` | Trigger signal. Dumps when transitions from zero to nonzero (k-rate only). |

The **i-rate** version dumps once when the instrument initializes.

The **k-rate** version dumps each time the trigger transitions from zero to nonzero.

The output includes:

- **Status**: Last ARA event, update counter
- **Metrics**: Source count, playback region count, musical context count, region sequence count, audio modification count, selected region count, current source index
- **Time Range**: Host arrangement timeline position
- **Musical Contexts**: All musical contexts with name, order, and colour
- **Region Sequences**: All region sequences (tracks) with name, order, parent context, and colour
- **Playback Regions**: All clips in the document with their arrangement position, source crop, and colour
- **Selected Regions**: Currently selected clips with timeline position and source crop
- **Audio Modifications**: All audio modifications with name and persistent ID
- **Sources**: All audio sources with channels, sample rate, duration, and region crop

## Examples

``` csound-orc
; Dump once at init
instr 1
  cabbageAraDump()
endin

; Dump on each ARA update
instr 2
  trig:k = cabbageAraGetUpdate()
  cabbageAraDump(trig)
endin
```

## Output Format

``` text
=========================================
ARA STATE DUMP
=========================================
[Status]  Last Event:   notifySelection
[Status]  Update:       5
[Metrics] Sources: 2  |  Regions: 5  |  Contexts: 1  |  Sequences: 3  |  Modifications: 2  |  Selected: 2  |  Hidden: 0  |  Current Index: 0
[Time]    Host Range: 1.000 to 3.500 (2.500s)

------------ MUSICAL CONTEXTS -----------
[1] 'Default Context'
    Order:  1
    Colour: (0.20, 0.40, 0.80)

------------ REGION SEQUENCES -----------
[1] 'Lead Guitar'
    Order:     1
    Context:   #1
    Colour:    (0.90, 0.20, 0.20)
[2] 'Rhythm Guitar'
    Order:     2
    Context:   #1
    Colour:    (0.20, 0.80, 0.20)

------------ PLAYBACK REGIONS -----------
[1] 'guitar.wav'
    Start:    1.000s
    Duration: 2.500s
    Source Crop: Start=44100 samples, Dur=110250 samples
    Colour:   (0.90, 0.20, 0.20)

------------ SELECTED REGIONS ------------
[1] 'guitar.wav'
    Timeline Pos: 1.000s (Dur: 2.500s)
    Source Crop:  Start=44100 samples, Dur=110250 samples (2.500s)

------------ AUDIO MODIFICATIONS ---------
[1] 'guitar.wav'
    Persistent ID: 'com.example.mod1'

------------ SOURCES ---------------------
[1] 'guitar.wav'
    Channels:    2
    Sample Rate: 44100 Hz
    Sample Count: 176400
    Duration:    4.000s
    Region:      Start=44100 (1.000s), Duration=110250 (2.500s)
=========================================
```

It is also quite simple to iterate over the global ARA pool manually by accessing the individual ARA properties:

``` csound-orc
instr ShowAllInfo
    cabbageAraDump()
    ; --- Top-level state ---
    idx:i = cabbageAraGet("currentIndex")
    srcCnt:i = cabbageAraGet("audioSourceCount")
    lastEvent:S = cabbageAraGet("lastEvent")

    ; Print the header block
    printfi("=========================================\n", 1)
    printfi("ARA UPDATE No.%d\n", 1, p5)
    printfi("=========================================\n", 1)
    printfi("[Status]  Last Event:   %s\n", 1, lastEvent)

    ; --- Selection properties ---
    regCnt:i = cabbageAraGet("playbackRegionCount")
    mcCnt:i = cabbageAraGet("musicalContextCount")
    rsCnt:i = cabbageAraGet("regionSequenceCount")
    modCnt:i = cabbageAraGet("audioModificationCount")
    selRegCnt:i = cabbageAraGet("editorView.selectedPlaybackRegionCount")
    printfi("[Metrics] Sources: %d  |  Regions: %d  |  Contexts: %d  |  Sequences: %d  |  Modifications: %d  |  Selected: %d  |  Current Index: %d\n", 1, srcCnt, regCnt, mcCnt, rsCnt, modCnt, selRegCnt, idx)

    ; --- Time Range Calculations ---
    trStart:i = cabbageAraGet("editorView.timeRange.start")
    trDur:i = cabbageAraGet("editorView.timeRange.duration")
    printfi("[Time]    Host Range:   %.3f to %.3f (%.3fs)\n\n", 1, trStart, trStart + trDur, trDur)

    ; --- Musical Contexts Loop ---
    printfi("------------ MUSICAL CONTEXTS -----------\n", 1)
    if mcCnt == 0 then
        printfi("    [None]\n", 1)
    else
        mcIdx:i = 0
        while mcIdx < mcCnt do
            mcName:S = cabbageAraGet("musicalContext.name", mcIdx)
            mcOrder:i = cabbageAraGet("musicalContext.orderIndex", mcIdx)
            mcColR:i = cabbageAraGet("musicalContext.color.r", mcIdx)
            mcColG:i = cabbageAraGet("musicalContext.color.g", mcIdx)
            mcColB:i = cabbageAraGet("musicalContext.color.b", mcIdx)

            printfi("[%d] '%s'\n", mcIdx + 1, mcIdx, mcName)
            printfi("    Order:  %d\n", 1, mcOrder)
            printfi("    Colour: (%.2f, %.2f, %.2f)\n", 1, mcColR, mcColG, mcColB)
            mcIdx += 1
        od
    endif
    printfi("\n", 1)

    ; --- Region Sequences Loop ---
    printfi("------------ REGION SEQUENCES -----------\n", 1)
    if rsCnt == 0 then
        printfi("    [None]\n", 1)
    else
        rsIdx:i = 0
        while rsIdx < rsCnt do
            rsName:S = cabbageAraGet("regionSequence.name", rsIdx)
            rsOrder:i = cabbageAraGet("regionSequence.orderIndex", rsIdx)
            rsMcIdx:i = cabbageAraGet("regionSequence.musicalContextIndex", rsIdx)
            rsColR:i = cabbageAraGet("regionSequence.color.r", rsIdx)
            rsColG:i = cabbageAraGet("regionSequence.color.g", rsIdx)
            rsColB:i = cabbageAraGet("regionSequence.color.b", rsIdx)

            printfi("[%d] '%s'\n", rsIdx + 1, rsIdx, rsName)
            printfi("    Order:     %d\n", 1, rsOrder)
            printfi("    Context:   #%d\n", 1, rsMcIdx)
            printfi("    Colour:    (%.2f, %.2f, %.2f)\n", 1, rsColR, rsColG, rsColB)
            rsIdx += 1
        od
    endif
    printfi("\n", 1)

    ; --- Playback Regions Loop ---
    printfi("------------ PLAYBACK REGIONS -----------\n", 1)
    if regCnt == 0 then
        printfi("    [None]\n", 1)
    else
        selIdx:i = 0
        while selIdx < regCnt do
            selName:S = cabbageAraGet("playbackRegion.name", selIdx)
            pbStart:i = cabbageAraGet("playbackRegion.start", selIdx)
            pbDur:i = cabbageAraGet("playbackRegion.duration", selIdx)
            pbColR:i = cabbageAraGet("playbackRegion.color.r", selIdx)
            pbColG:i = cabbageAraGet("playbackRegion.color.g", selIdx)
            pbColB:i = cabbageAraGet("playbackRegion.color.b", selIdx)

            printfi("[%d] '%s'\n", selIdx + 1, selIdx, selName)
            printfi("    Start:    %.3fs\n", 1, pbStart)
            printfi("    Duration: %.3fs\n", 1, pbDur)
            printfi("    Colour:   (%.2f, %.2f, %.2f)\n", 1, pbColR, pbColG, pbColB)
            selIdx += 1
        od
    endif
    printfi("\n", 1)

    ; --- Selected Regions Loop ---
    printfi("------------ SELECTED REGIONS -----------\n", 1)
    if selRegCnt == 0 then
        printfi("    [None]\n", 1)
    else
        activeSelIdx:i = 0
        while activeSelIdx < selRegCnt do
            selRegName:S = cabbageAraGet("editorView.selectedRegion.name", activeSelIdx)
            selTimelineStart:i = cabbageAraGet("editorView.selectedPlayback.start", activeSelIdx)
            selTimelineDur:i = cabbageAraGet("editorView.selectedPlayback.duration", activeSelIdx)
            selSrcStartSamp:i = cabbageAraGet("editorView.selectedRegion.startInSamples", activeSelIdx)
            selSrcDurSamp:i = cabbageAraGet("editorView.selectedRegion.durationInSamples", activeSelIdx)

            printfi("[%d] '%s'\n", activeSelIdx + 1, activeSelIdx, selRegName)
            printfi("    Timeline Pos: %.3fs (Dur: %.3fs)\n", 1, selTimelineStart, selTimelineDur)
            printfi("    Source Crop:  Start=%d samples, Dur=%d samples\n", 1, selSrcStartSamp, selSrcDurSamp)
            activeSelIdx += 1
        od
    endif
    printfi("\n", 1)

    ; --- Audio Modifications Loop ---
    printfi("------------ AUDIO MODIFICATIONS --------\n", 1)
    if modCnt == 0 then
        printfi("    [None]\n", 1)
    else
        modIdx:i = 0
        while modIdx < modCnt do
            modName:S = cabbageAraGet("audioModification.name", modIdx)
            modId:S = cabbageAraGet("audioModification.persistentId", modIdx)

            printfi("[%d] '%s'\n", modIdx + 1, modIdx, modName)
            printfi("    Persistent ID: '%s'\n", 1, modId)
            modIdx += 1
        od
    endif
    printfi("\n", 1)

    ; --- Sources Loop ---
    printfi("------------ SOURCES ---------------------\n", 1)
    if srcCnt == 0 then
        printfi("    [None]\n", 1)
    else
        srcIdx:i = 0
        while srcIdx < srcCnt do
            name:S = cabbageAraGet("audioSource.name", srcIdx)
            channels:i = cabbageAraGet("audioSource.channels", srcIdx)
            sampCnt:i = cabbageAraGet("audioSource.sampleCount", srcIdx)
            sr:i = cabbageAraGet("audioSource.sampleRate", srcIdx)
            duration:i = cabbageAraGet("audioSource.duration", srcIdx)
            regStart:i = cabbageAraGet("audioSource.region.startInSamples", srcIdx)
            regDur:i = cabbageAraGet("audioSource.region.durationInSamples", srcIdx)

            printfi("[%d] '%s'\n", srcIdx + 1, srcIdx, name)
            printfi("    Channels: %d\n", 1, channels)
            printfi("    Sample Rate: %d Hz\n", 1, sr)
            printfi("    Sample Count: %d\n", 1, sampCnt)
            printfi("    Duration: %.3fs\n", 1, duration)
            printfi("    Region: Start=%d, Duration=%d\n", 1, regStart, regDur)
            srcIdx += 1
        od
    endif
    printfi("=========================================\n", 1)

endin
```

## See also

- [cabbageAraGet](../opcodes/cabbageAraGet.md)
- [cabbageAraGetUpdate](../opcodes/cabbageAraGetUpdate.md)

## Credits

From the [Cabbage documentation](https://cabbageaudio.com/docs/opcodes/cabbagearadump/).
