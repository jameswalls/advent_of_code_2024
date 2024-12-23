use std::iter::zip;

fn safe_reports(path: &str) -> i32 {
    let file = std::fs::read_to_string(path).unwrap();
    let reports: Vec<Vec<i32>> = file.lines()
        .map(|l| {
            l.split(' ').map(|i| i.parse().unwrap()).collect()
        })
        .collect();

    reports.iter()
        .map(|r| {
            let len = r.len();
            let slice1 = &r[1..len];
            let slice2 = &r[..len-1];
            let differences: Vec<i32> = zip(slice2, slice1).map(|(x, y)| y - x).collect();

            let all_increasing = differences.iter().all(|&i| i > 0);
            let all_decreasing = differences.iter().all(|&i| i < 0);
            let between_one_and_three = differences.iter().all(|i| 1<=i.abs() && i.abs()<=3);

            ((all_increasing || all_decreasing) && between_one_and_three) as i32
        })
        .sum()
}

fn load_reports(path: &str) -> Vec<Vec<i32>> {
    let file = std::fs::read_to_string(path).unwrap();
    file.lines()
        .map(|l| {
            l.split(' ').map(|i| i.parse().unwrap()).collect()
        })
        .collect()
}

fn check_conditions(report: &Vec<i32>) -> bool {
    let len = report.len();
    let slice1 = &report[1..len];
    let slice2 = &report[..len-1];
    let differences: Vec<i32> = zip(slice2, slice1).map(|(x, y)| y - x).collect();

    let all_increasing = differences.iter().all(|&i| i > 0);
    let all_decreasing = differences.iter().all(|&i| i < 0);
    let between_one_and_three = differences.iter().all(|i| 1<=i.abs() && i.abs()<=3);

    (all_increasing || all_decreasing) && between_one_and_three
}

fn is_safe_with_removal(report: &Vec<i32>, i: usize) -> bool {
    if i == report.len() {
        false
    } else {
        let sub_report = [&report[..i], &report[i+1..]].concat();
        check_conditions(&sub_report) || is_safe_with_removal(&report, i+1)
    }

}

fn is_safe_report(report: &Vec<i32>) -> i32 {
    (check_conditions(&report) || is_safe_with_removal(&report, 0)) as i32
}

fn main() {
    let path = "src/part_1.txt";

    let reports = safe_reports(path);
    println!("part 1: {}", reports);

    let reports = load_reports(path);
    let total_safe_reports: i32 = reports.iter().map(is_safe_report).sum();
    println!("part 2: {}", total_safe_reports);
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_1() {
        let path = "src/test.txt";
        let reports = safe_reports(path);
        assert_eq!(reports, 2);
    }

    #[test]
    fn test_part_2() {
        let path = "src/test.txt";
        let reports = load_reports(path);
        let total_safe_reports: i32 = reports.iter().map(is_safe_report).sum();
        assert_eq!(total_safe_reports, 4);
    }
}
