use std::{f32::MAX_EXP, fmt, iter::Scan};

#[derive(Debug)]
enum ScanDirections {
    Horizontal,
    Vertical,
    ForwardDiagonal,
    BackwardDiagonal,
}

#[derive(Debug)]
struct Puzzle {
    puzzle: Vec<Vec<char>>,
    n_rows: usize,
    n_cols: usize,
    window_size: usize,
    scanned: bool,
    scanning_direction: ScanDirections,
    iter_idx: usize,
    row_counter: usize,
    col_counter: usize,
}

impl Puzzle {
    fn new(puzzle: Vec<Vec<char>>, window_size: usize) -> Self {
        let n_rows = puzzle.len();
        let n_cols = puzzle[0].len();
        let scanned = true;
        let scanning_direction = ScanDirections::Horizontal;
        let iter_idx = 0;
        let row_counter = 0;
        let col_counter = 0;
        

        Puzzle {
            puzzle,
            n_rows,
            n_cols,
            window_size,
            scanned,
            scanning_direction,
            iter_idx,
            row_counter,
            col_counter,
        }
    }

    fn next_horizontal_slice(&mut self) -> Option<String> {
        let end = self.iter_idx + self.window_size;
        if end <= self.n_cols {
            let range = self.iter_idx..end;
            let next_slice: String = self.puzzle[self.row_counter][range].iter().collect();
            self.iter_idx += 1;
            return Some(next_slice)
        } else if self.row_counter < self.n_rows - 1 {
            self.row_counter += 1;
        }
        else {
            self.scanning_direction = ScanDirections::Vertical;
        }
            self.iter_idx = 0;
            self.next()
    }

    fn next_vertical_slice(&mut self) -> Option<String> {
        let end = self.iter_idx + self.window_size;
        if end <= self.n_rows {
            let range = self.iter_idx..end;
            let next_slice: String = self.puzzle
                .iter()
                .map(|v| v[self.col_counter])
                .collect::<Vec<char>>()
                [range]
                .iter()
                .collect();
            self.iter_idx += 1;

            return Some(next_slice)
        } else if self.col_counter < self.n_cols - 1 {
            self.col_counter += 1;
        }
        else {
            self.scanning_direction = ScanDirections::ForwardDiagonal;
        }
        self.iter_idx = 0;
        self.next()
    }

    fn next_forward_diagonal_slice(&mut self) -> Option<String> {
        None
    }

    fn next_backward_diagonal_slice(&mut self) -> Option<String> {
        None
    }

}

impl Iterator for Puzzle {
    type Item = String;

    fn next(&mut self) -> Option<Self::Item> {
        if !self.scanned {
            None
        } else {
            match self.scanning_direction {
                ScanDirections::Horizontal => self.next_horizontal_slice(),
                ScanDirections::Vertical => self.next_vertical_slice(),
                ScanDirections::ForwardDiagonal => self.next_forward_diagonal_slice(),
                ScanDirections::BackwardDiagonal => self.next_backward_diagonal_slice(),
            }
        }
    }
}

impl fmt::Display for Puzzle {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "    ")?;
        for i in 0..self.n_cols {
            write!(f, "[{}] ", i)?;
        }
        writeln!(f)?;
        for (row_num, row) in self.puzzle.iter().enumerate() {
            write!(f, "[{}]  ", row_num)?;
            for col in row {
                write!(f, "{}   ", col)?;
            } 
            writeln!(f)?;
        }
        Ok(())
    }
}


fn scan(path: &str, size: usize) -> u32 {
    let file = std::fs::read_to_string(path).unwrap();
    let lines: Vec<Vec<char>> = file
        .lines()
        .map(|l| l.chars().collect())
        .collect();

    let mut puzzle = Puzzle::new(lines, size);
    println!("{}", puzzle);

    loop {
        if let Some(x) = puzzle.next() {
            println!("{}", x)
        } else {
            break    
        }

    }
    todo!()
}
fn main() {
    let path = "src/test.txt";
    let scanned = scan(path, 4);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_1() {
        let path = "src/test.txt";
        let scanned = scan(path, 4);
        assert_eq!(scanned, 18);
    }

    // #[test]
    // fn test_part_2() {
    //     let path = "src/test2.txt";
    //     let total = compute_toggled_total(path);
    //     assert_eq!(total, 48);
    // }
}
