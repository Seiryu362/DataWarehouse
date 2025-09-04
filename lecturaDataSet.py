import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Load data from CSV file
    dfLinkedin = pd.read_csv('postings.csv')
    dataFrameInfo(dfLinkedin)
    print(dfLinkedin['location'].unique())
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

def Showmenu(op=-1):
    match op:
        case -1:
            print(f'''
1. Load DataFrame
2. Show DataFrame info
3. Data Cleaning
4. Show DataFrame
''')
        case 2:
            print(f'''
                  1.All info
                  2. Attributes
                  0. Exit''')
        case _:
            print("Invalid option")

def option(m=0,n=5):
    option= input("Select an option: ")
    while option.isdigit()==False and int(option) not in range(m,n):
        print("Invalid option")
        option= input("Select a valid option: ")
    return int(option)

def menu():
    Showmenu()
    option= option(-1,5)
    while option!=0:
        match option:
            case 1:
                dfName= input("Enter the DataFrame variable name: ")
                try:
                    df=pd.read_csv(dfName)
                except Exception as e:
                    print("File name not found or invalid DataFrame variable.")
                    print(f"Error: {e}")
                    option=1
                
            case 2:
                Showmenu(2)
                suboption= option(0,3)
                match suboption:
                    case 1:
                        try:
                            dataFrameInfo(df)
                        except Exception as e:
                            print("DataFrame variable not found. Please load a DataFrame first.")
                            print(f"Error: {e}")
                            option=1
                    case 2:
                        try:
                            print(df.columns)
                        except Exception as e:
                            print("DataFrame variable not found. Please load a DataFrame first.")
                            print(f"Error: {e}")
                            option=1                     
                    case 0:
                        menu()
            
            case 3:
                try:
                    dataCleaning(df)
                except Exception as e:
                    print("DataFrame variable not found. Please load a DataFrame first.")
                    print(f"Error: {e}")
                    option=1
            case 4:
                try:
                    dataFrameInfo(df)
                except Exception as e:
                    print("DataFrame variable not found. Please load a DataFrame first.")
                    print(f"Error: {e}")
                    option=1
            case _:
                print("Invalid option")
        Showmenu()
        option= option(-1,5)
       

main()

