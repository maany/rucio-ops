import logging 
import logging
import colorlog
import pyperclip
from agent import RucioWebUIAgent
import time
from utils import load_csv
from tqdm import tqdm

logger = logging.getLogger(__name__)

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
    
    logger.warning("\n===================== Starting Scraping ===================")
    # Scope Scope:Name, FTS Link, Source URL, Destination URL for first 10 entries
    df['did'] = df[['Scope', 'Name']].agg(':'.join, axis=1)
    df['temp'] = df[['Scope','Name']].agg('&name='.join, axis=1).astype(str)
    df['webui_link'] = "https://rucio-ui.cern.ch/did?scope=" + df['temp']

    did_table = df[['did', 'FTS Link', 'webui_link', 'Destination RSE']]
    logger.info(did_table.head(10))

    #save df to a new csv file
    df.to_csv("transfer_details_23_feb_csv_with_did_unique.csv")
    pyperclip.paste()

    # print total number of transfers
    logger.info(f"Total number of transfers: {len(df)}")

    agent = RucioWebUIAgent()
    df_webui = df[['did', 'webui_link']]
    df = execute_agent(agent, df, df_webui)
    df.to_csv("transfer_details_23_feb_csv_with_did_and_checksum_unique.csv")

    df_fts = df[['did', 'FTS Link']]

def execute_agent(agent, df, df_clipped):
    total_time = 0.0
    for index, row in tqdm(df_clipped.iterrows(), total=len(df_clipped), desc="Progress"):
        start = time.time()
        if index > 2:
            break
        # Access each item in the row
        did = row['did']
        webui_link = row['webui_link']
        
        # Perform operations on the items
        logger.info(f"URL for {did}: {webui_link}")
        checksum = agent.execute(webui_link)
        logger.warning(f"Checksum for {did}: {checksum}")
        df.at[index, 'webui_checksum'] = checksum
        end = time.time()
        
        # Calculate time taken for each transfer
        time_per_transfer = end - start
        total_time += time_per_transfer
        average_time = total_time / (index + 1)
        transfers_remaining = len(df_clipped) - index
        time_remaining = transfers_remaining * average_time
        time_remaining_mins = round(time_remaining / 60)
        logger.warn(f"Time remaining: {time_remaining_mins} minutes")
    return df


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


