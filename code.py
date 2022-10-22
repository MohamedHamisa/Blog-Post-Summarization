!pip install transformers

from transformers import pipeline
from bs4 import BeautifulSoup
import requests

#Load Summarization Pipeline
summarizer = pipeline("summarization")

# Get Blog Post from Medium
URL = "https://towardsdatascience.com/a-bayesian-take-on-model-regularization-9356116b6457"
URL = "https://hackernoon.com/will-the-game-stop-with-gamestop-or-is-this-just-the-beginning-2j1x32aa"

r = requests.get(URL)

soup = BeautifulSoup(r.text, 'html.parser')
results = soup.find_all(['h1', 'p']) #it will starts with the headlines (h1)
text = [result.text for result in results]
ARTICLE = ' '.join(text)

# Chunk Text

max_chunk = 500 #bunch of words individually

ARTICLE = ARTICLE.replace('.', '.<eos>')
ARTICLE = ARTICLE.replace('?', '?<eos>')
ARTICLE = ARTICLE.replace('!', '!<eos>')

sentences = ARTICLE.split('<eos>') #to split text into sentences
current_chunk = 0 
chunks = []
for sentence in sentences:
    if len(chunks) == current_chunk + 1: #if we have chunck
        if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:#take the sentence and chunck and split them into words
            chunks[current_chunk].extend(sentence.split(' '))
        else:
            current_chunk += 1
            chunks.append(sentence.split(' ')) #if no create a new chunck
#if we currently don't hav chunks
    else:
        print(current_chunk)
        chunks.append(sentence.split(' ')) #take that sentence and split it by space then append it to our chunck 

for chunk_id in range(len(chunks)):
    chunks[chunk_id] = ' '.join(chunks[chunk_id])

len(chunks)

# Summarize Text

res = summarizer(chunks, max_length=120, min_length=30, do_sample=False)
res[0]

text = ' '.join([summ['summary_text'] for summ in res])

# Output to Text File
with open('blogsummary.txt', 'w') as f:
    f.write(text)
