import pandas as pd
import functions


def readFiles(master_path, disposal_path):
    try:
        master_box = pd.read_excel(master_path, 'Box')
    except Exception:
        print("There was an error reading the 'Box' sheet of the master file")
    try:
        master_transfer = pd.read_excel(master_path, 'Transfer')
    except Exception:
        print("There was an error reading the 'Transfer' sheet of the master file")
    try:
        disposal = pd.read_csv(disposal_path)
    except Exception:
        print("There was an error reading the disposal file")

    return master_box, master_transfer, disposal


def mergeDataFrames(dfs):
    # Convert key column values to str for merge
    dfs[0]['Transfer'] = dfs[0]['Transfer'].astype(str)
    dfs[0]['Box'] = dfs[0]['Box'].astype(str)
    dfs[1]['Transfer'] = dfs[1]['Transfer'].astype(str)
    dfs[2]['Transfer'] = dfs[2]['Transfer'].astype(str)
    dfs[2]['Box'] = dfs[2]['Box'].astype(str)

    # Left merge disposal dataframe where boxes are to be disposed with master data frames
    return pd.merge(dfs[2].query('Dispose == True'), dfs[0].drop('Branch / Board / Program', axis='columns'), how='left', on=['Transfer', 'Box']).merge(dfs[1], how='left', on='Transfer')


def extractFields(df):
    # Get all non-duplicate transfers from disposable dataframe
    transfers = df.drop_duplicates('Transfer')['Transfer'].tolist()

    fields = []
    for i in transfers:
        # Query each transfer in disposal dataframe
        transfer_query = df.query("Transfer == '{}'".format(i))

        # Format start and end into single variable date
        start = str(min(transfer_query['Fiscal (start)'].tolist())).strip('.0')
        end = str(max(transfer_query['Fiscal (end)'].tolist())).strip('.0')
        if start == end and start != 'nan':
            date = start
        elif start != 'nan' and end != 'nan':
            date = "{}-{}".format(start, end)
        elif start == 'nan' and end != 'nan':
            date = end
        elif start != 'nan' and end == 'nan':
            date = start
        else:
            date = "N/A"

        # Create list of dictionaries with keys for transfer, boxes, branch name, earliest year, latest year, description, and schedules
        fields.append({
            "transfer": i,
            "branch": transfer_query['Branch / Board / Program'].iloc[0],
            "boxes": functions.rangify(transfer_query['Box'].tolist()),
            "total": str(len(transfer_query['Box'].tolist())),
            "date": date,
            "description": transfer_query['Description of Records'].iloc[0],
            "schedule": transfer_query['Schedules'].iloc[0]
        })

    return fields