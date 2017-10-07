#!/usr/bin/env python3
# references:
#  https://fcitx-im.org/wiki/How_to_make_your_own_table-based_input_method
#  http://wiki.debian.org.hk/w/Create_input_method_with_scim-make-table
#  /usr/share/fcitx/configdesc/table.desc

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

    # Unique Name for Table
    print("UniqueName=%s" % im_name, file=f)

    # Code Table Name
    # name of this table, it's an I18N String.
    name = definitions['NAME']
    print("Name=%s" % name, file=f)

    locales = [k[5:] for k in definitions.keys() if k.startswith('NAME.')]
    for locale in locales:
        localename = definitions["NAME.%s" % locale]
        print("Name[%s]=%s" % (locale, localename), file=f)

    # Icon Name
    print("IconName=%s" % im_name, file=f)

    # Code Table File
    print("File=%s.mb" % im_name, file=f)

    # Adjust Order
    # adjust order by user input or not.
    # AdjustNo, AdjustFast, AdjustFreq
    adjust_order = {'TRUE': 'AdjustFreq', 'FALSE': 'AdjustNo'}[definitions['DYNAMIC_ADJUST']]
    print("AdjustOrder=%s" % adjust_order, file=f)

    # Level of simple code
    # print("SimpleCodeOrderLevel=", file=f)

    # Order of Code Table
    # what is this?
    # print("Priority=%d" % 30, file=f)

    # Use Pinyin
    # uses temporary pinyin mode or not
    # print("UsePY=%s" % False, file=f)

    # Pinyin Key
    # print("PYKey=", file=f)

    # Auto Send Candidate Word
    use_auto_send = definitions['AUTO_COMMIT'] == 'TRUE'
    print("UseAutoSend=%s" % use_auto_send, file=f)

    # Minimum length trigger auto send candidate word when only one candidate
    # When the input is longer than maximum code length, and if there is only one character,
    # it will automatically commit the candidate or not.
    # print("AutoSend=%d" % -1, file=f)

    # Minimum length trigger auto send candidate when there will be no candidate
    # Automatically commit the candidate string if there is no match.
    # For example, abcd has no matched item, but abc have matched item,
    # then the item matched abc will be committed, and d will reside in the input buffer.
    # print("NoneMatchAutoSend=%d" % 0, file=f)

    # Send Raw Preedit
    # print("SendRawPreedit=%s" % False, file=f)

    # End Key
    # print("EndKey=", file=f)

    # Use Matching Key
    # use wildcard or not.
    use_matching_key = 'SINGLE_WILDCARD_CHAR' in definitions or 'MULTI_WILDCARD_CHAR' in definitions
    print("UseMatchingKey=%s" % use_matching_key, file=f)

    # Matching Key
    if 'MULTI_WILDCARD_CHAR' in definitions:
        matching_key = definitions['MULTI_WILDCARD_CHAR']
    elif 'SINGLE_WILDCARD_CHAR' in definitions:
        matching_key = definitions['SINGLE_WILDCARD_CHAR']
    else:
        matching_key = ''
    print("MatchingKey=%s" % matching_key, file=f)

    # Exact Match
    # Only shows the exact match item in the table.
    print("ExactMatch=%s" % False, file=f)

    # Auto Phrase
    # automatically construct new phrase.
    auto_phrase = definitions['AUTO_FILL'] == 'TRUE'
    print("AutoPhrase=%s" % auto_phrase, file=f)

    # Keep current buffer when there is no match item and input length is equal code length
    # print("NoMatchDontCommit=", file=f)

    # Auto Phrase Length
    # length of automatically constructed phrase.
    # print("AutoPhraseLength=%d" % 4, file=f)

    # Auto Phrase Phrase
    # phrase will be used in automatically constructing phrase or not.
    # print("AutoPhrasePhrase=%s" % True, file=f)

    # Save Auto Phrase
    # count of the phrase need to be selected before saving an automatically constructed phrase. 0 means it will not be saved.
    # print("SaveAutoPhrase=%d" % 0, file=f)

    # Prompt Table Code
    # Show the hint for item in this table.
    prompt_table_code = definitions['SHOW_KEY_PROMPT'] == 'TRUE'
    print("PromptTableCode=%s" % prompt_table_code, file=f)

    # Candidate Table Layout
    # Not Set, Vertical, Horizontal
    # print("CandidateLayout=", file=f)

    # Symbol
    # symbol mode key
    # print("Symbol=", file=f)

    # Symbol File
    # symbol file name
    # print("SymbolFile=", file=f)

    # Choose
    #if 'SELECT_KEYS' in definitions:
    #    choose = ''.join(definitions['SELECT_KEYS'].split(','))
    #    print("Choose=%s" % choose, file=f)
    print("Choose=vwxyz", file=f)

    # Choose key modifier
    # None, Alt, Ctrl, Shift
    # print("ChooseModifier=", file=f)

    # Language Code for this table
    print("LangCode=zh_TW", file=f)

    # Enable
    # enable this table or not.
    print("Enabled=%s" % True, file=f)

    # Use Custom Prompt String defined in table
    # print("UseCustomPrompt=", file=f)

    # Keyboard Layout to be used
    # print("KeyboardLayout=", file=f)

    # Use Alternative Candidate Word Number
    # print("UseAlternativeCandidateWordNumber=", file=f)

    # Candidate Word Number
    # print("CandidateWordNumber=", file=f)

    # Use Alternative Key for paging
    # print("UseAlternativePageKey=", file=f)

    # Alternative Prev Page Key
    # print("AlternativePrevPage=", file=f)

    # Alternative Next Page Key
    # print("AlternativeNextPage=", file=f)

    # First Candidate Display as Preedit
    # print("FirstCandidateAsPreedit=", file=f)

    # Commit and pass when invalid key of this table pressed
    # print("CommitAndPassByInvalidKey=", file=f)

    # Commit key for select first candidate
    # print("CommitKey=", file=f)

    # Commit string when there is no match
    # print("CommitKeyCommitWhenNoMatch=", file=f)

    # Ignore Punctuation
    # print("IgnorePunc=", file=f)

    # Ignore some Punctuation, if it is empty, then ignore all punctuation
    # print("IgnorePuncList=", file=f)


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
