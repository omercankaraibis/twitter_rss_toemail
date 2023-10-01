from datetime import datetime, timedelta

import feedparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email credentials
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = ''
smtp_password = ''
recipient_email = ''



# Add the RSS feed urls to this list as strings, add at least one feed
rss_list = []


feed = feedparser.parse(rss_list[0])
for i in range(1, len(rss_list)):
    feed.entries.extend(feedparser.parse(rss_list[i]).entries)


today = datetime.now()
one_day_ago = today - timedelta(days=1)

# Filter tweets within the one-day interval
tweets_within_one_day = []

for entry in feed.entries:
    # Parse the publication date from the RSS entry
    entry_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")

    # Check if the tweet is within the one-day interval
    if entry_date >= one_day_ago and entry_date <= today:
        tweets_within_one_day.append(entry)

feed.entries = tweets_within_one_day

# Extract and send tweets via email
# Create the email message
msg = MIMEMultipart()
msg['From'] = smtp_username
msg['To'] = recipient_email
msg['Subject'] = 'New Tweet from Twitter RSS Feed'

for entry in feed.entries:
    tweet_text = entry.title
    tweet_link = entry.link
    # Attach tweet text and link to the email
    msg.attach(MIMEText(f'Tweet: {tweet_text}\n\nLink: {tweet_link}\n\n', 'plain'))

    # Connect to the SMTP server and send the email
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(smtp_username, smtp_password)
server.sendmail(smtp_username, recipient_email, msg.as_string())
server.quit()

print(f'Tweet sent to {recipient_email}: {tweet_text}')
