use rule_segmenter::{
    SentenceBreakIterator, SentenceBreakIteratorLatin1, SentenceBreakIteratorUtf16,
};
use std::char;
use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;
use std::u32;

#[test]
fn run_sentence_break_test() {
    // no failed tests
    let failed = [
        //"\u{0028}\u{0022}\u{0047}\u{006F}\u{002E}\u{0022}\u{0029}\u{0020}\u{0028}\u{0048}\u{0065}\u{0020}\u{0064}\u{0069}\u{0064}\u{002E}\u{0029}",
        //"\u{0028}\u{201C}\u{0047}\u{006F}\u{003F}\u{201D}\u{0029}\u{0020}\u{0028}\u{0048}\u{0065}\u{0020}\u{0064}\u{0069}\u{0064}\u{002E}\u{0029}",
        //"\u{0065}\u{0074}\u{0063}\u{002E}\u{0029}\u{2019}\u{0308}\u{0054}\u{0068}\u{0065}",
        //"\u{0065}\u{0074}\u{0063}\u{002E}\u{0029}\u{2019}\u{00A0}\u{2018}\u{0028}\u{0054}\u{0068}\u{0065}",
        //"\u{0065}\u{0074}\u{0063}\u{002E}\u{0029}\u{000A}\u{0308}\u{0054}\u{0068}\u{0065}",
        //"\u{2060}\u{0028}\u{2060}\u{0022}\u{2060}\u{0047}\u{2060}\u{006F}\u{2060}\u{002E}\u{2060}\u{0022}\u{2060}\u{0029}\u{2060}\u{0020}\u{2060}\u{0028}\u{2060}\u{0048}\u{2060}\u{0065}\u{2060}\u{0020}\u{2060}\u{0064}\u{2060}\u{0069}\u{2060}\u{0064}\u{2060}\u{002E}\u{2060}\u{0029}\u{2060}\u{2060}",
        //"\u{2060}\u{0028}\u{2060}\u{201C}\u{2060}\u{0047}\u{2060}\u{006F}\u{2060}\u{003F}\u{2060}\u{201D}\u{2060}\u{0029}\u{2060}\u{0020}\u{2060}\u{0028}\u{2060}\u{0048}\u{2060}\u{0065}\u{2060}\u{0020}\u{2060}\u{0064}\u{2060}\u{0069}\u{2060}\u{0064}\u{2060}\u{002E}\u{2060}\u{0029}\u{2060}\u{2060}",
        //"\u{2060}\u{0065}\u{2060}\u{0074}\u{2060}\u{0063}\u{2060}\u{002E}\u{2060}\u{0029}\u{2060}\u{2019}\u{2060}\u{00A0}\u{2060}\u{2018}\u{2060}\u{0028}\u{2060}\u{0074}\u{2060}\u{0068}\u{2060}\u{0065}\u{2060}\u{2060}",
        //"\u{2060}\u{0065}\u{2060}\u{0074}\u{2060}\u{0063}\u{2060}\u{002E}\u{2060}\u{0029}\u{2060}\u{2019}\u{2060}\u{00A0}\u{2060}\u{2018}\u{2060}\u{0028}\u{2060}\u{0054}\u{2060}\u{0068}\u{2060}\u{0065}\u{2060}\u{2060}",
        //"\u{2060}\u{0065}\u{2060}\u{0074}\u{2060}\u{0063}\u{2060}\u{002E}\u{2060}\u{0029}\u{2060}\u{2019}\u{2060}\u{0308}\u{0054}\u{2060}\u{0068}\u{2060}\u{0065}\u{2060}\u{2060}",
        //"\u{0065}\u{0074}\u{0063}\u{002E}\u{0029}\u{000A}\u{0308}\u{0054}\u{0068}\u{0065}",
        //"\u{2060}\u{0065}\u{2060}\u{0074}\u{2060}\u{0063}\u{2060}\u{002E}\u{2060}\u{0029}\u{2060}\u{000A}\u{2060}\u{0308}\u{2060}\u{0054}\u{2060}\u{0068}\u{2060}\u{0065}\u{2060}\u{2060}",
        "\u{0065}\u{0074}\u{0063}\u{002E}\u{0029}\u{2019}\u{00A0}\u{2018}\u{0028}\u{0074}\u{0068}\u{0065}",
        "\u{2060}\u{0065}\u{2060}\u{0074}\u{2060}\u{0063}\u{2060}\u{002E}\u{2060}\u{0029}\u{2060}\u{2019}\u{2060}\u{00A0}\u{2060}\u{2018}\u{2060}\u{0028}\u{2060}\u{0074}\u{2060}\u{0068}\u{2060}\u{0065}\u{2060}\u{2060}",
    ];

    let f = File::open("tests/SentenceBreakTest.txt");
    let f = BufReader::new(f.unwrap());
    for line in f.lines() {
        let line = line.unwrap();
        if line.starts_with("#") {
            continue;
        }
        let mut r = line.split("#");
        let r = r.next();
        let v: Vec<_> = r.unwrap().split_ascii_whitespace().collect();
        let mut char_break: Vec<_> = Vec::new();
        let mut u8_break: Vec<_> = Vec::new();
        let mut u16_break: Vec<_> = Vec::new();
        let mut char_vec: Vec<_> = Vec::new();
        let mut u8_vec: Vec<_> = Vec::new();
        let mut u16_vec: Vec<_> = Vec::new();
        let mut count = 0;

        let mut char_len = 0;
        let mut u8_len = 0;
        let mut u16_len = 0;

        let mut ascii_only = true;
        loop {
            if count >= v.len() {
                break;
            }
            if count % 2 == 1 {
                let ch = char::from_u32(u32::from_str_radix(v[count], 16).unwrap()).unwrap();
                char_vec.push(ch);
                char_len = char_len + ch.len_utf8();

                if ch as u32 >= 0x100 {
                    ascii_only = false;
                } else {
                    u8_vec.push(ch as u8);
                    u8_len = u8_len + 1;
                }

                if ch as u32 >= 0x10000 {
                    u16_vec.push((((ch as u32 - 0x10000) >> 10) | 0xd800) as u16);
                    u16_vec.push((((ch as u32) & 0x3ff) | 0xdc00) as u16);
                    u16_len = u16_len + 2;
                } else {
                    u16_vec.push(ch as u16);
                    u16_len = u16_len + 1;
                }
            } else {
                if v[count] != "\u{00d7}" {
                    assert_eq!(v[count], "\u{00f7}");
                    char_break.push(char_len);
                    u8_break.push(u8_len);
                    u16_break.push(u16_len);
                }
            }
            count = count + 1
        }
        let s: String = char_vec.into_iter().collect();
        let mut iter = SentenceBreakIterator::new(&s);
        if failed.contains(&&s.as_str()) {
            println!("Skip: {}", line);
            let result: Vec<usize> = iter.map(|x| x).collect();
            assert_ne!(result, char_break, "{}", line);
            continue;
        }

        {
            println!("UTF8: {}", line);
            let result: Vec<usize> = iter.map(|x| x).collect();
            assert_eq!(result, char_break, "{}", line);
        }

        {
            println!("UTF16: {}", line);
            let iter = SentenceBreakIteratorUtf16::new(&u16_vec);
            let result: Vec<usize> = iter.map(|x| x).collect();
            assert_eq!(result, u16_break, "UTF16: {}", line);
        }

        if ascii_only {
            println!("Latin1: {}", line);
            let iter = SentenceBreakIteratorLatin1::new(&u8_vec);
            let result: Vec<usize> = iter.map(|x| x).collect();
            assert_eq!(result, u8_break, "Latin1: {}", line);
        }
    }
}
