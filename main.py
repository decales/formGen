import pandas as pd

pd.options.display.width = 0
pd.options.display.max_rows = 500

# File paths
disposal_path = r'disposal.csv'
master_path = r'master.xlsx'

# Create data frames
disposal_df = pd.read_csv(disposal_path)
master_df = pd.read_excel(master_path, 'Box')

# Convert key column values to str for merge
disposal_df['Transfer'] = disposal_df['Transfer'].astype(str)
master_df['Transfer'] = master_df['Transfer'].astype(str)
disposal_df['Box'] = disposal_df['Box'].astype(str)
master_df['Box'] = master_df['Box'].astype(str)



merged = pd.merge(disposal_df.query('Dispose == True').get(['Transfer', 'Box']), master_df, how='left')
merged.pop('Current Location')
merged.pop('Notes')
flagged = merged.query("Status != 'Active' | Disposal > 2023")

print(merged)



