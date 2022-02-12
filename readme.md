# Scraping Fortune 500

In this project I delevop scraping script to scrape data from [Fortune 500](https://money.cnn.com/magazines/fortune/fortune500_archive/full/1955/1.html) and then write it out as CSV file. I use requests, beautifulsoup, pandas modules. For more details, requests module used to make a request GET to the server, beautifulsoup used to extract desired data via html tags, while pandas module used to convert all the list or dictionary variable into pandas dataframe and then write it as CSV.

## Specify the Scraping Years

On the [main.py](main.py) you can find `from_year` and `to_year` variable. You can change the years value within the range 1955-2005.

## Install the Requirements
```python
pip install -r requirements.txt
```

## Running the Scraping Script

It's quite easy actually, you can just open your terminal where the [main.py](main.py) is exist and then type:
```python
python main.py
```
