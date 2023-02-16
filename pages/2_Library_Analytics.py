import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go

st.set_page_config(page_title="Library Dashboard -Institutional Dashboard", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="auto")

# Importing all datasets

@st.cache(allow_output_mutation=True)
def load_lib_data():
    lib_dim = pd.read_csv("data/library_dimension.csv")
    lib_fact = pd.read_csv("data/library_fact.csv")
    lib_mem = pd.read_csv("data/library_members.csv")
    lib_foot = pd.read_csv("data/library_footfall_data.csv")
    return lib_dim, lib_fact, lib_mem, lib_foot

lib_dim, lib_fact, lib_mem, lib_foot = load_lib_data()


st.title("Library Dashboard")
st.header("Book Metrics")

# Declaring Metric Columns
unique_books_col , unique_authors_col, unique_pubs_col = st.columns(3)

with unique_books_col:
    st.image('images/book.png')
# To find the unique Number of Books
num_unique_books = lib_dim['Book Id'].nunique()
unique_books_col.metric("Unique Books ", num_unique_books)

with unique_authors_col:
    st.image('images/editor.png')
# To find the unique Number of Authors
num_unique_authors = lib_dim['Author'].nunique()
unique_authors_col.metric("Unique Authors ", num_unique_authors)

with unique_pubs_col:
    st.image('images/publisher.png')
# To find the unique Number of Publishers
num_unique_pubs = lib_dim['Publisher'].nunique()
unique_pubs_col.metric("Unique Publishers ", num_unique_pubs)

st.header("View Books by")
lang_graph_tab , genre_graph_tab, year_graph_tab, price_graph_tab, return_status_tab= st.tabs(["Language", "Genre", "Year of Publishing", "Price", "Return Status"])

# Plotting Graphs on Book Metrics

with lang_graph_tab:
    books_by_lang_fig = px.histogram(lib_dim, x="Language", nbins=50, title="Number of Books Based on Languages")
    books_by_lang_fig.update_traces(texttemplate='%{y}', textposition='outside')
    books_by_lang_fig.update_layout(xaxis_title='Language', yaxis_title='Number of Books', uniformtext_minsize=8, uniformtext_mode='hide')
    books_by_lang_fig.update_xaxes(showgrid=False)
    books_by_lang_fig.update_yaxes(showgrid=False)
    st.plotly_chart(books_by_lang_fig, use_container_width=True)

with genre_graph_tab:
    # Plot the distribution of books by genre
    books_by_genre_fig = px.histogram(lib_dim, x="Genre", nbins=50, title="Number of Books Based on Genre")
    books_by_genre_fig.update_traces(texttemplate='%{y}', textposition='outside')
    books_by_genre_fig.update_layout(xaxis_title='Genre', yaxis_title='Number of Books', uniformtext_minsize=8, uniformtext_mode='hide')
    books_by_genre_fig.update_xaxes(showgrid=False)
    books_by_genre_fig.update_yaxes(showgrid=False)
    st.plotly_chart(books_by_genre_fig, use_container_width=True)

with year_graph_tab:
    lib_dim['Year'] = pd.to_datetime(lib_dim['Year'], format='%Y')
    # Group the data by decade
    lib_dim['Decade'] = (lib_dim['Year'].dt.year // 10) * 10
    # Count the number of books per decade
    decade_counts = lib_dim.groupby('Decade')['Book Id'].count()
    # Create the bar graph using Plotly Express
    year_fig = px.bar(decade_counts, x=decade_counts.index, y=decade_counts.values, title="Books Based on Year of Publishing", labels={'x': 'Year of Publishing', 'y': 'Number of Books'})
    year_fig.update_traces(texttemplate='%{y}', textposition='outside')
    year_fig.update_xaxes(showgrid=False)
    year_fig.update_yaxes(showgrid=False)
    st.plotly_chart(year_fig, use_container_width=True)

with price_graph_tab:
    #Books based on Price
    bins = [400, 800, 1200, 1600, 2000, 2400, 2800, 3200, 3600]
    # Cut the Book Price column into bins
    lib_dim['Price Range'] = pd.cut(lib_dim['Book Price'], bins, labels=["400-800", "800-1200", "1200-1600", "1600-2000", "2000-2400", "2400-2800", "2800-3200", "3200-3600"])
    # Count the number of books in each bin
    bin_counts = lib_dim.groupby('Price Range')['Book Id'].count()
    # Create the bar graph using Plotly Express
    price_fig = px.bar(bin_counts, x=bin_counts.index, y=bin_counts.values, title="Books Based on Price", labels={'x': 'Price range (in INR)', 'y': 'Number of books'})
    price_fig.update_traces(texttemplate='%{y}', textposition='outside')
    price_fig.update_xaxes(showgrid=False)
    price_fig.update_yaxes(showgrid=False)
    st.plotly_chart(price_fig, use_container_width=True)

with return_status_tab:
    lib_fact['Due Date'] = pd.to_datetime(lib_fact['Due Date'])
    lib_fact_2019 = lib_fact[lib_fact['Due Date'].dt.year == 2019]
    lib_fact_2019['Due Date'] = pd.to_datetime(lib_fact_2019['Due Date'])
    lib_fact_2019['Month'] = lib_fact_2019['Due Date'].dt.month
    # Group the data by the Return Status and Month columns
    grouped_df = lib_fact_2019.groupby(['Returned  Status', 'Month'])['Returned  Status'].count().reset_index(name='Count')
    # Create a bar chart using Plotly Express
    return_status_fig = px.bar(grouped_df, x='Month', y='Count', color='Returned  Status')
    # Update the chart layout
    return_status_fig.update_layout(title='Return Status by Month in 2019', xaxis_title='Month', yaxis_title='Count')
    # Show the chart
    return_status_fig.update_xaxes(showgrid=False)
    return_status_fig.update_yaxes(showgrid=False)
    st.plotly_chart(return_status_fig, use_container_width=True)

st.header("The Top Tens")
popular_books_tab, auth_group_tab, pub_group_tab = st.tabs(["Top 10 Popular Book","Top 10 Authors by Number of Books", "Top 10 Publishers by Number of Books"])

with popular_books_tab:
    # Merging the two tables on the Book ID column
    merged_df = pd.merge(lib_dim, lib_fact, left_on='Book Id', right_on='Book ID', how='inner')
    # Grouping the data by Book ID and counting the number of times each book was checked out
    grouped_df = merged_df.groupby(['Book Id'])['Book ID'].count().reset_index(name='Count')
    # Sorting the data in descending order based on the count
    sorted_df = grouped_df.sort_values(by='Count', ascending=False)
    # Selecting the first 10 rows to get the top 10 books by popularity
    top_10_df = sorted_df.head(10)
    # Merging the top 10 books data with the `lib_dim` dataframe to get the Book Id, Name, Author, Publisher, Genre information
    result_df = pd.merge(top_10_df, lib_dim, left_on='Book Id', right_on='Book Id', how='inner')[['Book Id', 'Title', 'Author', 'Publisher', 'Genre']]
    # Displaying the result dataframe
    result_df.index += 1
    st.dataframe(result_df)

with auth_group_tab:
    # Displaying the Top 10 Authors by books
    author_group = lib_dim.groupby('Author').count()['Book Id']
    top_10_authors = author_group.nlargest(10)
    top_10_authors_df = pd.DataFrame({'Author': top_10_authors.index, 'Number of books': top_10_authors.values})
    top_10_authors_df = top_10_authors_df.reset_index(drop=True)
    top_10_authors_df.index += 1
    st.dataframe(top_10_authors_df)

with pub_group_tab:
    # Displaying Top 10 Publishers by Books
    publisher_grouped = lib_dim.groupby('Publisher')
    publisher_counts = publisher_grouped['Book Id'].count()
    publisher_df = publisher_counts.reset_index().rename(columns={'Book Id': 'Number of Books'})
    publisher_df = publisher_df.sort_values(by='Number of Books', ascending=False)
    publisher_df = publisher_df.reset_index(drop=True)
    publisher_df.index += 1
    st.dataframe(publisher_df.head(10))


st.header("Member Metrics")
#Member Metrics
staff_member_col, student_member_col, total_member_col = st.columns(3)

# Count the number of staff members
num_staff = len(lib_mem[lib_mem["Member_ID"].str.startswith("Staff")])
staff_member_col.metric("Staff Members:", num_staff)

# Count the number of student members
num_students = len(lib_mem[lib_mem["Member_ID"].str.startswith("Student")])
student_member_col.metric("Student Members:", num_students)

# Count the Total Members
total_lib_members = num_staff + num_students
total_member_col.metric("Total Members:", total_lib_members)

st.header("Footfall and Conversion in Library")
# Convert the 'Date' column to a datetime format
lib_foot['Date'] = pd.to_datetime(lib_foot['Date'])
# Group the data by month and year, and sum the footfall count and conversion count for each group
lib_foot_monthly = lib_foot.groupby(lib_foot['Date'].dt.to_period('M')).sum().astype(str)
# Convert the PeriodIndex to a string index
lib_foot_monthly.index = lib_foot_monthly.index.astype(str)
# Create a line graph using Plotly
lib_foot_monthly_fig = go.Figure()
lib_foot_monthly_fig.add_trace(go.Scatter(x=lib_foot_monthly.index, y=lib_foot_monthly['Footfall_Count'], name='Footfall_Count', text=lib_foot_monthly['Footfall_Count'], textposition='bottom center'))
lib_foot_monthly_fig.add_trace(go.Scatter(x=lib_foot_monthly.index, y=lib_foot_monthly['Conversion_Count'], name='Conversion_Count', text=lib_foot_monthly['Conversion_Count'], textposition='bottom center'))

# Set the title and axis labels
lib_foot_monthly_fig.update_layout(title='Footfall Count and Conversion Count by Month', xaxis_title='Month', yaxis_title='Count')

# Display the graph
st.plotly_chart(lib_foot_monthly_fig, use_container_width=True)