import requests
import tkinter as tk
from tkinter import ttk
import csv
from io import StringIO

def show_data_in_window(data):
    window = tk.Tk()
    window.title("NYSE Companies")

    # Create a treeview (table) to display the data
    tree = ttk.Treeview(window)

    # Define columns
    columns = data[0]
    tree["columns"] = tuple(columns)

    # Format column headings
    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, anchor="center")

    # Insert data into the treeview
    for item in data[1:]:
        values = [item[column] for column in columns]
        tree.insert("", "end", values=values)

    # Display the treeview
    tree.pack(expand=True, fill="both")

    window.mainloop()

api_key = '7ZMH1H134AURD89L'
base_url = 'https://www.alphavantage.co/query'

# Query to get a list of NYSE stocks
params = {
    'function': 'LISTING_STATUS',
    'apikey': api_key,
    'exchange': 'NYSE'
}

try:
    response = requests.get(base_url, params=params)
    response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx and 5xx)

    print(f"HTTP Status Code: {response.status_code}")
    print("Response Content:")
    print(response.text)

    if response.text.strip():  # Check if the response is not empty
        # Use csv module to parse the CSV-like content
        csv_reader = csv.DictReader(StringIO(response.text))
        data = list(csv_reader)

        # Now 'data' contains information about NYSE-listed stocks
        # You can extract symbols, company names, etc. from the response

        # Show the data in a new window
        show_data_in_window(data)
    else:
        print("Empty response received. Check your API key and parameters.")

except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
