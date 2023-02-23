import feedparser
import subprocess
import time
import socket

# RSS feed URLs
feed_urls = ['https://www.malaysiakini.com/rss/en/news.rss',
             'https://rss.astroawani.com/rss/latest/public',
             'https://www.malaymail.com/feed/rss/malaysia',
             'https://www.lowyat.net/feed/',
             'https://www.utusan.com.my/feed/',
             'https://www.hmetro.com.my/mutakhir.xml',
             'https://www.kosmo.com.my/feed/',
             'https://www.hmetro.com.my/utama.xml']
# https://blog.feedspot.com/malaysian_news_rss_feeds/ # Link rss sini

# Telegram channel ID and bot token
channel_id = 'Chat ID'
bot_token = 'Chat ID'

# Time threshold for filtering links
time_threshold = time.time() - (1 * 3600) # 1 hours ago

# Get hostname of the system
hostname = socket.gethostname()

# Parse the RSS feeds
all_links = []
for feed_url in feed_urls:
    feed = feedparser.parse(feed_url)
    links = []
    for entry in feed.entries:
        published_time = time.mktime(entry.published_parsed)
        if published_time > time_threshold:
            title = entry.title
            link = entry.link
            date = time.strftime('%Y-%m-%d %H:%M:%S', entry.published_parsed)
            links.append({'title': title, 'link': link, 'date': date})
    all_links.extend(links)

# Send links to Telegram channel using curl
for link in all_links:
    message = f"{link['title']}\n{link['link']}\n---| Additional Info |---\nDate: {link['date']}\nScraper ID : {hostname}"
    subprocess.run(['curl', '-d', f'chat_id={channel_id}', '-d', f'text={message}', f'https://api.telegram.org/bot{bot_token}/sendMessage'])
    time.sleep(3) # 3-second delay
