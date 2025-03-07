import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to read data from the Excel file instead of PostgreSQL
def get_data():
    # Path to the Excel file
    excel_file_path = '/lamideb/dash1-app/spt_a.xlsx'
    
    # Read the data from the Excel file into a pandas DataFrame
    df = pd.read_excel(excel_file_path, engine='openpyxl')
    
    return df

# Function to process data
def process_data(df):
    # Grouping by cld_yr to split the data into batches of 4
    df['batch'] = df.groupby('cld_yr').cumcount() // 4 + 1
    return df

# Function to create pie chart
def create_pie_chart(row):
    labels = ['sxm', 'sxf']
    sizes = [row['sxm'], row['sxf']]
    colors = ['brown', 'orange']
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    return fig

# Function to create vertical bar chart
def create_bar_chart(row):
    labels = ['mrd', 'mbl', 'mgn']
    values = [row['mrd'], row['mbl'], row['mgn']]
    colors = ['red', 'blue', 'green']
    
    fig, ax = plt.subplots()
    ax.bar(labels, values, color=colors)
    return fig

# Streamlit app layout
st.title('Sports Data Dashboard')

# Retrieve and process data
df = get_data()
df = process_data(df)

# Dropdown to select cld_yr
cld_yr_options = df['cld_yr'].unique()
selected_cld_yr = st.selectbox('Select a "cld_yr" value', cld_yr_options)

# Filter data based on selected cld_yr
filtered_df = df[df['cld_yr'] == selected_cld_yr]

# Extract the 4th row (which is the sum of previous 3 rows)
batch_data = filtered_df[filtered_df['batch'] == 1].iloc[3]

# Create tables and charts

# Table 1 (1 x 2): sxm, sxf values of the 4th row
st.subheader('Table 1: sxm and sxf')
table1 = pd.DataFrame({
    'sxm': [batch_data['sxm']],
    'sxf': [batch_data['sxf']]
})
st.table(table1)

# Pie chart for Table 1
st.subheader('Pie Chart: sxm vs sxf')
pie_chart = create_pie_chart(batch_data)
st.pyplot(pie_chart)

# Table 2 (1 x 3): mrd, mbl, mgn values of the 4th row
st.subheader('Table 2: mrd, mbl, mgn')
table2 = pd.DataFrame({
    'mrd': [batch_data['mrd']],
    'mbl': [batch_data['mbl']],
    'mgn': [batch_data['mgn']]
})
st.table(table2)

# Horizontal bar chart for ttl values (this comes after the pie chart now)
st.subheader('Horizontal Bar Chart for ttl')

# Create a horizontal bar chart for ttl values
fig, ax = plt.subplots()
ax.barh(filtered_df.iloc[:3]['cls_cat'], filtered_df.iloc[:3]['ttl'], color=['yellow', 'purple', 'grey'])
ax.set_xlabel('ttl')
ax.set_title('Horizontal Bar Chart for ttl')

st.pyplot(fig)

# Table 3 (3 x 2): cls_cat and ttl values of the first 3 rows
st.subheader('Table 3: cls_cat and ttl (First 3 Rows)')
table3 = pd.DataFrame({
    'cls_cat': filtered_df.iloc[:3]['cls_cat'],
    'ttl': filtered_df.iloc[:3]['ttl']
})
st.table(table3)

# Vertical bar chart for Table 2 (this comes last now)
st.subheader('Bar Chart: mrd, mbl, mgn')
bar_chart = create_bar_chart(batch_data)
st.pyplot(bar_chart)
