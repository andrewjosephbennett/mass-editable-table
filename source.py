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

# Store initial data in session_state
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(generate_sample_data(20))
if "edited_df" not in st.session_state:
    st.session_state.edited_df = st.session_state.df.copy()
if "edited" not in st.session_state:
    st.session_state.edited = False

st.title("Directly Editable Data Table (with Bulk Edit & Save)")

edit_mode = st.toggle("Edit mode", value=False)

df = st.session_state.edited_df.copy()

# Bulk edit logic
def bulk_edit_column(col, value):
    df[col] = value
    st.session_state.edited = True
    st.session_state.edited_df = df

# Column config for st.data_editor (no icons specified)
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

if edit_mode:
    st.markdown("#### Bulk Edit (Set entire column at once)")
    cols = st.columns(len(df.columns))
    for idx, col in enumerate(df.columns):
        with cols[idx]:
            if col in ["Manufacturer Name", "Equipment Number", "Product Status"]:
                # For dropdown columns
                options = manufacturer_names if col == "Manufacturer Name" else (
                    equipment_numbers if col == "Equipment Number" else product_statuses
                )
                val = st.selectbox(
                    f"Set all '{col}'", options=options, key=f"bulk_{col}_value"
                )
            else:
                max_chars = 80 if col == "Article Number" else 40
                val = st.text_input(
                    f"Set all '{col}'", value="", max_chars=max_chars, key=f"bulk_{col}_value"
                )
            # Only update if user clicks the button
            if st.button(f"Set All", key=f"set_all_{col}"):
                # For text, only apply if input is non-empty
                if (col in ["Article Number", "Description"] and val.strip() != "") or (col not in ["Article Number", "Description"]):
                    bulk_edit_column(col, val)
                    st.experimental_rerun()

    edited_df = st.data_editor(
        df,
        column_config=column_config,
        num_rows="fixed",
        key="data_editor",
        on_change=lambda: st.session_state.update({"edited": True})
    )

    # Detect changes by comparing dataframes
    if not edited_df.equals(st.session_state.edited_df):
        st.session_state.edited_df = edited_df
        st.session_state.edited = True

    st.info("Edit table and use 'Bulk Edit' to set values for entire columns.")

    # Save button, only enabled if edited
    save_btn = st.button("Save Changes", disabled=not st.session_state.edited)
    if save_btn:
        st.session_state.df = st.session_state.edited_df.copy()
        st.session_state.edited = False
        st.success("Changes saved!")

else:
    st.dataframe(st.session_state.df, use_container_width=True)
    st.info("Read-only mode.")
