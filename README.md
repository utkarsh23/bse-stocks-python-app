# BSE Equity Stocks
A CherryPy + Redis web app for BSE Equity Stocks.

## Functionality:

1. index page: /
- Top 10 Closing Stocks.
- Search Bar.

2. search page: /search
- All search results **by name**.
- Search Bar.

## Populating Redis
A cron job runs at 5 p.m., 6 p.m. and 7 p.m. every day of the week from Monday to Friday to execute the `populate_redis.py` script. This script updates Redis with present day's stocks statistics.
