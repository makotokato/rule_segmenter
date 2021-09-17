use core::char;
use core::str::CharIndices;

include!(concat!(env!("OUT_DIR"), "/generated_table.rs"));

fn get_break_property_utf32(codepoint: u32) -> u8 {
    let codepoint = codepoint as usize;
    if codepoint >= 0x20000 {
        panic!("Unspoorted");
    }
    PROPERTY_TABLE[codepoint / 1024][(codepoint & 0x3ff)]
}

#[inline]
fn get_break_property_latin1(codepoint: u8) -> u8 {
    let codepoint = codepoint as usize;
    PROPERTY_TABLE[codepoint / 1024][(codepoint & 0x3ff)]
}

#[inline]
fn get_break_property_utf8(codepoint: char) -> u8 {
    get_break_property_utf32(codepoint as u32)
}

#[inline]
fn is_break_from_table(rule_table: &[i8], property_count: usize, left: u8, right: u8) -> bool {
    let rule = rule_table[((left as usize)) * property_count + (right as usize)];
    if rule == KEEP_RULE {
        return false;
    }
    if rule >= 0 {
        // need additional next characters to get break rule.
        return false;
    }
    true
}

#[inline]
fn get_break_state_from_table(rule_table: &[i8], property_count: usize, left: u8, right: u8) -> i8 {
    println!("left={} right={}", left, right);
    println!(
        "break={}",
        rule_table[((left as usize)) * property_count + (right as usize)]
    );
    rule_table[((left as usize)) * property_count + (right as usize)]
}

macro_rules! break_iterator_impl {
    ($name:ident, $iter_attr:ty, $char_type:ty) => {
        #[allow(dead_code)]
        pub struct $name<'a> {
            iter: $iter_attr,
            len: usize,
            current_pos_data: Option<(usize, $char_type)>,
            result_cache: Vec<usize>,
            break_state_table: &'a [i8],
            rule_property_count: usize,
        }

        impl<'a> Iterator for $name<'a> {
            type Item = usize;

            fn next(&mut self) -> Option<Self::Item> {
                if self.current_pos_data.is_none() {
                    self.current_pos_data = self.iter.next();
                    if self.current_pos_data.is_some() {
                        // SOT x anything
                        let right_prop = self.get_break_property();
                        if self.is_break_from_table(PROP_SOT as u8, right_prop) {
                            return Some(self.current_pos_data.unwrap().0);
                        }
                    }
                }

                if self.is_eof() {
                    return None;
                }

                loop {
                    let left_prop = self.get_break_property();
                    //let left_codepoint = self.current_pos_data;
                    self.current_pos_data = self.iter.next();

                    if self.current_pos_data.is_none() {
                        // EOF
                        if get_break_state_from_table(
                            &self.break_state_table,
                            self.rule_property_count,
                            left_prop,
                            PROP_EOT as u8,
                        ) == NOT_MATCH_RULE
                        {}
                        return Some(self.len);
                    }
                    let right_prop = self.get_break_property();

                    // If break_state is equals or grater than 0, it is alias of property.
                    let mut break_state = get_break_state_from_table(
                        &self.break_state_table,
                        self.rule_property_count,
                        left_prop,
                        right_prop,
                    );

                    if break_state >= 0 as i8 {
                        // This isn't simple rule set.
                        let mut previous_iter = self.iter.clone();
                        let mut previous_pos_data = self.current_pos_data;
                        println!("COMPLEX {}", self.current_pos_data.unwrap().0);

                        loop {
                            self.current_pos_data = self.iter.next();
                            if self.current_pos_data.is_none() {
                                // Reached EOF. But we are analyzing multiple characters now, so next break may be previous point.
                                if get_break_state_from_table(
                                    &self.break_state_table,
                                    self.rule_property_count,
                                    break_state as u8,
                                    PROP_EOT as u8,
                                ) == NOT_MATCH_RULE
                                {
                                    self.iter = previous_iter;
                                    self.current_pos_data = previous_pos_data;
                                    return Some(previous_pos_data.unwrap().0);
                                }
                                // EOF
                                return Some(self.len);
                            }

                            let prop = self.get_break_property();
                            break_state = get_break_state_from_table(
                                &self.break_state_table,
                                self.rule_property_count,
                                break_state as u8,
                                prop,
                            );
                            if break_state < 0 {
                                break;
                            }

                            //previous_iter = self.iter.clone();
                            //previous_pos_data = self.current_pos_data;
                        }
                        if break_state == KEEP_RULE {
                            continue;
                        }
                        if break_state == NOT_MATCH_RULE {
                            self.iter = previous_iter;
                            self.current_pos_data = previous_pos_data;
                            println!("NOT_MATCH {}", previous_pos_data.unwrap().0);
                            return Some(previous_pos_data.unwrap().0);
                        }
                        return Some(self.current_pos_data.unwrap().0);
                    }

                    if break_state == NOT_MATCH_RULE {
                        // TODO
                    }

                    if self.is_break_from_table(left_prop, right_prop) {
                        return Some(self.current_pos_data.unwrap().0);
                    }
                }
            }
        }

        impl<'a> $name<'a> {
            #[inline]
            fn is_eof(&mut self) -> bool {
                if self.current_pos_data.is_none() {
                    self.current_pos_data = self.iter.next();
                    if self.current_pos_data.is_none() {
                        return true;
                    }
                }
                return false;
            }
        }
    };
}

break_iterator_impl!(WordBreakIterator, CharIndices<'a>, char);

impl<'a> WordBreakIterator<'a> {
    /// Create line break iterator
    pub fn new(input: &str) -> WordBreakIterator {
        WordBreakIterator {
            iter: input.char_indices(),
            len: input.len(),
            current_pos_data: None,
            result_cache: Vec::new(),
            break_state_table: &BREAK_STATE_MACHINE_TABLE,
            rule_property_count: PROP_COUNT,
        }
    }

    fn get_break_property(&mut self) -> u8 {
        self.get_break_property_with_rule(self.current_pos_data.unwrap().1)
    }

    fn get_break_property_with_rule(&mut self, c: char) -> u8 {
        get_break_property_utf8(c)
    }

    #[inline]
    fn is_break_from_table(&self, left: u8, right: u8) -> bool {
        is_break_from_table(
            &self.break_state_table,
            self.rule_property_count,
            left,
            right,
        )
    }
}

/// Latin-1 version of line break iterator.
#[derive(Clone)]
struct Latin1Indices<'a> {
    front_offset: usize,
    iter: &'a [u8],
}

impl<'a> Iterator for Latin1Indices<'a> {
    type Item = (usize, u8);

    #[inline]
    fn next(&mut self) -> Option<(usize, u8)> {
        if self.front_offset >= self.iter.len() {
            return None;
        }
        let ch = self.iter[self.front_offset];
        let index = self.front_offset;
        self.front_offset += 1;
        Some((index, ch))
    }
}

break_iterator_impl!(WordBreakIteratorLatin1, Latin1Indices<'a>, u8);

impl<'a> WordBreakIteratorLatin1<'a> {
    /// Create line break iterator using Latin-1/8-bit string.
    pub fn new(input: &[u8]) -> WordBreakIteratorLatin1 {
        WordBreakIteratorLatin1 {
            iter: Latin1Indices {
                front_offset: 0,
                iter: input,
            },
            len: input.len(),
            current_pos_data: None,
            result_cache: Vec::new(),
            break_state_table: &BREAK_STATE_MACHINE_TABLE,
            rule_property_count: PROP_COUNT,
        }
    }

    #[inline]
    fn get_break_property(&mut self) -> u8 {
        self.get_break_property_with_rule(self.current_pos_data.unwrap().1)
    }

    #[inline]
    fn get_break_property_with_rule(&mut self, c: u8) -> u8 {
        get_break_property_latin1(c)
    }

    #[inline]
    fn is_break_from_table(&self, left: u8, right: u8) -> bool {
        is_break_from_table(
            &self.break_state_table,
            self.rule_property_count,
            left,
            right,
        )
    }
}

/*
/// UTF-16 version of line break iterator.
#[derive(Clone)]
struct UTF16Indices<'a> {
    front_offset: usize,
    iter: &'a [u16],
}

impl<'a> Iterator for UTF16Indices<'a> {
    type Item = (usize, u32);

    #[inline]
    fn next(&mut self) -> Option<(usize, u32)> {
        if self.front_offset >= self.iter.len() {
            return None;
        }
        let ch = self.iter[self.front_offset];
        let index = self.front_offset;
        self.front_offset += 1;

        if (ch & 0xfc00) != 0xd800 {
            return Some((index, ch as u32));
        }

        let mut ch = ch as u32;
        if self.front_offset < self.iter.len() {
            let next = self.iter[self.front_offset] as u32;
            if (next & 0xfc00) == 0xdc00 {
                ch = ((ch & 0x3ff) << 10) + (next & 0x3ff) + 0x10000;
                self.front_offset += 1;
                return Some((index, ch));
            }
        }
        Some((index, ch))
    }
}

break_iterator_impl!(LineBreakIteratorUTF16, UTF16Indices<'a>, u32);

impl<'a> LineBreakIteratorUTF16<'a> {
    /// Create line break iterator using UTF-16 string.
    pub fn new(input: &[u16]) -> LineBreakIteratorUTF16 {
        LineBreakIteratorUTF16 {
            iter: UTF16Indices {
                front_offset: 0,
                iter: input,
            },
            len: input.len(),
            current_pos_data: None,
            result_cache: Vec::new(),
            break_rule: LineBreakRule::Strict,
            word_break_rule: WordBreakRule::Normal,
            ja_zh: false,
        }
    }

    /// Create line break iterator with CSS rules using UTF-16 string.
    pub fn new_with_break_rule(
        input: &[u16],
        line_break_rule: LineBreakRule,
        word_break_rule: WordBreakRule,
        ja_zh: bool,
    ) -> LineBreakIteratorUTF16 {
        LineBreakIteratorUTF16 {
            iter: UTF16Indices {
                front_offset: 0,
                iter: input,
            },
            len: input.len(),
            current_pos_data: None,
            result_cache: Vec::new(),
            break_rule: line_break_rule,
            word_break_rule,
            ja_zh,
        }
    }

    fn get_linebreak_property(&mut self) -> u8 {
        self.get_linebreak_property_with_rule(self.current_pos_data.unwrap().1)
    }

    fn get_linebreak_property_with_rule(&mut self, c: u32) -> u8 {
        get_linebreak_property_utf32_with_rule(c, self.break_rule, self.word_break_rule, self.ja_zh)
    }

    fn is_break_by_normal(&mut self) -> bool {
        is_break_utf32_by_normal(self.current_pos_data.unwrap().1 as u32, self.ja_zh)
    }

    #[inline]
    fn use_complex_breaking(c: u32) -> bool {
        use_complex_breaking_utf32(c)
    }

    fn get_line_break_by_platform_fallback(&mut self, input: &[u16]) -> Vec<usize> {
        if let Some(mut ret) = get_line_break_utf16(input) {
            ret.push(input.len());
            return ret;
        }
        [input.len()].to_vec()
    }
}
*/
