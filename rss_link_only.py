import feedparser
from datetime import datetime, timedelta
import re

# RSS feed URL
feed_url = 'https://www.malaysiakini.com/rss/en/news.rss'

# Number of hours to look back
hours = 1

# Parse RSS feed with feedparser library
feed = feedparser.parse(feed_url)

# Loop through feed entries and filter by time posted
filtered_entries = []
for entry in feed.entries:
    # Get the published datetime of the entry
    published = datetime.fromtimestamp(
        int(datetime(*entry.published_parsed[:6]).strftime('%s'))
    )

    # Compare the datetime to the current time
    time_delta = datetime.now() - published
    if time_delta <= timedelta(hours=hours):
        filtered_entries.append(entry)

# Extract links from filtered entries and get their titles and descriptions
links = []
for entry in filtered_entries:
    # Extract links from the "content" field, if present
    if 'content' in entry:
        for content in entry.content:
            link = re.findall(r'<a.*?href="(.*?)".*?>', content.value)
            if link:
                links.append({
                    'link': link[0],
                    'title': content.get('title', ''),
                    'description': content.get('value', '')
                })
    
    # Extract links from the "description" field, if present
    if 'description' in entry:
        link = re.findall(r'<a.*?href="(.*?)".*?>', entry.description)
        if link:
            links.append({
                'link': link[0],
                'title': entry.get('title', ''),
                'description': entry.description
            })
    
    # Extract links from the "link" field, if present
    links.append({
        'link': entry.link,
        'title': entry.get('title', ''),
        'description': entry.get('description', '')
    })

# Print out filtered links with their titles and descriptions
for link in links:
    print(link['link'])
    print(f"Title: {link['title']}")
    print(f"Description: {link['description']}\n")
