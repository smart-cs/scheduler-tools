# Scheduler Tools
```shell
# Install dependencies
pipenv install

# To scrape data from UBC Course Schedule
pipenv run ./cs.py scrape

# Upload a the scraped data to Firebase
pipenv run ./cs.py upload <FILENAME>
```