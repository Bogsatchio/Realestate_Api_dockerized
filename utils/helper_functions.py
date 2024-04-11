import pandas as pd
import chardet
import re
from datetime import datetime

# Custom function for extracting days from when_added_approx_days
def get_days(val):
    if val != None:
        val = val.replace("Data dodania: ", '').replace(" temu", '')
        if "g" in val:
            return 1
        elif "d" in val:
            return int(''.join(filter(str.isdigit, val)))
        else:
            return int(''.join(filter(str.isdigit, val))) * 30


def get_data_from_file(file_path, file_name):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())

    encoding = result['encoding']

    # Read the JSON file with the detected encoding
    df = pd.read_json(file_path, encoding=encoding, orient="index")

    # adding floors in the building column
    regex_pattern = r'^\d+/\d+$'
    df["floors_in_building"] = df['floor'].apply(
        lambda x: x[-1] if pd.notna(x) and pd.Series(x).str.match(regex_pattern).any() else None)
    df['floors_in_building'] = pd.to_numeric(df['floors_in_building'], errors='coerce').astype(pd.Int32Dtype())

    df["when_added_approx_days"] = df["when_added_approx_days"].apply(get_days)

    # int transformation (floor, build_year)
    # df["floor"] = df["floor"].apply(lambda x: 0 if "parter" in x else x[0])
    df["floor"] = df["floor"].apply(
        lambda x: 0 if (x is not None and "parter" in x) else (x[0] if (x and len(x) > 0) else None))
    df['floor'] = pd.to_numeric(df['floor'], errors='coerce').astype(pd.Int32Dtype())
    df['build_year'] = df['build_year'].str.replace(r'[^0-9]', '', regex=True).replace('', None)
    df['build_year'] = pd.to_numeric(df['build_year'], errors='coerce').astype(pd.Int32Dtype())
    df['n_rooms'] = pd.to_numeric(df['n_rooms'], errors='coerce').astype(pd.Int32Dtype())

    df['scrap_time'] = pd.to_datetime(df['scrap_time'], format='%Y-%m-%d-%H-%M')

    # float transformation
    float_cols = ["price", "size_m2", "price_sqm", "rent", ]
    for x in float_cols:
        df[x] = df[x].str.replace(",", ".").replace(r'[^0-9.]', '', regex=True)
        df[x] = pd.to_numeric(df[x], errors='coerce')

    # adding a column for origin file
    df["origin_file"] = file_name
    return df


def create_processed_files(file_name, df, is_inserted):
    current_datetime = datetime.now()
    search_crit, min_s, max_s = get_search_criteria(file_name)
    processed_files_dict = {"file": file_name,
                            "process_date": current_datetime,
                            "search_criteria": search_crit,
                            "min_search": min_s,
                            "max_search": max_s,
                            "rows_added": len(df),
                            "successfully_inserted": is_inserted
                            }
    df_pf = pd.DataFrame(processed_files_dict)
    return df_pf


def get_search_criteria(file_name):
    criteria_list = file_name.split("_")
    search_criteria = [datetime.now().date(), criteria_list[1],
                        int(re.sub(r'\D', '', criteria_list[2])),
                        int(re.sub(r'\D', '', criteria_list[3]))]
    return search_criteria, search_criteria[2], search_criteria[3]

