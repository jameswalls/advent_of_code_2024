use core::panic;
use std::iter::zip;
use std::collections::HashMap;

#[derive(Debug)]
struct Counter {
    counts: HashMap<i32, i32>
}

impl Counter {
    fn new(numbers: Vec<i32>) -> Counter {
        let mut counts: HashMap<i32, i32> = HashMap::new();

        numbers.iter()
            .for_each(|&i| {
                counts.entry(i).and_modify(|count| *count += 1).or_insert(1);
            });

        Counter { counts }
    }

    fn get(&self, key: &i32) -> i32 {
        *self.counts.get(key).unwrap_or(&0)
    }
}

fn load_data(path: &str) -> String {
    match std::fs::read_to_string(path) {
        Ok(content) => content,
        Err(e) => panic!("Error: {}", e),
    }
}

fn get_vecs(lines: String, sorted: bool) -> (Vec<i32>, Vec<i32>) {
    let (mut left, mut right): (Vec<i32>, Vec<i32>) = lines.lines()
                                .map(|line| {
                                    let [left, right] = line.split_whitespace()
                                        .map(|x| x.parse().unwrap())
                                        .collect::<Vec<i32>>()[..2] else { panic!() };
                                    (left, right)
                                })
    .unzip();
    if sorted {
        left.sort();
        right.sort();
    }

    (left, right)
}

fn total_difference(left: Vec<i32>, right: Vec<i32>) -> i32 {
    zip(left, right)
        .map(|(l, r)| (l - r).abs())
        .sum()
}

fn similarity_score(left: Vec<i32>, right: Vec<i32>) -> i32 {
    let counter = Counter::new(right);

    left.iter()
        .map(|l| l * counter.get(l))
        .sum()
}

fn main() {
    // part 1
    let lines = load_data("src/input_1.txt");
    let (left, right) = get_vecs(lines, true);
    let total_difference = total_difference(left, right);
    println!("part 1 - total difference: {}", total_difference);

    // part 2
    let lines = load_data("src/input_1.txt");
    let (left, right) = get_vecs(lines, false);
    let score = similarity_score(left, right);
    println!("part 2 - similarity scroe: {}", score);

}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_1() {
        let lines = load_data("src/test_input.txt");
        let (left, right) = get_vecs(lines, true);
        let total_difference = total_difference(left, right);
        assert_eq!(total_difference, 11);
    }

    #[test]
    fn test_part_2() {
        let lines = load_data("src/test_input.txt");
        let (left, right) = get_vecs(lines, false);
        let total_difference = similarity_score(left, right);
        assert_eq!(total_difference, 31);
    }
}
