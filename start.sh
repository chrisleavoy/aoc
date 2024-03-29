#!/bin/bash -e

[[ $1 -ge 1 && $1 -le 25 ]] || (echo "\$1 must be a day [1-25]"; exit 1)

year=2022
day=$(printf "day%02d" "$1")
day_short=$(printf "%d" "$1")
base=$(dirname "$0")/$year/$day
session=$(cat "$(dirname "$0")/.session")

[[ -d $base ]] || mkdir -p "$base"
cd "$base"

touch "$day-input.txt"

cat > "test_$day.py" <<EOF
from pathlib import Path


def read(filename: str) -> str:
    path = Path(__file__).parent.joinpath(filename)
    with open(path, encoding='utf-8') as f:
        return f.read()


def test_sol1():
    s = read('$day-input.txt')
    assert s


# def test_sol2():
EOF

curl -s "https://adventofcode.com/$year/day/$day_short/input" \
    -H "Cookie: session=$session" \
    -o "$day-input.txt"

echo "See https://adventofcode.com/$year/day/$day_short"
