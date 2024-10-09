import streamlit as st
import pandas as pd
from sklearn.impute import SimpleImputer

# Title of the Streamlit app
st.title('CSV File Uploader and Missing Values Imputer')

# File uploader to allow multiple CSV files
uploaded_files = st.file_uploader("Choose CSV files", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    # Iterate through uploaded files and process each one
    for idx, uploaded_file in enumerate(uploaded_files):
        st.header(f"File {idx + 1}: {uploaded_file.name}")
        try:
            # Read CSV file
            df = pd.read_csv(uploaded_file)
            
            # Display the data from the CSV file
            st.subheader("Data Preview")
            st.dataframe(df)
            
            # Identify columns with missing values
            missing_values = df.isnull().sum()
            missing_columns = missing_values[missing_values > 0]
    
            if not missing_columns.empty:
                st.subheader("Columns with Missing Values")
                
                # Determine if the columns are numerical or categorical
                column_types = df.dtypes
                column_info = {
                    "Column Name": missing_columns.index,
                    "Missing Values": missing_columns.values,
                    "Type": ["Numerical" if pd.api.types.is_numeric_dtype(df[col]) else "Categorical" for col in missing_columns.index]
                }
                column_info_df = pd.DataFrame(column_info)
                
                st.dataframe(column_info_df)
                
                # Dropdown menu to select columns with missing values for imputation
                selected_columns = st.multiselect(
                    "Select columns to impute missing values:",
                    options=missing_columns.index,
                    key=f"multiselect_{idx}"
                )
                
                if selected_columns:
                    # Button to trigger imputation
                    if st.button("Impute Missing Values", key=f"impute_button_{idx}"):
                        # Create copies to avoid modifying the original dataframe
                        df_imputed = df.copy()
                        
                        for col in selected_columns:
                            col_type = column_info_df[column_info_df["Column Name"] == col]["Type"].values[0]
                            
                            if col_type == "Numerical":
                                # Mean imputation for numerical columns
                                imputer = SimpleImputer(strategy='mean')
                            else:
                                # Mode imputation for categorical columns
                                imputer = SimpleImputer(strategy='most_frequent')
                            
                            imputed_data = imputer.fit_transform(df_imputed[[col]])
                            df_imputed[col] = imputed_data
                        
                        st.subheader("Data After Imputation")
                        st.dataframe(df_imputed)
                        
                        # Option to download the imputed DataFrame as a CSV
                        csv = df_imputed.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download Imputed Data as CSV",
                            data=csv,
                            file_name=f'imputed_{uploaded_file.name}',
                            mime='text/csv',
                            key=f"download_button_{idx}"
                        )
                else:
                    st.info("Please select at least one column for imputation.")
            else:
                st.success("No missing values found in this file.")
                
        except Exception as e:
            st.error(f"An error occurred while processing the file: {uploaded_file.name}")
            st.error(f"Error details: {e}")
