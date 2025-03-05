import streamlit as st
import pandas as pd
import psycopg2  # PostgreSQL connector
import matplotlib.pyplot as plt
import seaborn as sns

# Function to connect to PostgreSQL and retrieve data
def get_data():
    connection = psycopg2.connect(
        host="pg-14263e7d-lamze-f101.d.aivencloud.com",      # Update with your host
        database="defaultdb",    # Update with your database name
        user="avnadmin",      # Update with your database username
        password="AVNS_KbOp7Hz3mnvuMa47rvI",  # Update with your database password
        port = "24724",        # PostgreSQL port
        sslmode = "require"     # You can set to 'verify-full' for full verification
    )
    
    query = "select * from tbl_sports order by spt_id asc"
    df = pd.read_sql(query, connection)
    connection.close()
    
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

# Vertical bar chart for Table 2
st.subheader('Bar Chart: mrd, mbl, mgn')
bar_chart = create_bar_chart(batch_data)
st.pyplot(bar_chart)

# Table 3 (3 x 2): cls_cat and ttl values of the first 3 rows
st.subheader('Table 3: cls_cat and ttl (First 3 Rows)')
table3 = pd.DataFrame({
    'cls_cat': filtered_df.iloc[:3]['cls_cat'],
    'ttl': filtered_df.iloc[:3]['ttl']
})
st.table(table3)

# Pie chart for ttl values (each row of ttl has a different color)
st.subheader('Pie Chart for ttl')
colors_ttl = ['yellow', 'purple', 'grey']
ttl_sizes = filtered_df.iloc[:3]['ttl']
fig, ax = plt.subplots()
ax.pie(ttl_sizes, labels=filtered_df.iloc[:3]['cls_cat'], colors=colors_ttl, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig)
