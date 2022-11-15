import csv
import feedparser
import datetime

dt_now = datetime.datetime.now()
td = datetime.timedelta(days=1)
dt_yesterday = dt_now - td
dt_yesterday = str(dt_yesterday)
dt_yesterday = dt_yesterday[0:10]

with open('file.txt', 'w') as f:
    print(dt_yesterday + "<br>", file=f)
    print("--------------------------------" + "<br>", file=f)
    with open('sites.csv', 'r') as file:
        reader = csv.reader(file)

        for row in reader:
            RSS_URL = row[1]
            blog_RSS = feedparser.parse(RSS_URL)

            for entry in blog_RSS.entries:
                if dt_yesterday == entry.date[0:10]:
                    print("<a href=\"" + entry.link + "\">" + entry.title + "</a>" + ":" + row[0] + "<br>", file=f)
                    print("...................." + "<br>", file=f)
