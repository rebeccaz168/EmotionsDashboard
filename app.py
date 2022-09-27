import pandas as pd;
import matplotlib.pyplot as plt
import streamlit as st; 
import csv;
from wordcloud import WordCloud;
from datetime import datetime;


@st.cache
def loadData():
    data = pd.read_csv(r'rygs.csv');
    data = pd.DataFrame(data, columns = ['Timestamp','Elaboration', 'Emotion', 'Selection', 'SlackOrgId', 'SlackTeamId', 'SlackUserId']);
    data['Timestamp'] = pd.to_datetime(data['Timestamp']);
    print(data['Timestamp']);
    return data; 
# create a subset of data for just that day 

# build the filters 
def buildFilters(df): 
    slackOrgId = st.sidebar.multiselect(
        "Select the Organization:", 
        options = df["SlackOrgId"].unique(), 
        default = df["SlackOrgId"].unique()
    );

    df_org_selected = df.query(
         "SlackOrgId == @slackOrgId"
    );

    slackTeamId = st.sidebar.multiselect(
        "Select the Team Id", 
        options = df_org_selected["SlackTeamId"].unique(), 
    );

    df_team_selected = df.query(
        "SlackTeamId == @slackTeamId"
    );

    slackUserId = st.sidebar.multiselect(
        "Select the User Id", 
        options = df_team_selected["SlackUserId"].unique(), 
    );

    df_selection = df.query(
        "SlackUserId == @slackUserId"
    );

    # no user selected
    if len(df_selection) == 0 and len(df_team_selected) == 0: 
        return df_org_selected;
    elif len(df_selection) == 0:
        return df_team_selected;
    else:
        return df_selection;

# for a specific org and slack group, create a wordcloud for all of the emotions
def createBarChart(filtered): 
    emotions = filtered[['Emotion', 'Timestamp', 'Elaboration']].drop_duplicates().dropna();
    emotionsString = " ".join(emotion for emotion in emotions['Emotion']).strip("_");
    if len(emotionsString) == 0: 
        return;
    st.subheader("Emotions Wordcloud");
    fig, ax = plt.subplots();
    fig.set_facecolor('lightgrey');
    wordcloud = WordCloud(collocations = False, background_color = 'lightgrey').generate(emotionsString);
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off");
    plt.show();
    st.pyplot(fig);

# bar chart for RGY for selected User, org, and group 
def createPieChart(filtered):
    st.subheader("Overall RGYs");
    filtered.set_index(['Selection'], inplace=True)
    all_selections = filtered.groupby(['Selection'], as_index=False).size();
    colors = all_selections['Selection'];
    selections = filtered.groupby(['Selection']).size();
    fig1, ax1 = plt.subplots();
    fig1.set_facecolor('lightgrey');
    ax1.pie(selections, colors = colors, autopct='%1.1f%%', wedgeprops={'alpha':0.5});
    st.pyplot(fig1);

# for a specific user, display the comments ==> sort by most recent 
def displayComments(filtered):
    st.subheader("Recent messages:");
    filtered = filtered.sort_values(by="Timestamp");
    comments = filtered['Elaboration'].drop_duplicates().dropna();
    count = 0 ;
    for comment in comments: 
        st.text(comment);
    #if no comments currently display no current comments 
    if len(comments) == 0:
        st.text("no recent elaboration")


def main():
    data = loadData();
    filteredData = buildFilters(data);
    # here is the menu 
    st.title('Daily Well-being Check 🐶');
    createPieChart(filteredData);
    createBarChart(filteredData);
    displayComments(filteredData);
    

if __name__ == "__main__":
    main()