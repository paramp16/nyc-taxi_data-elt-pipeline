import pandas as pd
# Show every column without truncation
pd.set_option("display.max_columns", None)

# Ensurse wide columns don't wrap to a new line in the terminal
pd.set_option("display.width", 1000)
df = pd.read_parquet('data/yellow_tripdata_2026-01.parquet')


# print(df.head())

# print(df.info())

# print(df.describe())

# rows = len(df)
# print("The number of rows in this dataset {0}".format(rows))


# types = df.dtypes
# print("These are the different Data Types in the dataset: {x}".format(x=types))

# sh = df.shape

# print('This is the shape of the dataset: {s}'.format(s=sh))



# print(df.columns[df.isnull().any()])


# matching_rows = df[(df['VendorID'] == 2) & (df['tpep_pickup_datetime'] == '2026-01-22 21:30:20')
#                    & (df['tpep_dropoff_datetime'] == '2026-01-22 21:31:05') &
#                     (df['trip_distance'] == 0.04) & (df['passenger_count'] == 1) ]

# print(matching_rows)

file = input("Enter file name: ")
# Check filename in load_batches - if success (skip)


df = pd.read_parquet(f'data/{file}.parquet')
print(df.head())