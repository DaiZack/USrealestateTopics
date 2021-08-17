import pandas as pd
from io import StringIO
outfilename = 'The Wall Street Journal - Covid\covidWallstreet.json'
with open(outfilename) as f:
    dj = f.read()

df = pd.read_json(StringIO(dj), orient='records')

df.to_excel(outfilename.replace('.json', '.xlsx'), index=0)