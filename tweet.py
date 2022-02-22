import tweepy
import time
import os

from PIL import Image
from PIL import ImageDraw

from keys import ACCESS_KEY, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET, COLOR_BOT_ID, COLOR_BOT_USERNAME, COLOR_PALETTE_USERNAME, PANTONE_BOT_USERNAME
from palette import Palette

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

COLOR_BOT_ID = COLOR_BOT_ID

def generate_palette(color):
    palette = Palette(color)
    return palette

def generate_palette_image(palette):
    img = Image.new('RGBA', (600,335), '#fff')

    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (120, 335)], fill = palette.main)
    draw.rectangle([(120, 0), (240, 335)], fill = palette.secondary)
    draw.rectangle([(240, 0), (360, 335)], fill = palette.complementary)
    draw.rectangle([(360, 0), (480, 335)], fill = palette.split_complementary)
    draw.rectangle([(480, 0), (600, 335)], fill = palette.neutral)
    
    img.save(palette.main + '-palette.png')
    return img

def hex_string(hex):
    return '#' + hex.split('#')[1]

def generate_palette_tweet(tweet, hex, reply_id):
    palette = generate_palette(hex)
    generate_palette_image(palette)

    filename = hex + '-palette.png'
    status = f'{hex_string(palette.main)}, {hex_string(palette.secondary)}, {hex_string(palette.complementary)}, {hex_string(palette.split_complementary)}, {hex_string(palette.neutral)}'

    api.retweet(tweet.id) 
    api.update_with_media(filename, status = status) 
    os.remove(filename)
    
def reply_to_tweets(since_palette_id):
    print('Replying to tweets...')
    every_color_tweets = api.user_timeline(user_id = COLOR_BOT_ID, since_id = since_palette_id, count = 3)

    for tweet in reversed(every_color_tweets):
        print('found new @everycolorbot color!')
        # print(str(tweet.id) + ' - ' + tweet.text)

        full_text = tweet.text.split(' ')[0]
        hex = '#' + full_text.split(" ")[0][2:8]
        generate_palette_tweet(tweet, hex, COLOR_BOT_USERNAME)

def get_last_color_reply():
    print('Getting most colorbot reply...')
    # reply = api.user_timeline(id = COLOR_PALETTE_USERNAME, in_reply_to_screen_name = COLOR_BOT_USERNAME, count = 1)
    reply = api.user_timeline(id = COLOR_PALETTE_USERNAME, count = 2)

    # print(reply[0])
    try:
        return reply[1].retweeted_status.id
    except:
        return reply[0].retweeted_status.id
    return None

while True:
    print('Running bot...')
    last_replied_color_id = get_last_color_reply()
    if last_replied_color_id is not None:
        reply_to_tweets(last_replied_color_id)
    time.sleep(60)

# last_replied_color_id = get_last_color_reply()
