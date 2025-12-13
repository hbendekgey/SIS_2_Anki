import warnings
from cryptography.utils import CryptographyDeprecationWarning
warnings.filterwarnings(
    "ignore",
    category=CryptographyDeprecationWarning
)

import sys
import camelot
import pandas as pd

input_filename = sys.argv[1]
target_filename = sys.argv[2]
image_folder = sys.argv[3]
note = sys.argv[4]

tables = camelot.read_pdf(input_filename, pages='all')
tables.export('python/roster.csv', f='csv') # json, excel, html, markdown, sqlite

all_names = pd.Series()
all_ids = pd.Series()
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

df = pd.concat([notes, all_names, filenames, all_ids], axis=1)

with open(target_filename, "w") as f:
    df.to_csv(f, sep="\t", index=False, header=False)