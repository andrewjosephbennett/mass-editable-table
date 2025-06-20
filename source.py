import streamlit as st
import pandas as pd
import random

# Predefined values
manufacturer_names = [
    "Siemens", "ABB", "Schneider Electric", "Bosch", "Mitsubishi",
    "Omron", "Honeywell", "Eaton", "Rockwell Automation"
]
equipment_numbers = ["123", "124", "125", "126"]
product_statuses = ["active", "inactive"]

# Generate sample data for 20 rows
def generate_sample_data(n):
    data = []
    for i in range(n):
        data.append({
            "Manufacturer Name": random.choice(manufacturer_names),
            "Article Number": f"ART{random.randint(10000000, 99999999)}",
            "Description": f"Spare part {chr(65 + (i % 26))}",
            "Equipment Number": random.choice(equipment_numbers),
            "Product Status": random.choice(product_statuses)
        })
    return data

# Initialize session state
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(generate_sample_data(20))
if "edited_df" not in st.session_state:
    st.session_state.edited_df = st.session_state.df.copy()
if "edited" not in st.session_state:
    st.session_state.edited = False
if "bulk_column_open" not in st.session_state:
    st.session_state.bulk_column_open = {col: False for col in st.session_state.df.columns}
if "bulk_values" not in st.session_state:
    st.session_state.bulk_values = {col: "" for col in st.session_state.df.columns}
if "bulk_trigger" not in st.session_state:
    st.session_state.bulk_trigger = {col: False for col in st.session_state.df.columns}

st.title("Bulk-editable table")

edit_mode = st.toggle("Edit mode", value=False)

# Column config (no icons)
column_config = {
    "Manufacturer Name": st.column_config.SelectboxColumn(
        "Manufacturer Name", options=manufacturer_names
    ),
    "Article Number": st.column_config.TextColumn(
        "Article Number", max_chars=80
    ),
    "Description": st.column_config.TextColumn(
        "Description", max_chars=40
    ),
    "Equipment Number": st.column_config.SelectboxColumn(
        "Equipment Number", options=equipment_numbers
    ),
    "Product Status": st.column_config.SelectboxColumn(
        "Product Status", options=product_statuses
    ),
}

def bulk_edit_column(col, value):
    st.session_state.edited_df[col] = value
    st.session_state.edited = True

if edit_mode:
    st.markdown("#### Edit in bulk 👇")
    # Show table header with clickable "Set All" for each column
    cols = st.columns(len(st.session_state.edited_df.columns))
    for idx, col in enumerate(st.session_state.edited_df.columns):
        with cols[idx]:
            if st.button(f"Set All: {col}", key=f"open_bulk_{col}"):
                st.session_state.bulk_column_open[col] = not st.session_state.bulk_column_open[col]
            # Show bulk edit UI if open
            if st.session_state.bulk_column_open[col]:
                st.markdown(f"**Bulk set all values for _{col}_**")
                # Dropdown columns
                if col in ["Manufacturer Name", "Equipment Number", "Product Status"]:
                    options = manufacturer_names if col == "Manufacturer Name" else (
                        equipment_numbers if col == "Equipment Number" else product_statuses
                    )
                    st.session_state.bulk_values[col] = st.selectbox(
                        f"New value for all '{col}'", options=options, key=f"bulk_val_{col}"
                    )
                else:
                    max_chars = 80 if col == "Article Number" else 40
                    st.session_state.bulk_values[col] = st.text_input(
                        f"New value for all '{col}'", value=st.session_state.bulk_values[col], max_chars=max_chars, key=f"bulk_val_{col}"
                    )
                if st.button("Apply to all", key=f"apply_bulk_{col}"):
                    value = st.session_state.bulk_values[col]
                    if col in ["Article Number", "Description"]:
                        if value.strip() == "":
                            st.warning("Please enter a value.")
                        else:
                            st.session_state.bulk_trigger[col] = True
                            st.session_state.bulk_column_open[col] = False
                    else:
                        st.session_state.bulk_trigger[col] = True
                        st.session_state.bulk_column_open[col] = False

    # Bulk apply changes just before data editor
    for col, trigger in st.session_state.bulk_trigger.items():
        if trigger:
            bulk_edit_column(col, st.session_state.bulk_values[col])
            st.session_state.bulk_trigger[col] = False  # Reset trigger

    st.markdown("#### Edit individual fields 👇")
    
    edited_df = st.data_editor(
        st.session_state.edited_df,
        column_config=column_config,
        num_rows="fixed",
        key="data_editor"
    )

    # Detect changes (compare dataframes)
    if not edited_df.equals(st.session_state.edited_df):
        st.session_state.edited_df = edited_df
        st.session_state.edited = True

    # Save Changes button
    save_btn = st.button("Save Changes", disabled=not st.session_state.edited)
    if save_btn:
        st.session_state.df = st.session_state.edited_df.copy()
        st.session_state.edited = False
        st.success("Changes saved!")

    st.info("Edit table cells directly. Use the Set All buttons above to bulk edit columns.")

else:
    st.dataframe(st.session_state.df, use_container_width=True)
    st.info("Read-only mode.")
