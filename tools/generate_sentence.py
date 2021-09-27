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

# Extend
v = get_property_list("Grapheme_Extend")
v.extend(get_script_list("", "Mc"))
v.append(0x200d)
v.sort()
print("{ \"name\": \"Extend\", \"value\": { \"codepoint\":")
print(v)
print("}},")
extend = v

# Sep
v = [0x0085, 0x2028, 0x2029]
print("{ \"name\": \"Sep\", \"value\": { \"codepoint\":")
print(v)
print("}},")
sep = v

# Format
v = get_script_list("", "Cf")
v.remove(0x200c)
v.remove(0x200d)
v.sort()
print("{ \"name\": \"Format\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Sp
v = get_proplist_list("White_Space")
for i in sep:
    try:
        v.remove(i)
    except ValueError:
        pass
v.remove(0x000a)
v.remove(0x000d)
print("{ \"name\": \"Sp\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Lower
v = get_property_list("Lowercase") # LowerCase = Yes
for i in get_property_list("Grapheme_Extend"):
    try:
        v.remove(i)
    except ValueError:
        pass
for i in range(0x10d0, 0x10fb):
    try:
        v.remove(i)
    except ValueError:
        pass
v.remove(0x10fd)
v.remove(0x10fe)
v.remove(0x10ff)
print("{ \"name\": \"Lower\", \"value\": { \"codepoint\":")
print(v)
print("}},")
lower = v

# Upper
v = get_script_list("", "Lt") # Titlecase_Letter
v.extend(get_property_list("Uppercase")) # Uppercase = Yes
for i in range(0x1c90, 0x1cbb):
    try:
        v.remove(i)
    except ValueError:
        pass
v.remove(0x1cbd)
v.remove(0x1cbe)
v.remove(0x1cbf)
v.sort()
print("{ \"name\": \"Upper\", \"value\": { \"codepoint\":")
print(v)
print("}},")
upper = v

# OLetter
v = get_property_list("Alphabetic")
v.append(0x00a0)
v.append(0x05f3)
for i in lower:
    try:
        v.remove(i)
    except ValueError:
        pass
for i in upper:
    try:
        v.remove(i)
    except ValueError:
        pass
for i in extend:
    try:
        v.remove(i)
    except ValueError:
        pass
v.sort()

print("{ \"name\": \"ALetter\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Numeric
v = get_linebreak_list("NU") # LineBreak = Numeric
for i in range(0xff10, 0xff20):
    v.append(i)
v.sort()
print("{ \"name\": \"Numeric\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# ATerm
v = [0x002e, 0x2024, 0xfe52, 0xfe0e]
print("{ \"name\": \"ATerm\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# SContinue
v = [0x002c, 0x002d, 0x003a, 0x055d, 0x060c, 0x060d, 0x07f8, 0x1802, 0x1808, 0x2013, 0x2014, 0x3001, 0xfe10, 0xfe11, 0xfe13, 0xfe31, 0xfe32, 0xfe50, 0xfe51, 0xfe58, 0xfe63, 0xff0c, 0xff0d, 0xff1a, 0xff64]
print("{ \"name\": \"SContinue\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# STerm
v = get_proplist_list("Sentence_Terminal")
print("{ \"name\": \"STerm\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Close
v = get_script_list("", "Ps") # Open_Punctuation
v.extend(get_script_list("", "Pe")) # Close_Punctuation
v.extend(get_linebreak_list("QU")) # LineBreak = Quotation
try:
    v.remove(0x5f3)
except ValueError:
    pass
for i in [0x002e, 0x2024, 0xfe52, 0xfe0e]: # ATerm = No
    try:
        v.remove(i)
    except ValueError:
        pass
for i in get_proplist_list("Sentence_Terminal"): # STerm = No
    try:
        v.remove(i)
    except ValueError:
        pass
v.sort()
print("{ \"name\": \"Close\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Alias
# (WB4)
print("{ \"name\": \"Lower\", \"value\": { \"left\": \"Lower\", \"right\": \"Extend\" }},")
print("{ \"name\": \"Lower\", \"value\": { \"left\": \"Lower\", \"right\": \"Format\" }},")
print("{ \"name\": \"Upper\", \"value\": { \"left\": \"Upper\", \"right\": \"Extend\" }},")
print("{ \"name\": \"Upper\", \"value\": { \"left\": \"Upper\", \"right\": \"Format\" }},")
print("{ \"name\": \"OLetter\", \"value\": { \"left\": \"OLetter\", \"right\": \"Extend\" }},")
print("{ \"name\": \"OLetter\", \"value\": { \"left\": \"OLetter\", \"right\": \"Format\" }},")
# SB7
print("{ \"name\": \"Upper_ATerm\", \"value\": { \"left\": \"Upper\", \"right\": \"ATerm\" }},")
print("{ \"name\": \"Lower_ATerm\", \"value\": { \"left\": \"Lower\", \"right\": \"ATerm\" }},")
print("{ \"name\": \"ATerm_Close\", \"value\": { \"left\": \"ATerm\", \"right\": \"Close\" }},")
print("{ \"name\": \"ATerm_Close\", \"value\": { \"left\": \"ATerm_Close\", \"right\": \"Close\" }},")
print("{ \"name\": \"ATerm_Close_Sp\", \"value\": { \"left\": \"ATerm\", \"right\": \"Sp\" }},")
print("{ \"name\": \"ATerm_Close_Sp\", \"value\": { \"left\": \"ATerm_Close\", \"right\": \"Sp\" }},")
print("{ \"name\": \"ATerm_Close_Sp\", \"value\": { \"left\": \"ATerm_Close_Sp\", \"right\": \"Sp\" }},")
print("{ \"name\": \"ATerm_Close_Sp_ParaSep\", \"value\": { \"left\": \"ATerm_Close_Sp\", \"right\": \"Sep\" }},")
print("{ \"name\": \"ATerm_Close_Sp_ParaSep\", \"value\": { \"left\": \"ATerm_Close_Sp\", \"right\": \"CR\" }},")
print("{ \"name\": \"ATerm_Close_Sp_ParaSep\", \"value\": { \"left\": \"ATerm_Close_Sp\", \"right\": \"LF\" }},")
print("{ \"name\": \"ATerm_Close_Sp_ParaSep\", \"value\": { \"left\": \"ATerm_Close_Sp_ParaSep\", \"right\": \"Sep\" }},")
print("{ \"name\": \"ATerm_Close_Sp_ParaSep\", \"value\": { \"left\": \"ATerm_Close_Sp_ParaSep\", \"right\": \"CR\" }},")
print("{ \"name\": \"ATerm_Close_Sp_ParaSep\", \"value\": { \"left\": \"ATerm_Close_Sp_ParaSep\", \"right\": \"LF\" }},")
print("{ \"name\": \"STerm_Close\", \"value\": { \"left\": \"STerm\", \"right\": \"Close\" }},")
print("{ \"name\": \"STerm_Close\", \"value\": { \"left\": \"STerm_Close\", \"right\": \"Close\" }},")
print("{ \"name\": \"STerm_Close_Sp\", \"value\": { \"left\": \"STerm\", \"right\": \"Sp\" }},")
print("{ \"name\": \"STerm_Close_Sp\", \"value\": { \"left\": \"STerm_Close\", \"right\": \"Sp\" }},")
print("{ \"name\": \"STerm_Close_Sp\", \"value\": { \"left\": \"STerm_Close_Sp\", \"right\": \"Sp\" }},")
print("{ \"name\": \"STerm_Close_Sp_ParaSep\", \"value\": { \"left\": \"STerm_Close_Sp\", \"right\": \"Sep\" }},")
print("{ \"name\": \"STerm_Close_Sp_ParaSep\", \"value\": { \"left\": \"STerm_Close_Sp\", \"right\": \"CR\" }},")
print("{ \"name\": \"STerm_Close_Sp_ParaSep\", \"value\": { \"left\": \"STerm_Close_Sp\", \"right\": \"LF\" }}")

# Rules

print("], \"rules\": [")
# SB1
print("{ \"left\": [\"sot\"], \"right\": [\"Any\"], \"break_state\": true },")
# SB2
print("{ \"left\": [\"Sep\", \"Lower\", \"Upper\", \"OLetter\", \"Numeric\", \"Extend\", \"Format\"], \"right\": [\"eot\"], \"break_state\": true },")
print("{ \"left\": [\"STerm_Close_Sp\"], \"right\": [\"eot\"], \"break_state\": true },")
# SB3
print("{ \"left\": [\"CR\"], \"right\": [\"LF\"], \"break_state\": false },")
# SB4
print("{ \"left\": [\"Sep\", \"CR\", \"LF\"], \"right\": [\"ATerm\", \"Numeric\", \"Sep\", \"Lower\", \"Upper\", \"OLetter\", \"Sp\", \"Unknown\", \"STerm\", \"Close\", \"SContinue\", \"Format\", \"Extend\", \"Sep\", \"CR\"], \"break_state\": true },")
print("{ \"left\": [\"Sep\", \"LF\"], \"right\": [\"LF\"], \"break_state\": true },")
# SB6
print("{ \"left\": [\"ATerm\"], \"right\": [\"Numeric\"], \"break_state\": false },")
# SB7
print("{ \"left\": [\"Upper_ATerm\", \"Lower_ATerm\"], \"right\": [\"Upper\"], \"break_state\": false },")
# SB8
print("{ \"left\": [\"ATerm\", \"ATerm_Close\", \"ATerm_Close_Sp\"], \"right\": [\"Lower\"], \"break_state\": false },")
# SB8a
print("{ \"left\": [\"ATerm\", \"ATerm_Close\", \"ATerm_Close_Sp\", \"STerm\", \"STerm_Close\", \"STerm_Close_Sp\"], \"right\": [\"SContinue\", \"ATerm\", \"STerm\"], \"break_state\": false },")
# SB9
# print("{ \"left\": [\"ATerm\", \"ATerm_Close\", \"STerm\", \"STerm_Close\"], \"right\": [\"Close\", \"Sp\", \"Sep\", \"CR\", \"LF\"], \"break_state\": false },")
# print("{ \"left\": [\"ATerm\", \"ATerm_Close\", \"ATerm_Close_Sp\"], \"right\": [\"Sp\", \"Sep\", \"CR\", \"LF\"], \"break_state\": false },")
# print("{ \"left\": [\"ATerm\", \"ATerm_Close\", \"ATerm_Close_Sp\", \"ATearm_Close_Sp_ParaSep\"], \"right\": [\"Sp\", \"ParaSep\"], \"break_state\": true },")
# SB11
print("{ \"left\": [\"ATerm_Close_Sp_ParaSep\", \"STerm_Close_Sp_ParaSep\"], \"right\": [\"ATerm\", \"Lower\", \"OLetter\", \"Upper\", \"Numeric\", \"STerm\"], \"break_state\": true },")
print("{ \"left\": [\"ATerm_Close_Sp\", \"STerm_Close_Sp\"], \"right\": [\"Numeric\"], \"break_state\": true },")
print("{ \"left\": [\"ATerm_Close\", \"STerm\", \"STerm_Close\"], \"right\": [\"Numeric\"], \"break_state\": true },")
print("{ \"left\": [\"ATerm\", \"STerm\"], \"right\": [\"Unknown\"], \"break_state\": true },")
# SB998
print("{ \"left\": [\"Any\"], \"right\": [\"Any\"], \"break_state\": false }")
print("]}")
