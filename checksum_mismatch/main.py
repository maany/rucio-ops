import logging 
import logging
import colorlog
import pyperclip
from agent import FTSLogScrapingAgent, RucioWebUIAgent
import time
from utils import load_csv
from tqdm import tqdm
import os
logger = logging.getLogger(__name__)
import pandas as pd

def main():
    df = load_csv("transfer_details_23_feb_csv.csv")
    # drop duplicates
    df = df.drop_duplicates(subset=['Name'])

    # list all columns in the DataFrame
    logger.debug(df.columns)
    # list unique values in Destination RSE column
    unique_dest_rses = df["Destination RSE"].unique()
    logger.debug(f"Unique Destination RSEs: {unique_dest_rses}")
    # count the number of transfers for each destination RSE
    dest_rse_counts = df["Destination RSE"].value_counts()

    # show average File Size, max File Size, and min File Size, median File Size
    file_size_gb = df['File size'] / 1073741824
    logger.info(f"Average File Size: {file_size_gb.mean()} GB")
    logger.info(f"Max File size: {file_size_gb.max()} GB")
    logger.info(f"Min File size: {file_size_gb.min()} GB")
    logger.info(f"Median File size: {file_size_gb.median()} GB")

    # Show Scope and Name columns for entries with max file size
    max_file_size_entries = df[df['File size'] == df['File size'].max()]
    logger.info("Entries with Max File Size:")
    logger.info(max_file_size_entries[['Scope', 'Name']])

    # Show Scope and Name columns for entries with min file size
    min_file_size_entries = df[df['File size'] == df['File size'].min()]
    logger.info("Entries with Min File Size:")
    logger.info(min_file_size_entries[['Scope', 'Name']])
    
    # logger.warning("\n===================== Starting Scraping ===================")
    # # Scope Scope:Name, FTS Link, Source URL, Destination URL for first 10 entries
    # df['did'] = df[['Scope', 'Name']].agg(':'.join, axis=1)
    # df['temp'] = df[['Scope','Name']].agg('&name='.join, axis=1).astype(str)
    # df['webui_link'] = "https://rucio-ui.cern.ch/did?scope=" + df['temp']

    # did_table = df[['did', 'FTS Link', 'webui_link', 'Destination RSE']]
    # logger.info(did_table.head(10))

    # #save df to a new csv file
    # df.to_csv("transfer_details_23_feb_csv_with_did_unique.csv")
    # pyperclip.paste()

    # # print total number of transfers
    # logger.info(f"Total number of transfers: {len(df)}")

    # fts_agent = FTSLogScrapingAgent()
    # df_fts = df[['did', 'FTS Link']]
    # df = execute_agent(fts_agent, df, df_fts, 'FTS Link', log_output=False)
    # df.to_csv("transfer_details_23_feb_csv_with_did_and_checksum_and_fts_unique.csv")

    # agent = RucioWebUIAgent()
    # df_webui = df[['did', 'webui_link']]
    # df = execute_agent(agent, df, df_webui, 'webui_link')
    # df.to_csv("transfer_details_23_feb_csv_with_did_and_checksum_unique.csv")

    dids_to_filter_for =   extract_files("/Users/maany/Downloads/final")
    list_of_names = [x['Name'] for x in dids_to_filter_for]
    list_of_scopes = [x['Scope'] for x in dids_to_filter_for]
    df_filtered = df[df['Scope'].isin(list_of_scopes)]
    df_filtered = df_filtered[df_filtered['Name'].isin(list_of_names)] 
    # add rucio checksum and destination checksum to the df
    df_filtered = df_filtered.merge(pd.DataFrame(dids_to_filter_for), on='Name', how='left')
    df_final = df_filtered[['Timestamp', 'Scope_x', 'Name', 'Destination RSE', 'Destination URL', 'Rucio_Checksum', 'Destination_Checksum']]
    df_final.to_csv("transfer_details_23_feb_csv_needs_seal_checksum.csv")
    logger.info(df_final)



def execute_agent(agent, df, df_clipped, url_field, log_output=True):
    total_time = 0.0
    for index, row in tqdm(df_clipped.iterrows(), total=len(df_clipped), desc="Progress"):
        start = time.time()
        # Access each item in the row
        did = row['did']
        link = row[url_field]
        
        # Perform operations on the items
        logger.info(f"URL for {did}: {link}")
        output = agent.execute(link, row)
        if log_output:
            logger.warning(f"output for {did}: {output}")
        df.at[index, 'output'] = output
        end = time.time()
        
        # Calculate time taken for each transfer
        time_per_transfer = end - start
        total_time += time_per_transfer
        average_time = total_time / (index + 1)
        transfers_remaining = len(df_clipped) - index
        time_remaining = transfers_remaining * average_time
        time_remaining_mins = round(time_remaining / 60)
        logger.warning(f"Time remaining: {time_remaining_mins} minutes")
    return df


def extract_checksums_from_last_line(file):
    """Extract the checksums from the last line of the file if it contains "DESTINATION CHECKSUM MISMATCH".

    Args:
        file (str): The file to extract checksums from.

    Returns:
        (str, str): The adler32 and md5 checksums if found, otherwise None.
    """
    with open(file, 'r') as f:
        lines = f.readlines()
        last_line = lines[-1].strip()
        if "DESTINATION CHECKSUM MISMATCH" in last_line:
            start_index = last_line.find("(") + 1
            end_index = last_line.find(")")
            checksums = last_line[start_index:end_index].split(" != ")
            if len(checksums) == 2:
                return checksums[0], checksums[1]
    return None

def extract_files(location):
    """Extract all txt files from a given location. The file name is the DID.
    Returns the list of file names.

    Args:
        location (str): The location to extract files from.
    """
    file_names = []
    for file in os.listdir(location):
        if file.endswith(".txt"):
            file_name = os.path.splitext(file)[0]
            scope = file_name.split("-")[0]
            did = "".join(file_name.split("-")[1:])
            checksums = extract_checksums_from_last_line(os.path.join(location, file))
            if(checksums is not None):
                Rucio_Checksum, Destination_Checksum = checksums
                file_names.append({"Name": did, "Scope": scope, "Rucio_Checksum": Rucio_Checksum, "Destination_Checksum": Destination_Checksum})
            
    return file_names

if __name__ == '__main__':
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(message)s%(reset)s",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)

    main()
    # checksums = extract_checksums_from_last_line("/Users/maany/Downloads/final/mc16_13TeV-AOD.14795494._007439.pool.root.1.txt")
    # logger.info(checksums)
    # file_names = extract_files("/Users/maany/Downloads/final")
    # logger.info(file_names)


