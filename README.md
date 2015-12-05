# Allen_AI_Science_Challenge_JunweiPan

## 1. Information Retrieval Based Method

We build a local search engine, then use the question as query to get the top results. Then we calculate the word count of the answers in these top results, the answers that get the highest word count is choosed as the prediction.

### Data Preparation

We use the wikipedia page of the ck-12 keywords to build index. The ck-12 keywords are scraped from the https://www.ck12.org using the [scrape.py](https://github.com/kemaswill/Allen_AI_Science_Challenge_JunweiPan/blob/master/scrape.py) script. Then we get the wikipedia page content of these keywords using [get_wikipedia_data.py](https://github.com/kemaswill/Allen_AI_Science_Challenge_JunweiPan/blob/master/get_wikipedia_data.py).

### Indexing and Searching

We use the lucene to index and search. The index is built using IndexFiles.java(java org.apache.lucene.demo.IndexFiles  -docs data/wikipedia_content_based_on_ck_12_keyword_one_file_per_keyword/), and search is done by [Get_Top_Documents_Based_on_Lucene.java](https://github.com/kemaswill/Allen_AI_Science_Challenge_JunweiPan/blob/master/Get_Top_Documents_Based_on_Lucene.java), which is just a modification of the SearchFiles.java.

### Prediction

For each answer, we calculate the word count of its words(excluding stop words) on the top N search results. Then the answer which get the highest word count is chosen as the prediction.

### Performance

We can get a score of 0.36, please refer to https://www.kaggle.com/c/the-allen-ai-science-challenge/leaderboard for the current leaderboard.

