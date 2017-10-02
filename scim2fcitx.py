#!/usr/bin/env python3
# references:
#  https://fcitx-im.org/wiki/How_to_make_your_own_table-based_input_method
#  http://wiki.debian.org.hk/w/Create_input_method_with_scim-make-table

import argparse
import sys


def gen_fcitx_conf_file(im_name, definitions, table, output2stdout):
    if output2stdout:
        f = sys.stdout
    else:
        fname = im_name + '.conf'
        print("write to %s" % fname)
        f = open(fname, 'w')

    print("[CodeTable]", file=f)
    print("UniqueName=%s" % im_name, file=f)

    # name of this table, it's an I18N String.
    name = definitions['NAME']
    print("Name=%s" % name, file=f)

    locales = [k[5:] for k in definitions.keys() if k.startswith('NAME.')]
    for locale in locales:
        localename = definitions["NAME.%s" % locale]
        print("Name[%s]=%s" % (locale, localename), file=f)

    # icon name
    print("IconName=%s" % im_name, file=f)

    # table data file name
    print("File=%s.mb" % im_name, file=f)

    # adjust order by user input or not.
    adjust_order = {'TRUE': 'AdjustFreq', 'FALSE': 'AdjustNo'}[definitions['DYNAMIC_ADJUST']]
    print("AdjustOrder=%s" % adjust_order, file=f)

    # what is this?
    print("Priority=%d" % 0, file=f)

    # uses temporary pinyin mode or not
    print("UsePY=%s" % False, file=f)

    # When the input is longer than maximum code length, and if there is only one character,
    # it will automatically commit the candidate or not.
    print("AutoSend=%d" % -1, file=f)

    # Automatically commit the candidate string if there is no match.
    # For example, abcd has no matched item, but abc have matched item,
    # then the item matched abc will be committed, and d will reside in the input buffer.
    print("NoneMatchAutoSend=%d" % 0, file=f)

    # use wildcard or not.
    use_matching_key = 'SINGLE_WILDCARD_CHAR' in definitions or 'MULTI_WILDCARD_CHAR' in definitions
    print("UseMatchingKey=%s" % use_matching_key, file=f)

    # automatically construct new phrase.
    print("AutoPhrase=%s" % False, file=f)

    # length of automatically constructed phrase.
    print("AutoPhraseLength=%d" % 4, file=f)

    # phrase will be used in automatically constructing phrase or not.
    print("AutoPhrasePhrase=%s" % False, file=f)

    # count of the phrase need to be selected before saving an automatically constructed phrase. 0 means it will not be saved.
    print("SaveAutoPhrase=%d" % 3, file=f)

    # Only shows the exact match item in the table.
    print("ExactMatch=%s" % False, file=f)

    # Show the hint for item in this table.
    prompt_table_code = definitions['SHOW_KEY_PROMPT'] == 'TRUE'
    print("PromptTableCode=%s" % prompt_table_code, file=f)

    # symbol mode key
    #print("Symbol=", file=f)

    # symbol file name
    #print("SymbolFile=", file=f)

    # enable this table or not.
    print("Enabled=%s" % True, file=f)

    # what is this?
    print("LangCode=zh_TW", file=f)


def gen_fcitx_data_file(im_name, definitions, table, output2stdout):
    if output2stdout:
        f = sys.stdout
    else:
        fname = im_name + '.txt'
        print("write to %s" % fname)
        f = open(fname, 'w')

    print(";fcitx Version 0x03 Table file", file=f)

    # key will be used in this table, need to be ascii character.
    key_code = definitions['VALID_INPUT_CHARS']
    print("KeyCode=%s" % key_code, file=f)

    # Max Length for item in this table
    length = int(definitions['MAX_KEY_LENGTH'])
    print("Length=%d" % length, file=f)

    # the string start with this character means it's a pinyin.
    print("Pinyin=%s" % '@', file=f)

    # maximum pinyin length in this table.
    print("PinyinLength=%d" % 5, file=f)

    # what is this?
    print("Prompt=%s" % '&', file=f)

    # what is this?
    print("ConstructPhrase=%s" % '^', file=f)

    print("[Data]", file=f)

    for row in table:
        keys, phrase, priority = row
        print("%s %s" % (keys, phrase), file=f)


def process_scim_file(scimfile):
    definitions = {}
    table = []

    state = 'TOP'
    with open(scimfile) as f:
        for line in f:
            line = line.strip()

            if state == 'TOP':
                if line == 'BEGIN_DEFINITION':
                    state = 'DEFINITION'
                elif line == 'BEGIN_TABLE':
                    state = 'TABLE'

            elif state == 'DEFINITION':
                if line == 'END_DEFINITION':
                    state = 'TOP'
                else:
                    key, val = line.split('=')
                    key = key.strip()
                    val = val.strip()
                    definitions[key] = val

            elif state == 'TABLE':
                if line == 'END_TABLE':
                    state = 'TOP'
                else:
                    row = line.split('\t')
                    table.append(row)

    return definitions, table


def main(args):
    definitions, table = process_scim_file(args.infile)
    print(definitions)

    gen_fcitx_conf_file(args.name, definitions, table, args.stdout)
    gen_fcitx_data_file(args.name, definitions, table, args.stdout)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert scim table file to fcitx table files')
    parser.add_argument('-n', '--name', required=True, help='input method short name')
    parser.add_argument('-s', '--stdout', action='store_true', help='output to stdout')
    parser.add_argument('infile', metavar='INFILE', help='input scim table file')

    args = parser.parse_args()
    main(args)
