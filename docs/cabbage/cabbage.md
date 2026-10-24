# **Cabbage Opcodes**

[Cabbage](https://cabbageaudio.com) ships with a number of opcodes that provide an interface to each widget's underlying JSON object. Any property of a widget's `props` member can be accessed or modified using the [cabbageGet](../opcodes/cabbageGet.md)/[cabbageSet](../opcodes/cabbageSet.md) opcodes. A widget's value can be queried and set using the [cabbageGetValue](../opcodes/cabbageGetValue.md) and [cabbageSetValue](../opcodes/cabbageSetValue.md) opcodes. A number of utility opcodes are also included.

These opcodes are only available when running Csound inside Cabbage. See the [Cabbage documentation](https://cabbageaudio.com/docs/opcodes/overview/) for details.

## Widgets

- [cabbageCreate](../opcodes/cabbageCreate.md)
- [cabbageDump](../opcodes/cabbageDump.md)
- [cabbageGet](../opcodes/cabbageGet.md)
- [cabbageGetValue](../opcodes/cabbageGetValue.md)
- [cabbageGetWidgets](../opcodes/cabbageGetWidgets.md)
- [cabbageHasKey](../opcodes/cabbageHasKey.md)
- [cabbageSendMessage](../opcodes/cabbageSendMessage.md)
- [cabbageSet](../opcodes/cabbageSet.md)
- [cabbageSetValue](../opcodes/cabbageSetValue.md)

## JSON

- [cabbageJsonGet](../opcodes/cabbageJsonGet.md)
- [cabbageJsonHas](../opcodes/cabbageJsonHas.md)
- [cabbageJsonLen](../opcodes/cabbageJsonLen.md)
- [cabbageJsonSet](../opcodes/cabbageJsonSet.md)
- [cabbageJsonType](../opcodes/cabbageJsonType.md)

## Files and State

- [cabbageCreateFileName](../opcodes/cabbageCreateFileName.md)
- [cabbageGetFiles](../opcodes/cabbageGetFiles.md)
- [cabbageLoadState](../opcodes/cabbageLoadState.md)
- [cabbageSaveState](../opcodes/cabbageSaveState.md)

## ARA

- [cabbageAraDump](../opcodes/cabbageAraDump.md)
- [cabbageAraGet](../opcodes/cabbageAraGet.md)
- [cabbageAraGetSourceSamples](../opcodes/cabbageAraGetSourceSamples.md)
- [cabbageAraGetStateJson](../opcodes/cabbageAraGetStateJson.md)
- [cabbageAraGetUpdate](../opcodes/cabbageAraGetUpdate.md)
- [cabbageAraGetUpdateEvent](../opcodes/cabbageAraGetUpdateEvent.md)
