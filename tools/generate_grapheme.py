#!/usr/bin/env python3

import os
import re
import subprocess


def get_script_list(script_name, general_category):
    value = []
    with open('Scripts.txt', 'r') as file:
        line = file.readline()
        while line:
            line = line.strip()
            if not line.startswith('#'):
                m = re.search("([0-9A-F]{1,6})\.\.([0-9A-F]{1,6})\s*\;\s*([A-Za-z]{2,})\s*#\s*([A-Za-z&]{2,})",
                              line)
                if m:
                    if (script_name == "" or m.group(3) == script_name) and (general_category == "" or m.group(4) == general_category):
                        length = int(m.group(2), 16) - int(m.group(1), 16) + 1
                        s = int(m.group(1), 16)
                        for x in range(length):
                            value.append(s + x);
                else:
                    m = re.search("([0-9A-F]{1,6})\s*\;\s*([A-Za-z]{2,})\s*#\s*([A-Za-z&]{2,})", line)
                    if m:
                        if int(m.group(1), 16) >= 0x20000:
                            line = file.readline()
                            continue
                        if (script_name == "" or m.group(2) == script_name) and (general_category == "" or m.group(3) == general_category):
                            s = int(m.group(1), 16)
                            value.append(s);
            line = file.readline()
    return value


def get_property_list(property_name):
    value = []
    with open('DerivedCoreProperties.txt', 'r') as file:
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

    return value


def get_proplist_list(property_name):
    value = []
    with open('PropList.txt', 'r') as file:
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
                        if m.group(2) == property_name:
                            s = int(m.group(1), 16)
                            value.append(s);
            line = file.readline()

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


def get_linebreak_list(property_name):
    value = []
    with open('LineBreak.txt', 'r') as file:
        line = file.readline()
        while line:
            line = line.strip()
            if not line.startswith('#'):
                m = re.search("([0-9A-F]{1,6})\.\.([0-9A-F]{1,6})\;(\w{2,})", line)
                if m:
                    if m.group(3) == property_name:
                        length = int(m.group(2), 16) - int(m.group(1), 16) + 1
                        s = int(m.group(1), 16)
                        for x in range(length):
                            value.append(s + x);
                else:
                    m = re.search("([0-9A-F]{1,6})\;(\w{2,})", line)
                    if m:
                        if m.group(2) == property_name:
                            s = int(m.group(1), 16)
                            value.append(s);
            line = file.readline()
    return value


def get_indic_syllabic(name):
    value = []
    with open('IndicSyllabicCategory.txt', 'r') as file:
        line = file.readline()
        while line:
            line = line.strip()
            if not line.startswith('#'):
                m = re.search("([0-9A-F]{1,6})\.\.([0-9A-F]{1,6})\s*\;\s*(\w{1,})", line)
                if m:
                    if m.group(3) == name:
                        length = int(m.group(2), 16) - int(m.group(1), 16) + 1
                        s = int(m.group(1), 16)
                        for x in range(length):
                            value.append(s + x);
                else:
                    m = re.search("([0-9A-F]{1,6})\s*\;\s*(\w{1,})", line)
                    if m:
                        if m.group(2) == name:
                            s = int(m.group(1), 16)
                            value.append(s);
            line = file.readline()
    return value


def get_hangul_syllable(name):
    value = []
    with open('HangulSyllableType.txt', 'r') as file:
        line = file.readline()
        while line:
            line = line.strip()
            if not line.startswith('#'):
                m = re.search("([0-9A-F]{1,6})\.\.([0-9A-F]{1,6})\s*\;\s*(\w{1,})", line)
                if m:
                    if m.group(3) == name:
                        length = int(m.group(2), 16) - int(m.group(1), 16) + 1
                        s = int(m.group(1), 16)
                        for x in range(length):
                            value.append(s + x);
                else:
                    m = re.search("([0-9A-F]{1,6})\s*\;\s*(\w{1,})", line)
                    if m:
                        if m.group(2) == name:
                            s = int(m.group(1), 16)
                            value.append(s);
            line = file.readline()
    return value
    

print("{ \"tables\": [")

# CR
v = [0x000d]
print("{ \"name\": \"CR\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# LF
v = [0x000a]
print("{ \"name\": \"LF\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Control
v = []
v.extend(get_script_list("", "Zl"))
v.extend(get_script_list("", "Zp"))
v.extend(get_script_list("", "Cc"))
v.extend(get_script_list("", "Cf"))
v.remove(0x000d)
v.remove(0x000a)
v.remove(0x200c)
v.remove(0x200d)
v.sort()
print("{ \"name\": \"Control\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Extend
v = get_property_list("Grapheme_Extend")
v.extend(get_emoji_list("Emoji_Modifier"))
v.extend(get_script_list("", "Me"))
v.extend(get_script_list("", "Mn"))
v.append(0x200c)
v.sort()
print("{ \"name\": \"Extend\", \"value\": { \"codepoint\":")
print(v)
print("}},")
extend = v

# ZWJ
v = [0x200d]
print("{ \"name\": \"ZWJ\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Regional_Indicator
v = get_proplist_list("Regional_Indicator")
v.sort()
print("{ \"name\": \"Regional_Indicator\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Prepend
v = get_indic_syllabic("Consonant_Preceding_Repha")
v.extend(get_indic_syllabic("Consonant_Prefixed"))
v.extend(get_proplist_list("Prepended_Concatenation_Mark"))
v.sort()
print("{ \"name\": \"Prepend\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# SpacingMark
v = get_script_list("", "Mc")
for i in extend:
    try:
        v.remove(i)
    except ValueError:
        pass
v.append(0x0e33)
v.append(0x0eb3)
v.remove(0x102b)
v.remove(0x102c)
v.remove(0x1038)
for i in range(0x1062, 0x1065):
    try:
        v.remove(i)
    except ValueError:
        pass
for i in range(0x1067, 0x106e):
    try:
        v.remove(i)
    except ValueError:
        pass
v.remove(0x1083)
for i in range(0x1087, 0x108d):
    try:
        v.remove(i)
    except ValueError:
        pass
v.remove(0x108f)
for i in range(0x109a, 0x109d):
    try:
        v.remove(i)
    except ValueError:
        pass
# v.remove(0x1a61)
# v.remove(0x1a63)
# v.remove(0x1a64)
v.remove(0xaa7b)
v.remove(0xaa7d)
v.remove(0x11720)
v.remove(0x11721)
v.sort()
print("{ \"name\": \"SpacingMark\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# L
v = get_hangul_syllable("L")
print("{ \"name\": \"L\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# V
v = get_hangul_syllable("V")
print("{ \"name\": \"V\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# T
v = get_hangul_syllable("T")
print("{ \"name\": \"T\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# LV
v = get_hangul_syllable("LV")
print("{ \"name\": \"LV\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# LVT
v = get_hangul_syllable("LVT")
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
print("{ \"left\": [\"L\", \"V\", \"T\", \"LV\", \"LVT\", \"Unknown\", \"RI_RI\"], \"right\": [\"eot\"], \"break_state\": true },")
# GB3
print("{ \"left\": [\"CR\"], \"right\": [\"LF\"], \"break_state\": false },")
# GB4
print("{ \"left\": [\"Control\", \"CR\", \"LF\"], \"right\": [\"Control\", \"CR\", \"Extend\", \"L\", \"LV\", \"LVT\", \"V\", \"T\"], \"break_state\": true },")
print("{ \"left\": [\"Control\", \"LF\"], \"right\": [\"LF\"], \"break_state\": true },")
# GB6 
print("{ \"left\": [\"L\"], \"right\": [\"L\", \"V\", \"LV\", \"LVT\"], \"break_state\": false },")
# GB7
print("{ \"left\": [\"LV\", \"V\"], \"right\": [\"V\", \"T\"], \"break_state\": false },")
# GB8
print("{ \"left\": [\"LVT\", \"T\"], \"right\": [\"T\"], \"break_state\": false },")
# GB9
print("{ \"left\": [\"L\", \"V\", \"T\", \"LV\", \"LVT\", \"Regional_Indicator\", \"Unknown\", \"Extend\", \"SpacingMark\", \"Extended_Pictographic\", \"ZWJ\", \"RI_RI\"], \"right\": [\"Extend\", \"ZWJ\"], \"break_state\": false },")
# GB9a
print("{ \"left\": [\"L\", \"V\", \"T\", \"LV\", \"LVT\", \"Extend\", \"Prepend\", \"Unknown\", \"SpacingMark\", \"Extended_Pictographic\", \"ZWJ\", \"Regional_Indicator\"], \"right\": [\"SpacingMark\"], \"break_state\": false },")
# GB9b
print("{ \"left\": [\"Prepend\"], \"right\": [\"Extend\", \"Unknown\", \"Regional_Indicator\", \"Prepend\", \"L\", \"V\", \"T\", \"LV\", \"LVT\", \"Extended_Pictographic\", \"ZWJ\"], \"break_state\": false },")
# GB11
print("{ \"left\": [\"Extended_Pictographic_Extend_ZWJ\"], \"right\": [\"Extended_Pictographic\"], \"break_state\": false },")
# GB12
print("{ \"left\": [\"RI_RI\"], \"right\": [\"Regional_Indicator\"], \"break_state\": true },")

# GB999
print("{ \"left\": [\"Any\"], \"right\": [\"Any\"], \"break_state\": true }")
print("]}")
