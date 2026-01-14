import warnings
from cryptography.utils import CryptographyDeprecationWarning
warnings.filterwarnings(
    "ignore",
    category=CryptographyDeprecationWarning
)

import sys
import camelot
import pandas as pd

deck_filename = sys.argv[1]
target_filename = sys.argv[2]
image_folder = sys.argv[3]
note = sys.argv[4]
update_mode = int(sys.argv[5])

all_names = pd.Series()
all_ids = pd.Series(dtype=int)
for i in range(20):
    try:
        csv = pd.read_csv(f'python/roster-page-{i+1}-table-1.csv')
    except:
        break
    s = csv['Name'].str.replace('\n', '', regex=False).dropna()
    all_names = pd.concat([all_names, s], ignore_index=True)
    all_ids = pd.concat([all_ids, csv['Id'].dropna().astype(int)], ignore_index=True)

filenames = pd.Series([f"{image_folder}/idphoto-{i:03d}.jpg" for i in range(len(all_names))])
notes = pd.Series([note for i in range(len(all_names))])
df = pd.DataFrame({'Front': notes, 'Back': all_names, 'ImagePath': filenames, 'Id': all_ids})

existing = pd.read_csv(
    deck_filename,      # or .csv, whatever it’s called
    sep="\t",               # tab-separated
    comment="#",            # ignore lines starting with '#'
    header=None,            # no header row (Anki exports raw data)
    index_col=False,
    names=["Front", "Back", "ImagePath", "Id"]  # give names manually
)

merged = existing.merge(df, on="Id", how="outer", suffixes=("", "_new"))

if update_mode == -1:
    print("Not implemented yet")
elif update_mode == 1:
    # Add new students
    for col in ['Front', 'Back', 'ImagePath']:
        mask = merged[col].isna()
        merged.loc[mask, col] = merged.loc[mask, f"{col}_new"]

    # Check for students without note, and add it
    mask = ~merged["Front"].str.contains(note, regex=False, na=False) & ~merged["Front_new"].isna()
    merged.loc[mask, "Front"] = (merged.loc[mask, "Front"] + "\n" + note)

    merged = merged[["Front", "Back", "ImagePath", "Id"]]

    with open(target_filename, "w") as f:
        merged.to_csv(f, sep="\t", index=False, header=False)
else:
    print("Invalid update mode.")