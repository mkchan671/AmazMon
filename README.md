# AmazMon
Monitor item prices from Amazon

Install required package

Command:
pip3 install -r ./requirements.txt

Firefox is used in the script, please download the driver from https://github.com/mozilla/geckodriver/releases.

Plesae save the amazon code into list.csv to monitor the items from Amazon.
item code could be found in URI after "/dp/"  or "gp", "https://www.amazon.com/dp/B07CRG94G3" item code is B07CRG94G3

To update the latest list with the latest price, run script with:
./scraper.py
