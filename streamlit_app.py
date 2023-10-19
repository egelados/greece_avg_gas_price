import streamlit as st
import requests
from bs4 import BeautifulSoup

# Replace this URL with the one you want to scrape
url = "https://www.insurancemarket.gr/energy/gas"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find the table by its ID
    table_id = "autonomi"
    table = soup.find("table", {"id": table_id})
    if table:
        # Find the index of the "Τιμή/Kwh" column
        header_row = table.find("tr")
        headers = [header.text for header in header_row.find_all("th")]
        column_index = headers.index("Τιμή/Kwh")
        # Extract and calculate the average of numeric data from the "Τιμή/Kwh" column
        numeric_values = []
        for row in table.find_all("tr")[1:]:  # Skip the header row
            cells = row.find_all("td")
            if column_index < len(cells):
                cell_data = cells[column_index - 1].text
                # Extract the numeric part of the data
                numeric_part = cell_data.split('€')[0]
                numeric_value = float(numeric_part.replace(',', '.'))  # Convert to float
                numeric_values.append(numeric_value)
        # Calculate the average of the numeric values
        if numeric_values:
            average = sum(numeric_values) / len(numeric_values)
            st.write(f"Average Price: {average:.5f}€/Kwh")
        else:
            st.write("No numeric values found in the column.")
    else:
        st.write(f"Table with ID '{table_id}' not found on the page.")
else:
    st.write(f"Failed to retrieve the web page. Status code: {response.status_code}")
