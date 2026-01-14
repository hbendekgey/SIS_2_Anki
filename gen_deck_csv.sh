#!/bin/bash
ANKI_USERNAME="User 1" # Should be visible at the top of the Anki window

if [[ "$#" -ne 3 && "$#" -ne 4 ]]; then
  echo "Usage: ./gen_deck_csv.sh <roster_filename.pdf> <target_filename.csv> '<Note for students>' [deck_filename.csv]"
  exit 1 # Exit with a non-zero status code to indicate an error
fi

IMG_DIR_NAME=$(date +"%s")

ROSTER_FILE="$1"
TARGET_FILE="$2"
CARD_NOTE="$3"

if [[ $# -eq 3 ]]; then
  mkdir ~/Library/Application\ Support/Anki2/"$ANKI_USERNAME"/collection.media/"$IMG_DIR_NAME"/
  pdfimages -all "$ROSTER_FILE" ~/Library/Application\ Support/Anki2/"$ANKI_USERNAME"/collection.media/"$IMG_DIR_NAME"/idphoto
  python python/gen_anki_csv.py "$ROSTER_FILE" "$TARGET_FILE" "$IMG_DIR_NAME" "$CARD_NOTE"
fi

if [[ $# -eq 4 ]]; then
  DECK_FILE="$4"
  python python/check_for_new_students.py "$ROSTER_FILE" "$DECK_FILE"

  if [ $? -eq 0 ]; then
      echo "No new students detected"
  else
      echo "New students detected. Generating idphoto jpegs"
      mkdir ~/Library/Application\ Support/Anki2/"$ANKI_USERNAME"/collection.media/"$IMG_DIR_NAME"/
      pdfimages -all "$ROSTER_FILE" ~/Library/Application\ Support/Anki2/"$ANKI_USERNAME"/collection.media/"$IMG_DIR_NAME"/idphoto
  fi

  python python/update_anki_csv.py "$DECK_FILE" "$TARGET_FILE" "$IMG_DIR_NAME" "$CARD_NOTE" "1"

fi

rm python/roster*
