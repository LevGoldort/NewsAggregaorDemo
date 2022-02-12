# **News Aggregator Demo**

Backend for simple email news subscription service.

The program parse https://www.ynetnews.com/category/3089, categorize the news for 4 categories - politics, sports, finance and weather and saves them to DB.

There are three types of user subscription - ASAP, Daily and Weekly. For each type there are a number of time and day options when the user will get the email notifications.

### **Modules:**

`newsparser` package contains all functions for parsing and working with db:

`constants.py` - program constants such as CATEGORIES set and system variables, such as abspath to files and username.

`crud.py` - all function to get/put data to db

`db.py` - Database details and initiation

`models.py` - Database models used in the program

`output.py` - Functions to deliver updates to users, currently `send_mail`.

`parse.py` - function to parse websites, currenty only ynews

Global script modules:

`cron-news-updater.py` - module to run scrapers and update ASAP subscribers

`cron-manager.py` - module to initiate crons.

### **Starting up**

clone the project and start `cron-manager.py` 