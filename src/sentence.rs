use core::str::CharIndices;

use crate::break_iterator_impl;
use crate::rule_segmenter::*;
use crate::utils::{Latin1Indices, Utf16Indices};

include!(concat!(env!("OUT_DIR"), "/generated_sentence_table.rs"));

// UTF-8 version of sentence break iterator.
break_iterator_impl!(SentenceBreakIterator, CharIndices<'a>, char);

impl<'a> SentenceBreakIterator<'a> {
    /// Create line break iterator
    pub fn new(input: &'a str) -> Self {
        Self {
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

// Latin-1 version of sentence break iterator.
break_iterator_impl!(SentenceBreakIteratorLatin1, Latin1Indices<'a>, u8);

impl<'a> SentenceBreakIteratorLatin1<'a> {
    /// Create break iterator using Latin-1/8-bit string.
    pub fn new(input: &'a [u8]) -> Self {
        Self {
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
break_iterator_impl!(SentenceBreakIteratorUtf16, Utf16Indices<'a>, u32);

impl<'a> SentenceBreakIteratorUtf16<'a> {
    /// Create line break iterator using UTF-16 string.
    pub fn new(input: &'a [u16]) -> Self {
        Self {
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
