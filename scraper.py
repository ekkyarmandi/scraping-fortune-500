from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import argparse
import csv
import os

# check the output folder
if not os.path.exists("output"):
    os.mkdir("output")

def get(url):
    '''
    Render the html on the backend.
    :param url: str -> the URL
    :return page: bs4 or BeautifulSoup object
    '''
    headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"}
    req = requests.get(url,headers=headers)
    if req:
        return BeautifulSoup(req.text,"html.parser")

def get_500(year):
    '''
    Crawl Fortune 500 based on year input.
    :param year: int or str -> year position
    :return companies: list -> the list of 500 company data
    '''
    index = [1+i*100 for i in range(5)]
    companies = []
    for i in index:
        url = f"https://money.cnn.com/magazines/fortune/fortune500_archive/full/{year}/{i}.html"
        page = get(url)
        for row in page.find("table",class_="maglisttable").find_all("tr",id="tablerow"):
            td = row.find_all("td")
            link = row.find("a").get("href")
            company = {
                "Rank": td[0].get_text().strip(),
                "Company": td[1].get_text().strip(),
                "Revenues ($ millions)": td[2].get_text().strip(),
                "Profit ($ millions)": td[3].get_text().strip(),
                "Company ID": link.split("/")[-1].strip(".html"),
                "Year": year
            }
            companies.append(company)
    return companies

def write_csv(data,years) -> None:
    '''
    Write data out as CSV.
    :param data: list -> list of data
    :param years: tuple -> tuple of from_year and to_year variable
    '''
    a,b = years
    write_header = True
    filename = f"output/fortune-500-{a}-{b}.csv"
    with open(filename,"w",newline="") as csvfile:
        file = csv.writer(csvfile,delimiter=",")
        for row in data:
            # write the header
            if write_header:
                write_header = False
                file.writerow(list(row.keys()))
            # write out the value
            file.writerow(list(row.values()))

    ## printout message
    print(filename,"has been created!")


if __name__ == "__main__":

    ## CLI
    parser = argparse.ArgumentParser(
        description="Fortune 500 data scraping"
    )
    parser.add_argument(
        "from_year",
        type=int,
        help="From year variable"
        )
    parser.add_argument(
        "to_year",
        type=int,
        help="To year variable"
        )
    args = parser.parse_args()

    ## iterate the process through years
    data = []
    from_year = args.from_year
    to_year = args.to_year
    msg = f"Scraping Fortune 500 Company Data from {from_year} to {to_year}"
    data = [get_500(year) for year in tqdm(range(from_year,to_year+1), msg)]

    ## write out the retrived data
    write_csv(data,(from_year,to_year))