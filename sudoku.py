import argparse
import copy
import random
import sys

SIZE = 9
BOX = 3

DIFFICULTIES = {
    "easy": 40,
    "medium": 32,
    "hard": 28,
    "expert": 24,
}


def is_valid(board, row, col, value):
    if any(board[row][c] == value for c in range(SIZE)):
        return False
    if any(board[r][col] == value for r in range(SIZE)):
        return False
    box_row, box_col = BOX * (row // BOX), BOX * (col // BOX)
    for r in range(box_row, box_row + BOX):
        for c in range(box_col, box_col + BOX):
            if board[r][c] == value:
                return False
    return True


def find_best_empty(board):
    """Find the empty cell with the fewest legal candidates (MRV heuristic).
    Keeps backtracking fast on sparse boards. Returns (row, col, candidates)
    or None if the board is full."""
    best = None
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] != 0:
                continue
            candidates = [v for v in range(1, SIZE + 1) if is_valid(board, r, c, v)]
            if best is None or len(candidates) < len(best[2]):
                best = (r, c, candidates)
                if len(candidates) <= 1:
                    return best
    return best


def solve(board, randomize=False):
    """Fill board in place with the first solution found via backtracking.
    Returns True if solved."""
    best = find_best_empty(board)
    if best is None:
        return True
    row, col, candidates = best
    if randomize:
        random.shuffle(candidates)
    for value in candidates:
        board[row][col] = value
        if solve(board, randomize):
            return True
        board[row][col] = 0
    return False


def count_solutions(board, limit=2):
    """Count solutions up to `limit` (stops early once limit is reached)."""
    best = find_best_empty(board)
    if best is None:
        return 1
    row, col, candidates = best
    total = 0
    for value in candidates:
        board[row][col] = value
        total += count_solutions(board, limit - total)
        board[row][col] = 0
        if total >= limit:
            break
    return total


def generate_full_board():
    board = [[0] * SIZE for _ in range(SIZE)]
    solve(board, randomize=True)
    return board

def generate_puzzle(difficulty="medium"):
    """Return (puzzle, solution) with `clues` cells filled, unique solution."""
    clues = DIFFICULTIES.get(difficulty, DIFFICULTIES["medium"])
    solution = generate_full_board()
    puzzle = copy.deepcopy(solution)

    cells = [(r, c) for r in range(SIZE) for c in range(SIZE)]
    random.shuffle(cells)

    removable = SIZE * SIZE - clues
    removed = 0    
    for row, col in cells:
        if removed >= removable:
            break
        backup = puzzle[row][col]
        if backup == 0:
            continue
        puzzle[row][col] = 0
        board_copy = copy.deepcopy(puzzle)
        if count_solutions(board_copy, limit=2) != 1:
            puzzle[row][col] = backup
        else:
            removed += 1

    return puzzle, solution


def parse_board_string(text):
    """Parse an 81-char string (0 or . for blanks) into a 9x9 board."""
    digits = [ch for ch in text if ch.isdigit() or ch == "."]
    if len(digits) != SIZE * SIZE:
        raise ValueError("Expected 81 cells, got %d" % len(digits))
    board = []
    for r in range(SIZE):
        row = []
        for c in range(SIZE):
            ch = digits[r * SIZE + c]
            row.append(0 if ch == "." else int(ch))
        board.append(row)
    return board


def format_row(row):
    cells = []
    for i, value in enumerate(row):
        cells.append(str(value) if value != 0 else ".")
        if i % BOX == BOX - 1 and i != SIZE - 1:
            cells.append("|")
    return " ".join(cells)


def print_board(board):
    sep = "-" * 21
    for r, row in enumerate(board):
        if r % BOX == 0 and r != 0:
            print(sep)
        print(format_row(row))


def board_is_full(board):
    return all(value != 0 for row in board for value in row)


def play(difficulty="medium"):
    puzzle, solution = generate_puzzle(difficulty)
    board = copy.deepcopy(puzzle)
    given = [[cell != 0 for cell in row] for row in puzzle]

    print("Sudoku (%s) -- enter moves as 'row col value' (1-9), "
          "or 'hint', 'solve', 'quit'." % difficulty)
    print("Rows and columns are numbered 1-9.\n")

    while True:
        print_board(board)
        if board_is_full(board):
            if board == solution:
                print("\nSolved! Well done.")
            else:
                print("\nBoard is full but incorrect. Type 'solve' to reveal "
                      "the answer or 'quit' to give up.")
        print()
        try:
            command = input("> ").strip().lower()
        except EOFError:
            print()
            return

        if command in ("quit", "exit"):
            print("Goodbye!")
            return

        if command == "solve":
            board = copy.deepcopy(solution)
            continue

        if command == "hint":
            empties = [(r, c) for r in range(SIZE) for c in range(SIZE)
                       if board[r][c] == 0]
            if not empties:
                print("No empty cells left.")
                continue
            r, c = random.choice(empties)
            board[r][c] = solution[r][c]
            print("Hint: R%dC%d = %d" % (r + 1, c + 1, solution[r][c]))
            continue

        parts = command.split()
        if len(parts) != 3:
            print("Please enter three numbers: row col value "
                  "(e.g. '3 5 7'), or a command.")
            continue

        try:
            row, col, value = (int(p) for p in parts)
        except ValueError:
            print("Row, column and value must be numbers 1-9.")
            continue

        if not (1 <= row <= SIZE and 1 <= col <= SIZE and 0 <= value <= SIZE):
            print("Row and column must be 1-9, value must be 0-9 (0 clears).")
            continue

        row -= 1
        col -= 1
        if given[row][col]:
            print("That cell is a given clue and can't be changed.")
            continue

        board[row][col] = value


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command")

    play_parser = subparsers.add_parser("play", help="play an interactive game")
    play_parser.add_argument("--difficulty", choices=sorted(DIFFICULTIES),
                              default="medium")

    solve_parser = subparsers.add_parser("solve", help="solve a puzzle")
    solve_parser.add_argument("puzzle", nargs="?",
                               help="81-char puzzle string (0/. for blanks); "
                                    "reads from stdin if omitted")

    gen_parser = subparsers.add_parser("generate", help="print a new puzzle")
    gen_parser.add_argument("--difficulty", choices=sorted(DIFFICULTIES),
                             default="medium")

    args = parser.parse_args(argv)

    if args.command == "solve":
        text = args.puzzle if args.puzzle else sys.stdin.read()
        board = parse_board_string(text)
        if solve(board):
            print_board(board)
        else:
            print("No solution exists for that puzzle.")
            return 1
        return 0

    if args.command == "generate":
        puzzle, _ = generate_puzzle(args.difficulty)
        print_board(puzzle)
        return 0

    difficulty = getattr(args, "difficulty", "medium")
    play(difficulty)
    return 0


if __name__ == "__main__":
    sys.exit(main())
