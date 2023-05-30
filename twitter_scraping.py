from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.buy_me_a_coffee import button
from streamlit_extras.mention import mention
import snscrape.modules.twitter as sntwitter
from datetime import date, timedelta
import streamlit as st
import pandas as pd
import pymongo
import io

# Page Config


st.set_page_config(page_title='Twitter Scraper', page_icon = 'Related Images and Videos/bird.png', layout = 'wide',
                                                 menu_items = {
                                                'About': """This web app allows you to scrape tweets from Twitter using the snscrape library and visualize the data using Streamlit.
This app was developed by Nirmal Kumar, a data science enthusiast and Python developer. The app is intended for educational and research purposes only, and should not be used for any commercial or unethical activities.
If you have any questions, comments, or suggestions for the app, please feel free to contact me at [nirmal.works@outlook.com]."""
                                                })

st.title(':blue[Twitter Scraper]')

add_vertical_space(2)

# Basic Inputs

option = st.radio('How would you like to search for tweets?', ('Username', 'Keyword', 'Hashtag'), key='option', horizontal = True)

add_vertical_space(1)

mention(
    label="Go to Twitter",
    icon="twitter",
    url="https://twitter.com"
    )

add_vertical_space(1)

opt, buff = st.columns([4,7])

if option == "Username":
    word = opt.text_input(label=f'Enter {option}', value="BBCEarth", help="Don't add @ before the username").removeprefix('@')
elif option == "Keyword":
    word = opt.text_input(label=f'Enter {option}', value="python")
elif option == "Hashtag":
    word = opt.text_input(label=f'Enter {option}', value="python", help="Don't add # before the tag").removeprefix('#')

add_vertical_space(1)

col1, col2, buff = st.columns([4,4,3])

tday = date.today()

start = col1.date_input(label="Start date", value=tday - timedelta(days=100), key="start")
end = col2.date_input(label="End date", value=tday, key='end')

start = start.strftime("%Y-%m-%d")
end = end.strftime("%Y-%m-%d")

add_vertical_space(1)

col1, buff = st.columns([4, 7])

no_of_tweets = col1.number_input(
                                label='How many tweets to scrape?',
                                min_value=1, max_value=1000,
                                value=10, key='no_of_tweets'
                                )

tweets_list = []

add_vertical_space(1)

scrape = st.button(label="Scrape Tweets", key='scrape')

# Function Definitions

@st.cache_data(show_spinner=False)
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

def create_df():
    tweets_df = pd.DataFrame(
                            tweets_list,
                            columns=(["Datetime", "User_ID", "Username", "Language", "TweetContent",
                                    "Source", "URL", "LikeCount", "RetweetCount", "ReplyCount"]),
                            index=range(1, len(tweets_list) + 1)
                            )
    return tweets_df

def upload_to_mongodb():
    try:
        scraped_word = word.title().removeprefix('#').removeprefix('@')
        scraped_date = tday.strftime("%d/%m/%Y")
        scraped_data = tweets_df.to_dict("records")

        scraped_doc = {
            "Scraped Word": scraped_word,
            "Scraped Date": scraped_date,
            "Scraped Data": scraped_data
        }
        
        client = pymongo.MongoClient(st.secrets['mongo_db']['URI'])
        mydb = client["Twitter"]
        collection = mydb["tweets_collection"]
        filter = {"Scraped Word": scraped_word}
        collection.replace_one(filter, scraped_doc, upsert=True)
        return scraped_word
    
    except:
        st.error("App encountered some unforeseen error... Try again later")
        return None
    
def fetch_data():
    client = pymongo.MongoClient(st.secrets['mongo_db']['URI'])
    mydb = client["Twitter"]
    collection = mydb["tweets_collection"]
    last_document = collection.find().sort("_id", -1).limit(1)
    last_word = last_document[0]["Scraped Word"]
    if last_document:
        return pd.DataFrame(last_document[0]["Scraped Data"]), last_word
    else:
        return pd.DataFrame(), last_word


# Scraping Part

if word and scrape:
    try:
        if option == 'Username':
            for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{word} since:{start} until:{end}').get_items()):
                if i > no_of_tweets - 1:
                    break
                scraped_tweet = scrape_tweets(tweet)
                tweets_list.append(scraped_tweet)
                
        elif option == 'Keyword':
            for i, tweet in enumerate(
                    sntwitter.TwitterSearchScraper(f'{word.lower()} since:{start} until:{end}').get_items()):
                if i > no_of_tweets - 1:
                    break
                scraped_tweet = scrape_tweets(tweet)
                tweets_list.append(scraped_tweet)

        elif option == 'Hashtag':
            for i, tweet in enumerate(
                    sntwitter.TwitterHashtagScraper(f'{word.lower()} since:{start} until:{end}').get_items()):
                if i > no_of_tweets - 1:
                    break
                scraped_tweet = scrape_tweets(tweet)
                tweets_list.append(scraped_tweet)
                
        tweets_df = create_df()
        upload_to_mongodb()
        st.success(body='Tweets scraped successfully...')
        
    except Exception:
        st.error(
            "Twitter server not responding. Please check your internet connection, try again later, or contact support.",
            icon="⚠️")

elif not word:
    st.warning(body=f'{option} field can\'t be left empty', icon="⚠️")

else:
    st.write('')

# Additional Facilities

tab1, tab2, tab3 = st.tabs(['SCRAPED CONTENT       ', 'UPLOAD TO YOUR DATABASE', 'DOWNLOAD'])

with tab1:
    if st.button(label = 'Show Data', key = 'show_df'):
        scraped_df, scraped_word = fetch_data()
        scraped_df.index = range(1, len(scraped_df) + 1)
        st.dataframe(scraped_df, use_container_width = True)
        
with tab2:
    
    col1, col2 = st.columns(2)
    user_mongo_string = col1.text_input(label = 'Enter your MongoDB connection string')
    push_to_mongodb = st.button(label = 'Push to your database', key = 'mongo')

    if push_to_mongodb:
        my_client = pymongo.MongoClient(st.secrets['mongo_db']['URI'])
        mydb = my_client["Twitter"]
        my_collection = mydb["tweets_collection"]
        last_document = my_collection.find().sort("_id", -1).limit(1)
        user_client = pymongo.MongoClient(user_mongo_string)
        user_db = user_client["Twitter"]
        user_collection = user_db["tweets_collection"]
        filter = {"Scraped Word": word.title()}
        user_collection.replace_one(filter, last_document, upsert=True)
        st.success("Successfully uploaded to the database")    

with tab3:
    
    col1, col2, col3 = st.columns(3)
    
    scraped_df, scraped_word = fetch_data()
    
    csv_bytes = scraped_df.to_csv(index=False).encode()
    col1.download_button("Download CSV file", data=csv_bytes,
                        file_name=f"{scraped_word.lower()}_tweets.csv".removeprefix('#').removeprefix('@'),
                        mime="text/csv")

    json_bytes = scraped_df.to_json(orient="records").encode()
    col2.download_button("Download JSON file", data=json_bytes,
                        file_name=f"{scraped_word.lower()}_tweets.json".removeprefix('#').removeprefix('@'),
                        mime="application/json")

    excel_buffer = io.BytesIO()
    scraped_df.to_excel(excel_buffer, engine ='xlsxwriter', index = False)
    excel_bytes = excel_buffer.getvalue()

    col3.download_button("Download Excel file", data = excel_bytes,
                        file_name = f'{scraped_word.lower()}_tweets.xlsx'.removeprefix('#').removeprefix('@'),
                        mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        key = 'excel'
                        )


# Document history in the sidebar

with st.sidebar.expander("Scraping History"):
    
    client = pymongo.MongoClient(st.secrets['mongo_db']['URI'])
    mydb = client["Twitter"]
    collection = mydb["tweets_collection"]

    last_5_documents = collection.find().sort("_id", -1).limit(5)

    scraped_words = []

    for document in last_5_documents:
        scraped_word = document["Scraped Word"].title()
        scraped_words.append(scraped_word)

    scrape_history = pd.DataFrame(scraped_words, columns=["Scrape History"])
    scrape_history.index = range(1, len(scrape_history) + 1)

    st.write("\n\n")
    st.dataframe(scrape_history, use_container_width=True)


with st.sidebar:
    add_vertical_space(14)
    button('nirmal.datageek', emoji='🕮', text = 'Buy me a book', floating = False)