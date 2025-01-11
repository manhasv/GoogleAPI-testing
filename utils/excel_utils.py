import os
import pandas as pd

#***************
# To run these snippets, you need to install the following packages: 
# pip install pandas openpyxl
#***************


def combine_excels(upload_folder, output_file):
    """Combine all Excel files in a folder into a single file."""
    combined_data = pd.DataFrame()  # Initialize an empty DataFrame
    print("Combining Excel files...")
    # Get all Excel files in the folder
    for file_name in os.listdir(upload_folder):
        print(f"Processing {file_name}...")
        if file_name.endswith((".xlsx", ".xls")):  # Check for Excel files
            file_path = os.path.join(upload_folder, file_name)

            # Read the Excel file into a DataFrame
            try:
                data = pd.read_excel(file_path)
                print(f"Loaded {file_name} with columns: {list(data.columns)}")

                # Align columns with the combined DataFrame
                for col in combined_data.columns.difference(data.columns):
                    data[col] = pd.NA  # Add missing columns to the new DataFrame

                for col in data.columns.difference(combined_data.columns):
                    combined_data[col] = pd.NA  # Add missing columns to the combined DataFrame

                # Append the current DataFrame to the combined DataFrame
                combined_data = pd.concat([combined_data, data], ignore_index=True)
            except Exception as e:
                print(f"Error reading {file_name}: {e}")

    # Save the combined DataFrame to an Excel file
    try:
        combined_data.to_excel(output_file, index=False)
        print(f"Combined file saved as {output_file}")
    except Exception as e:
        print(f"Error saving the combined file: {e}")