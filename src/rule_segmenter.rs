use core::char;

pub const BREAK_RULE: i8 = -128;
pub const NOT_MATCH_RULE: i8 = -2;
pub const KEEP_RULE: i8 = -1;

pub fn get_break_property_utf32(codepoint: u32, property_table: &[&[u8; 1024]; 128]) -> u8 {
    let codepoint = codepoint as usize;
    if codepoint >= 0x20000 {
        // Unknown
        return 0;
    }
    property_table[codepoint / 1024][(codepoint & 0x3ff)]
}

#[inline]
pub fn get_break_property_latin1(codepoint: u8, property_table: &[&[u8; 1024]; 128]) -> u8 {
    let codepoint = codepoint as usize;
    property_table[codepoint / 1024][(codepoint & 0x3ff)]
}

#[inline]
pub fn get_break_property_utf8(codepoint: char, property_table: &[&[u8; 1024]; 128]) -> u8 {
    get_break_property_utf32(codepoint as u32, property_table)
}

#[macro_export]
macro_rules! break_iterator_impl {
    ($name:ident, $iter_attr:ty, $char_type:ty) => {
        #[allow(dead_code)]
        pub struct $name<'a> {
            iter: $iter_attr,
            len: usize,
            current_pos_data: Option<(usize, $char_type)>,
            result_cache: Vec<usize>,
            break_state_table: &'a [i8],
            property_table: &'a [&'a [u8; 1024]; 128],
            rule_property_count: usize,
            last_codepoint_property: i8,
            sot_property: u8,
            eot_property: u8,
        }

        impl<'a> Iterator for $name<'a> {
            type Item = usize;

            fn next(&mut self) -> Option<Self::Item> {
                if self.current_pos_data.is_none() {
                    self.current_pos_data = self.iter.next();
                    if self.current_pos_data.is_some() {
                        // SOT x anything
                        let right_prop = self.get_break_property();
                        if self.is_break_from_table(self.sot_property, right_prop) {
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
                        if self.get_break_state_from_table(left_prop, self.eot_property)
                            == NOT_MATCH_RULE
                        {}
                        return Some(self.len);
                    }
                    let right_prop = self.get_break_property();

                    // If break_state is equals or grater than 0, it is alias of property.
                    let mut break_state = self.get_break_state_from_table(left_prop, right_prop);

                    if break_state >= 0 as i8 {
                        // This isn't simple rule set. We need marker to restore iterator to previous position.
                        let mut previous_iter = self.iter.clone();
                        let mut previous_pos_data = self.current_pos_data;
                        println!("COMPLEX {}", self.current_pos_data.unwrap().0);

                        loop {
                            self.current_pos_data = self.iter.next();
                            if self.current_pos_data.is_none() {
                                // Reached EOF. But we are analyzing multiple characters now, so next break may be previous point.
                                if self.get_break_state_from_table(
                                    break_state as u8,
                                    self.eot_property as u8,
                                ) == NOT_MATCH_RULE
                                {
                                    self.iter = previous_iter;
                                    self.current_pos_data = previous_pos_data;
                                    return Some(previous_pos_data.unwrap().0);
                                }
                                // EOF
                                return Some(self.len);
                            }

                            let previous_break_state = break_state;
                            let prop = self.get_break_property();
                            break_state = self.get_break_state_from_table(break_state as u8, prop);
                            if break_state < 0 {
                                break;
                            }
                            if previous_break_state >= 0
                                && previous_break_state <= self.last_codepoint_property
                            {
                                // Move marker
                                previous_iter = self.iter.clone();
                                previous_pos_data = self.current_pos_data;
                            }
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

            fn get_break_state_from_table(&mut self, left: u8, right: u8) -> i8 {
                //println!("left={} right={}", left, right);
                //println!(
                //    "break={}",
                //    rule_table[(left as usize) * property_count + (right as usize)]
                //);
                self.break_state_table
                    [(left as usize) * self.rule_property_count + (right as usize)]
            }

            fn is_break_from_table(&self, left: u8, right: u8) -> bool {
                let rule = self.break_state_table
                    [(left as usize) * self.rule_property_count + (right as usize)];
                if rule == KEEP_RULE {
                    return false;
                }
                if rule >= 0 {
                    // need additional next characters to get break rule.
                    return false;
                }
                true
            }
        }
    };
}
