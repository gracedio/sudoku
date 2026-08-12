import unittest

from sudoku import (
    SIZE,
    count_solutions,
    generate_full_board,
    generate_puzzle,
    is_valid,
    parse_board_string,
    solve,
)


def is_valid_solution(board):
    def is_group_valid(group):
        return sorted(group) == list(range(1, SIZE + 1))

    for row in board:
        if not is_group_valid(row):
            return False
    for col in range(SIZE):
        if not is_group_valid([board[row][col] for row in range(SIZE)]):
            return False
    for br in range(0, SIZE, 3):
        for bc in range(0, SIZE, 3):
            box = [board[r][c] for r in range(br, br + 3) for c in range(bc, bc + 3)]
            if not is_group_valid(box):
                return False
    return True


class SudokuTests(unittest.TestCase):
    def test_generate_full_board_is_valid(self):
        board = generate_full_board()
        self.assertTrue(is_valid_solution(board))

    def test_solve_easy_puzzle(self):
        puzzle_text = (
            "53..7...."
            "6..195..."
            ".98....6."
            "8...6...3"
            "4..8.3..1"
            "7...2...6"
            ".6....28."
            "...419..5"
            "....8..79"
        )
        board = parse_board_string(puzzle_text)
        self.assertTrue(solve(board))
        self.assertTrue(is_valid_solution(board))

    def test_unsolvable_puzzle(self):
        # Same as the easy puzzle above, but with a duplicated clue (two 5s
        # in row 0), which makes it unsolvable.
        puzzle_text = (
            "55..7...."
            "6..195..."
            ".98....6."
            "8...6...3"
            "4..8.3..1"
            "7...2...6"
            ".6....28."
            "...419..5"
            "....8..79"
        )
        board = parse_board_string(puzzle_text)
        self.assertFalse(solve(board))

    def test_generate_puzzle_has_unique_solution(self):
        puzzle, solution = generate_puzzle("easy")
        self.assertTrue(is_valid_solution(solution))
        self.assertEqual(count_solutions([row[:] for row in puzzle], limit=2), 1)
        clue_count = sum(1 for row in puzzle for v in row if v != 0)
        self.assertGreater(clue_count, 0)

    def test_is_valid(self):
        board = [[0] * SIZE for _ in range(SIZE)]
        board[0][0] = 5
        self.assertFalse(is_valid(board, 0, 3, 5))  # same row
        self.assertFalse(is_valid(board, 3, 0, 5))  # same column
        self.assertFalse(is_valid(board, 1, 1, 5))  # same box
        self.assertTrue(is_valid(board, 4, 4, 5))

    def test_parse_board_string_rejects_bad_length(self):
        with self.assertRaises(ValueError):
            parse_board_string("123")


if __name__ == "__main__":
    unittest.main()
