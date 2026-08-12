# Sudoku

A command-line Sudoku game written in Python. It can generate puzzles with a
guaranteed unique solution, let you play them interactively, or solve any
puzzle you give it.

## Features

- **Solver** — backtracking search with a minimum-remaining-values (MRV)
  heuristic, so it stays fast even on nearly empty boards.
- **Generator** — builds a full valid grid, then removes clues one at a time
  while checking that the puzzle still has exactly one solution.
- **Interactive play** — fill in the grid from the terminal, with hints and a
  reveal-the-solution option.
- **Difficulty levels** — `easy`, `medium`, `hard`, `expert` (more clues =
  easier).

## Requirements

- Python 3
- No external dependencies (standard library only)

## Usage

### Play interactively

```bash
python3 sudoku.py play --difficulty medium
```

(`--difficulty` defaults to `medium` and accepts `easy`, `medium`, `hard`, or
`expert`. Running `python3 sudoku.py` with no subcommand also starts a game.)

Enter moves as `row col value`, using 1-9 for rows/columns and 0-9 for the
value (`0` clears a cell), e.g.:

```
> 3 5 7
```

Other commands available during play:

| Command  | Effect                                   |
|----------|-------------------------------------------|
| `hint`   | Fills in one random empty cell for you    |
| `solve`  | Reveals the full solution                 |
| `quit` / `exit` | Ends the game                      |

Cells that were given as starting clues can't be overwritten.

### Solve a puzzle

Pass an 81-character puzzle string (digits `1`-`9`, with `0` or `.` for blank
cells), either as an argument or piped in via stdin:

```bash
python3 sudoku.py solve "53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79"

echo "53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79" | python3 sudoku.py solve
```

### Generate a puzzle

```bash
python3 sudoku.py generate --difficulty hard
```

Prints a new puzzle grid to stdout (`--difficulty` works the same as above).

## Running tests

```bash
python3 -m unittest test_sudoku.py -v
```

## Project structure

| File             | Purpose                                      |
|------------------|-----------------------------------------------|
| `sudoku.py`      | Game logic, solver, generator, and CLI        |
| `test_sudoku.py` | Unit tests for solving, generation, and validation |
