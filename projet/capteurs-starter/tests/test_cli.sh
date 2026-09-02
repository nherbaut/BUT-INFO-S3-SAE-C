#!/bin/sh
set -eu

program=$1
csv_file=$(mktemp)
trap 'rm -f "$csv_file"' EXIT HUP INT TERM

"$program" --label "Essai CLI" --csv "$csv_file" --file tests/data/sensors-history.json

test -s "$csv_file"
head -n 1 "$csv_file" | grep -Fx \
    'label,updated_at,count,indoor_minimum,indoor_maximum,indoor_average,outdoor_minimum,outdoor_maximum,outdoor_average,average_gap'
