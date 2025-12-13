#!/bin/bash
ANKI_USERNAME="User 1" # Should be visible at the top of the Anki window

if [ "$#" -ne 4 ]; then
  echo "Usage: ./update_anki_csv.sh <roster_filename.pdf> <deck_filename.csv> <target_filename.csv> <Note for students (in quotes)>"
  exit 1 # Exit with a non-zero status code to indicate an error
fi

IMG_DIR_NAME=$(date +"%s")

ROSTER_FILE="$1"
DECK_FILE="$2"
TARGET_FILE="$3"
CARD_NOTE="$4"

python python/check_for_new_students.py "$ROSTER_FILE" "$DECK_FILE"

if [ $? -eq 0 ]; then
    echo "No new students detected"
else
    echo "New students detected. Generating idphoto jpegs"
    mkdir ~/Library/Application\ Support/Anki2/"$ANKI_USERNAME"/collection.media/"$IMG_DIR_NAME"/
    pdfimages -all "$ROSTER_FILE" ~/Library/Application\ Support/Anki2/"$ANKI_USERNAME"/collection.media/"$IMG_DIR_NAME"/idphoto
fi

python python/update_anki_csv.py "$DECK_FILE" "$TARGET_FILE" "$IMG_DIR_NAME" "$CARD_NOTE" "1"

rm python/roster*