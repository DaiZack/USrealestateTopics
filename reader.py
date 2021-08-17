from lxml import html
import os, json, re
import pandas as pd

# sources = [s for s in os.listdir() if '.' not in s]
sources = ['The New York Times','The Wall Street Journal','USA Today']
outfilename = 'USrealestate.csv'


Journal = ['The New York Times','The Wall Street Journal','USA Today']

# s0 = sources[0]
header = True
for s0 in sources:
    pages = [p for p in os.listdir(s0) if 'html' in p]

# page = pages[0]
    for page in pages:
        with open(os.path.join(s0,page), encoding='utf-8') as f:
            text = f.read()
        res = html.fromstring(text)
        articles = res.xpath('//div[@class="article enArticle"]')
        for article in articles:
        # article = articles[3]
            line = pd.Series()
            line['title'] = (article.xpath('./div/span/text()')+[''])[0].strip()
            line['source'] = s0
            line['date'] = (re.findall(r'\d{1,2} \w{3,11} 20\d{2}', '\n'.join(article.xpath('.//text()')))+[''])[0].strip()
            line['Journal'] = (re.findall('|'.join(Journal),'\n'.join(article.xpath('.//text()')))+[''])[0]
            line['author'] = (article.xpath('./div[@class="author"]/text()')+[''])[0].strip()
            line['wordscount'] = (re.findall(r'(\d+) words', '\n'.join(article.xpath('.//text()')))+[''])[0].strip()
            line['content'] = '\n'.join(article.xpath('.//p[@class="articleParagraph enarticleParagraph"]//text()'))
            line.to_frame().T.to_csv(outfilename, index=0, header=header, mode='w' if header else 'a')
            header = False
            # line['Journal'] = s0
            # out.write(json.dumps(line).encode('utf-8')+b',\n')
# out.seek(-2,2)
# out.truncate()
# out.write(b']')
# out.close()

# with open(outfilename) as f:
#     dj = f.read()

# df = pd.read_json(dj, orient='records')

# df.to_csv(outfilename.replace('.json', '.csv'), index=0)
pd.read_csv(outfilename).to_excel(outfilename.replace('.csv','.xlsx'), index=0)
