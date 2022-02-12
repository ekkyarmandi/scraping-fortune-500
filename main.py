import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from tqdm import tqdm

def render_html(url):
    '''
    Render the html on the backend.
    :param url: str -> the URL
    :return page: bs4 or BeautifulSoup object
    '''
    headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"}
    req = requests.get(url,headers=headers)
    page = BeautifulSoup(req.text,"html.parser")
    return page

def get_500_companies(year):
    '''
    Crawl Fortune 500 based on year input.
    :param year: int or str -> year position
    :return companies: list -> the list of 500 company data
    '''
    index = [1,101,201,301,401]
    companies = []
    for i in index:
        url = "https://money.cnn.com/magazines/fortune/fortune500_archive/full/{}/{}.html".format(year,i)
        page = render_html(url)
        for row in page.find("table",class_="maglisttable").find_all("tr",id="tablerow"):
            td = row.find_all("td")
            link = row.find("a")['href']
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

if __name__ == "__main__":

    # iterate the process through years
    data = []
    from_year = 1955
    to_year = 1995
    msg = f"Scraping Fortune 500 Company Data from {from_year} to {to_year}"
    for year in tqdm(range(from_year,to_year+1), msg):
        companies = get_500_companies(year)
        data.extend(companies)

    # write out the retrived data
    df = DataFrame(data)
    if from_year != to_year:
        df.to_csv(f"fortune-500-company-data-{from_year}-{to_year}.csv",index=False)
    else:
        df.to_csv(f"fortune-500-company-data-year-{from_year}.csv",index=False)
    print("done")