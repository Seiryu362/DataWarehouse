import pandas as pd
import random as random
import numpy as np

def loadData():
    file_name = input("Enter the name of the CSV file (with extension): ")
    
    try:
        # Read the CSV file
        data = pd.read_csv(file_name)
        print("CSV file content:")
        print(data)
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{file_name}' is empty.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return data

def saveData(df):
        '''
        Save the updated DataFrame back to the CSV
        '''
        file_name = input("Enter the name of the CSV file (with extension): ")
        df.to_csv(file_name, index=False)
        print(f"Updated CSV saved as '{file_name}'")

#This function was IA GENERATED
def fill_applies(df):
    """
    Fill missing/blank values in the 'applies' column with 
    random numbers based on a weighted probability distribution:
      - 0: very rare
      - 1–15: most common
      - 16–100: less common
    """
    # Define probability weights
    values = [0] + list(range(1, 101))  # 0–100
    probs = [0.01]  # 1% chance for 0
    
    # Make 1–15 much more common
    probs += [0.05] * 15  # total 75%
    
    # Spread remaining probability for 16–100
    remaining_prob = 1 - (0.01 + 0.05*15)
    n_remaining = 100 - 15
    probs += [remaining_prob / n_remaining] * n_remaining
    
    # Normalize just in case
    probs = np.array(probs)
    probs = probs / probs.sum()
    
    # Replace nulls and blanks
    mask = df["applies"].isna() | (df["applies"].astype(str).str.strip() == "")
    
    df.loc[mask, "applies"] = np.random.choice(values, size=mask.sum(), p=probs)
    
    # Make sure column is integer
    df["applies"] = df["applies"].astype(int)
    
    return df

#IA GENERATED
def clean_remote_allowed(df):
    """
    Convert 'remote_allowed' column to boolean:
      - True if value == 1
      - False otherwise (including blanks)
    """
    df["remote_allowed"] = df["remote_allowed"].apply(lambda x: True if str(x).strip() == "1" else False)
    return df
#AI GENERATED
def simulate_sponsored(df):
    """
    Fill 'sponsored' with random booleans:
      - False (majority)
      - True (low probability, e.g., 10%)
    """
    mask = df["sponsored"] == 0
    
    df.loc[mask, "sponsored"] = np.random.choice(
    [0, 1],
    size=mask.sum(),
    p=[0.9, 0.1]
)
    df["sponsored"] = df["sponsored"].astype(bool)
    return df

def main():
    df = loadData()
    if 'original_listed_time' in df.columns:
        try:
            # Ensure the column is in datetime format
            df['original_listed_time'] = pd.to_datetime(df['original_listed_time'])
            
            # Generate random dates within the specified range
            new_dates = []
            for date in df['original_listed_time']:
                random_days = random.randint(14, 30)  # Random days between 2 weeks and 1 month
                new_date = date + pd.Timedelta(days=random_days)
                new_dates.append(new_date)
            
            # Add the new dates as a column to the DataFrame
            df['closed_time'] = new_dates
            

        except Exception as e:
            print(f"An error occurred while processing dates: {e}")
    else:
        print("Error: 'original_listed_time' column not found in the DataFrame.")

    df = fill_applies(df)
    df= clean_remote_allowed(df)
    df = simulate_sponsored(df)
    saveData(df)

if __name__ == "__main__":
    main()