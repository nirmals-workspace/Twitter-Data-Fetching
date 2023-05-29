# Required packages:

import snscrape.modules.twitter as sntwitter
from datetime import date, timedelta
import streamlit as st
import pandas as pd
import pymongo
import io



st.set_page_config(page_title='Twitter Scraper', page_icon = 'Related Images and Videos/bird.png', layout = 'wide',
                                                 menu_items = {
                                                'About': """This web app allows you to scrape tweets from Twitter using the snscrape library and visualize the data using Streamlit.
This app was developed by Nirmal Kumar, a data science enthusiast and Python developer. The app is intended for educational and research purposes only, and should not be used for any commercial or unethical activities.
If you have any questions, comments, or suggestions for the app, please feel free to contact me at [nirmal.works@outlook.com]."""
                                                })

st.title(':red[Twitter Scraper]')



option = st.radio('How you would like to search for tweets ?',('Keyword', 'Hashtag'), horizontal = True, key = 'option')

if option == "Keyword":
    word = st.text_input(label = f'Enter {option}', value = "python")
elif option == "Hashtag":
    word = st.text_input(label = f'Enter {option}', value = "python", help = "Don't add # before the tag")


tday = date.today()
col1, col2 = st.columns(2)

start = col1.date_input(label = "Start date",  value = tday - timedelta(days = 100), key = "start")
end = col2.date_input(label = "End date", value = tday, key = 'end')
    
no_of_tweets = st.slider(
                         label = 'How many tweets to scrape ?',
                         min_value = 1, max_value = 1000,
                         value = 1, key = 'no_of_tweets'
                         )

tweets_list = []
scrape_button = st.button(label = "Scrape Tweets", key = 'scrape')

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

if word and scrape_button:
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
        st.success(body = 'Tweets scraped successfully...')
    except Exception:

        st.error("Twitter server not responding. Please check your internet connection, try again later or contact support.", icon = "⚠️")

elif not word:
    st.warning(body = f'{option} field can\'t be left empty', icon = "⚠️")

else:
    st.write('')
    

tweets_df = pd.DataFrame(
                         tweets_list,
                         columns = (["Datetime", "User_ID", "Username", "Language", "TweetContent",
                                     "Source", "URL", "LikeCount", "RetweetCount", "ReplyCount"]),
                         index=range(1, len(tweets_list) + 1)
                         )


exp = st.expander('See scraped content')

exp.dataframe(tweets_df, use_container_width = True)


col1, col2, col3 = st.columns(3)

# For Downloading csv file
tweets_csv = tweets_df.to_csv()
col1.download_button(
                        "Download CSV file", data = tweets_csv,
                        file_name = f'{word.lower()}_tweets.csv'.removeprefix('#'),
                        mime = 'text/csv', key = 'csv'
                        )

#For Downloading json file
tweets_json = tweets_df.to_json(orient ='records')
col2.download_button(
                        "Download JSON file", data = tweets_json,
                        file_name = f'{word.lower()}_tweets.json'.removeprefix('#'),
                        mime = 'application/json', key = 'json'
                        )

#For Downloading excel file
excel_buffer = io.BytesIO()
tweets_df.to_excel(excel_buffer, engine ='xlsxwriter', index = False)
excel_bytes = excel_buffer.getvalue()

col3.download_button("Download Excel file", data = excel_bytes,
                    file_name = f'{word.lower()}_tweets.xlsx'.removeprefix('#'),
                    mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    key = 'excel'
                    )
    

# Uploading the scraped data into MongoDB:

with st.sidebar:
    st.subheader('Upload data to MongoDB')
    
    upload = st.button(label = "Upload", key = 'upload')
    
    @st.cache_resource
    def init_connection():
        return pymongo.MongoClient(**st.secrets["mongo_db"])
    
    if upload:
        try:
            # Set the scraped word, date and data
            scraped_word = word.title()
            scraped_date = tday.strftime('%d/%m/%Y')
            scraped_data = tweets_df.to_dict("records") 

            # Create a dictionary with the scraped data
            scraped_doc = {'Scraped Word': scraped_word,
                            'Scraped Date': scraped_date,
                            'Scraped Data': scraped_data}
            
            client = init_connection()
            mydb = client["Twitter"]
            collection = mydb['tweets_collection']
            filter = {'Scraped Word': scraped_word}
            collection.replace_one(filter, scraped_doc, upsert=True)
            st.success(body = 'Successfully uploaded to database', icon = '✅')
        except:
            st.error("App encountered some unforeseen error... Try again later")

with st.sidebar:
    
    expander = st.expander("See Upload History")
        
    client = init_connection()
    mydb = client["Twitter"]
    collection = mydb['tweets_collection']

    last_5_documents = collection.find().sort("_id", -1).limit(5)

    scraped_words = []

    for document in last_5_documents:
        scraped_word = document['Scraped Word'].title()
        scraped_words.append(scraped_word)

    document_history = pd.DataFrame(scraped_words, columns=["Document History"])
    document_history.index = range(1, len(document_history) + 1)
    
    expander.write("\n\n")
    expander.markdown('### Document History')
    expander.write("\n\n")
    expander.write(document_history)