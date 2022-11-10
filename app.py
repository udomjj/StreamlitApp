import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title='Midterm Results')
st.header('Midterm Results 2022')
st.subheader('Was the test helpful?')

### --- LOAD DATAFRAME
excel_file = 'Midterm_Results.xlsx'
sheet_name = 'DATA'

df = pd.read_excel(excel_file,
                   sheet_name=sheet_name,
                   usecols='B:D',
                   header=3)

df_students = pd.read_excel(excel_file,
                                sheet_name= sheet_name,
                                usecols='F:G',
                                header=3)
df_students.dropna(inplace=True)

# --- STREAMLIT SELECTION
scrange = df['Range'].unique().tolist()
# scores = df['Score'].unique().tolist()
scores = df['Score'].tolist()

score_selection = st.slider('Score:',
                        min_value= min(scores),
                        max_value= max(scores),
                        value=(min(scores),max(scores)))

scrange_selection = st.multiselect('Range:',
                                    scrange,
                                    default=scrange)

# --- FILTER DATAFRAME BASED ON SELECTION
mask = (df['Score'].between(*score_selection)) & (df['Range'].isin(scrange_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_result}*')

# --- GROUP DATAFRAME AFTER SELECTION
df_grouped = df[mask].groupby(by=['Range']).count()[['Score']]
df_grouped = df_grouped.rename(columns={'Score': 'Votes'})
df_grouped = df_grouped.reset_index()

# --- PLOT BAR CHART
bar_chart = px.bar(df_grouped,
                   x='Range',
                   y='Votes',
                   text='Votes',
                   color_discrete_sequence = ['#F63366']*len(df_grouped),
                   template= 'plotly_white')
st.plotly_chart(bar_chart)

# --- PLOT PIE CHART
pie_chart = px.pie(df_students,
                title='Total No. of Students',
                values='Students',
                names='Students')

# st.plotly_chart(pie_chart)

# --- DISPLAY IMAGE & DATAFRAME
col1, col2 = st.columns(2)
# image = Image.open('images/room.jpg')
# col1.image(image,
#         caption='Photo by Udom',
#         use_column_width=True)
col2.plotly_chart(pie_chart)
        
col1.dataframe(df[mask])