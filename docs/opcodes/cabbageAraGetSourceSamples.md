<!--
id:cabbageAraGetSourceSamples
category:Cabbage:ARA
-->
# cabbageAraGetSourceSamples
Reads PCM audio data from an ARA source. Available in four variants: a-rate (audio output), k-rate (k-rate output), k-array, and i-array.

## Syntax

=== "Modern"
    ``` csound-orc
    out:a = cabbageAraGetSourceSamples(aPos, iChan, iSourceIndex)
    out:k = cabbageAraGetSourceSamples(kPos, iChan, iSourceIndex)
    samples:k[] = cabbageAraGetSourceSamples(iStart, iCount, iChan, iSourceIndex)
    samples:i[] = cabbageAraGetSourceSamples(iStart, iCount, iChan, iSourceIndex)
    ```

### Initialization

* *iChan* — zero-based channel index within the source
* *iSourceIndex* — zero-based source index (obtain from `cabbageAraGet "currentIndex"`)
* *iStart* — first sample to read (array variants)
* *iCount* — number of samples to read (array variants)

### Performance

* *aPos* / *kPos* — sample position to read at (per-sample or per-k-cycle)
* *aOut* / *kOut* — output sample value at the given position

### Output arrays

* *kSamples[]* / *iSamples[]* — array of PCM samples from `iStart` to `iStart + iCount - 1`

## Description

This opcode provides direct access to the raw PCM audio data of an ARA source. The a-rate and k-rate variants read a single sample at the position given by `aPos`/`kPos`. The array variants read a contiguous block of samples starting at `iStart` for `iCount` samples.

Sample positions outside the valid range return 0. Prints warnings if the source index, channel index, or PCM data are invalid.

## Examples

``` csound-orc
instr 1
  index:i = cabbageAraGet("currentIndex")

  ; Read first 100 samples from channel 0 as an array
  samples:i[] = cabbageAraGetSourceSamples(0, 100, 0, index)

  ; Or read sample-by-sample at audio rate
  position:a = phasor(sr / lenarray(samples)) * lenarray(samples)
  out:a = cabbageAraGetSourceSamples(position, 0, index)
endin
```

## See also

- [cabbageAraGet](../opcodes/cabbageAraGet.md)
- [cabbageAraGetUpdate](../opcodes/cabbageAraGetUpdate.md)

## Credits

From the [Cabbage documentation](https://cabbageaudio.com/docs/opcodes/cabbagearagetsourcesamples/).
