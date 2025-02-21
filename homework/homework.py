"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel
import pandas as pd
import zipfile

def readfiles():
    files_dfs = []

    for i in range(10):
        zip_path = f"files/input/bank-marketing-campaing-{i}.csv.zip"
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            file_names = zip_file.namelist()
            with zip_file.open(file_names[0]) as file:
                file_df = pd.read_csv(file)
                files_dfs.append(file_df)
    return pd.concat(files_dfs)

def define_client_df(df):
    client_df = df[[
        "client_id",
        "age",
        "job",
        "marital",
        "education",
        "credit_default",
        "mortgage"
        ]].copy()

    client_df["job"] = client_df["job"].str.replace(".", "").str.replace("-", "_")
    client_df["education"] = client_df["education"].str.replace(".", "_").replace({"unknown": pd.NA})
    
    client_df["credit_default"] = client_df["credit_default"].map(lambda x: 1 if x == "yes" else 0)
    client_df["mortgage"] = client_df["mortgage"].map(lambda x: 1 if x == "yes" else 0)

    return client_df

def define_campaign_df(df):
    campaign_df = df[[
        "client_id",        
        "number_contacts",        
        "contact_duration",        
        "previous_campaign_contacts",        
        "previous_outcome",
        "campaign_outcome"
    ]].copy()

    campaign_df["previous_outcome"] = campaign_df["previous_outcome"].map(lambda x: 1 if x == "success" else 0)    
    campaign_df["campaign_outcome"] = campaign_df["campaign_outcome"].map(lambda x: 1 if x == "yes" else 0)    

    month_mapping = {
    "jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05", "jun": "06",
    "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12"
    }

    df["month"] = df["month"].map(month_mapping)

    campaign_df["last_contact_date"] = "2022-" + df["month"] + "-" + df["day"].astype(str).str.zfill(2)

    return campaign_df

def define_economics_df(df):
    economics_df = df[[
    "client_id",
    "cons_price_idx",
    "euribor_three_months"
    ]].copy()

    return economics_df


def clean_campaign_data():
    
    df = readfiles()
    client_df = define_client_df(df)
    campaign_df = define_campaign_df(df)
    economics_df = define_economics_df(df)

    client_df.to_csv("files/output/client.csv", index = False)
    campaign_df.to_csv("files/output/campaign.csv", index = False)
    economics_df.to_csv("files/output/economics.csv", index = False)


if __name__ == "__main__":
    clean_campaign_data()
