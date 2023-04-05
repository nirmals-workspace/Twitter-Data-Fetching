# Required packages:

import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import pymongo
from datetime import date, timedelta


# Set page config, title, favicon and app header:

st.set_page_config(page_title='Twitter Scraper', page_icon = 'bird.png',
                                                 menu_items = {
                                                'About': """This web app allows you to scrape tweets from Twitter using the snscrape library and visualize the data using Streamlit.
This app was developed by Nirmal Kumar, a data science enthusiast and Python developer. The app is intended for educational and research purposes only, and should not be used for any commercial or unethical activities.
If you have any questions, comments, or suggestions for the app, please feel free to contact me at [nirmal.works@outlook.com]."""
                                                })

st.title('_:red[Twitter Scraper]_')


# Required variables:

option = st.radio('How you would like to search for tweets:',('Keyword', 'Hashtag'), horizontal = True)

if option == "Keyword":
    word = st.text_input(f'{option}', "Python")
elif option == "Hashtag":
    word = st.text_input(f'{option}', "Python", help = "Don't add # before the tag")

### Getting input for start date and end date and putting them side by side:

tday = date.today()
col1, col2 = st.columns(2)
with col1:
    start = st.date_input("Start date", tday - timedelta(days = 100))
with col2:
    end = st.date_input("End date", tday)
    
no_of_tweets = st.slider('How many tweets to scrape', 1, 1000, 1)

tweets_list = []
scrape_button = st.button("Scrape Tweets")

# Function definition to scrape just the data that we need to make it resource:

def scrape_tweets(tweet):
    date = tweet.date.strftime('%d/%m/%Y %H:%M:%S')
    user_id = tweet.user.id
    user = tweet.user.username
    language = tweet.lang
    content = tweet.rawContent
    source = tweet.source
    url = tweet.url
    likes = tweet.likeCount
    retweets = tweet.retweetCount
    replies = tweet.replyCount
    return [date, user_id, user, language, content, source, url, likes, retweets, replies]

if word:
    try:
        if option == 'Keyword':
            for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{word} since:{start} until:{end}').get_items()):  
                if i > no_of_tweets - 1:
                    break
                scrapped_tweet = scrape_tweets(tweet)
                tweets_list.append(scrapped_tweet)

        elif option == 'Hashtag':
            for i,tweet in enumerate(sntwitter.TwitterHashtagScraper(f'{word} since:{start} until:{end}').get_items()):
                if i > no_of_tweets - 1:
                    break            
                scrapped_tweet = scrape_tweets(tweet)
                tweets_list.append(scrapped_tweet)

    except Exception as e:

        st.error("Twitter server not responding. Please check your internet connection, try again later or contact support.", icon = "⚠️")
        st.stop()

else:
    st.warning(option, ' field can\'t be left empty', icon = "⚠️")
    st.stop()
        
# Creating dataframe out of scraped data:

tweets_df = pd.DataFrame(tweets_list, columns = (["Datetime", "User_ID", "Username", "Language", "TweetContent",
                                                  "Source", "URL", "LikeCount", "RetweetCount", "ReplyCount"]))
tweets_df.index = range(1, len(tweets_df) + 1)

# Creating 2 tabs to carry out 2 different actions with the data scrapped:

show, download = st.tabs(["SHOW", "DOWNLOAD"])

# Displaying scraped data stored in dataframe:

with show:
    if st.button("Show"):
        st.dataframe(tweets_df)

# Downloading the scraped data in deirable formats:

with download:
    
    col1, col2 = st.columns(2)

    # For Downloading csv file
    tweets_csv = tweets_df.to_csv()
    col1.download_button("Download CSV file", data = tweets_csv, file_name = f'{word}.csv', mime = 'text/csv')

    #For Downloading json file
    tweets_json = tweets_df.to_json(orient ='records')
    col2.download_button("Download JSON file", data = tweets_json, file_name = f'{word}.json', mime = 'application/json')

# Uploading the scraped data into MongoDB:

with st.sidebar:
    st.write('# MongoDB')
    st.write('### Upload Data')

    # Set the scraped word, date and data
    scraped_word = word
    scraped_date = tday.strftime('%d/%m/%Y')
    scraped_data = tweets_df.to_dict("records") 

    # Create a dictionary with the scraped data
    scraped_doc = {'Scraped Word': scraped_word,
                    'Scraped Date': scraped_date,
                    'Scraped Data': scraped_data}
    
    uri = st.text_input('Enter your MongoDB URI', 'mongodb://localhost:27017/')
    upload = st.button("UPLOAD")

    # --- Initialising SessionState ---
    
    if "upload_state" not in st.session_state:
        st.session_state.upload_state = False

    if upload or st.session_state.upload_state:
        st.session_state.upload_state = True

        client = pymongo.MongoClient(uri)
        mydb = client["Twitter"]
        collection = mydb[f'{word}_tweets']
        collection.insert_one(scraped_doc)
        st.success('Successfully uploaded to database', icon="✅")

with st.sidebar:
    client = pymongo.MongoClient(uri)
    mydb = client["Twitter"]
    collection_history = pd.DataFrame(mydb.list_collection_names(), columns=["Collection History"])
    collection_history.index = range(1, len(collection_history) + 1)
    st.write("\n\n")
    st.markdown('### Collection History')
    st.dataframe(collection_history, use_container_width=True)
