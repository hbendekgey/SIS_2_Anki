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
deck_filename = sys.argv[2]

tables = camelot.read_pdf(input_filename, pages='all')
tables.export('python/roster.csv', f='csv') # json, excel, html, markdown, sqlite

all_ids = pd.Series(dtype=int)
for i in range(20):
    try:
        csv = pd.read_csv(f'python/roster-page-{i+1}-table-1.csv')
    except:
        break
    s = csv['Name'].str.replace('\n', '', regex=False).dropna()
    all_ids = pd.concat([all_ids, csv['Id'].dropna().astype(int)], ignore_index=True)

existing = pd.read_csv(
    deck_filename,      # or .csv, whatever it’s called
    sep="\t",               # tab-separated
    comment="#",            # ignore lines starting with '#'
    header=None,            # no header row (Anki exports raw data)
    index_col=False,
    names=["Front", "Back", "ImagePath", "Id"]  # give names manually
)

if all_ids.isin(existing['Id']).all():
    sys.exit(0)   # true
else:
    sys.exit(1)   # false