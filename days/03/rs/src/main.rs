use std::i32;

use regex::Regex;

fn compute_total(path: &str) -> u32 {
    let stream = std::fs::read_to_string(path).unwrap();
    let re = Regex::new(r"mul\((\d{1,3}),(\d{1,3})\)").unwrap();
    let matches: Vec<(u32, u32)> = re.captures_iter(&stream)
        .map(|c| {
            let (_, [a, b]) = c.extract::<2>();
            (a.parse::<u32>().unwrap(), b.parse::<u32>().unwrap())
        }).collect();

    matches
        .iter()
        .map(|(a, b)| a * b)
        .sum()
}

fn exec_mul(m: &str) -> i32 {
    let re = Regex::new(r"\d{1,3}").unwrap();
    let matches: Vec<i32> = re.find_iter(&m)
        .map(|c| c.as_str().parse::<i32>().unwrap())
        .collect();
    
    matches[0] * matches[1]
}

fn compute_toggled_total(path: &str) -> i32 {
    let stream = std::fs::read_to_string(path).unwrap();
    let re = Regex::new(r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don\'t\(\)").unwrap();

    let mut total = 0;
    let mut enabled = true;
    stream.lines()
        .for_each(|l| {
            let matches: Vec<_> = re.find_iter(&l)
                .map(|c| c.as_str()).collect();

            for m in matches {
                match m {
                    "do()" => { enabled = true; },
                    "don't()" => { enabled = false; },
                    _ => { if enabled { 
                        total += exec_mul(m);
                    } }
                }
            }
        });

    total
}

fn main() {
    // part 1
    let path = "src/part1.txt";
    let total = compute_total(path);
    println!("Total {}", total);

    // part 2
    let path = "src/part1.txt";
    let total = compute_toggled_total(path);
    println!("Total {}", total);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_1() {
        let path = "src/test.txt";
        let total = compute_total(path);
        assert_eq!(total, 161);
    }

    #[test]
    fn test_part_2() {
        let path = "src/test2.txt";
        let total = compute_toggled_total(path);
        assert_eq!(total, 48);
    }
}
