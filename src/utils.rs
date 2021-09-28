/// Similar to CharIndices for Latin-1 character
#[derive(Clone)]
pub struct Latin1Indices<'a> {
    front_offset: usize,
    iter: &'a [u8],
}

impl<'a> Latin1Indices<'a> {
    pub fn new(input: &'a [u8]) -> Self {
        Self {
            front_offset: 0,
            iter: input,
        }
    }
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

/// Similar to CharIndices for UTF-16 character
#[derive(Clone)]
pub struct Utf16Indices<'a> {
    front_offset: usize,
    iter: &'a [u16],
}

impl<'a> Utf16Indices<'a> {
    pub fn new(input: &'a [u16]) -> Self {
        Self {
            front_offset: 0,
            iter: input,
        }
    }
}

impl<'a> Iterator for Utf16Indices<'a> {
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
