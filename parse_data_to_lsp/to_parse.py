import json
import os
import re
import html

PATH_TO_OPCODES_ROOT: str = "../docs/opcodes"
PATH_TO_FLAGS_ROOT: str = "../docs/invoke/cs-options-alphabetically.md"
TEMPLATE_OPCODE_ADDRESS = "https://csound.com/manual/opcodes/"
TEMPLATE_CABBAGE_OPCODE_ADDRESS = "https://cabbageaudio.com/docs/opcodes/"
CABBAGE_CATEGORY_FLAG = "category:Cabbage"

TEMPLATE = {
    "prefix": "",
    "body": "",
    "description": ""
}

NAME_FLAG = "# "
SYNTAX_FLAG = "## Syntax"
MODERN_FLAG = '=== "Modern"'
ORC_SPACE_FLAG = "``` csound-orc"
ORC_NOSPACE_FLAG = "```csound-orc"

regex = re.compile(r"\(\.\./opcodes/.*\.md\)")
regex_new = re.compile(r'[A-Za-z0-9_\[\]]+:[A-Za-z0-9_\[\]]+')
regex_c = re.compile(r'[A-Za-z0-9_\[\]]\([A-Za-z0-9_\[\]:,\{\}]+\)')
regex_d = re.compile(r'\([A-Za-z0-9_]\)')
regex_e = re.compile(r'\[[^\[\]]*=[^\[\]]*\]')
regex_typed = re.compile(r'[A-Za-z0-9_\[\]]+:[A-Za-z0-9_\[\]{*]')

def check_newline(lines, current_line, current_index, counter):
    while current_line.endswith("\\"):
        current_line = current_line[:-1] + lines[current_index + counter].strip()
        counter += 1
    return current_line, counter

def escape_dollar(prefix):
    return re.sub(r'\$', r'\\$', prefix)

def prev_nonempty_line(lines, current_index):
    j = current_index - 1
    while j >= 0 and not lines[j].strip():
        j -= 1
    return lines[j] if j >= 0 else ""

def strip_comment(line):
    # remove a trailing ; comment, ignoring ; inside string literals
    in_string = False
    for k, char in enumerate(line):
        if char == '"':
            in_string = not in_string
        elif char == ";" and not in_string:
            return line[:k].rstrip()
    return line

def opcode_args(line):
    # text between the first "(" and its matching ")"
    start = line.find("(")
    if start == -1:
        return None
    depth = 0
    for k in range(start, len(line)):
        if line[k] == "(":
            depth += 1
        elif line[k] == ")":
            depth -= 1
            if depth == 0:
                return line[start + 1:k]
    return line[start + 1:]

def split_args(args):
    # split on commas outside (), {} and strings; [ ] of optional args stay on the tokens
    parts = []
    depth = 0
    in_string = False
    current = ""
    for char in args:
        if char == '"':
            in_string = not in_string
        elif not in_string and char in "({":
            depth += 1
        elif not in_string and char in ")}":
            depth -= 1
        if char == "," and depth == 0 and not in_string:
            parts.append(current)
            current = ""
        else:
            current += char
    parts.append(current)
    return parts

def split_optional_marks(token):
    # "kValue [" -> ("", "kValue", "["), "[id:i]" -> ("[", "id:i", "]"); array [] stays in the core
    core = token.strip()
    lead = ""
    trail = ""
    while core.startswith("["):
        lead += "["
        core = core[1:].strip()
    while True:
        core = core.rstrip()
        if core.endswith("["):
            trail = "[" + trail
            core = core[:-1]
        elif core.endswith("]") and core.count("]") > core.count("["):
            trail = "]" + trail
            core = core[:-1]
        else:
            break
    return lead, core, trail

def first_arg_rest(line):
    # first argument name without its rate prefix, e.g. "amp" for "xamp"
    args = opcode_args(line)
    if args is None:
        return None
    name = re.match(r'[\s\[]*([A-Za-z0-9_"]*)', args).group(1)
    return name[1:]

def merge_typed_args(variants):
    # merge "name:type" args position by position, e.g. val:S + val:k -> val:{S, k}
    base = [split_optional_marks(part) for part in split_args(opcode_args(variants[0]))]
    names = [core.split(":")[0] for _, core, _ in base]
    types = [[core.split(":", 1)[1]] if ":" in core else [] for _, core, _ in base]
    for variant in variants[1:]:
        args = opcode_args(variant)
        if args is None:
            continue
        parts = [split_optional_marks(part)[1] for part in split_args(args)]
        if [core.split(":")[0] for core in parts] != names:
            continue
        for k, core in enumerate(parts):
            if ":" in core:
                t = core.split(":", 1)[1]
                if t not in types[k]:
                    types[k].append(t)
    merged = []
    for (lead, core, trail), name, t in zip(base, names, types):
        if len(t) > 1:
            core = f"{name}:{{{', '.join(sorted(t))}}}"
        core = re.sub(r"\{[^{}]*\}", lambda m: re.sub(r",\s*", ", ", m.group(0)), core)
        merged.append(f"{lead}{core}{trail.replace('[', ' [')}")
    return ", ".join(merged)

def parse_opcode_types(current_line):
    tsplit_equal = current_line.split("=")
    # print(tsplit_equal[0].strip())
    if len(tsplit_equal) > 1:
        tsplit_equal = tsplit_equal[1]
    else:
        tsplit_equal = tsplit_equal[0]
    tsplit_par = tsplit_equal.split("(")
    if len(tsplit_par) > 1:
        tsplit_par = tsplit_par[1]
    else:
        tsplit_par = tsplit_par[0]
    if not regex_new.search(tsplit_par):
        tsplit_par = tsplit_par[0].strip()
        if tsplit_par not in ["[", '"']:
            tsplit_par = re.sub(r"[^A-Za-z]", "", tsplit_par)
    else:
        if tsplit_par.endswith(")"):
            tsplit_par = tsplit_par[:-1]
        else:
            tsplit_par = tsplit_par[:-2]
        tsplit_par = f"{tsplit_par.strip()}"
    if tsplit_par.endswith(")"):
        tsplit_par = tsplit_par[:-1]
    format_split = tsplit_par.split(",")
    format_split = [c.strip() for c in format_split]
    if len(format_split) > 1:
        tsplit_par = ', '.join(format_split)
    else:
        tsplit_par = format_split[0]
    # print("tsplit: ", tsplit_par)
    return tsplit_par

def parse_opcode_body(lines, returned_body, current_index):
    body = lines[current_index]
    if body.endswith("\\"):
        body = returned_body
    tbody = body
    body = body.split("=")
    if regex_e.search(tbody):
        body_par = tbody.split("(")
    else:
        if len(body) > 1:
            body = body[1]
        else:
            body = body[0]
        body_par = body.split("(")
    return body_par

def format_types(types):
    types = sorted(types)
    if len(types) == 0:
        types = ""
    elif len(types) == 1:
        types = types.pop()
    else:
        types = f"{{{', '.join(types).strip()}}}"
        # print("types: ", types)
    return types

def get_snippet(opnames, opcode_body, types):
    body_clos = opcode_body[1].strip()[1:]
    if ":" not in body_clos:
        if not body_clos.endswith(")"):
            body_clos += ")"
        opcode_body_args = f"({types}{body_clos}"
    else:
        opcode_body_args = f"({types})"
        print("t: ", opcode_body_args)

    if "[, " in opcode_body_args:
        # index_leg = opcode_body_args.find("[, ")
        indexes_leg = re.finditer(r'(\[, )', opcode_body_args)
        matches = [m.start() for m  in indexes_leg]
        temp_args = []
        prev = 0
        print("B: ", opcode_body_args)
        # temp_args.append(opcode_body_args[:matches[0]])
        for i, start_index  in enumerate(matches):
            t = opcode_body_args[prev:start_index].strip()
            if t.endswith(","):
                t = t[:-1]
            temp_args.append(t)
            prev = start_index
            print(i, start_index, temp_args)
        temp_args.append(opcode_body_args[prev:])
        opcode_body_args = ' '.join(temp_args)
        # print(opcode_body_args)
    if opcode_body_args[-2] == ",":
        opcode_body_args =  f"{opcode_body_args[:-2]})"
    body = f"{opnames}{opcode_body_args}"
    print(body)
    return body

FLAG_NO_CS7 = ["--expression-opt"]
FLAG_ROW = "####"
FLAG_TEMPLATE = { "prefix": "", "body": "", "description": "" }
BODY_MARK = r'(^-[-+a-zA-Z0-9_&#]+)'
def generate_flags():
    flags = {}
    with open(PATH_TO_FLAGS_ROOT, "r", encoding="utf-8") as f:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith(FLAG_ROW):
                split_line = line.split(FLAG_ROW)
                flag = split_line[1].strip()
                if flag not in flags:
                    if flag not in FLAG_NO_CS7:
                        flags[flag] = FLAG_TEMPLATE.copy()
                        flags[flag]["prefix"] = html.unescape(flag.strip())
                        body = flag.split(",")[0]
                        body = re.findall(BODY_MARK, body)

                        if body:
                            flags[flag]["body"] = body[0].strip()

                        count = i + 1
                        descr = []
                        while count < len(lines) and not lines[count].startswith(FLAG_ROW):
                            line_content = lines[count]
                            if line_content:
                                descr.append(line_content)
                            count += 1

                        description = " ".join(descr)
                        flags[flag]["description"] = description

                        print(flag)
                        print(body)
                        print(description)
                        i = count - 1
                        continue
            i += 1

    with open("json_data/flags.json", "w", encoding="utf-8") as fout:
        json.dump(flags, fout, ensure_ascii=False, indent=4)

def main() -> None:
    opcodes_files = os.listdir(PATH_TO_OPCODES_ROOT)
    same_to_check = []
    opcodes_dict = {}
    opcode_indexes = {}
    for opcode in opcodes_files:
        if opcode.endswith(".md"):
            path_to_opcode = os.path.join(PATH_TO_OPCODES_ROOT, opcode)
            with open(path_to_opcode, "r", encoding="utf-8") as f:
                opmd = f.read()
                lines = opmd.splitlines()
                name_line = None
                op = TEMPLATE.copy()
                for i, line in enumerate(lines):
                    if line.startswith(NAME_FLAG):
                        opnames = f"{html.unescape(line.split(' ')[1])}"
                        opnames = escape_dollar(prefix=opnames)
                        if opnames not in opcodes_dict:
                            name_line = i
                            opcodes_dict[opnames] = op
                            opcodes_dict[opnames]["body"] = opnames

                            op_index_name = opcode.split(".")[0]
                            if CABBAGE_CATEGORY_FLAG in opmd:
                                opcode_indexes[op_index_name] = f"{TEMPLATE_CABBAGE_OPCODE_ADDRESS}{op_index_name.lower()}/"
                            else:
                                opcode_indexes[op_index_name] = f"{TEMPLATE_OPCODE_ADDRESS}{op_index_name}/"

                    if line.strip().lower().startswith("same as"):
                        find_ref = re.findall(r'\[(\w+)\]', line)
                        # print("REFERENCE: ", find_ref, "CURRENT: ", opnames)
                        if find_ref:
                            same_op = find_ref[0]
                            # print("FINDED REFERENCE: ", same_op)
                            if same_op in opcodes_dict:
                                opcodes_dict[opnames]["prefix"] = re.sub(same_op, opnames, opcodes_dict[same_op]["prefix"])
                                opcodes_dict[opnames]["description"] = re.sub(same_op, opnames, opcodes_dict[same_op]["description"])
                                # print("FIX: ", opcodes_dict[opnames])
                            else:
                                same_to_check.append((opnames, same_op)) # if not yet exists check after (op to complete, ref op)
                        else:
                            print(f"[WARNING] Same opcode ref not found for {opnames}")
                        break
                    if line.startswith(SYNTAX_FLAG) and name_line is not None:
                        count_descr = name_line + 1
                        description = lines[count_descr]
                        while not description:
                            count_descr += 1
                            description = lines[count_descr]
                        description = f"{html.unescape(description)}"
                        if regex.search(description):
                            description = regex.sub("", description)
                        opcodes_dict[opnames]["description"] = escape_dollar(prefix=description)
                    if line.startswith(MODERN_FLAG):
                        if prev_nonempty_line(lines, i).strip().startswith(SYNTAX_FLAG):
                            syntax_lines = [strip_comment(l) for l in lines]
                            j = i + 1
                            condition = not syntax_lines[j].strip().startswith(ORC_NOSPACE_FLAG) and not syntax_lines[j].strip().startswith(ORC_SPACE_FLAG)
                            while j < len(syntax_lines) and condition:
                                j += 1
                            index = j + 1
                            current_line = syntax_lines[index]
                            # print(current_line)
                            types = set()
                            variants = []
                            count_line = 0
                            return_body = ""
                            while current_line.strip() != "```":
                                check_line = current_line.strip()
                                count_line += 1
                                if not (len(check_line) == 1 and check_line == ")"):
                                    return_body, count_line = check_newline(syntax_lines, current_line, index, count_line)
                                    variants.append(return_body)
                                    # merge rate prefixes only for the same first argument (xamp/kamp, not SChannel/kTrig)
                                    if first_arg_rest(return_body) == first_arg_rest(variants[0]):
                                        optypes = parse_opcode_types(current_line)
                                        types.add(optypes)
                                    # print(types)
                                current_line = syntax_lines[index + count_line]
                            if len(types) > 1:
                                types.discard("[")
                                types.discard('"')
                            opcode_body = parse_opcode_body(syntax_lines, return_body, index)
                            types.discard("")
                            first_args = opcode_args(variants[0]) if variants else None
                            if first_args is not None and regex_typed.search(first_args):
                                body = f"{opnames}({merge_typed_args(variants)})"
                                opcodes_dict[opnames]["prefix"] = escape_dollar(prefix=body)
                            elif len(opcode_body) > 1:
                                types = format_types(types)
                                # print("types format: ", types)
                                # print("op body format: ", types)
                                body = get_snippet(opnames, opcode_body, types)
                                # print("body: ", body)
                                opcodes_dict[opnames]["prefix"] = escape_dollar(prefix=body)
                                # print(opcodes_dict[opnames])
                            else:
                                print(f"[WARNING] Wrong opcode prefix format {opnames, current_line, j, index}")
                            break
                    if line.strip().startswith(ORC_NOSPACE_FLAG) or line.strip().startswith(ORC_SPACE_FLAG):
                        if prev_nonempty_line(lines, i).strip().startswith(SYNTAX_FLAG):
                            j = i
                            while j < len(lines) and not lines[j].strip().startswith(ORC_NOSPACE_FLAG) and not lines[j].strip().startswith(ORC_SPACE_FLAG):
                                j += 1
                            index = j + 1
                            current_line = lines[index]
                            if regex_c.search(current_line):
                                opcode_body = current_line.split(" ")
                                if len(opcode_body) > 0:
                                    opcodes_dict[opnames]["prefix"] = escape_dollar(prefix=opcode_body[0])
                            else:
                                opcodes_dict[opnames]["prefix"] =  escape_dollar(prefix=current_line)



    if len(same_to_check) > 0:
        for item in same_to_check:
            same = item[0]
            ref = item[1]
            if ref in opcodes_dict:
                opcodes_dict[same]["prefix"] = re.sub(ref, same, opcodes_dict[ref]["prefix"])
                opcodes_dict[same]["description"] = re.sub(ref, same, opcodes_dict[ref]["description"])
            else:
                print(f"[WARNING] Reference opcode {ref} for {same} not exists")

    # print(opcodes_dict)

    with open("stemplate.json", "r") as s:
        snip_to = json.load(s)
        for snippet, value in snip_to.items():
            if snippet in opcodes_dict:
                opcodes_dict[snippet]["body"] = value["body"]
            else:
                opcodes_dict[snippet] = value

    with open("json_data/csound.json", "w", encoding="utf-8") as f:
        json.dump(opcodes_dict, f, ensure_ascii=True, indent=4)
    with open("json_data/manual_indexes.json", "w", encoding="utf-8") as m:
        json.dump(opcode_indexes, m, ensure_ascii=True, indent=4)



if __name__ == "__main__":
    main()
    generate_flags()
