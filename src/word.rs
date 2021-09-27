use core::str::CharIndices;

use crate::break_iterator_impl;
use crate::rule_segmenter::*;
use crate::utils::{Latin1Indices, Utf16Indices};

include!(concat!(env!("OUT_DIR"), "/generated_word_table.rs"));

// UTF-8 version of rule based break iterator.
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
            property_table: &PROPERTY_TABLE,
            rule_property_count: PROPERTY_COUNT,
            last_codepoint_property: LAST_CODEPOINT_PROPERTY,
            sot_property: PROP_SOT as u8,
            eot_property: PROP_EOT as u8,
        }
    }

    fn get_break_property(&mut self) -> u8 {
        get_break_property_utf8(self.current_pos_data.unwrap().1, self.property_table)
    }
}

// Latin-1 version of rule based break iterator.
break_iterator_impl!(WordBreakIteratorLatin1, Latin1Indices<'a>, u8);

impl<'a> WordBreakIteratorLatin1<'a> {
    /// Create line break iterator using Latin-1/8-bit string.
    pub fn new(input: &[u8]) -> WordBreakIteratorLatin1 {
        WordBreakIteratorLatin1 {
            iter: Latin1Indices::new(input),
            len: input.len(),
            current_pos_data: None,
            result_cache: Vec::new(),
            break_state_table: &BREAK_STATE_MACHINE_TABLE,
            property_table: &PROPERTY_TABLE,
            rule_property_count: PROPERTY_COUNT,
            last_codepoint_property: LAST_CODEPOINT_PROPERTY,
            sot_property: PROP_SOT as u8,
            eot_property: PROP_EOT as u8,
        }
    }

    #[inline]
    fn get_break_property(&mut self) -> u8 {
        get_break_property_latin1(self.current_pos_data.unwrap().1, self.property_table)
    }
}

// UTF-16 version of break iterator.
break_iterator_impl!(WordBreakIteratorUtf16, Utf16Indices<'a>, u32);

impl<'a> WordBreakIteratorUtf16<'a> {
    /// Create line break iterator using UTF-16 string.
    pub fn new(input: &[u16]) -> WordBreakIteratorUtf16 {
        WordBreakIteratorUtf16 {
            iter: Utf16Indices::new(input),
            len: input.len(),
            current_pos_data: None,
            result_cache: Vec::new(),
            break_state_table: &BREAK_STATE_MACHINE_TABLE,
            property_table: &PROPERTY_TABLE,
            rule_property_count: PROPERTY_COUNT,
            last_codepoint_property: LAST_CODEPOINT_PROPERTY,
            sot_property: PROP_SOT as u8,
            eot_property: PROP_EOT as u8,
        }
    }

    #[inline]
    fn get_break_property(&mut self) -> u8 {
        get_break_property_utf32(self.current_pos_data.unwrap().1, self.property_table)
    }
}
