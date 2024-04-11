import pandas as pd
import sqlite3
import os

from utils.helper_functions import get_data_from_file, create_processed_files, get_search_criteria
from utils.sqls import sql_create_real_estate_data, sql_create_processed_files


def process_file(file_path, conn):
    file_name = file_path.split("data/")[1].replace(".json", "")
    print(f"Processing file {file_name}")
    file_search_crit = get_search_criteria(file_name)

    # Check if all table exists and query the processed_files table
    cursor = conn.cursor()
    cursor.execute(sql_create_real_estate_data)
    cursor.execute(sql_create_processed_files)
    query = 'SELECT * FROM processed_files;'
    db_df_pf = pd.read_sql_query(query, conn)
    if file_name in list(db_df_pf["file"]) or file_search_crit in list(db_df_pf["search_criteria"]):
        print("Data already present in the database")
        is_inserted = False
        df = pd.DataFrame()
    else:
        df = get_data_from_file(file_path, file_name)
        is_inserted = True
        # Write df to "real_estate_data" table
        df.to_sql('real_estate_data', conn, index=False, if_exists='append')
        print("Saved data into real_estate_data table")

    # CREATE AND SAVE TABLE PROCESSED_FILES
    if file_name not in list(db_df_pf["file"]):
        df_pf = create_processed_files(file_name, df, is_inserted)
        df_pf.to_sql('processed_files', conn, index=False, if_exists='append')
        print("Saved data into processed_files table")
    else:
        print(f"File {file_name} has already been processed")


def file_processing(file_path, db, files_added):
    file_name = file_path.split("data/")[1].replace(".json", "")
    print(f"Processing file {file_name}")
    file_search_crit = get_search_criteria(file_name)

    # Check if all table exists and query the processed_files table
    with db.engine.connect() as connection:
        connection.execute(sql_create_real_estate_data)
        connection.execute(sql_create_processed_files)
    query = 'SELECT * FROM processed_files;'
    db_df_pf = pd.read_sql_query(query, db.engine)
    if file_name in list(db_df_pf["file"]) or file_search_crit in list(db_df_pf["search_criteria"]):
        print("Data already present in the database")
        is_inserted = False
        df = pd.DataFrame()
    else:
        df = get_data_from_file(file_path, file_name)
        is_inserted = True
        # Write df to "real_estate_data" table
        df.to_sql('real_estate_data', db.engine, index=False, if_exists='append')
        print("Saved data into real_estate_data table")

    # CREATE AND SAVE TABLE PROCESSED_FILES
    if file_name not in list(db_df_pf["file"]):
        df_pf = create_processed_files(file_name, df, is_inserted)
        df_pf.to_sql('processed_files', db.engine, index=False, if_exists='append')
        print("Saved data into processed_files table")
        files_added.append(file_name)
    else:
        print(f"File {file_name} has already been processed")


def refresh_database(db):
    folder_path = os.path.join(os.getcwd(), 'data')
    files_added = []
    for filename in os.listdir(folder_path):
        # Construct the full file path by joining the folder path and filename
        file_path = os.path.join(folder_path, filename)
        # Check if it's a file (not a subdirectory)
        if os.path.isfile(file_path):
            file_processing(file_path, db, files_added)
        return files_added




# STANDARD PROCEDURE

#SQLite database file
# db_file = 'real_estate_db.db'
#
# # Create a connection to the SQLite database
# conn = sqlite3.connect(db_file)
#
# #folder_path = r"C:\Users\ADMIN\Desktop\Pliki\Data_Stuff\Python\API_real_estate\data"
# folder_path = os.path.join(os.getcwd(), 'data')
# #file_path = r"data/2024-01-08-09-07_Plock_output.json"
# for filename in os.listdir(folder_path):
#     # Construct the full file path by joining the folder path and filename
#     file_path = os.path.join(folder_path, filename)
#
#     # Check if it's a file (not a subdirectory)
#     if os.path.isfile(file_path):
#         process_file(file_path, conn)











# def process_file(file_path):
#     file_name = file_path.split("data/")[1].replace(".json", "")
#     file_search_crit = get_search_criteria(file_name)
#
#     # Query the processed_files table
#     query = 'SELECT * FROM processed_files;'
#     db_df_pf = pd.read_sql_query(query, conn)
#
#     # TODO Comparison with metadata table processed_files and deciding whether to process the file
#     if (file_name in db_df_pf["file"] or file_search_crit in db_df_pf["search_criteria"]):
#         print("Data already present in the database")
#         is_inserted = False
#         df = pd.DataFrame()
#     else:
#         df = get_data_from_file(file_path, file_name)
#         is_inserted = True
#         # Write df to "real_estate_data" table
#         df.to_sql('real_estate_data', conn, index=False, if_exists='append')
#         print("Saved data into real_estate_data table")
#
#     # CREATE AND SAVE TABLE PROCESSED_FILES
#     df_pf = create_processed_files(file_name, df, is_inserted)
#     df_pf.to_sql('processed_files', conn, index=False, if_exists='append')
#     print("Saved data into processed_files table")


# Query the SQLite database
# query = 'SELECT min(size_m2), max(size_m2) FROM real_estate_data;'
# result_df = pd.read_sql_query(query, conn)

