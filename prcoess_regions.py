import pandas as pd
import openpyxl

def load_and_process_data(file_path):
    # Load data from a CSV file
    data = pd.read_csv(file_path)
    print("Data loaded successfully.")

    print(data.describe())
    return data


def convert_df(data):
    regions = ['southwest', 'northeast', 'northwest']  # adjust if you have more

    processed = data.copy()

    # Create region by selecting the column with the max value per row
    processed['region'] = processed[regions].idxmax(axis=1)

    # If a row has all zeros, idxmax will still return the first column — replace those with NA
    no_flag_mask = (processed[regions].sum(axis=1) == 0)
    processed.loc[no_flag_mask, 'region'] = 'none'

    # Detect ties: more than one column equals the row max
    row_max = processed[regions].max(axis=1)
    ties_mask = processed[regions].eq(row_max, axis=0).sum(axis=1) > 1
    processed.loc[ties_mask, 'region'] = 'none'  # or handle ties differently if you prefer
    print("no_flag rows:", no_flag_mask.sum())
    print("tie rows:", ties_mask.sum())
    return processed

def copy_df(data):
        new_cols = ['sex', 'region', 'smoker','age', 'bmi', 'children',  'charges']
        new_df = pd.DataFrame(columns=new_cols)
        new_df = pd.concat([new_df, data[new_cols].copy()], ignore_index=True)
        return new_df

def send_to_excel(data, file_name="Insurance_Data.xlsx"):
    data.to_excel(file_name, index=False)
    print(f"Data exported to {file_name} successfully.")
    
if __name__ == "__main__":
    file_path = "insurance_clean.csv"  # Replace with your CSV file path
    data = load_and_process_data(file_path)
    processed_data = convert_df(data)
    copied_data = copy_df(processed_data)
    send_to_excel(copied_data)