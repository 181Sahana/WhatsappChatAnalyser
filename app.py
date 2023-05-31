import streamlit as st
import preprocessor, helper
import pandas as pd
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp chat analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    # this file will be stream of byte data
    data = bytes_data.decode("utf-8")

    # st.text(data)
    df = preprocessor.preprocess(data)

    #print(type(df))
    st.dataframe(df)

    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    #print(type(user_list))
    selected_user = st.sidebar.selectbox("show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media shared")
            st.title(num_media_messages)

        with col4:
            st.header("Total Links")
            st.title(num_links)

        if selected_user == "Overall":
            st.title("Most Busy user")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # Word Cloud
        st.title("WordCloud ")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        most_common_df = helper.most_common_words(selected_user, df)

        st.dataframe(most_common_df)




