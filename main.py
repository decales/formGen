import sys
import data
import generation

# File paths
disposal_path = r'input/disposal.csv'
master_path = r'input/master.xlsx'

# Create data frames and merge
dataframes = data.readFiles(master_path, disposal_path)
merge = data.mergeDataFrames(dataframes)

# Separate disposable and flagged boxes
flag = merge.query("Status != 'Active' | Disposal > 2023")
dispose = merge.query("Status == 'Active' & Disposal <= 2023")

fields_list = data.extractFields(dispose)

generation.generateAll(fields_list, sys.path[0])