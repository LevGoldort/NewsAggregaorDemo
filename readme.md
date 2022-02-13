# **News Aggregator Demo**

Backend for simple email news subscription service.

The program parse https://www.ynetnews.com/category/3089 and https://news.sky.com, categorize the news for categories and saves them to DB.

There are three types of user subscription - ASAP, Daily and Weekly. For each type there are a number of time and day options when the user will get the email notifications.

Both category and subscription data loaded from config.json and can be changed easily.

### **Modules:**

`newsparser` package contains all functions for parsing and working with db:

`crud.py` - all function to get/put data to db

`db.py` - Database details and initiation

`models.py` - Database models used in the program

`output.py` - Functions to deliver updates to users, currently `send_mail`.

`parse.py` - function to parse websites, currenty only ynews

Global script modules:

`jobs.py` - module for jobs functions

`main.py` - point of start

`adduser.py` - CLI to add subscribers to db. Run `python adduser.py -h` to get help with calling it.

`exploration.py` - some functions and data manipulation to explore collected data. Figures generated on some initial data located in `figures` folder

### **Starting up**

clone the project, generate config and start `main.py` 
