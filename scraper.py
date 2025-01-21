import csv
from bs4 import BeautifulSoup
import requests

# Base URL for the website
base_url = "https://www.ismyshowcancelled.com/shows/cancelled/page/{}/?sort=1&filterNetwork=Netflix&filterGenre=All"

all_shows = []

# Start from page 1 and scrape until there are no more pages
page_num = 1
while True:
    url = base_url.format(page_num)

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    shows = soup.find_all("div", class_="shows-item")
    if not shows:
        break

    # Extract information for each show
    for show in shows:
        title = show.find("h3").text.strip()
        year = show.find("div", class_="stat").find_all("span")[1].text.strip()
        network = show.find("div", class_="stat").find_next_sibling("div", class_="stat").find_all("span")[1].text.strip()
        genre = show.find("div", class_="stat").find_next_sibling("div", class_="stat").find_next_sibling("div", class_="stat").find_all("span")[1].text.strip()

        all_shows.append({"Title": title, "Year": year, "Network": network, "Genre": genre})

    nextprev_span = soup.find("span", class_="nextprev")
    next_page_url = nextprev_span.find("a", string="Next >")

    if not next_page_url:
        break

    page_num += 1

# Export the data to a CSV file
with open("cancelled_netflix_shows.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Title", "Year", "Network", "Genre"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for show in all_shows:
        writer.writerow(show)

print("Data exported to cancelled_tv_shows.csv file.")