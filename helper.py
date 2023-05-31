from urlextract import URLExtract
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
#this library gives methods to extract urls
extract = URLExtract()#create an object to extract links
def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    #counts the number of message sent by the user
    num_messages = df.shape[0]

    #counts the number of words in a overall message sent by the user
    words = []
    for message in df['message']:
        words.extend(message.split())

    #counts the number of media shared
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    #fetches the number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user' : 'percent'})
    return x, df

def create_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

#most common words
def most_common_words(selected_user, df):

    f = open('stop_words_english.txt', encoding='utf8')
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)


    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df




