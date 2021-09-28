#!/usr/bin/env python3

import os
import re
import subprocess


def get_sentence_property_list(property_name):
    value = []
    with open('SentenceBreakProperty.txt', 'r') as file:
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


print("{ \"tables\": [")

# CR
v = get_sentence_property_list("CR")
v.sort()
print("{ \"name\": \"CR\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# LF
v = get_sentence_property_list("LF")
v.sort()
print("{ \"name\": \"LF\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Extend
v = get_sentence_property_list("Extend")
v.sort()
print("{ \"name\": \"Extend\", \"value\": { \"codepoint\":")
print(v)
print("}},")
extend = v

# Sep
v = get_sentence_property_list("Sep")
v.sort()
print("{ \"name\": \"Sep\", \"value\": { \"codepoint\":")
print(v)
print("}},")
sep = v

# Format
v = get_sentence_property_list("Format")
v.sort()
print("{ \"name\": \"Format\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Sp
v = get_sentence_property_list("Sp")
v.sort()
print("{ \"name\": \"Sp\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Lower
v = get_sentence_property_list("Lower")
v.sort()
print("{ \"name\": \"Lower\", \"value\": { \"codepoint\":")
print(v)
print("}},")
lower = v

# Upper
v = get_sentence_property_list("Upper")
v.sort()
print("{ \"name\": \"Upper\", \"value\": { \"codepoint\":")
print(v)
print("}},")
upper = v

# OLetter
v = get_sentence_property_list("OLetter")
v.sort()
print("{ \"name\": \"OLetter\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Numeric
v = get_sentence_property_list("Numeric")
v.sort()
print("{ \"name\": \"Numeric\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# ATerm
v = get_sentence_property_list("ATerm")
v.sort()
print("{ \"name\": \"ATerm\", \"value\": { \"codepoint\":")
print(v)
print("}},")
aterm = v

# SContinue
v = get_sentence_property_list("SContinue")
v.sort()
print("{ \"name\": \"SContinue\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# STerm
v = get_sentence_property_list("STerm")
v.sort()
print("{ \"name\": \"STerm\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Close
v = get_sentence_property_list("Close")
v.sort()
print("{ \"name\": \"Close\", \"value\": { \"codepoint\":")
print(v)
print("}},")

# Alias
# SB4
print("{ \"name\": \"Lower\", \"value\": { \"left\": \"Lower\", \"right\": \"Extend\" }},")
print("{ \"name\": \"Lower\", \"value\": { \"left\": \"Lower\", \"right\": \"Format\" }},")
print("{ \"name\": \"Upper\", \"value\": { \"left\": \"Upper\", \"right\": \"Extend\" }},")
print("{ \"name\": \"Upper\", \"value\": { \"left\": \"Upper\", \"right\": \"Format\" }},")
print("{ \"name\": \"OLetter\", \"value\": { \"left\": \"OLetter\", \"right\": \"Extend\" }},")
print("{ \"name\": \"OLetter\", \"value\": { \"left\": \"OLetter\", \"right\": \"Format\" }},")
print("{ \"name\": \"ATerm\", \"value\": { \"left\": \"ATerm\", \"right\": \"Extend\" }},")
print("{ \"name\": \"ATerm\", \"value\": { \"left\": \"ATerm\", \"right\": \"Format\" }},")
print("{ \"name\": \"STerm\", \"value\": { \"left\": \"STerm\", \"right\": \"Extend\" }},")
print("{ \"name\": \"STerm\", \"value\": { \"left\": \"STerm\", \"right\": \"Format\" }},")
# SB5
print("{ \"name\": \"ATerm_Close\", \"value\": { \"left\": \"ATerm_Close\", \"right\": \"Extend\" }},")
print("{ \"name\": \"ATerm_Close\", \"value\": { \"left\": \"ATerm_Close\", \"right\": \"Format\" }},")
print("{ \"name\": \"ATerm_Close_Sp\", \"value\": { \"left\": \"ATerm_Close_Sp\", \"right\": \"Extend\" }},")
print("{ \"name\": \"ATerm_Close_Sp\", \"value\": { \"left\": \"ATerm_Close_Sp\", \"right\": \"Format\" }},")
print("{ \"name\": \"STerm_Close\", \"value\": { \"left\": \"STerm_Close\", \"right\": \"Extend\" }},")
print("{ \"name\": \"STerm_Close\", \"value\": { \"left\": \"STerm_Close\", \"right\": \"Format\" }},")
print("{ \"name\": \"STerm_Close_Sp\", \"value\": { \"left\": \"STerm_Close_Sp\", \"right\": \"Extend\" }},")
print("{ \"name\": \"STerm_Close_Sp\", \"value\": { \"left\": \"STerm_Close_Sp\", \"right\": \"Format\" }},")
print("{ \"name\": \"Upper_ATerm\", \"value\": { \"left\": \"Upper_ATerm\", \"right\": \"Extend\" }},")
print("{ \"name\": \"Upper_ATerm\", \"value\": { \"left\": \"Upper_ATerm\", \"right\": \"Format\" }},")
print("{ \"name\": \"Lower_ATerm\", \"value\": { \"left\": \"Lower_ATerm\", \"right\": \"Extend\" }},")
print("{ \"name\": \"Lower_ATerm\", \"value\": { \"left\": \"Lower_ATerm\", \"right\": \"Format\" }},")
# SB7
print("{ \"name\": \"Upper_ATerm\", \"value\": { \"left\": \"Upper\", \"right\": \"ATerm\" }},")
print("{ \"name\": \"Lower_ATerm\", \"value\": { \"left\": \"Lower\", \"right\": \"ATerm\" }},")
# SB8
print("{ \"name\": \"ATerm_Close\", \"value\": { \"left\": \"ATerm\", \"right\": \"Close\" }},")
print("{ \"name\": \"ATerm_Close\", \"value\": { \"left\": \"ATerm_Close\", \"right\": \"Close\" }},")
print("{ \"name\": \"ATerm_Close\", \"value\": { \"left\": \"Upper_ATerm\", \"right\": \"Close\" }},")
print("{ \"name\": \"ATerm_Close\", \"value\": { \"left\": \"Lower_ATerm\", \"right\": \"Close\" }},")
print("{ \"name\": \"ATerm_Close_Sp\", \"value\": { \"left\": \"ATerm\", \"right\": \"Sp\" }},")
print("{ \"name\": \"ATerm_Close_Sp\", \"value\": { \"left\": \"Upper_ATerm\", \"right\": \"Sp\" }},")
print("{ \"name\": \"ATerm_Close_Sp\", \"value\": { \"left\": \"Lower_ATerm\", \"right\": \"Sp\" }},")
print("{ \"name\": \"ATerm_Close_Sp\", \"value\": { \"left\": \"ATerm_Close\", \"right\": \"Sp\" }},")
print("{ \"name\": \"ATerm_Close_Sp\", \"value\": { \"left\": \"ATerm_Close_Sp\", \"right\": \"Sp\" }},")
print("{ \"name\": \"ATerm_Close_Sp_ParaSep\", \"value\": { \"left\": \"ATerm_Close\", \"right\": \"Sep\" }},")
print("{ \"name\": \"ATerm_Close_Sp_ParaSep\", \"value\": { \"left\": \"ATerm_Close\", \"right\": \"CR\" }},")
print("{ \"name\": \"ATerm_Close_Sp_ParaSep\", \"value\": { \"left\": \"ATerm_Close\", \"right\": \"LF\" }},")
print("{ \"name\": \"ATerm_Close_Sp_ParaSep\", \"value\": { \"left\": \"ATerm_Close_Sp\", \"right\": \"Sep\" }},")
print("{ \"name\": \"ATerm_Close_Sp_ParaSep\", \"value\": { \"left\": \"ATerm_Close_Sp\", \"right\": \"CR\" }},")
print("{ \"name\": \"ATerm_Close_Sp_ParaSep\", \"value\": { \"left\": \"ATerm_Close_Sp\", \"right\": \"LF\" }},")
#print("{ \"name\": \"ATerm_Close_Sp_ParaSep\", \"value\": { \"left\": \"ATerm_Close_Sp_ParaSep\", \"right\": \"Sep\" }},")
#print("{ \"name\": \"ATerm_Close_Sp_ParaSep\", \"value\": { \"left\": \"ATerm_Close_Sp_ParaSep\", \"right\": \"CR\" }},")
#print("{ \"name\": \"ATerm_Close_Sp_ParaSep\", \"value\": { \"left\": \"ATerm_Close_Sp_ParaSep\", \"right\": \"LF\" }},")
print("{ \"name\": \"STerm_Close\", \"value\": { \"left\": \"STerm\", \"right\": \"Close\" }},")
print("{ \"name\": \"STerm_Close\", \"value\": { \"left\": \"STerm_Close\", \"right\": \"Close\" }},")
print("{ \"name\": \"STerm_Close_Sp\", \"value\": { \"left\": \"STerm\", \"right\": \"Sp\" }},")
print("{ \"name\": \"STerm_Close_Sp\", \"value\": { \"left\": \"STerm_Close\", \"right\": \"Sp\" }},")
print("{ \"name\": \"STerm_Close_Sp\", \"value\": { \"left\": \"STerm_Close_Sp\", \"right\": \"Sp\" }},")
print("{ \"name\": \"STerm_Close_Sp_ParaSep\", \"value\": { \"left\": \"STerm_Close\", \"right\": \"Sep\" }},")
print("{ \"name\": \"STerm_Close_Sp_ParaSep\", \"value\": { \"left\": \"STerm_Close\", \"right\": \"CR\" }},")
print("{ \"name\": \"STerm_Close_Sp_ParaSep\", \"value\": { \"left\": \"STerm_Close\", \"right\": \"LF\" }},")
print("{ \"name\": \"STerm_Close_Sp_ParaSep\", \"value\": { \"left\": \"STerm_Close_Sp\", \"right\": \"Sep\" }},")
print("{ \"name\": \"STerm_Close_Sp_ParaSep\", \"value\": { \"left\": \"STerm_Close_Sp\", \"right\": \"CR\" }},")
print("{ \"name\": \"STerm_Close_Sp_ParaSep\", \"value\": { \"left\": \"STerm_Close_Sp\", \"right\": \"LF\" }}")

# Rules

print("], \"rules\": [")
# SB1
print("{ \"left\": [\"sot\"], \"right\": [\"Any\"], \"break_state\": true },")
# SB2
print("{ \"left\": [\"Sep\", \"Lower\", \"Upper\", \"OLetter\", \"Numeric\", \"Extend\", \"Format\"], \"right\": [\"eot\"], \"break_state\": true },")
print("{ \"left\": [\"ATerm_Close\", \"ATerm_Close_Sp\", \"ATerm_Close_Sp_ParaSep\"], \"right\": [\"eot\"], \"break_state\": true },")
print("{ \"left\": [\"STerm_Close\", \"STerm_Close_Sp\", \"STerm_Close_Sp_ParaSep\"], \"right\": [\"eot\"], \"break_state\": true },")
print("{ \"left\": [\"Lower_ATerm\", \"Upper_ATerm\"], \"right\": [\"eot\"], \"break_state\": true },")
# SB3
print("{ \"left\": [\"CR\"], \"right\": [\"LF\"], \"break_state\": false },")
# SB4
print("{ \"left\": [\"Sep\", \"CR\", \"LF\"], \"right\": [\"ATerm\", \"Numeric\", \"Sep\", \"Lower\", \"Upper\", \"OLetter\", \"Sp\", \"Unknown\", \"STerm\", \"Close\", \"SContinue\", \"Format\", \"Extend\", \"CR\"], \"break_state\": true },")
print("{ \"left\": [\"Sep\", \"LF\", \"ATerm_Close\", \"ATerm_Close_Sp\"], \"right\": [\"LF\"], \"break_state\": true },")
print("{ \"left\": [\"ATerm_Close_Sp_ParaSep\", \"STerm_Close_Sp_ParaSep\"], \"right\": [\"ATerm\", \"Numeric\", \"Lower\", \"Upper\", \"OLetter\", \"Sp\", \"Unknown\", \"STerm\", \"Close\", \"SContinue\", \"Format\", \"Extend\"], \"break_state\": true },")
# SB6
print("{ \"left\": [\"ATerm\", \"Upper_ATerm\", \"Lower_ATerm\"], \"right\": [\"Numeric\"], \"break_state\": false },")
# SB7
print("{ \"left\": [\"Upper_ATerm\", \"Lower_ATerm\"], \"right\": [\"Upper\"], \"break_state\": false },")
# SB8
print("{ \"left\": [\"ATerm\", \"ATerm_Close\", \"ATerm_Close_Sp\"], \"right\": [\"Lower\"], \"break_state\": false },")
print("{ \"left\": [\"Lower_ATerm\", \"Upper_ATerm\"], \"right\": [\"Lower\"], \"break_state\": false },")
# SB8a
print("{ \"left\": [\"ATerm\", \"ATerm_Close\", \"ATerm_Close_Sp\", \"STerm\", \"STerm_Close\", \"STerm_Close_Sp\", \"Lower_ATerm\", \"Upper_ATerm\"], \"right\": [\"SContinue\", \"ATerm\", \"STerm\"], \"break_state\": false },")
# SB9
# print("{ \"left\": [\"ATerm\", \"ATerm_Close\"], \"right\": [\"Sep\", \"CR\", \"LF\"], \"break_state\": false },")
# print("{ \"left\": [\"STerm\", \"STerm_Close\"], \"right\": [\"Sep\", \"CR\", \"LF\"], \"break_state\": false },")
# print("{ \"left\": [\"ATerm\", \"ATerm_Close\", \"STerm\", \"STerm_Close\"], \"right\": [\"Close\", \"Sp\", \"Sep\", \"CR\", \"LF\"], \"break_state\": false },")
# print("{ \"left\": [\"ATerm\", \"ATerm_Close\", \"ATerm_Close_Sp\"], \"right\": [\"Sp\", \"Sep\", \"CR\", \"LF\"], \"break_state\": false },")
# print("{ \"left\": [\"ATerm\", \"ATerm_Close\", \"ATerm_Close_Sp\", \"ATearm_Close_Sp_ParaSep\"], \"right\": [\"Sp\", \"ParaSep\"], \"break_state\": true },")
# SB11
print("{ \"left\": [\"ATerm_Close_Sp_ParaSep\", \"STerm_Close_Sp_ParaSep\"], \"right\": [\"ATerm\", \"Lower\", \"OLetter\", \"Upper\", \"Numeric\", \"STerm\"], \"break_state\": true },")
print("{ \"left\": [\"ATerm_Close_Sp\", \"STerm_Close_Sp\"], \"right\": [\"Numeric\", \"Upper\", \"Close\"], \"break_state\": true },")
print("{ \"left\": [\"ATerm_Close\", \"STerm\", \"STerm_Close\"], \"right\": [\"Numeric\", \"Upper\"], \"break_state\": true },")
print("{ \"left\": [\"ATerm\", \"Upper_ATerm\", \"Lower_ATerm\", \"STerm\"], \"right\": [\"Unknown\", \"Upper\", \"Lower\", \"OLetter\", \"ATerm\", \"STerm\"], \"break_state\": true },")
# SB998
print("{ \"left\": [\"Any\"], \"right\": [\"Any\"], \"break_state\": false }")
print("]}")
