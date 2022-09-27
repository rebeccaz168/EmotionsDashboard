# kona

## Description

This app creates a dashboard that allows MVPs to see how employees are doing at a glance. It takes prior collected slack data and creates two visualizations: a pie chart of RGYs, and a word plot of most frequently expressed emotions. Lastly the comments are displayed in reverse chronological order. 
The displays are filtered based on organizationId, groupId, and userId. 

## Dependencies 
streamlit, matplotlib, pandas, wordcloud, and datetime libraries are being used. 

## Executing Program 
From the terminal run : streamlit run app.py

## Future developments 
The data was all from the same day but if more dates were added, time would be used as another query criteria. Furthermore, some form of caching could be used to hold recent displayed data. 
