from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


@app.route('/')
def index():
    # Web scraping logic
    url = 'https://cio.economictimes.indiatimes.com/events'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract information from the HTML
        events = []
        for event in soup.find_all('li', class_='award-stroy-panel__item'):
            headline = event.find('h2').get_text()
            description = event.find('h3').get_text()

            # Check if date element exists
            date_element = event.find('li', class_='sprite-icon-img calender-icon')
            date = date_element.find_next('p').get_text() if date_element and date_element.find_next('p') else 'N/A'

            # Check if location element exists
            location_element = event.find('li', class_='sprite-icon-img location-icon')
            location = location_element.find_next('p').get_text() if location_element and location_element.find_next(
                'p') else 'N/A'

            link = event.find('a')['href']

            events.append({
                'headline': headline,
                'description': description,
                'date': date,
                'location': location,
                'link': link,
            })

        # Render the HTML template with the extracted information
        return render_template('index.html', events=events)

    else:
        return f'Failed to retrieve the webpage. Status code: {response.status_code}'


if __name__ == '__main__':
    app.run(debug=True)
