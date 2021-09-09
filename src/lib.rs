mod rule_segmenter;

pub use crate::rule_segmenter::*;

#[cfg(test)]
mod tests {
    use crate::WordBreakIteratorLatin1;

    #[test]
    fn rule_break() {
        let input: [u8; 2] = [13, 10];
        let mut iter = WordBreakIteratorLatin1::new(&input);
        assert_eq!(Some(2), iter.next());

        let input: [u8; 5] = [0x41, 0x41, 0x20, 0x41, 0x41];
        let mut iter = WordBreakIteratorLatin1::new(&input);
        assert_eq!(Some(2), iter.next());
        assert_eq!(Some(3), iter.next());

        let input: [u8; 5] = [0x30, 0x31, 0x32, 0x33, 0x34];
        let mut iter = WordBreakIteratorLatin1::new(&input);
        assert_eq!(Some(5), iter.next());
    }
}
