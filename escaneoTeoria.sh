#!/bin/bash

OUTPUT="toda_la_teoria.txt"
> "$OUTPUT"   # vacía el archivo si ya existe

for file in "teoria"/*; do
  if [[ -f "$file" ]]; then
    echo "----- ARCHIVO: $file -----" >> "$OUTPUT"
    echo >> "$OUTPUT"
    cat "$file" >> "$OUTPUT"
    echo >> "$OUTPUT"
    echo >> "$OUTPUT"
  fi
done
