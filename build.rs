use serde::Deserialize;
use std::env;
use std::fs::File;
use std::io::Write;
use std::path::Path;
use std::path::PathBuf;

const WORD_SEGMENTER_JSON: &[u8; 254903] = include_bytes!("data/w.json");

#[derive(Deserialize, Debug)]
struct SegmenterPropertyValueMap {
    alphabetic: Option<bool>,
    codepoint: Option<Vec<u32>>,
    general_category: Option<String>,
    line_break: Option<String>,
    script: Option<String>,
}

#[derive(Deserialize, Debug)]
struct SegmenterProperty {
    name: String,
    value: SegmenterPropertyValueMap,
}

#[derive(Deserialize, Debug)]
struct SegmenterState {
    left: Vec<String>,
    right: Vec<String>,
    break_state: bool,
}

#[derive(Deserialize, Debug)]
struct SegmenterRuleTable {
    tables: Vec<SegmenterProperty>,
    rules: Vec<SegmenterState>,
}

#[allow(dead_code)]
const BREAK_RULE: i8 = -128;
const UNKNOWN_RULE: i8 = -127;
const PREVIOUS_BREAK_RULE: i8 = -2;
const KEEP_RULE: i8 = -1;

fn set_break_state(
    break_state_table: &mut [i8],
    property_length: usize,
    left_index: usize,
    right_index: usize,
    break_state: i8,
) {
    if break_state_table[left_index as usize * property_length + right_index as usize]
        == UNKNOWN_RULE
    {
        break_state_table[left_index as usize * property_length + right_index as usize] =
            break_state;
    }
}

fn main() {
    //let mut properties_map: [u8; 0x200000] = [0; 0x200000];
    let mut properties_map: [u8; 0x10000] = [0; 0x10000];
    let mut properties_names = Vec::<String>::new();

    let word_segmenter: SegmenterRuleTable =
        serde_json::from_slice(WORD_SEGMENTER_JSON).expect("JSON syntax error");

    for p in word_segmenter.tables {
        properties_names.push(p.name.clone());

        if let Some(codepoint) = p.value.codepoint {
            for c in codepoint {
                if c >= 0x10000 {
                    break;
                }
                println!("{} = {}", c, properties_names.len());
                properties_map[c as usize] = properties_names.len() as u8;
            }
        }
        if let Some(alphabetic) = p.value.alphabetic {}

        if let Some(line_break) = p.value.line_break {}
    }

    println!("property length={}", properties_names.len());
    let rule_size = properties_names.len() * properties_names.len();
    let mut break_state_table = Vec::<i8>::with_capacity(rule_size);
    for _i in 0..rule_size {
        break_state_table.push(UNKNOWN_RULE);
    }

    for rule in word_segmenter.rules {
        let break_state = if rule.break_state {
            BREAK_RULE
        } else {
            KEEP_RULE
        };

        for l in &rule.left {
            if l == "Any" {
                // Special case: left is Any
                for r in &rule.right {
                    if r == "Any" {
                        for i in 0..rule_size {
                            if break_state_table[i] == UNKNOWN_RULE {
                                break_state_table[i] = break_state;
                            }
                        }
                    } else {
                        let right_index = properties_names.iter().position(|n| n.eq(r)).unwrap();
                        for i in 0..properties_names.len() {
                            set_break_state(
                                &mut break_state_table,
                                properties_names.len(),
                                i,
                                right_index,
                                break_state,
                            );
                        }
                    }
                }
                continue;
            }
            println!("left={}", l);
            let left_index = properties_names.iter().position(|n| n.eq(l)).unwrap();
            for r in &rule.right {
                // Special case: right is Any
                if r == "Any" {
                    for i in 0..properties_names.len() {
                        set_break_state(
                            &mut break_state_table,
                            properties_names.len(),
                            left_index,
                            i,
                            break_state,
                        );
                    }
                    continue;
                }
                let right_index = properties_names.iter().position(|n| n.eq(r)).unwrap();
                set_break_state(
                    &mut break_state_table,
                    properties_names.len(),
                    left_index,
                    right_index,
                    break_state,
                );
            }
        }
    }

    let mut i = 1;
    for c in properties_names.iter() {
        println!("{} = {}", i, c);
        i += 1;
    }

    let out_dir = env::var("OUT_DIR").unwrap();
    let out = Path::new(&out_dir).join("generated_table.rs");
    let mut out = File::create(&out).unwrap();
    let mut i = 0;

    let mut page = 0;

    writeln!(out, "pub const BREAK_PROPERTIES_{}: [u8; 1024] = [", page);
    for c in properties_map.iter() {
        write!(out, "{: >2},", c);
        i += 1;

        if (i % 16) == 0 {
            writeln!(out, "");
        }

        if i > 1 && (i % 1024) == 0 {
            writeln!(out, "];");
            if i >= 0x10000 {
                break;
            }
            page += 1;
            writeln!(out, "pub const BREAK_PROPERTIES_{}: [u8; 1024] = [", page);
            continue;
        }
    }

    writeln!(out, "pub const PROPERTY_TABLE: [&[u8; 1024]; 8] = [");
    writeln!(out, "    &BREAK_PROPERTIES_0,");
    writeln!(out, "    &BREAK_PROPERTIES_1,");
    writeln!(out, "    &BREAK_PROPERTIES_2,");
    writeln!(out, "    &BREAK_PROPERTIES_3,");
    writeln!(out, "    &BREAK_PROPERTIES_4,");
    writeln!(out, "    &BREAK_PROPERTIES_5,");
    writeln!(out, "    &BREAK_PROPERTIES_6,");
    writeln!(out, "    &BREAK_PROPERTIES_7,");
    writeln!(out, "];");

    writeln!(
        out,
        "pub const BREAK_STATE_MACHINE_TABLE: [i8; {}] = [",
        rule_size
    );
    let mut i = 1;
    writeln!(out, "// {}", properties_names[i - 1]);
    for c in break_state_table.iter() {
        write!(out, "{: >4},", c);
        i += 1;
        if (i % properties_names.len()) == 0 {
            writeln!(out, "");
            if (i / properties_names.len()) < properties_names.len() {
                writeln!(out, "// {}", properties_names[i / properties_names.len()]);
            }
        }
    }
    writeln!(out, "];");

    writeln!(
        out,
        "pub const PROP_COUNT: usize = {};",
        properties_names.len()
    );

    let mut i = 1;
    for p in properties_names.iter() {
        writeln!(out, "// {} = {}", p, i);
        i += 1;
    }

    writeln!(out, "");
    writeln!(out, "#[allow(dead_code)]");
    writeln!(out, "pub const BREAK_RULE: i8 = -128;");
    writeln!(out, "pub const PREVIOUS_BREAK_RULE: i8 = -2;");
    writeln!(out, "pub const KEEP_RULE: i8 = -1;");
}
