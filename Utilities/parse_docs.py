def parse_file(filepath):
    """
    Parses RR docs into a list of dictionaries, each dictionary has the following format:
    Events: {'Identifier': '', 'Event': '.', 'Exports': '', 'Class': ''}
    Conditions: {'Identifier': '', 'Trigger requirements': '', 'Parameters': '', 'Sample use': '', 'Description': '', 'Battle or Strat': '', 'Class': '', 'Implemented': ''}
    Commands: {'Identifier': 'Words', 'Parameters': '', 'Description': "WordsWordsWordsWords", 'Sample use': 'v v d', 'Class': 'Words', 'Implemented': 'Yes'}
    """
    with open(filepath, "r") as file:
        lines = file.read()

    data = []
    blocks = lines.split("---------------------------------------------------")

    blocks = [block.strip() for block in blocks if block]

    for block in blocks:
        lines = block.split("\n")

        block_dict = {}
        current_key = ""
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)

                key = key.strip()
                value = value.strip()

                block_dict[key] = value
                current_key = key
            else:
                # print(line, current_key)
                block_dict[current_key] += "\n" + line

            # If the current key is "Identifier", ensure the value is only one word long
            if current_key == "Identifier":
                words = block_dict[current_key].split()
                block_dict[current_key] = words[0]

        data.append(block_dict)

    return data


def get_hover_entries(collection):
    out = dict()
    for i in collection:
        li = list()
        for j in i.keys():
            li.append(j + ": " + i[j])
        out[i["Identifier"]] = (
            "\n".join(li)
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("<=", "&le;")
            .replace(">=", "&ge;")
            .replace("\n", "<br>")
        )
    return out


def get_autocomplete_entires(collection, kind):
    # {
    #     "trigger": "character_party",
    #     "contents": "character_party",
    #     "details": "Input Scopes: character ⇨ Output Scopes: party",
    #     "kind": ["namespace", "S", "Scope"]
    # },
    entires = list()
    for i in collection:
        try:
            desc = i["Description"]
        except KeyError:
            desc = i["Event"]
        desc = (
            desc.replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("<=", "&le;")
            .replace(">=", "&ge;")
            .replace("\n", "<br>")
        )
        entires.append(
            f'{{\n\t"trigger": "{i["Identifier"]}",\n\t"contents": "{i["Identifier"]}",\n\t"details": "{desc}",\n\t"kind": ["{kind[0]}", "{kind[1]}", "{kind[2]}"]\n}},'
        )
    return entires


if __name__ == "__main__":
    commands = parse_file("docudemon_commands.txt")
    events = parse_file("docudemon_events.txt")
    conditions = parse_file("docudemon_conditions.txt")
    console_commands = parse_file("docudemon_romeshell.txt")

    # command_dict = get_hover_entries(commands)
    # event_dict = get_hover_entries(events)
    # condition_dict = get_hover_entries(conditions)
    # console_dict = get_hover_entries(console_commands)

    header = f'{{\n"scope": "text.rome",\n\t"completions":\n\t['
    footer = f"\t]\n}}"
    command_list = get_autocomplete_entires(commands, ["keyword", "C", "Command"])
    condition_list = get_autocomplete_entires(conditions, ["navigation", "C", "Condition"])
    event_list = get_autocomplete_entires(events, ["namespace", "E", "Event"])
    console_list = get_autocomplete_entires(events, ["snippet", "C", "Console Command"])

    for i in condition_list:
        print(i)
