# Twitter scraping web app

Twitter is a powerful platform for accessing real-time information, and it can be a valuable source of data for a variety of applications. However, collecting and analyzing data from Twitter can be a challenging task, especially for those without specialized technical skills. In this context, a web app that simplifies the process of scraping Twitter data and provides useful features for analyzing and visualizing the data can be a useful tool for researchers, journalists, businesses, and individuals. This is an open source web app that allows you to scrape tweets from Twitter using the snscrape library, visualize the data using Streamlit and upload the scraped content to Mongo DB for future usage. It has been developed by me, Nirmal Kumar, a Data science enthusiast and Python developer. The app is intended for educational and research purposes only, and should not be used for any commercial or unethical activities.

## Prerequisites

Before you begin, you will need to have a few tools installed on your machine:

* Python 3.7 or higher.
    [Note: Streamlit only supports .py files as of now. So, notebook(.ipynb) files are not recommended]
* MongoDB software.
* The snscrape, pandas and streamlit, pymongo packages.

#### Python

Python is the programming language used to develop this project. It is a popular high-level programming language known for its readability and versatility. It is widely used for web development, data analysis, and machine learning. It provides a powerful and flexible foundation for scraping and analyzing Twitter data.

#### MongoDB

MongoDB is a cross-platform document-oriented database program. It uses JSON-like documents with optional schemas and is classified as a NoSQL database. We used it here to store the scraped Twitter data. It provides a flexible and scalable solution for managing large amounts of data.

#### SNScrape

SNScrape is a Python library that allows you to scrape social media data without using an API or request limits. Moreover, you don't even need an active account to scrape content when you use snscrape. It supports a variety of platforms including Twitter, Facebook, and Instagram. We used it here to scrape tweets from Twitter. It provides greater flexibility and control over the data we collect.

#### Streamlit

Streamlit is an open-source Python library that makes it easy to create and share custom web apps for machine learning and data science. We used it here to deploy our project as a web app. It makes it easy to create an interactive user interface for exploring and visualizing the scraped Twitter data.

#### PyMongo

PyMongo is a Python distribution containing tools for working with MongoDB. We used it here to connect to a MongoDB server and perform database operations using Python.

#### Pandas

Pandas is a popular Python library used for data manipulation and analysis. We used pandas to convert scraped tweets list into dataframe and to convert dataframe into .csv, .json and .dict formats

## Ethical perspective of scraping tweets using streamlit

Scraping tweets using Streamlit is legal, but it is important to ensure that you are not violating any applicable laws or the terms of service of Twitter. It is always recommended to obtain explicit consent from Twitter users before scraping their tweets, and to use ethical and responsible scraping practices. Streamlit provides a convenient way to scrape up to 100,000 tweets, which is considered to be well within Twitter's guidelines and framework.

## Features

* ##### Search and Filter: You can search and filter the scraped tweets based on various criteria such as hashtags, keywords, and dates. This feature makes it easy to find relevant tweets for analysis or research purposes.

* ##### Display Results: The app allows for easy creation of user interfaces. You can view the scraped tweets in an interactive and visually appealing way. But here I just used dataframe to display the scraped tweets.

* ##### Download Data: You can easily download the scraped tweets in various formats such as CSV or JSON, making it easy to use the data in other applications or for further analysis.

* ##### Save to MongoDB: The app also provides the option to upload the scraped tweets to MongoDB using the PyMongo library. This allows for easy storage and retrieval of large volumes of data.

* ##### View saved collection history: You can view what collections you uploaded previously to MongoDB server.

## User Guide

1. Go to the web app URL in your web browser.
2. Choose the type of search - **Keyword** or **Hashtag**
3. Enter the keyword/hashtag of your choice
4. Set **Start Date** and an **End Date**. By default start date will be 100 days before today
5. You can also view your selected options under the **Details Pane:** in the sidebar to ensure accuracy.
6. Select number of tweets to scrape
7. Click on the **Scrape Tweets** button
8. Use the two tabs – **SHOW**, **DOWNLOAD** – to view the scraped data then and there and you can download scraped tweets in .csv or .json format
9. In the sidebar  you can  **UPLOAD DATA TO MONGO_DB**  and you can view the **COLLECTIONS HISTORY**

## Developer Guide

To run the app, follow these steps:

    1. Clone the repository to your local machine using the following command: git clone [https://github.com/Nirmal7781/Twitter_scrapping.git].
    2. Install the required libraries by running the following command: pip install -r requirements.txt.
    3. Open the twitter_scraper.py file in a code editor.
    4. Open a terminal window and navigate to the directory where the app is located using the following command: cd [.py file directory].
    5. Run the command streamlit run twitter_scraper.py to start the app.
    6. The app should now be running on a local server. If it doesn't start automatically, you can access it by going to either 
        * Local URL: [http://localhost:8501] or * Network URL: [http://192.168.43.83:8501].

To modify the app, you can:

    1. Add filters to the search results table to allow users to sort and filter the results.
    2. Add a visualization of the search results, such as a word cloud or a chart.
    3. Allow users to save their search queries for future use.
    4. Use machine learning algorithms to perform sentiment analysis on the tweets and display the results.

## Potential Applications

1. Social media monitoring: A company can use the app to monitor mentions of its brand on Twitter and analyze the sentiment of those mentions.

2. Influencer marketing: An influencer can use the app to track their own social media presence and engagement metrics, or to identify other influencers in their industry.

3. Market research: A business can use the app to monitor conversations about their industry on Twitter and gather insights on consumer behavior, preferences, and trends.

4. News and journalism: A journalist can use the app to track breaking news and trending topics on Twitter and gather data for a news story.

5. Academic research: A researcher can use the app to collect data from Twitter for academic studies, such as sentiment analysis or social network analysis.

6. Political analysis: A political analyst can use the app to monitor public opinion on political issues and track the social media activity of political candidates and parties.

## Potential issue with the app

1. Before knowing about this issue let's know a bit about session_state in streamlit.

    ### What is session state and why it came into picture?

    Session state is a powerful feature in Streamlit that allows for the creation of dynamic and interactive apps with a more reactive user interface. Session state came into the picture because **Streamlit is a stateless framework**, which means that **each time a user interacts with the app, the entire script is re-executed from top to bottom**. This can lead to performance issues and can make it difficult to create interactive apps that rely on storing user data across multiple interactions.

    To solve this problem, Streamlit introduced the session state feature, which allows the app to store and retrieve data across multiple interactions without the need to re-execute the entire script. This makes it easier to create dynamic and interactive apps that can respond to user input in real-time.

    Thus, session state came into the picture to solve the problem of state management in stateless frameworks like Streamlit.

  Now the potential issue here is eventhough session_state is a powerful feature it's still under development and this could cause the app to rerun on its own from top to bottom even if we use session_state feature to prevent this action.

2. This app would work extremely well and good every aspect that I have mentioned above in local server. But when you deploy it in cloud you can't uuse pymongo there to upload the dataset to MongoDB. This is a persistent issue that most developers acknowledge this issue in streamlit community forum and we have to wait a bit more to get this rectified.
    ![The issue mentioned above]()
    ![Sample for streamlit community's acknowledgement of the issue]()

## Web App Snap

![Twitter Scraper](https://github.com/Nirmal7781/Twitter_scrapping/blob/888c4af80f2ff4ce6cccdedd992584db1f30cb8f/ts_web_app.png)

## Web App Demo Video

[Demo Video][https://www.linkedin.com/posts/nirmal-kumar-600203263_twitter-datascience-webapp-activity-7049124308266225664-8jWQ?utm_source=share&utm_medium=member_desktop]

## Streamlit web URL

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://nirmal7781-twitter-scrapping-twitter-scraping-t11msc.streamlit.app/)

## Disclaimer

This application is intended for educational and research purposes only and should not be used for any commercial or unethical activities.

## Contact

If you have any questions, comments, or suggestions for the app, please feel free to contact me at [nirmal.works@outlook.com]