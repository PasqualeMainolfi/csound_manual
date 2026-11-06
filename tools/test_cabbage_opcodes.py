import unittest

from cabbage_opcodes import parse_structs


PAGE = """---
title: "Csound 7"
---

### Built-in Trigger Structs

Many Cabbage get opcodes return a value plus a trigger. Cabbage registers two struct types:

| Struct type | Members | Use with |
|-------------|---------|----------|
| `CabbageNumTrig` | `val:k`, `trig:k` | numeric channels |
| `CabbageStrTrig` | `val:S`, `trig:k` | string channels |

The following opcode forms accept them:

- [`cabbageGetValue`](/docs/opcodes/cabbagegetvalue/) — both types
- [`cabbageGet`](/docs/opcodes/cabbageget/) — `CabbageStrTrig`

## Next section

- [`other`](/docs/opcodes/other/) — both types
"""


class ParseStructsTest(unittest.TestCase):
    def test_reads_the_struct_table(self):
        structs = parse_structs(PAGE, "https://cabbageaudio.com/docs/using/csound7/")
        self.assertEqual(list(structs), ["CabbageNumTrig", "CabbageStrTrig"])
        num = structs["CabbageNumTrig"]
        self.assertEqual(num["members"], [["val", "k"], ["trig", "k"]])
        self.assertEqual(num["source"], "Cabbage")
        self.assertEqual(num["doc"], "https://cabbageaudio.com/docs/using/csound7/#built-in-trigger-structs")
        self.assertEqual(
            num["description"],
            "Many Cabbage get opcodes return a value plus a trigger. Cabbage registers two struct types. Use with numeric channels.",
        )

    def test_opcodes_that_accept_each_struct(self):
        structs = parse_structs(PAGE, "u")
        self.assertEqual(structs["CabbageNumTrig"]["opcodes"], ["cabbageGetValue"])
        self.assertEqual(structs["CabbageStrTrig"]["opcodes"], ["cabbageGetValue", "cabbageGet"])

    def test_no_table(self):
        self.assertEqual(parse_structs("---\ntitle: x\n---\nNo structs here.\n", "u"), {})


if __name__ == "__main__":
    unittest.main()
