#!/bin/bash

OUTPUT="todo_el_contenido.txt"
> "$OUTPUT"   # vacía el archivo si ya existe

for dir in bloque*; do
  if [[ -d "$dir" ]]; then
    echo "===== CARPETA: $dir =====" >> "$OUTPUT"
    echo >> "$OUTPUT"

    for file in "$dir"/*; do
      if [[ -f "$file" ]]; then
        echo "----- ARCHIVO: $file -----" >> "$OUTPUT"
        echo >> "$OUTPUT"
        cat "$file" >> "$OUTPUT"
        echo >> "$OUTPUT"
        echo >> "$OUTPUT"
      fi
    done
  fi
done