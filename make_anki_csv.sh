#!/bin/bash
ANKI_USERNAME="User 1" # Should be visible at the top of the Anki window

if [ "$#" -ne 3 ]; then
  echo "Usage: ./make_anki_csv.sh <roster_filename.pdf> <target_filename.csv> <Note for students (in quotes)>"
  exit 1 # Exit with a non-zero status code to indicate an error
fi

IMG_DIR_NAME=$(date +"%s")

ROSTER_FILE="$1"
TARGET_FILE="$2"
CARD_NOTE="$3"

mkdir ~/Library/Application\ Support/Anki2/"$ANKI_USERNAME"/collection.media/"$IMG_DIR_NAME"/

pdfimages -all "$ROSTER_FILE" ~/Library/Application\ Support/Anki2/"$ANKI_USERNAME"/collection.media/"$IMG_DIR_NAME"/idphoto

python python/gen_anki_csv.py "$ROSTER_FILE" "$TARGET_FILE" "$IMG_DIR_NAME" "$CARD_NOTE"

rm python/roster*