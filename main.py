import pandas as pd

pd.options.display.width = 0
pd.options.display.max_rows = 1000

# File paths
disposal_path = r'disposal.csv'
master_path = r'master.xlsx'

# Create data frames
disposal_df = pd.read_csv(disposal_path)
master_box_df = pd.read_excel(master_path, 'Box')
master_transfer_df = pd.read_excel(master_path, 'Transfer')

# Convert key column values to str for merge
disposal_df['Transfer'] = disposal_df['Transfer'].astype(str)
master_box_df['Transfer'] = master_box_df['Transfer'].astype(str)
master_transfer_df['Transfer'] = master_transfer_df['Transfer'].astype(str)
disposal_df['Box'] = disposal_df['Box'].astype(str)
master_box_df['Box'] = master_box_df['Box'].astype(str)

# Left merge disposal dataframe where boxes are to be disposed with master data frames
merge = pd.merge(disposal_df.query('Dispose == True'), master_box_df.drop('Branch / Board / Program', axis='columns'), how='left', on=['Transfer', 'Box']).merge(master_transfer_df, how='left', on='Transfer')

# Separate disposable and flagged boxes
flag = merge.query("Status != 'Active' | Disposal > 2023")
dispose = merge.query(("Status == 'Active' & Disposal <= 2023"))

transfers = dispose.drop_duplicates('Transfer')['Transfer'].tolist()
branches = []
boxes = []
start_years = []
end_years = []
descriptions = []
schedules = []

for i in transfers:
    # Query each transfer in disposal dataframe
    transfer_query = dispose.query("Transfer == '{}'".format(i))

    # Extract transfer boxes, branch name, earliest year, latest year, description, and schedules
    boxes.append(transfer_query['Box'].tolist())
    branches.append(transfer_query['Branch / Board / Program'].iloc[0])
    start_years.append(min(transfer_query['Fiscal (start)'].tolist()))
    end_years.append(max(transfer_query['Fiscal (end)'].tolist()))
    descriptions.append(transfer_query['Description of Records'].iloc[0])
    schedules.append(transfer_query['Schedules'].iloc[0])

# for i in range(len(transfers)):
#     print("Transfer: {}\nBranch: {}\nBoxes: {}\nStart: {}\nEnd: {}\nDescription: {}\nSchedule: {}\n".format([transfers[i]], branches[i], boxes[i], start_years[i], end_years[i], descriptions[i], schedules[i]))

