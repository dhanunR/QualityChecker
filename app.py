import os
import io
import re
import sys
from select import select
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np

st.title("Error Makers Quality Checker")
st.write("This application will allow you to upload your dataset and run a quality check on it.")
st.markdown("---")




# Uploading the dataset
st.subheader("Upload your files here : ")

upload_data = st.file_uploader("Choose a CSV file", type = ['CSV'])
if upload_data is not None:
    read_data = pd.read_csv(upload_data, encoding='latin-1',on_bad_lines='skip')


# Looking at your dataset
st.write("Dataset Overview : ")
try:
    number_of_rows = st.slider("No of rows:",5,10)
    head = st.radio("View from Top or Bottom",('Head','Tail'))
    if head=='Head':
        st.dataframe(read_data.head(number_of_rows))
    else:
        st.dataframe(read_data.tail(number_of_rows))
except:
    st.info("KINDLY UPLOAD YOUR CSV FILE !!!")
    st.stop()

# Dataset Shape
st.write("Rows and Columns size : ")
st.write(read_data.shape)

# Dataset Summary
st.write("Descriptive Statistics of your dataset : ")
st.write(read_data.describe())
st.markdown("---")

# information about the Datatype
if st.button('Datatypes:',key=0):
    buffer = io.StringIO()
    read_data.info(buf=buffer)
    s = buffer.getvalue()
    with open("dataset_info.txt", "w", encoding="utf-8")as f:
       f.write(s)
       st.download_button(label="Download",data= s,file_name='Datasetinfo.txt',mime='text')
    #st.write(s)

st.markdown("---")



# More Exploration
st.subheader("Explore your Dataset More :")
st.markdown("---")

# total number of Unique Values
if st.button('Total Number of Unique Values:',key=1):
    st.write("Total Number of Unique Values :")
    st.write(read_data.nunique())
st.markdown("---")


    

#Checking for Null Values : 
if st.button(label='Checking for Missing Values',key=2): 
    null_values = read_data.isnull().sum()/len(read_data)*100
    missing = null_values.sum().round(2)
    st.write(read_data.isnull().sum())
    if missing >=30:
        st.error("Poor Data Quality : more than 30 percent of missing values !")
    else:
        st.success("Looks Good !")

    st.text("Ideally 20-30 perecent is the maximum missing values allowed,")
    st.text("beyond which we should consider dropping the variable.")
    st.text("However, this depends from case to case")

if st.button(label='Click to Remove Null Values',key=3):
    new_datanullvalue = read_data.dropna(axis=0)
    st.download_button(label="Download data as CSV",data = new_datanullvalue.to_csv(index=False).encode('utf-8'),file_name='NullValuesRemoved.csv',mime='text/csv')
        
#Remove Null Values From Specific Column  
st.markdown('Click to Remove Null Values From Specific Column')
with st.form(key="my_form0"):
    column = read_data.columns
    option = st.selectbox("Select the Column",column)
    submit_button = st.form_submit_button(label="Submit")
    new_datasnv = read_data
    new_datasnv=new_datasnv.dropna(axis=0, subset=[option])
    new_data = new_datasnv.to_csv(index=False).encode('utf-8')
new_data = new_data
st.download_button(label="Download data as CSV",data=new_data,file_name='SNullValuesRemoved.csv',mime='text/csv')
st.markdown("---")
    
# Check for duplication
if st.button('Checking for Duplication Rate',key=5): 
    duplicate = read_data.duplicated().sum()
    duplication_ratio = round(duplicate/len(read_data),2)
    st.write("Duplication Rate for the dataset : ",duplication_ratio)

    st.text("There is no rule to decide the threshold for duplication rate.")
    st.text("It depends from case to case ")

# Removing Duplicate Values
if st.button('Click to Remove Duplicate Values',key=6):
    new_dataduplicate = read_data
    dum = new_dataduplicate[new_dataduplicate.duplicated()]
    st.write("\n\nDuplicate Rows : \n",dum)
    new_dataduplicate = new_dataduplicate.drop_duplicates(keep='first')
    new_dataduplicate = new_dataduplicate.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download data as CSV",data=new_dataduplicate,file_name='DuplicateRemoved.csv',mime='text/csv')
st.markdown("---")
#Check for completeness ratio
if st.button("Check for Completeness Ratio",key=7):
    not_missing = (read_data.notnull().sum().round(2))
    completeness = round(sum(not_missing)/len(read_data),2)
    st.write("Completeness Ratio for the dataset : ",completeness)
    if completeness >=0.80:
        st.success('Looks Good !')
    else:
        st.error('Poor Data Quality due to low completeness ratio : less than 80 perecent !')
        st.text('Completeness is defined as the ratio of non-missing values to total records in dataset.')
st.markdown("---")


# Renaming a Column
st.markdown('Renaming a Column')
with st.form(key="my_form1"):
    selectedcolumn = st.selectbox('Select the Column',options=read_data.columns)
    newname = st.text_input("Enter the new Name: ")
    submit_button = st.form_submit_button(label="Submit")
    new_datarename = read_data
    new_datarename = new_datarename.rename(columns={selectedcolumn:newname})
renamed =new_datarename.to_csv(index=False).encode('utf-8')
st.download_button(label="Download data as CSV",data=renamed,file_name='Renamed.csv',mime='text/csv')
st.markdown("---")

#Changing the datatype of a column
st.markdown("Change the Datatype of a Column")
with st.form(key="my_form3"):
    newread_data = read_data.select_dtypes(include=['int64','float64','bool'])
    selectedcolumn = st.selectbox('Select the Column',options=newread_data.columns)
    datatypes = newread_data.dtypes[selectedcolumn]
    option = st.selectbox('Select the new Datatype:',('int64','float64','bool','object'))
    st.write('You seleccted:', option)
    submit_button = st.form_submit_button(label="Submit")
    newdata_datatype =  read_data
    newdata_datatype[selectedcolumn] = newdata_datatype[selectedcolumn].astype(option)

# download option
dt = newdata_datatype.to_csv(index=False).encode('utf-8')
st.download_button(label="Download data as CSV",data=dt,file_name='Columndatatypechanged.csv',mime='text/csv')
st.markdown("---")


# Replace numerical value with string
st.markdown("Replace numerical value with string")
with st.form(key="my_form2"):
    selectedcolumn = st.selectbox('Select the Column',options=read_data.columns)
    firstvalue = st.text_input(" Enter the string for 0: ")
    secondvalue = st.text_input(" Enter the string for 1: ")
    submit_button = st.form_submit_button(label="Submit") 
    newdata_value = read_data   
    newdata_value[selectedcolumn].replace(0,firstvalue,inplace=True)
    newdata_value[selectedcolumn].replace(1,secondvalue,inplace=True)

    # download option
replacevalue =newdata_value.to_csv(index=False).encode('utf-8')
st.download_button(label="Download data as CSV",data=replacevalue,file_name='ValueReplaced.csv',mime='text/csv')
st.markdown("---")




#Data Cleaning
if st.button("Clean the Data",key=8):
    st.write("Checking for Null Values:")
    read_data = read_data.dropna(axis=0)
    st.write("Removing Null Values...")
    st.write("Null Values Removed")
    st.write("Checking for Duplicate Values: ")
    st.write("Removing Duplicate Values... ")
    dfr2 = read_data.drop_duplicates(keep='first')
    st.write("Duplicate Values Removed ")
    dfr4 = dfr2.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download Cleaned Data",data=dfr4,file_name='CleanedData.csv',mime='text/csv')
st.markdown("---")
    
#Removing Special Char 
if st.button(label='Remove special character',key=10):
    spec_chars = ["!",'"',"#","%","&","'","(",")",
              "*","+",",","-",".","/",":",";","<",
              "=",">","?","@","[","\\","]","^","_",
              "`","{","|","}","~","–","$"]
    #newdata = read_data
    read_data = read_data.drop(label=["!",'"',"#","%","&","'","(",")",
              "*","+",",","-",".","/",":",";","<",
              "=",">","?","@","[","\\","]","^","_",
              "`","{","|","}","~","–","$"],axis = 0)
    #read_data = read_data.str.replace(spec_chars,"")
    #read_data = read_data.replace(spec_chars,"")
    #read_data = read_data.dropna(axis=0)
    read_data = read_data.to_csv(index=False).encode('utf-8')
    
    st.download_button(label="Download data as CSV",data=read_data,file_name='Specialchar.csv',mime='text/csv')
    #read_data.to_csv(r'C:\Users\217648\Downloads\file3.csv', index=False)
st.markdown("---")

# concatenate Two Columns
st.markdown("Concatenate TWO columns")
with st.form(key="new_form"):
    #read_data1 = read_data.select_dtypes(include=['object'])
    newread_data1 = read_data.select_dtypes(include=['object'])
    selectedcolumn3 = st.selectbox('Select the First Column',options=newread_data1.columns)
    selectedcolumn4 = st.selectbox('Select the Second Column',options=newread_data1.columns)
    newcolumn = st.text_input("Enter the New Column Name:")
    submit_button = st.form_submit_button(label="submit")
    df_read_data = read_data
    df_read_data[newcolumn] = df_read_data[[selectedcolumn3, selectedcolumn4]].apply(" ".join, axis=1)
    #read_data = newread_data1[selectedcolumn3].astype(str) + newread_data1[selectedcolumn4]
    #download option
df1_read_data = df_read_data.to_csv(index=False).encode('utf-8')
st.download_button(label="Download data as CSV",data=df1_read_data,file_name='Concatenate.csv',mime='text/csv')
st.markdown("---")

    


    




st.subheader('> Thank you for using the Quality Checker.')
st.subheader('Team Error Makers')
