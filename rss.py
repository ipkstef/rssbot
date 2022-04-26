import feedparser
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
import os

d = feedparser.parse('https://yts.mx/rss')

webhookurl = os.getenv('WEBHOOKURL')

webhook = DiscordWebhook(url=webhookurl, rate_limit_retry=True)

day_parsed = str(d.feed.updated_parsed[2])

movies_list = []

movie_title_duplicates = []
movie_title_clean = []

with open('last_date' + '.txt', 'r') as f:
    last_date = f.read()



#save this for later
class Movie:
    def __init__(self, title, image, date, link, description):
        self.title = title
        self.image = image
        self.date = date
        self.link = link
        self.description = description

    def __str__(self):
        return f'{self.title, self.image, self.date, self.link, self.description}'


for title in d.entries:
    if title.title:
        if title.title.find('1080p') != -1:
            movie_title_duplicates.append(title.title)
            for title in movie_title_duplicates:
                if title not in movie_title_clean:
                    if title.find('1080p') != -1:
                        movie_title_clean.append(title)
                    
                    

if int(day_parsed) > int(last_date):
    for entry in d.entries:
        if entry.title in movie_title_clean:
            # print('entry title:', entry.title)
            img_src = entry.description.split('src="')[1].split('"')[0]
            title = entry.title
            link = entry.link
            date = entry.updated_parsed[2]
            description = entry.description
            print(description)
            embed = DiscordEmbed(title=title, description=description, color=0x00ff00)
            embed.set_image(url=img_src)
            embed.set_timestamp()
            embed.set_url(url=link)
            webhook.add_embed(embed)
            movies = Movie(title=title, image=img_src, date=date , link=link, description=description)
            movies_list.append(str(movies))
            response = webhook.execute(remove_embeds=True)
            time.sleep(1)
            
        with open('last_date' + '.txt', 'w') as f:
            f.write(str(day_parsed))
            f.close()
    
        with open( 'movielist' + '.txt', 'w') as f:
            f.write((str(movies_list)))
    else:
        print('No new movies')
        pass
else:
    print('last date is not older than current date')
    pass
        
           
