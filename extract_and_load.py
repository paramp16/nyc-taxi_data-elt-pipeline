import pandas as pd
import psycopg
import os, sys
from dotenv import load_dotenv
load_dotenv()

file = input("Enter file name: ").strip()
# Check filename in load_batches - if success (skip)
try:
    conn = psycopg.connect(
        host = os.getenv("PSQL_HOST"),
        user = os.getenv("PSQL_USER"),
        port = os.getenv("PSQL_PORT"),
        dbname = os.getenv("PSQL_DBNAME"),
        password = os.getenv("PSQL_PASSWORD")
    )
    with conn.cursor() as cur:
        cur.execute("SELECT file_name, batch_status FROM load_batches WHERE file_name = %s AND batch_status = 'success'; ",(file,))
        result = cur.fetchone()
        if result is not None:
            print("This batch_file has already been processed.")
            sys.exit()
        else:
            # Flush out staging_data to put in the batch files
            cur.execute("DELETE FROM staging_data;")
except Exception as e:
    print(e)
    conn.rollback()
    sys.exit()



df = pd.read_parquet(f'data/{file}.parquet')
table_name = "staging_data"
target_cols = {
    "VendorID":"vendorID",
    "tpep_pickup_datetime":"trip_pickup_datetime",
    "tpep_dropoff_datetime":"trip_dropoff_datetime",
    "passenger_count":"passenger_count",
    "trip_distance":"trip_distance",
    "RatecodeID":"rateID",
    "store_and_fwd_flag":"store_and_fwd",
    "PULocationID":"meter_engage",
    "DOLocationID":"meter_disengage",
    "payment_type":"payment_type",
    "fare_amount":"fare_amount",
    "extra":"extra_chrg",
    "mta_tax":"metre_tax",
    "tip_amount":"tip_amt",
    "tolls_amount":"toll_amt",
    "improvement_surcharge":"imprvmt_surcharge",
    "total_amount":"total_amt",
    "congestion_surcharge":"congest_surcharge",
    "Airport_fee":"airport_fee",
    "cbd_congestion_fee":"cbd_congest_fee"
    }

df_renamed = df.rename(columns=target_cols)
db_columns = list(target_cols.values())

nyc_dataset = df_renamed[db_columns].where(pd.notnull(df_renamed[db_columns]),None)
columns_str = ",".join(db_columns)
copy_sql = f"COPY staging_data ({columns_str}) FROM STDIN"
try:
    with conn.cursor() as cur:
        with cur.copy(copy_sql) as copy:
            for row in nyc_dataset.itertuples(index=False, name=None):
                copy.write_row(row)

    # Write into raw_trips tables
    with conn.cursor() as cur:
        cur.execute("INSERT INTO raw_trips SELECT * FROM staging_data;")
        print(f'Copied {cur.rowcount} rows from staging to raw_trips.')
        cur.execute("INSERT INTO load_batches VALUES(%s,NOW(),(SELECT COUNT(*) FROM staging_data), 'success');",(file,))
        cur.execute("DELETE FROM staging_data;")
    conn.commit()

except Exception as error:
    print(error)
    conn.rollback()
    sys.exit()

finally:
    conn.close()
