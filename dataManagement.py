import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    menu()

def splitLocation(df):
    '''
    Split the 'location' column into 'city' and 'state' using normalization and state dictionary.
    '''
    location_normalization = {
    "Greater Philadelphia": ("Philadelphia", "PA"),
    "United States": (None, None),  # Missing detail
    "Washington DC": ("Washington", "DC"),
    "D.C.": ("Washington", "DC"),
    "NYC": ("New York", "NY"),
    "Los Angeles Area": ("Los Angeles", "CA"),
    "Bay Area": ("San Francisco", "CA"),  
}
    state_dict = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New hampshire", "NJ": "New jersey", "NM": "New mexico", "NY": "New york",
    "NC": "North carolina", "ND": "North dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode island", "SC": "South carolina",
    "SD": "South dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West virginia",
    "WI": "Wisconsin", "WY": "Wyoming", "DC": "District of columbia",
    "PR": "Puerto rico", "GU": "Guam", "VI": "Virgin islands", "AS": "American samoa",
    "MP": "Northern mariana islands"
}
    cities, states = [], []
    
    for loc in df["location"]:
        if pd.isna(loc):
            cities.append(None)
            states.append(None)
            

        # Apply normalization mapping if exact match
        elif loc in location_normalization:
            city, state = location_normalization[loc]
            cities.append(city)
            states.append(state)
            

        # Standard format: "City, ST"
        elif "," in loc:
            city, state_abbr = [x.strip() for x in loc.split(",", 1)]
            state_full = state_dict.get(state_abbr.upper(), state_abbr)
            cities.append(city)
            states.append(state_full)
        else:
            cities.append(loc.strip())
            states.append(None)

    df["city"] = cities
    df["state"] = states
    df.drop(columns=["location"], inplace=True)

    return df




def selectAttributes(df):
    '''
    Select specific attributes from the dataframe based on user input.
    '''
    # Select specific attributes from the dataframe
    selected_columns = []
    column = input("Enter attribute name to select (or 'done' to finish): ")
    
    while column.lower() != 'done':
        if column in df.columns:
            selected_columns.append(column)
        else:
            print(f"Attribute '{column}' does not exist in the dataframe.")
        column = input("Enter attribute name to select (or 'done' to finish): ")

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

def columnVtype(df,Vtype):
    '''
    Recognize and returns attributes of a specific type in the dataframe.(int,date,String)
    '''
    attributes=[]
    match Vtype:
        case 'int':
            Vtype='int64'
        case 'date':
            Vtype='datetime64[ns]'
        case 'String':
            Vtype='object'
        case _:
            print("Invalid type")
            Vtype=input("Enter a valid type (int, date, String): ")
            columnVtype(df,Vtype)

    for col in df.columns:
    # Check if the column's dtype matches the given Vtype
        if df[col].dtype == Vtype:
             attributes.append(col)         
    return attributes

#FIX DATEVALUES 
def fillMissingValues(df, attributes):
    '''
    Fill missing values in the dataframe for specified attributes.
    '''
    for e in attributes:
        if df[e].dtype == 'object':
            df[e] = df[e].fillna("Unknown")
        elif df[e].dtype == 'int64':
            # Convert Unix timestamps (milliseconds) to datetime
            df[e] = pd.to_numeric(df[e], errors="coerce")
            if (df[e] > 10**12).any():
                df[e] = pd.to_datetime(df[e] // 1000, unit='s', errors="coerce")
            else:
                df[e] = df[e].fillna(0).astype(int)

    return df

def Showmenu(op=-1):
    match op:
        case -1:
            print(f'''
1. Load DataFrame
2. Show DataFrame info
3. Data Cleaning
4. Show DataFrame
5. Save DataFrame
0. Exit
''')
        case 2:
            print(f'''
                  1. All info
                  2. Attributes
                  0. Exit''')
        case 3:
            print(f'''
                  1. Clear NULL and empty values by attribute
                  2. Select specific attributes
                  3. Fill missing values in String columns
                  4. Fill missing values in Numeric columns
                  5. Fill missing values in Date columns
                  0. Exit
                  ''')
        case _:
            print("Invalid option")

def option(m=0,n=6):
    option= input("Select an option: ")
    while option.isdigit()==False and int(option) not in range(m,n):
        print("Invalid option")
        option= input("Select a valid option: ")
    return int(option)

def normalizeTimestamps(df, cols):
    """
    Convert Unix timestamp columns (in milliseconds) into datetime.
    """
    for col in cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            # Only convert if values look like ms timestamps
            if (df[col] > 10**12).any():
                df[col] = pd.to_datetime(df[col] // 1000, unit="s", errors="coerce")
    return df

def menu():
    Showmenu()
    opt=option()
    while opt!=0:
        match opt:
            case 1:
                dfName= input("Enter the DataFrame variable name: ")
                if dfName[-4:]!=".csv":
                    dfName+= ".csv"
                try:
                    df=pd.read_csv(dfName)
                    df = normalizeTimestamps(df, ["original_listed_time", "expiry"])
                    print("\nDataFrame loaded successfully!")
                except Exception as e:
                    print("File name not found or invalid DataFrame variable.")
                    print(f"Error: {e}")
                    opt=1
                
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
                            opt=1
                    case 2:
                        try:
                            print(df.columns)
                        except Exception as e:
                            print("DataFrame variable not found. Please load a DataFrame first.")
                            print(f"Error: {e}")
                            opt=1                     
                    case 0:
                        menu()
            
            case 3:
                Showmenu(3)
                suboption = option(0,6)
                match suboption:
                    case 1:
                        try:
                            dataCleaning(df)
                        except Exception as e:
                            print("DataFrame variable not found. Please load a DataFrame first.")
                            print(f"Error: {e}")
                            opt=1
                    case 2:
                        try:
                            df=selectAttributes(df)
                            print("Attributes selected successfully!")
                        except Exception as e:
                            print("DataFrame variable not found. Please load a DataFrame first.")
                            print(f"Error: {e}")
                            opt=1
                    case 3:            
                        try:
                            attributes=columnVtype(df,'String')
                            df=fillMissingValues(df,attributes)
                            print("Missing values filled successfully!")

                        except Exception as e:
                            print("DataFrame variable not found. Please load a DataFrame first.")
                            print(f"Error: {e}")
                            opt=1
                    case 4:
                        try:
                            attributes=columnVtype(df,'int')
                            df=fillMissingValues(df,attributes)
                            print("Missing values filled successfully!")
                            
                        except Exception as e:
                            print("DataFrame variable not found. Please load a DataFrame first.")
                            print(f"Error: {e}")
                            opt=1
                    case 5:
                        try:
                            attributes=columnVtype(df,'date')
                            df=fillMissingValues(df,attributes)
                            print("Missing values filled successfully!")
                            
                        except Exception as e:
                            print("DataFrame variable not found. Please load a DataFrame first.")
                            print(f"Error: {e}")
                            opt=1
               
            case 4:
                try:
                    att=input("Enter the attribute to display: ")
                    while att not in df.columns:
                        print("Attribute not found")
                        att=input("Enter a valid attribute to display: ")
                    print(df[att])
                except Exception as e:
                    print("DataFrame variable not found. Please load a DataFrame first.")
                    print(f"Error: {e}")
                    opt=1
            case 5:
                try:
                    filename= input("Enter the filename to save the DataFrame (with .csv extension): ")
                    encoding= input("Enter the encoding (utf-8, latin1): ")
                    if encoding not in ['utf-8','latin1']:
                        encoding='utf-8'
                    saveDataFrame(df,filename,encoding)
                except Exception as e:
                    print("DataFrame variable not found. Please load a DataFrame first.")
                    print(f"Error: {e}")
                    opt=1
            case _:
                print("Invalid option")
        Showmenu()
        opt= option(-1,5)

    #df = splitLocation(df)
    #saveDataFrame(df,"depuradoV1.csv","UTF-8")


main()

