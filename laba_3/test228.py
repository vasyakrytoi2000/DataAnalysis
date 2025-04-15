import streamlit as st
import requests
import urllib.request
import pandas as pd
import numpy as np
from datetime import datetime
import os
import glob
import seaborn as sns
import matplotlib.pyplot as plt

def download():
    old = True
    now = datetime.now()
    date_for_name = now.strftime("%d-%m-%Y-%H")
    cur_year, cur_week = now.isocalendar()[0], now.isocalendar()[1]

    pattern = "data/*_vhi_id_*.csv"  
    check_files = glob.glob(pattern)
    if check_files:
        for file in check_files:
            baza = os.path.basename(file)
            date_part = baza.split("_vhi_id_")[0]
            file_date = datetime.strptime(date_part, "%d-%m-%Y-%H")
            file_year, file_week = file_date.isocalendar()[0], file_date.isocalendar()[1]
            if (file_year, file_week) < (cur_year, cur_week):
                st.write("You have old data, wait for reinstall ...")
                all_files = glob.glob("data/*") 
                for old_file in all_files:
                    os.remove(old_file)
                for i in range(1,28):
                    url = f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={i}&year1=1981&year2={cur_year}&type=Mean"
                    vhi_url = urllib.request.urlopen(url)  
                    out = open(f"data/{date_for_name}_vhi_id_{i}.csv", 'wb')
                    out.write(vhi_url.read())
                    out.close()
                st.write("Done")
                old = False
                break
        if old:
            st.write("You alredy have nice data 👍")
    elif not check_files:
        st.write("You do not have data, wait for loading")
        for i in range(1, 28):
            url= f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={i}&year1=1981&year2=2025&type=Mean"
            vhi_url = urllib.request.urlopen(url)  
            out = open(f"data/{date_for_name}_vhi_id_{i}.csv", 'wb')
            out.write(vhi_url.read())
            out.close()
        st.write("All VHI data is downloaded...")

def dataframe():
    pattern = "data/*_vhi_id_*.csv"
    check_files2 = glob.glob(pattern)
    df_list = []
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
    col = [0,1,2,3,4,5,6]
    for file in check_files2:
        area_id = int(file.split("_vhi_id_")[1].split(".csv")[0])
        df0 = pd.read_csv(file, header = 2, names = headers, usecols = col, skipfooter=3, engine='python')
        df0['Area'] = area_id
        df_list.append(df0)

    df = pd.concat(df_list, ignore_index = True)
    df["Area"] = df["Area"].replace({
        24:1, 25:2, 5:3, 6:4, 27:5, 23:6, 26:7, 7:8, 11:9, 13:10,
        14:11, 15:12, 16:13, 17:14, 18:15, 19:16, 21:17, 22:18, 8:19, 9:20, 
        10:21, 1:22, 3:23, 2:24, 4:25, 20:26, 12:27
    })
    df = df.drop(df.loc[df['VHI'] == -1].index)
    return df
st.title("Analysis of the state of vegetation in the regions of Ukraine")
st.info("For starting use the app, you need to check your data, if you have old or just don't have data, it will be download, and if you have nice data, nothing will happen")    
is_clicked=st.button("Check data", type='primary')
if is_clicked:
    download()

df = dataframe()



#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
st.markdown("<br>", unsafe_allow_html=True) 
st.subheader("Visualization")
st.markdown("<br>", unsafe_allow_html=True) 

area_turtle = { 
    'Cherkasy' : 22,
    'Chernihiv' : 24,
    'Chernivtsi' : 23,
    'Crimea' : 25,
    'Dnipro' : 3,
    'Kyiv' : 9,
    'Lviv' : 12,
    'Odesa' : 14,
    'Kharkiv' : 19,
    'Zaporizhzhia' : 7,
    'Donetsk' : 4,
    'Luhansk' : 11,
    'Vinnytsia' : 1,
    'Ternopil' : 18,
    'Ivano-Frankivsk' : 8,
    'Sumy' : 17,
    'Poltava' : 15,
    'Rivne' : 16,
    'Khmelnytskyi' : 21,
    'Zhytomyr' : 5,
    'Mykolaiv' : 13,
    'Kherson' : 20,
    'Kyiv_City' : 27,
    'Kirovohrad' : 10,
    'Sevastopol' : 26,    
    'Transcarpathia' : 6,
    'Volyn' : 2,
    'None' : None
}

default_values = {
        "indicator" : 'VCI',
        "area1" : 'Cherkasy',
        "area2" : 'Cherkasy',
        "week" : [1, 52],
        "year" : [1982, 2024],
        "compare" : False,
        "sort_down" : False,
        "sort_up" : False
    }

if 'number_of_rows' not in st.session_state:
    st.session_state['number_of_rows'] = 5

col1, col2 = st.columns([3, 10])
with col1:
    #reset
    def reset():
        for key, value in default_values.items():
            st.session_state[key] = value
        st.session_state["number_of_rows"] = 5

    #index
    indecators_list = ['VCI', 'TCI', 'VHI']
    indicator_box = st.selectbox("", indecators_list, label_visibility= "collapsed", key= "indicator")

    #area
    area_names = list(area_turtle.keys()) 
    area_box1 = st.selectbox("", area_names, label_visibility="collapsed", key = "area1")
    compare_area = st.empty()
    area_box2 = 'None'
    compare_2 = st.checkbox("Compare with another one ...... (use only on tab3!)", key="compare", )
    if compare_2:
        area_box2 = compare_area.selectbox("Only for tab 3", area_names, label_visibility="collapsed", key = "area2")
    
    #week
    min_week = df['Week'].values.min()
    max_week = df['Week'].values.max()
    min_w, max_w = st.slider(
        "", min_value=min_week, max_value=max_week,value=(min_week, max_week), step=1, key = "week"
        ) 
      
    #year
    min_year = df['Year'].values.min()
    max_year = df['Year'].values.max()
    min_y, max_y = st.slider(
        "", min_value=min_year, max_value=max_year, value=(min_year, max_year) , step=1, key = "year"
        )
 
    col3, col4 = st.columns([1, 1])
    with col3:
        if st.button("➕ row"):
            st.session_state['number_of_rows'] += 1

        srt_up = st.checkbox("Sort up", key= "sort_up")  

        st.button("Reset", on_click=reset, type="primary")

    with col4:
        if st.button("➖ row"):
            st.session_state['number_of_rows'] -= 1

        srt_dwn = st.checkbox("Sort down", key= "sort_down")

    if srt_up and srt_dwn:
        st.warning("Use only one sorting!")
        srt_dwn = False
    elif srt_up:
        df = df.sort_values(by=indicator_box, ascending=True)
    elif srt_dwn:
        df = df.sort_values(by=indicator_box, ascending=False)
    
with col2:
    tab1, tab2, tab3 = st.tabs(["Table", "Plot1", "Plot2"])

    with tab1:
        st.table(df.head(st.session_state['number_of_rows'])) 
    
    with tab2:
        sns.set_theme(style="darkgrid")
        df_tab2 = df[
            (df['Area'] == area_turtle[area_box1]) &
            (df['Year'] >= min_y) & (df['Year'] <= max_y) & 
            (df['Week'] >= min_w) & (df['Week'] <= max_w) 
            ]
        df_tab3 = df[
            (df['Area'] == area_turtle[area_box1]) |
            (df['Area'] == area_turtle[area_box2]) &
            (df['Year'] >= min_y) & (df['Year'] <= max_y) & 
            (df['Week'] >= min_w) & (df['Week'] <= max_w) 
            ]
        inv_turtle_area = {v: k for k, v in area_turtle.items()}

        df_tab3['AreaName'] = df_tab3['Area'].map(inv_turtle_area)

        if min_y == max_y:
            plt.figure(figsize=(12,8))
            sns.lineplot(data=df_tab2, x = 'Week', y=indicator_box)
            st.pyplot(plt)
        elif min_y == max_y and min_w == max_w:
            plt.figure(figsize=(12,8))
            sns.scatterplot(data=df_tab2, x = 'Week', y=indicator_box)
            st.pyplot(plt)
        else:
            plt.figure(figsize=(12,8))
            sns.lineplot(data=df_tab2, x = 'Year', y=indicator_box)
            plt.title(area_box1)
            st.pyplot(plt)
        
    with tab3:
        if compare_2:
            if min_y == max_y:
                plt.figure(figsize=(12,10))
                sns.lineplot(data=df_tab3, x = 'Week', hue="AreaName", y=indicator_box, palette=['red', 'green', 'blue'])
                st.pyplot(plt)
            elif min_y == max_y and min_w == max_w:
                plt.figure(figsize=(12,10))
                sns.scatterplot(data=df_tab3, x = 'Week', hue="AreaName", y=indicator_box, palette=['red', 'green', 'blue'])
                st.pyplot(plt)
            else:
                plt.figure(figsize=(12,10))
                sns.lineplot(data=df_tab3, x = 'Year', hue="AreaName", y=indicator_box, palette=['red', 'green', 'blue'])
                st.pyplot(plt)
        else:
            if min_y == max_y:
                df_for_all = df[
                    (df['Area'] != area_turtle[area_box1]) &
                    (df['Year'] == min_y) & 
                    (df['Week'] >= min_w) & (df['Week'] <= max_w)
                    ]
            else :
                df_for_all = df[
                    (df['Area'] != area_turtle[area_box1]) &
                    (df['Year'] >= min_y) & (df['Year'] <= max_y) & 
                    (df['Week'] >= min_w) & (df['Week'] <= max_w)
                    ]
                
            avg_all = df_for_all.groupby("Area")[indicator_box].mean().reset_index()
            avg_choosed = df_tab2.groupby("Area")[indicator_box].mean().reset_index()
            avg = pd.concat([avg_all, avg_choosed])
            avg['AreaName'] = avg['Area'].map(inv_turtle_area)
            if srt_up:
                avg = avg.sort_values(by=indicator_box, ascending=True)
            elif srt_dwn:
                avg = avg.sort_values(by=indicator_box, ascending=False)

            paletakyrwa = {area_name: 'purple' for area_name in avg['AreaName'].unique()}  
            paletakyrwa[area_box1] = 'red'

            plt.figure(figsize=(12,10))
            sns.barplot(data=avg, x = indicator_box, y="AreaName", orient='h', palette=paletakyrwa)
            st.pyplot(plt)
            