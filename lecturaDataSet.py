import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Load data from CSV file
    dfLinkedin = pd.read_csv('postings.csv')
    dataFrameInfo(dfLinkedin)
    dfSelected = selectAttributes(dfLinkedin)
    dfCleaned = dataCleaning(dfSelected)

    # Manage missing values in String columns
    dfCleaned["description"] = dfCleaned["description"].fillna("No description provided")
    dfCleaned["pay_period"] = dfCleaned["pay_period"].fillna("Unknown")
    dfCleaned["location"] = dfCleaned["location"].fillna("Unknown")
    dfCleaned["currency"] = dfCleaned["currency"].fillna("Unknown")
    dfCleaned["compensation_type"] = dfCleaned["compensation_type"].fillna("Unknown")

    # Manage missing values in Numeric columns
    dfCleaned["views"] = pd.to_numeric(dfCleaned["views"], errors="coerce").fillna(0).astype(int)
    dfCleaned["applies"] = pd.to_numeric(dfCleaned["applies"], errors="coerce").fillna(0).astype(int)

    # Manage missing values in Date columns
    date_cols = ["original_listed_time", "closed_time", "listed_time"]
    for col in date_cols:
        dfCleaned[col] = pd.to_datetime(dfCleaned[col], errors="coerce")
    
    dataFrameInfo(dfCleaned)
    saveDataFrame(dfCleaned, "depuradoV1.csv")

def selectAttributes(df):
    '''
    Select specific attributes from the dataframe based on user input.
    '''
    # Select specific attributes from the dataframe
    selected_columns = []
    column = input("Enter column name to select (or 'done' to finish): ")
    
    while column.lower() != 'done':
        if column in df.columns:
            selected_columns.append(column)
        else:
            print(f"Column '{column}' does not exist in the dataframe.")
        column = input("Enter column name to select (or 'done' to finish): ")

    df_selected = df[selected_columns]
    return df_selected

def dataCleaning(df):
    '''
    Clean the dataframe by removing rows with null or empty values in specified attributes.
    '''
    attribute= input("Enter the attribute to clean (e.g., 'company_name')\n (or 'done' to finish): ")
    df_cleaned = df.copy()
    # Clean the dataframe by removing rows with null values in 'company_name'
    while attribute.lower() != 'done':
        if attribute in df_cleaned.columns:
            df_cleaned = df_cleaned[df_cleaned[attribute].notnull()]
            df_cleaned = df_cleaned[df_cleaned[attribute].str.strip() != ""].drop_duplicates()
        else:
            print(f"Column '{attribute}' does not exist in the dataframe.")
        attribute = input("Enter the attribute to clean (or 'done' to finish): ")
    
    df_cleaned = df_cleaned.reset_index(drop=True)
    return df_cleaned

def dataFrameInfo(df):
    '''
    Display information about the dataframe.
    '''
    # Display dataframe information
    print(df.head())
    print(df.shape)
    print(df.info())

def saveDataFrame(df, filename,encoding='utf-8'):
    '''
    Save the dataframe to a CSV file. Default encoding is 'utf-8'.
    '''
    try:
        df.to_csv(filename, index=False, encoding=encoding)
        print(f"DataFrame saved to {filename} successfully!")
    except Exception as e:
        print(f"Error saving DataFrame to {filename}: {e}")
main()

