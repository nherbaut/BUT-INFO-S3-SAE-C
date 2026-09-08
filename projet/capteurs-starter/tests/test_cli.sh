#!/bin/sh
set -eu

program=$1
csv_file=$(mktemp)
stdout_file=$(mktemp)
stderr_file=$(mktemp)
trap 'rm -f "$csv_file" "$stdout_file" "$stderr_file"' EXIT HUP INT TERM

show_file() {
    label=$1
    file=$2

    printf '%s:\n' "$label" >&2
    if test -s "$file"; then
        cat "$file" >&2
    else
        printf '(vide)\n' >&2
    fi
}

expect_exit() {
    expected=$1
    shift

    if "$@" >"$stdout_file" 2>"$stderr_file"; then
        actual=0
    else
        actual=$?
    fi

    if test "$actual" -ne "$expected"; then
        printf 'Code de sortie incorrect. Attendu : %s ; obtenu : %s\n' \
            "$expected" "$actual" >&2
        printf 'Commande :' >&2
        printf ' %s' "$@" >&2
        printf '\n' >&2
        show_file 'stdout produit' "$stdout_file"
        show_file 'stderr produit' "$stderr_file"
        exit 1
    fi
}

expect_equal() {
    label=$1
    expected=$2
    actual=$3

    if test "$actual" != "$expected"; then
        printf '%s incorrect.\n' "$label" >&2
        printf 'Attendu : [%s]\n' "$expected" >&2
        printf 'Obtenu  : [%s]\n' "$actual" >&2
        exit 1
    fi
}

expected_header='label,updated_at,count,indoor_minimum,indoor_maximum,indoor_average,outdoor_minimum,outdoor_maximum,outdoor_average,average_gap'

expect_exit 0 "$program" --label "Essai CLI" --csv "$csv_file" \
    --file tests/data/sensors-history.json

if ! test -s "$csv_file"; then
    printf 'Le fichier CSV attendu est absent ou vide : %s\n' "$csv_file" >&2
    exit 1
fi

actual_header=$(head -n 1 "$csv_file")
expect_equal 'En-tete CSV' "$expected_header" "$actual_header"

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
