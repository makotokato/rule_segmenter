#!/usr/bin/env python3

import os
import re
import subprocess

def get_grapheme_property_list(property_name):
    value = []
    with open('GraphemeBreakProperty.txt', 'r') as file:
        line = file.readline()
        while line:
            line = line.strip()
            if not line.startswith('#'):
                m = re.search("([0-9A-F]{1,6})\.\.([0-9A-F]{1,6})\s*\;\s*(\w{1,})", line)
                if m:
                    if m.group(3) == property_name:
                        length = int(m.group(2), 16) - int(m.group(1), 16) + 1
                        s = int(m.group(1), 16)
                        for x in range(length):
                            value.append(s + x);
                else:
                    m = re.search("([0-9A-F]{1,6})\s*\;\s*(\w{1,})", line)
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



print("{ \"tables\": [")

# CR
v = get_grapheme_property_list("CR")
print("{ \"name\": \"CR\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# LF
v = get_grapheme_property_list("LF")
print("{ \"name\": \"LF\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Control
v = get_grapheme_property_list("Control")
print("{ \"name\": \"Control\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Extend
v = get_grapheme_property_list("Extend")
print("{ \"name\": \"Extend\", \"value\": { \"codepoint\":")
print(v)
print("}},")
extend = v

# ZWJ
v = get_grapheme_property_list("ZWJ")
print("{ \"name\": \"ZWJ\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Regional_Indicator
v = get_grapheme_property_list("Regional_Indicator")
print("{ \"name\": \"Regional_Indicator\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Prepend
v = get_grapheme_property_list("Prepend")
print("{ \"name\": \"Prepend\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# SpacingMark
v = get_grapheme_property_list("SpacingMark")
print("{ \"name\": \"SpacingMark\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# L
v = get_grapheme_property_list("L")
print("{ \"name\": \"L\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# V
v = get_grapheme_property_list("V")
print("{ \"name\": \"V\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# T
v = get_grapheme_property_list("T")
print("{ \"name\": \"T\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# LV
v = get_grapheme_property_list("LV")
print("{ \"name\": \"LV\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# LVT
v = get_grapheme_property_list("LVT")
print("{ \"name\": \"LVT\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Extended_Pictographic
v = get_emoji_list("Extended_Pictographic")
v.sort()
print("{ \"name\": \"Extended_Pictographic\", \"value\": { \"codepoint\":")
print(v)
print("}},")


# Alias
# (GB11)
print("{ \"name\": \"Extended_Pictographic_Extend\", \"value\": { \"left\": \"Extended_Pictographic\", \"right\": \"Extend\" }},")
print("{ \"name\": \"Extended_Pictographic_Extend\", \"value\": { \"left\": \"Extended_Pictographic_Extend\", \"right\": \"Extend\" }},")
print("{ \"name\": \"Extended_Pictographic_Extend_ZWJ\", \"value\": { \"left\": \"Extended_Pictographic\", \"right\": \"ZWJ\" }},")
print("{ \"name\": \"Extended_Pictographic_Extend_ZWJ\", \"value\": { \"left\": \"Extended_Pictographic_Extend\", \"right\": \"ZWJ\" }},")
# (GB12)
print("{ \"name\": \"RI_RI\", \"value\": { \"left\": \"Regional_Indicator\", \"right\": \"Regional_Indicator\" }}")

# Rules

print("], \"rules\": [")
# GB1
print("{ \"left\": [\"sot\"], \"right\": [\"Any\"], \"break_state\": true },")
# GB2
print("{ \"left\": [\"L\", \"V\", \"T\", \"LV\", \"LVT\", \"Unknown\", \"RI_RI\", \"Extended_Pictographic_Extend\", \"Extended_Pictographic_Extend_ZWJ\"], \"right\": [\"eot\"], \"break_state\": true },")
# GB3
print("{ \"left\": [\"CR\"], \"right\": [\"LF\"], \"break_state\": false },")
# GB4
print("{ \"left\": [\"Control\", \"CR\", \"LF\"], \"right\": [\"Control\", \"CR\", \"Extend\", \"L\", \"LV\", \"LVT\", \"V\", \"T\"], \"break_state\": true },")
print("{ \"left\": [\"Control\", \"LF\"], \"right\": [\"LF\"], \"break_state\": true },")
# GB5
print("{ \"left\": [\"Extended_Pictographic_Extend_ZWJ\", \"Extended_Pictographic_Extend\"], \"right\": [\"Control\", \"CR\", \"LF\"], \"break_state\": true },")
# GB6 
print("{ \"left\": [\"L\"], \"right\": [\"L\", \"V\", \"LV\", \"LVT\"], \"break_state\": false },")
# GB7
print("{ \"left\": [\"LV\", \"V\"], \"right\": [\"V\", \"T\"], \"break_state\": false },")
# GB8
print("{ \"left\": [\"LVT\", \"T\"], \"right\": [\"T\"], \"break_state\": false },")
# GB9
print("{ \"left\": [\"L\", \"V\", \"T\", \"LV\", \"LVT\", \"Regional_Indicator\", \"Unknown\", \"Extend\", \"SpacingMark\", \"Extended_Pictographic\", \"ZWJ\", \"RI_RI\"], \"right\": [\"Extend\", \"ZWJ\"], \"break_state\": false },")
# GB9a
print("{ \"left\": [\"L\", \"V\", \"T\", \"LV\", \"LVT\", \"Extend\", \"Prepend\", \"Unknown\", \"SpacingMark\", \"Extended_Pictographic\", \"ZWJ\", \"Regional_Indicator\", \"Extended_Pictographic_Extend_ZWJ\", \"Extended_Pictographic_Extend\"], \"right\": [\"SpacingMark\"], \"break_state\": false },")
# GB9b
print("{ \"left\": [\"Prepend\"], \"right\": [\"Extend\", \"Unknown\", \"Regional_Indicator\", \"Prepend\", \"L\", \"V\", \"T\", \"LV\", \"LVT\", \"Extended_Pictographic\", \"ZWJ\"], \"break_state\": false },")
# GB11
print("{ \"left\": [\"Extended_Pictographic_Extend_ZWJ\"], \"right\": [\"Extended_Pictographic\"], \"break_state\": false },")
# GB12
print("{ \"left\": [\"RI_RI\"], \"right\": [\"Regional_Indicator\"], \"break_state\": true },")

# GB999
print("{ \"left\": [\"Extended_Pictographic_Extend\", \"Extended_Pictographic_Extend_ZWJ\"], \"right\": [\"Regional_Indicator\", \"Prepend\", \"L\", \"V\", \"T\", \"LV\", \"LVT\", \"Extended_Pictographic\", \"Unknown\"], \"break_state\": true },")
print("{ \"left\": [\"RI_RI\"], \"right\": [\"Unknown\"], \"break_state\": true },")
print("{ \"left\": [\"Any\"], \"right\": [\"Any\"], \"break_state\": true }")
print("]}")
