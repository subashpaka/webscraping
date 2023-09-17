from crontab import CronJobBase, Schedule
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from .models import Property, ScrapingLog, CronJobStatus, CronJobSchedule

class ScrapePropertiesJob(CronJobBase):
    RUN_EVERY_MINS = 30  # Default schedule, can be changed by admin
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'property_scraper.cron.scrape_properties'

    def is_enabled(self):
        try:
            job_status = CronJobStatus.objects.get(job_name=self.code)
            return job_status.is_enabled
        except CronJobStatus.DoesNotExist:
            return True

    def do(self):
        if not self.is_enabled():
            print(f'Cron job {self.code} is disabled. Skipping execution.')
            return

        # Define cities and their respective localities
        cities_and_localities = [
            ('Pune', 'Maharashtra'),
            ('Delhi', 'Delhi'),
            ('Mumbai', 'Maharashtra'),
            ('Lucknow', 'Uttar Pradesh'),
            ('Agra', 'Uttar Pradesh'),
            ('Ahmedabad', 'Gujarat'),
            ('Kolkata', 'West Bengal'),
            ('Jaipur', 'Rajasthan'),
            ('Chennai', 'Tamil Nadu'),
            ('Bengaluru', 'Karnataka'),
        ]

        for city, state in cities_and_localities:
            # Define the URL for 99acres property listings in a specific city and locality
            url = f'https://www.99acres.com/search/property/buy/{city.lower()}-all?city=38&preference=S&area_unit=1&res_com=R'

            # Send an HTTP GET request to the 99acres URL
            response = requests.get(url)

            if response.status_code == 200:
                # Parse the HTML content using BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract property listings
                listings = soup.find_all('div', class_='property-listing')

                # Track the number of records successfully scraped
                records_scrapped_count = 0

                for listing in listings:
                    try:
                        # Extract property details
                        property_name = listing.find('a', class_='proTitle').text.strip()
                        property_cost = listing.find('td', class_='price').text.strip()
                        property_type = listing.find('td', class_='proInfo-1').text.strip()
                        property_area = listing.find('td', class_='proInfo-2').text.strip()
                        property_locality = listing.find('a', class_='localityLink').text.strip()
                        property_link = urljoin(url, listing.find('a', class_='proTitle')['href'])

                        # Create a new Property object and save it to the database
                        Property.objects.create(
                            property_name=property_name,
                            property_cost=property_cost,
                            property_type=property_type,
                            property_area=property_area,
                            property_locality=property_locality,
                            property_city=city,
                            property_link=property_link
                        )

                        # Increment the successful scrape count
                        records_scrapped_count += 1
                    except Exception as e:
                        print(f'Error processing listing: {str(e)}')

                # Log the successful scrape count in the ScrapingLog model
                ScrapingLog.objects.create(
                    city=city,
                    locality=state,
                    records_scrapped_count=records_scrapped_count
                )

            else:
                print(f'Failed to fetch data for {city}, {state} - HTTP {response.status_code}')