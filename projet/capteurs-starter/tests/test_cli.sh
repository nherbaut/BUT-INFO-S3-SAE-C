#!/bin/sh
set -eu

program=$1
csv_file=$(mktemp)
trap 'rm -f "$csv_file"' EXIT HUP INT TERM

expect_exit() {
    expected=$1
    shift
    if "$@" >/dev/null 2>&1; then
        actual=0
    else
        actual=$?
    fi
    test "$actual" -eq "$expected"
}

"$program" --label "Essai CLI" --csv "$csv_file" --file tests/data/sensors-history.json

test -s "$csv_file"
head -n 1 "$csv_file" | grep -Fx \
    'label,updated_at,count,indoor_minimum,indoor_maximum,indoor_average,outdoor_minimum,outdoor_maximum,outdoor_average,average_gap'

expect_exit 2 "$program" --file tests/data/sensors-history.json --csv "$csv_file"
expect_exit 2 "$program" --label
expect_exit 2 "$program" --label "Essai" --csv
expect_exit 2 "$program" --label "Essai" --csv "$csv_file" --unknown valeur
expect_exit 2 "$program" --label "Essai" --label "Double" --csv "$csv_file"
expect_exit 2 "$program" --label "Essai" --csv "$csv_file" --csv "$csv_file"
expect_exit 2 "$program" --label "Essai" --csv "$csv_file" \
    --file tests/data/sensors-history.json --file tests/data/sensors-history.json
expect_exit 2 "$program" --label "Essai" --csv "$csv_file" \
    --url https://example.invalid/ --url https://example.invalid/
expect_exit 2 "$program" --label "Essai" --csv "$csv_file" \
    --file tests/data/sensors-history.json --url https://example.invalid/
expect_exit 2 "$program" --label "Essai" --csv "$csv_file" \
    --url https://example.invalid/ --file tests/data/sensors-history.json
expect_exit 1 "$program" --label "" --csv "$csv_file" \
    --file tests/data/sensors-history.json
expect_exit 1 "$program" --label "Avec,virgule" --csv "$csv_file" \
    --file tests/data/sensors-history.json

if test -e /dev/full; then
    expect_exit 1 "$program" --label "Echec CSV" --csv /dev/full \
        --file tests/data/sensors-history.json
fi
