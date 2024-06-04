import pandas as pd
import re

# Define a function to extract the desired substring
def extract_substring(description):
    match = re.search(r'\[.*?\]\s*\[.*?\]\s*(.*?)\s+(\S+\s+\S+\s+\S+)', description)
    if match:
        return match.group(1) + ' ' + match.group(2)
    else:
        return description  # Return original description if pattern not found

# Read the Excel file
xls = pd.ExcelFile("incidents-latest.xlsx")

# Initialize a dictionary to store the first occurrence of each processed description
first_occurrence = {}

# Iterate over each sheet in the Excel file
with pd.ExcelWriter("latest_incident_occurrences-new.xlsx", engine='openpyxl') as writer:
    for sheet_name in xls.sheet_names:
        # Read the data from the current sheet
        df = pd.read_excel(xls, sheet_name=sheet_name)
        
        # Skip processing if the DataFrame is empty
        if df.empty:
            print("Skipping sheet", sheet_name, "because it is empty.")
            continue
        
        # Apply the function to the Description column to create a new column
        df['Processed_Description'] = df['Description'].apply(extract_substring)
        
        # Iterate over rows in DataFrame to track first occurrence of each processed description
        for index, row in df.iterrows():
            processed_desc = row['Processed_Description']
            if processed_desc not in first_occurrence:
                first_occurrence[processed_desc] = row['Description']

        # Group the DataFrame by Processed_Description and count the occurrences
        grouped = df.groupby('Processed_Description').size().reset_index(name='Occurrences')

        # Sort the grouped DataFrame by occurrences in descending order
        grouped = grouped.sort_values(by='Occurrences', ascending=False)
        
        # Add Full Description column with first occurrence description
        grouped['Full_Description'] = grouped['Processed_Description'].map(first_occurrence)

        # Drop the Processed_Description column
        grouped.drop(columns=['Processed_Description'], inplace=True)
        
        # Rearrange the columns to have Full_Description first
        grouped = grouped[['Full_Description', 'Occurrences']]

        # Explicitly convert any non-string values in the 'Occurrences' column to strings
        grouped['Occurrences'] = grouped['Occurrences'].apply(lambda x: str(x) if not isinstance(x, str) else x)

        # Write the result to a new sheet in the output Excel file if there are rows
        if not grouped.empty:
            grouped.to_excel(writer, sheet_name=sheet_name, index=False)
