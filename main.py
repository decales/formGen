import data

# File paths
disposal_path = r'disposal.csv'
master_path = r'master.xlsx'

# Create data frames and merge
dataframes = data.readFiles(master_path, disposal_path)
merge = data.mergeDataFrames(dataframes)

# Separate disposable and flagged boxes
flag = merge.query("Status != 'Active' | Disposal > 2023")
dispose = merge.query(("Status == 'Active' & Disposal <= 2023"))


fields = data.extractFields(dispose)



