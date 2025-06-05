import streamlit as st
import pandas as pd

# Define the dropdown options for relevant columns
manufacturer_names = [
    "Siemens", "ABB", "Schneider Electric", "Bosch", "Mitsubishi", "Omron", "Honeywell", "Eaton", "Rockwell Automation"
]
equipment_numbers = ["123", "124", "125", "126"]
product_statuses = ["active", "inactive"]

# Initial table data
data = [
    {
        "Manufacturer Name": "Siemens",
        "Article Number": "ART12345678",
        "Description": "Spare part A",
        "Equipment Number": "123",
        "Product Status": "active"
    },
    {
        "Manufacturer Name": "ABB",
        "Article Number": "ART87654321",
        "Description": "Spare part B",
        "Equipment Number": "124",
        "Product Status": "inactive"
    },
    {
        "Manufacturer Name": "Mitsubishi",
        "Article Number": "ART11223344",
        "Description": "Spare part C",
        "Equipment Number": "125",
        "Product Status": "active"
    },
]

df = pd.DataFrame(data)

st.title("Directly Editable Data Table")

# Toggle for Edit/View
edit_mode = st.toggle("Edit mode", value=False)

# Set column config for st.data_editor (to enable dropdowns and validation)
column_config = {
    "Manufacturer Name": st.column_config.SelectboxColumn(
        "Manufacturer Name", options=manufacturer_names, required=True
    ),
    "Article Number": st.column_config.TextColumn(
        "Article Number", max_chars=80, required=True
    ),
    "Description": st.column_config.TextColumn(
        "Description", max_chars=40, required=True
    ),
    "Equipment Number": st.column_config.SelectboxColumn(
        "Equipment Number", options=equipment_numbers, required=True
    ),
    "Product Status": st.column_config.SelectboxColumn(
        "Product Status", options=product_statuses, required=True
    ),
}

# Render the table
if edit_mode:
    edited_df = st.data_editor(
        df,
        column_config=column_config,
        num_rows="fixed", # or "dynamic" if you want to allow adding/removing rows
        key="data_editor"
    )
    st.info("You are in edit mode! Changes are shown above.")
else:
    st.dataframe(df, use_container_width=True)
    st.info("Read-only mode.")

# If you want to do something with the edited data:
# st.write("Edited Data:", edited_df)
