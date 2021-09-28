mod grapheme;
mod rule_segmenter;
mod sentence;
mod utils;
mod word;

pub use crate::grapheme::{
    GraphemeBreakIterator, GraphemeBreakIteratorLatin1, GraphemeBreakIteratorUtf16,
};
pub use crate::sentence::{SentenceBreakIterator, SentenceBreakIteratorLatin1, SentenceBreakIteratorUtf16};
pub use crate::word::{WordBreakIterator, WordBreakIteratorLatin1, WordBreakIteratorUtf16};

#[cfg(test)]
mod tests {
    use crate::WordBreakIterator;
    use crate::WordBreakIteratorLatin1;

    #[test]
    fn rule_break() {
        let s = "\u{0001}\u{00ad}";
        let mut iter = WordBreakIterator::new(&s);
        assert_eq!(Some(0), iter.next());
        assert_eq!(Some(3), iter.next());

        let input: [u8; 3] = [0x5F, 0x31, 0x3A];
        let mut iter = WordBreakIteratorLatin1::new(&input);
        assert_eq!(Some(0), iter.next());
        assert_eq!(Some(2), iter.next());
        assert_eq!(Some(3), iter.next());

        let input: [u8; 3] = [0x61, 0x3a, 0x61];
        let mut iter = WordBreakIteratorLatin1::new(&input);
        assert_eq!(Some(0), iter.next());
        assert_eq!(Some(3), iter.next());

        let input: [u8; 2] = [0x61, 0x3a];
        let mut iter = WordBreakIteratorLatin1::new(&input);
        assert_eq!(Some(0), iter.next());
        assert_eq!(Some(1), iter.next());
        assert_eq!(Some(2), iter.next());

        let input: [u8; 2] = [13, 10];
        let mut iter = WordBreakIteratorLatin1::new(&input);
        assert_eq!(Some(0), iter.next());
        assert_eq!(Some(2), iter.next());

        let input: [u8; 5] = [0x41, 0x41, 0x20, 0x41, 0x41];
        let mut iter = WordBreakIteratorLatin1::new(&input);
        assert_eq!(Some(0), iter.next());
        assert_eq!(Some(2), iter.next());
        assert_eq!(Some(3), iter.next());

        let input: [u8; 5] = [0x30, 0x31, 0x32, 0x33, 0x34];
        let mut iter = WordBreakIteratorLatin1::new(&input);
        assert_eq!(Some(0), iter.next());
        assert_eq!(Some(5), iter.next());

        let input: [u8; 2] = [0x01, 0x1];
        let mut iter = WordBreakIteratorLatin1::new(&input);
        assert_eq!(Some(0), iter.next());
        assert_eq!(Some(1), iter.next());
    }
}
