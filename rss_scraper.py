import feedparser
import subprocess
import time

# RSS feed URL
feed_url = 'https://www.malaysiakini.com/rss/en/news.rss'

# Telegram channel ID and bot token
channel_id = 'Put Your Channel ID'
bot_token = 'Put Your Bot Token'

# Time threshold for filtering links
time_threshold = time.time() - (1 * 3600) # 1 hours ago

# Parse the RSS feed
feed = feedparser.parse(feed_url)

# Extract links posted within the time threshold
links = []
for entry in feed.entries:
    published_time = time.mktime(entry.published_parsed)
    if published_time > time_threshold:
        title = entry.title
        link = entry.link
        links.append({'title': title, 'link': link})

# Send links to Telegram channel using curl
for link in links:
    message = f"{link['title']}\n{link['link']}\nLatest post 1 hours ago"
    subprocess.run(['curl', '-d', f'chat_id={channel_id}', '-d', f'text={message}', f'https://api.telegram.org/bot{bot_token}/sendMessage'])
