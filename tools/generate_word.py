#!/usr/bin/env python3

import os
import re
import subprocess


def get_word_property_list(property_name):
    value = []
    with open('WordBreakProperty.txt', 'r') as file:
        line = file.readline()
        while line:
            line = line.strip()
            if not line.startswith('#'):
                m = re.search("([0-9A-F]{1,6})\.\.([0-9A-F]{1,6})\s*\;\s*(\w{2,})", line)
                if m:
                    if m.group(3) == property_name:
                        length = int(m.group(2), 16) - int(m.group(1), 16) + 1
                        s = int(m.group(1), 16)
                        for x in range(length):
                            value.append(s + x);
                else:
                    m = re.search("([0-9A-F]{1,6})\s*\;\s*(\w{2,})", line)
                    if m:
                        if int(m.group(1), 16) >= 0x20000:
                            line = file.readline()
                            continue
                        if m.group(2) == property_name:
                            s = int(m.group(1), 16)
                            value.append(s);
            line = file.readline()

    value.sort()
    return value


def get_emoji_list(property_name):
    value = []
    with open('emoji/emoji-data.txt', 'r') as file:
        line = file.readline()
        while line:
            line = line.strip()
            if not line.startswith('#'):
                m = re.search("([0-9A-F]{1,6})\.\.([0-9A-F]{1,6})\s*\;\s*(\w{2,})",
                              line)
                if m:
                    if m.group(3) == property_name:
                        length = int(m.group(2), 16) - int(m.group(1), 16) + 1
                        s = int(m.group(1), 16)
                        for x in range(length):
                            value.append(s + x);
                else:
                    m = re.search("([0-9A-F]{1,6})\s*\;\s*(\w{2,})", line)
                    if m:
                        if m.group(2) == property_name:
                            s = int(m.group(1), 16)
                            value.append(s);
            line = file.readline()
    return value


def get_linebreak(property_name):
    value = []
    with open('LineBreak.txt', 'r') as file:
        line = file.readline()
        while line:
            line = line.strip()
            if not line.startswith('#'):
                m = re.search("([0-9A-F]{1,6})\.\.([0-9A-F]{1,6})\;([0-9A-Z]{2,})",
                              line)
                if m:
                    if m.group(3) == property_name:
                        length = int(m.group(2), 16) - int(m.group(1), 16) + 1
                        s = int(m.group(1), 16)
                        for x in range(length):
                            value.append(s + x);
                else:
                    m = re.search("([0-9A-F]{1,6})\;([0-9A-Z]{2,})", line)
                    if m:
                        if m.group(2) == property_name:
                            s = int(m.group(1), 16)
                            value.append(s);
            line = file.readline()
    return value



print("{ \"tables\": [")

# CR
v = get_word_property_list("CR")
print("{ \"name\": \"CR\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# LF
v = get_word_property_list("LF")
print("{ \"name\": \"LF\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Newline
v = get_word_property_list("Newline")
print("{ \"name\": \"Newline\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Extend
v = get_word_property_list("Extend")
print("{ \"name\": \"Extend\", \"value\": { \"codepoint\":")
print(v)
print("}},")
extend = v

# ZWJ
v = get_word_property_list("ZWJ")
print("{ \"name\": \"ZWJ\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Regional_Indicator
v = get_word_property_list("Regional_Indicator")
print("{ \"name\": \"Regional_Indicator\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Format
v = get_word_property_list("Format")
print("{ \"name\": \"Format\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Katakana
v = get_word_property_list("Katakana")
print("{ \"name\": \"Katakana\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Hebrew_Letter
v = get_word_property_list("Hebrew_Letter")
print("{ \"name\": \"Hebrew_Letter\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# ALetter
v = get_word_property_list("ALetter")
print("{ \"name\": \"ALetter\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Single_Quote
v = get_word_property_list("Single_Quote")
print("{ \"name\": \"Single_Quote\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Double_Quote
v = get_word_property_list("Double_Quote")
print("{ \"name\": \"Double_Quote\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# MidNumLet
v = get_word_property_list("MidNumLet")
print("{ \"name\": \"MidNumLet\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# MidLetter
v = get_word_property_list("MidLetter")
print("{ \"name\": \"MidLetter\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# MidNum
v = get_word_property_list("MidNum")
print("{ \"name\": \"MidNum\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Numeric
v = get_word_property_list("Numeric")
print("{ \"name\": \"Numeric\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# ExtendNumLet
v = get_word_property_list("ExtendNumLet")
print("{ \"name\": \"ExtendNumLet\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# WSegSpace
v = get_word_property_list("WSegSpace")
print("{ \"name\": \"WSegSpace\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Extended_Pictographic
v = get_emoji_list("Extended_Pictographic")
v.sort()
print("{ \"name\": \"Extended_Pictographic\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# SA
v = get_linebreak("SA")
v.sort()
print("{ \"name\": \"SA\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Alias
# (WB4)
print("{ \"name\": \"ALetter\", \"value\": { \"left\": \"ALetter\", \"right\": \"Extend\" }},")
print("{ \"name\": \"ALetter\", \"value\": { \"left\": \"ALetter\", \"right\": \"Format\" }},")
print("{ \"name\": \"ALetter\", \"value\": { \"left\": \"ALetter_ZWJ\", \"right\": \"Extend\" }},")
print("{ \"name\": \"ALetter\", \"value\": { \"left\": \"ALetter_ZWJ\", \"right\": \"Format\" }},")
print("{ \"name\": \"ALetter_ZWJ\", \"value\": { \"left\": \"ALetter\", \"right\": \"ZWJ\" }},")
print("{ \"name\": \"ALetter_ZWJ\", \"value\": { \"left\": \"ALetter_ZWJ\", \"right\": \"ZWJ\" }},")
print("{ \"name\": \"Numeric\", \"value\": { \"left\": \"Numeric\", \"right\": \"Extend\" }},")
print("{ \"name\": \"Numeric\", \"value\": { \"left\": \"Numeric\", \"right\": \"Format\" }},")
print("{ \"name\": \"Numeric\", \"value\": { \"left\": \"Numeric\", \"right\": \"ZWJ\" }},")
print("{ \"name\": \"ExtendNumLet\", \"value\": { \"left\": \"ExtendNumLet\", \"right\": \"Extend\" }},")
print("{ \"name\": \"ExtendNumLet\", \"value\": { \"left\": \"ExtendNumLet\", \"right\": \"Format\" }},")
print("{ \"name\": \"ExtendNumLet\", \"value\": { \"left\": \"ExtendNumLet\", \"right\": \"ZWJ\" }},")
print("{ \"name\": \"Single_Quote\", \"value\": { \"left\": \"Single_Quote\", \"right\": \"Extend\" }},")
print("{ \"name\": \"Single_Quote\", \"value\": { \"left\": \"Single_Quote\", \"right\": \"Format\" }},")
print("{ \"name\": \"Single_Quote\", \"value\": { \"left\": \"Single_Quote\", \"right\": \"ZWJ\" }},")
print("{ \"name\": \"Double_Quote\", \"value\": { \"left\": \"Double_Quote\", \"right\": \"Extend\" }},")
print("{ \"name\": \"Double_Quote\", \"value\": { \"left\": \"Double_Quote\", \"right\": \"Format\" }},")
print("{ \"name\": \"Double_Quote\", \"value\": { \"left\": \"Double_Quote\", \"right\": \"ZWJ\" }},")
print("{ \"name\": \"MidLetter\", \"value\": { \"left\": \"MidLetter\", \"right\": \"Extend\" }},")
print("{ \"name\": \"MidLetter\", \"value\": { \"left\": \"MidLetter\", \"right\": \"Format\" }},")
print("{ \"name\": \"MidLetter\", \"value\": { \"left\": \"MidLetter\", \"right\": \"ZWJ\" }},")
print("{ \"name\": \"MidNum\", \"value\": { \"left\": \"MidNum\", \"right\": \"Extend\" }},")
print("{ \"name\": \"MidNum\", \"value\": { \"left\": \"MidNum\", \"right\": \"Format\" }},")
print("{ \"name\": \"MidNum\", \"value\": { \"left\": \"MidNum\", \"right\": \"ZWJ\" }},")
print("{ \"name\": \"MidNumLet\", \"value\": { \"left\": \"MidNumLet\", \"right\": \"Extend\" }},")
print("{ \"name\": \"MidNumLet\", \"value\": { \"left\": \"MidNumLet\", \"right\": \"Format\" }},")
print("{ \"name\": \"MidNumLet\", \"value\": { \"left\": \"MidNumLet\", \"right\": \"ZWJ\" }},")
print("{ \"name\": \"WSegSpace_Extend\", \"value\": { \"left\": \"WSegSpace\", \"right\": \"Extend\" }},")
print("{ \"name\": \"WSegSpace_Extend\", \"value\": { \"left\": \"WSegSpace_Extend\", \"right\": \"Extend\" }},")
print("{ \"name\": \"WSegSpace_Format\", \"value\": { \"left\": \"WSegSpace\", \"right\": \"Format\" }},")
print("{ \"name\": \"WSegSpace_Format\", \"value\": { \"left\": \"WSegSpace_Format\", \"right\": \"Format\" }},")
print("{ \"name\": \"WSegSpace_Extend\", \"value\": { \"left\": \"WSegSpace_Format\", \"right\": \"Extend\" }},")
print("{ \"name\": \"WSegSpace_Format\", \"value\": { \"left\": \"WSegSpace_Extend\", \"right\": \"Format\" }},")
print("{ \"name\": \"WSegSpace_ZWJ\", \"value\": { \"left\": \"WSegSpace\", \"right\": \"ZWJ\" }},")
print("{ \"name\": \"WSegSpace_ZWJ\", \"value\": { \"left\": \"WSegSpace_ZWJ\", \"right\": \"ZWJ\" }},")
print("{ \"name\": \"WSegSpace_ZWJ\", \"value\": { \"left\": \"WSegSpace_Extend\", \"right\": \"ZWJ\" }},")
print("{ \"name\": \"WSegSpace_ZWJ\", \"value\": { \"left\": \"WSegSpace_Format\", \"right\": \"ZWJ\" }},")
print("{ \"name\": \"WSegSpace_Extend\", \"value\": { \"left\": \"WSegSpace_ZWJ\", \"right\": \"Extend\" }},")
print("{ \"name\": \"WSegSpace_Format\", \"value\": { \"left\": \"WSegSpace_ZWJ\", \"right\": \"Format\" }},")
print("{ \"name\": \"Unknown\", \"value\": { \"left\": \"Unknown\", \"right\": \"Extend\" }},")
print("{ \"name\": \"Unknown\", \"value\": { \"left\": \"Unknown\", \"right\": \"Format\" }},")
print("{ \"name\": \"Unknown_ZWJ\", \"value\": { \"left\": \"Unknown\", \"right\": \"ZWJ\" }},")
print("{ \"name\": \"Katakana\", \"value\": { \"left\": \"Katakana\", \"right\": \"Extend\" }},")
print("{ \"name\": \"Katakana\", \"value\": { \"left\": \"Katakana\", \"right\": \"Format\" }},")
print("{ \"name\": \"Katakana\", \"value\": { \"left\": \"Katakana\", \"right\": \"ZWJ\" }},")
print("{ \"name\": \"Regional_Indicator\", \"value\": { \"left\": \"Regional_Indicator\", \"right\": \"Extend\" }},")
print("{ \"name\": \"Regional_Indicator\", \"value\": { \"left\": \"Regional_Indicator\", \"right\": \"Format\" }},")
print("{ \"name\": \"Regional_Indicator\", \"value\": { \"left\": \"Regional_Indicator\", \"right\": \"ZWJ\" }},")
print("{ \"name\": \"Hebrew_Letter\", \"value\": { \"left\": \"Hebrew_Letter\", \"right\": \"Extend\" }},")
print("{ \"name\": \"Hebrew_Letter\", \"value\": { \"left\": \"Hebrew_Letter\", \"right\": \"Format\" }},")
print("{ \"name\": \"Hebrew_Letter\", \"value\": { \"left\": \"Hebrew_Letter\", \"right\": \"ZWJ\" }},")
print("{ \"name\": \"Extended_Pictographic\", \"value\": { \"left\": \"Extended_Pictographic\", \"right\": \"Extend\" }},")
print("{ \"name\": \"Extended_Pictographic\", \"value\": { \"left\": \"Extended_Pictographic\", \"right\": \"Format\" }},")
print("{ \"name\": \"Extended_Pictographic_ZWJ\", \"value\": { \"left\": \"Extended_Pictographic\", \"right\": \"ZWJ\" }},")
print("{ \"name\": \"Extended_Pictographic\", \"value\": { \"left\": \"Extended_Pictographic_ZWJ\", \"right\": \"Extend\" }},")
print("{ \"name\": \"Extended_Pictographic\", \"value\": { \"left\": \"Extended_Pictographic_ZWJ\", \"right\": \"Format\" }},")
print("{ \"name\": \"Format\", \"value\": { \"left\": \"Format\", \"right\": \"Extend\" }},")
print("{ \"name\": \"Format\", \"value\": { \"left\": \"Format\", \"right\": \"Format\" }},")
print("{ \"name\": \"Format\", \"value\": { \"left\": \"Format\", \"right\": \"ZWJ\" }},")
print("{ \"name\": \"Extend\", \"value\": { \"left\": \"Extend\", \"right\": \"Extend\" }},")
print("{ \"name\": \"Extend\", \"value\": { \"left\": \"Extend\", \"right\": \"Format\" }},")
print("{ \"name\": \"Extend\", \"value\": { \"left\": \"Extend\", \"right\": \"ZWJ\" }},")
print("{ \"name\": \"ZWJ_Extend\", \"value\": { \"left\": \"ZWJ\", \"right\": \"Extend\" }},")
print("{ \"name\": \"ZWJ_Extend\", \"value\": { \"left\": \"ZWJ_Extend\", \"right\": \"Extend\" }},")
print("{ \"name\": \"ZWJ_Format\", \"value\": { \"left\": \"ZWJ\", \"right\": \"Format\" }},")
print("{ \"name\": \"ZWJ_Format\", \"value\": { \"left\": \"ZWJ_Format\", \"right\": \"Format\" }},")
print("{ \"name\": \"ZWJ_Extend\", \"value\": { \"left\": \"ZWJ_Format\", \"right\": \"Extend\" }},")
print("{ \"name\": \"ZWJ_Format\", \"value\": { \"left\": \"ZWJ_Extend\", \"right\": \"Format\" }},")
print("{ \"name\": \"ZWJ\", \"value\": { \"left\": \"ZWJ\", \"right\": \"ZWJ\" }},")
print("{ \"name\": \"ZWJ\", \"value\": { \"left\": \"ZWJ_Extend\", \"right\": \"ZWJ\" }},")
print("{ \"name\": \"ZWJ\", \"value\": { \"left\": \"ZWJ_Format\", \"right\": \"ZWJ\" }},")
print("{ \"name\": \"ALetter_MidLetter\", \"value\": { \"left\": \"ALetter_MidLetter\", \"right\": \"Extend\" }},")
print("{ \"name\": \"ALetter_MidLetter\", \"value\": { \"left\": \"ALetter_MidLetter\", \"right\": \"Format\" }},")
print("{ \"name\": \"ALetter_Single_Quote\", \"value\": { \"left\": \"ALetter_Single_Quote\", \"right\": \"Extend\" }},")
print("{ \"name\": \"ALetter_Single_Quote\", \"value\": { \"left\": \"ALetter_Single_Quote\", \"right\": \"Format\" }},")
print("{ \"name\": \"Numeric_Single_Quote\", \"value\": { \"left\": \"Numeric_Single_Quote\", \"right\": \"Extend\" }},")
print("{ \"name\": \"Numeric_Single_Quote\", \"value\": { \"left\": \"Numeric_Single_Quote\", \"right\": \"Format\" }},")
print("{ \"name\": \"Numeric_MidNum\", \"value\": { \"left\": \"Numeric_MidNum\", \"right\": \"Extend\" }},")
print("{ \"name\": \"Numeric_MidNum\", \"value\": { \"left\": \"Numeric_MidNum\", \"right\": \"Format\" }},")
print("{ \"name\": \"Numeric_MidNumLet\", \"value\": { \"left\": \"Numeric_MidNumLet\", \"right\": \"Extend\" }},")
print("{ \"name\": \"Numeric_MidNumLet\", \"value\": { \"left\": \"Numeric_MidNumLet\", \"right\": \"Format\" }},")
print("{ \"name\": \"Unknown\", \"value\": { \"left\": \"Unknown\", \"right\": \"Extend\" }},")
print("{ \"name\": \"Unknown\", \"value\": { \"left\": \"Unknown\", \"right\": \"Format\" }},")
# (WB7)
print("{ \"name\": \"ALetter_MidLetter\", \"value\": { \"left\": \"ALetter\", \"right\": \"MidLetter\" }},")
print("{ \"name\": \"ALetter_MidLetter\", \"value\": { \"left\": \"ALetter_ZWJ\", \"right\": \"MidLetter\" }},")
print("{ \"name\": \"ALetter_MidNumLet\", \"value\": { \"left\": \"ALetter\", \"right\": \"MidNumLet\" }},")
print("{ \"name\": \"ALetter_MidNumLet\", \"value\": { \"left\": \"ALetter_ZWJ\", \"right\": \"MidNumLet\" }},")
print("{ \"name\": \"ALetter_Single_Quote\", \"value\": { \"left\": \"ALetter\", \"right\": \"Single_Quote\" }},")
print("{ \"name\": \"ALetter_Single_Quote\", \"value\": { \"left\": \"ALetter_ZWJ\", \"right\": \"Single_Quote\" }},")
print("{ \"name\": \"Hebrew_Letter_MidLetter\", \"value\": { \"left\": \"Hebrew_Letter\", \"right\": \"MidLetter\" }},")
print("{ \"name\": \"Hebrew_Letter_MidNumLet\", \"value\": { \"left\": \"Hebrew_Letter\", \"right\": \"MidNumLet\" }},")
print("{ \"name\": \"Hebrew_Letter_Single_Quote\", \"value\": { \"left\": \"Hebrew_Letter\", \"right\": \"Single_Quote\" }},")
print("{ \"name\": \"Hebrew_Letter_Double_Quote\", \"value\": { \"left\": \"Hebrew_Letter\", \"right\": \"Double_Quote\" }},")
# (WB11)
print("{ \"name\": \"Numeric_MidNum\", \"value\": { \"left\": \"Numeric\", \"right\": \"MidNum\" }},")
print("{ \"name\": \"Numeric_MidNumLet\", \"value\": { \"left\": \"Numeric\", \"right\": \"MidNumLet\" }},")
print("{ \"name\": \"Numeric_Single_Quote\", \"value\": { \"left\": \"Numeric\", \"right\": \"Single_Quote\" }},")
# (WB15)
print("{ \"name\": \"RI_RI\", \"value\": { \"left\": \"Regional_Indicator\", \"right\": \"Regional_Indicator\" }},")
print("{ \"name\": \"RI_RI_ZWJ\", \"value\": { \"left\": \"RI_RI\", \"right\": \"ZWJ\" }}")

# Rules

print("], \"rules\": [")
# WB1
print("{ \"left\": [\"sot\"], \"right\": [\"Any\"], \"break_state\": true },")
# WB2
print("{ \"left\": [\"ALetter\", \"Katakana\", \"Hebrew_Letter\", \"Numeric\", \"MidNumLet\", \"ExtendNumLet\", \"MidNumLet\", \"MidLetter\", \"ZWJ\", \"Extend\", \"Format\", \"Regional_Indicator\", \"Extended_Pictographic\", \"Single_Quote\", \"Double_Quote\"], \"right\": [\"eot\"], \"break_state\": true },")
print("{ \"left\": [\"ALetter_ZWJ\", \"Unknown_ZWJ\", \"Extended_Pictographic_ZWJ\"], \"right\": [\"eot\"], \"break_state\": true },")
print("{ \"left\": [ \"Hebrew_Letter_Single_Quote\"], \"right\": [\"eot\"], \"break_state\": true },") # WB7
# WB3
print("{ \"left\": [\"CR\"], \"right\": [\"LF\"], \"break_state\": false },")
# WB3a
# WB3b
# WB3c
print("{ \"left\": [\"ZWJ\", \"Extended_Pictographic_ZWJ\", \"ALetter_ZWJ\", \"Unknown_ZWJ\"], \"right\": [\"Extended_Pictographic\"], \"break_state\": false },")
# WB3d
print("{ \"left\": [\"WSegSpace\"], \"right\": [\"WSegSpace\"], \"break_state\": false },")
# WB4
# WB5
print("{ \"left\": [\"ALetter\", \"ALetter_ZWJ\", \"Hebrew_Letter\"], \"right\": [\"ALetter\", \"Hebrew_Letter\"], \"break_state\": false },")
# WB7
print("{ \"left\": [ \"ALetter_MidLetter\", \"ALetter_MidNumLet\", \"ALetter_Single_Quote\", \"Hebrew_Letter_MidLetter\", \"Hebrew_Letter_MidNumLet\", \"Hebrew_Letter_Single_Quote\"], \"right\": [\"ALetter\", \"Hebrew_Letter\"], \"break_state\": false },")
# WB7a
print("{ \"left\": [ \"Hebrew_Letter\"], \"right\": [\"Single_Quote\"], \"break_state\": false },")
# WB7b/WB7c
print("{ \"left\": [ \"Hebrew_Letter_Double_Quote\"], \"right\": [\"Hebrew_Letter\"], \"break_state\": false },")
# WB8
print("{ \"left\": [\"Numeric\"], \"right\": [\"Numeric\"], \"break_state\": false },")
# WB9
print("{ \"left\": [\"ALetter\", \"ALetter_ZWJ\", \"Hebrew_Letter\"], \"right\": [\"Numeric\"], \"break_state\": false },")
# WB10
print("{ \"left\": [\"Numeric\"], \"right\": [\"ALetter\", \"Hebrew_Letter\"], \"break_state\": false },")
# WB11/WB12
print("{ \"left\": [\"Numeric_MidNum\", \"Numeric_MidNumLet\", \"Numeric_Single_Quote\"], \"right\": [\"Numeric\"], \"break_state\": false },")
print("{ \"left\": [\"Numeric_Single_Quote\"], \"right\": [\"Any\"] },")
# WB13
print("{ \"left\": [\"Katakana\"], \"right\": [\"Katakana\"], \"break_state\": false },")
# WB13a
print("{ \"left\": [\"ALetter\", \"ALetter_ZWJ\", \"Hebrew_Letter\", \"Numeric\", \"Katakana\", \"ExtendNumLet\"], \"right\": [\"ExtendNumLet\"], \"break_state\": false },")
# WB13b
print("{ \"left\": [\"ExtendNumLet\"], \"right\": [\"ALetter\", \"Hebrew_Letter\", \"Numeric\", \"Katakana\"], \"break_state\": false },")
# WB999
print("{ \"left\": [\"sot\"], \"right\": [\"Any\"], \"break_state\": true },")
# WB2
print("{ \"left\": [\"ALetter_ZWJ\"], \"right\": [\"eot\"], \"break_state\": true },")
print("{ \"left\": [\"ALetter_ZWJ\"], \"right\": [\"WSegSpace\"], \"break_state\": true },")
print("{ \"left\": [\"Any\"], \"right\": [\"Any\"], \"break_state\": true }")
print("]}")
