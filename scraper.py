import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape_internships(keyword):
    url = "https://internshala.com/internships"
    params = {'keywords': keyword}

    response = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')

    internships = []
    for internship in soup.select(".individual_internship"):
        title_tag = internship.find('a')
        title = title_tag.text.strip() if title_tag else 'N/A'
        link = "https://internshala.com" + title_tag['href'] if title_tag and 'href' in title_tag.attrs else 'N/A'

        # Company name
        company_tag = internship.find('div', class_='company_and_premium')
        if company_tag:
            company_anchor = company_tag.find('a')
            company = company_anchor.text.strip() if company_anchor else 'N/A'
        else:
            company = 'N/A'

        # Location
        location_tag = internship.find('div', class_='location_container')
        location = location_tag.text.strip() if location_tag else 'N/A'

        # Duration
        duration = 'N/A'
        for detail in internship.find_all('div', class_='other_detail_item'):
            if 'month' in detail.text.lower():
                duration = detail.text.strip()
                break

        # Stipend
        stipend_tag = internship.find('span', class_='stipend')
        stipend = stipend_tag.text.strip() if stipend_tag else 'N/A'

        internships.append({
            'Title': title,
            'Company': company,
            'Location': location,
            'Duration': duration,
            'Stipend': stipend,
            'Link': link
        })

    # Save to CSV
    df = pd.DataFrame(internships)
    df.to_csv('internships.csv', index=False)

    return internships
