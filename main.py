import sys
import data
import generation

# File paths
disposal_path = r'input/disposal.csv'
master_path = r'input/master.xlsx'

# Create data frames and merge
dataframes = data.readFiles(master_path, disposal_path)
merge = data.mergeDataFrames(dataframes)

# Get merge and flag data frames
merge_df = merge[0]
flag_df = merge[1]

fields_list = data.extractFields(merge_df)

generation.generateAll(fields_list, sys.path[0], flag_df)