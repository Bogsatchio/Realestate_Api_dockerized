
sql_create_real_estate_data = """
CREATE TABLE IF NOT EXISTS `real_estate_data` (
  `link` TEXT,
  `city` TEXT,
  `title` TEXT,
  `price` REAL,
  `price_sqm` INTEGER,
  `when_added_approx_days` INTEGER,
  `scrap_time` DATE,
  `address` TEXT,
  `size_m2` REAL,
  `n_rooms` INTEGER,
  `floor` INTEGER,
  `rent` REAL,
  `ownership_type` TEXT,
  `condition` TEXT,
  `outdoor` TEXT,
  `heating` TEXT,
  `market_type` TEXT,
  `advertiser_type` TEXT,
  `build_year` INTEGER,
  `building_type` TEXT,
  `windows_type` TEXT,
  `elevator` TEXT,
  `security_type` TEXT,
  `equipment_type` TEXT,
  `add_info` TEXT,
  `building_material` TEXT,
  `description` TEXT,
  `floors_in_building` INTEGER,
  `origin_file` TEXT
)"""

sql_create_processed_files = """
CREATE TABLE IF NOT EXISTS `processed_files` (
  `file` TEXT,
  `process_date` TIMESTAMP,
  `search_criteria` TEXT,
  `min_search` INTEGER,
  `max_search` INTEGER,
  `rows_added` INTEGER,
  `successfully_inserted` INTEGER
)
"""

# First part of the query is not taking into account continuous duplicate in scrapping
sql_data_overview = """ 
SELECT
main_tbl1.*, main_tbl2.min_scrap_time, main_tbl2.max_scrap_time
FROM
(
SELECT
city, MIN(size_m2) as min_size, MAX(size_m2) as max_size, CAST(AVG(build_year) AS SIGNED) as average_building_year,
CAST(AVG(price_sqm) AS SIGNED) AS average_price_sqm, COUNT(DISTINCT link) AS num_of_adverts, 
CAST(AVG(rent) AS SIGNED) AS average_rent
FROM 
(SELECT DISTINCT link, city, size_m2, build_year, price_sqm, rent FROM real_estate_data) as src_tbl
GROUP BY city
) as main_tbl1
left join 
(
SELECT city, MIN(scrap_time) as min_scrap_time, MAX(scrap_time) as max_scrap_time
from real_estate_data GROUP BY city
) as main_tbl2
on main_tbl1.city = main_tbl2.city
"""

sql_price_change = """ select changed_price_tbl.link, data_tbl.scrap_time, data_tbl.price
FROM real_estate_data as data_tbl join 
(
SELECT link, count(price) FROM
(select distinct link, price from real_estate_data) as src_tbl
group by link having count(price) > 1
) as changed_price_tbl
on data_tbl.link = changed_price_tbl.link
"""

sql_market_comparison = """ 
SELECT 
city, market, CAST(AVG(price_sqm) AS SIGNED) AS average_price_sqm, 
CAST(AVG(size_m2) AS SIGNED) AS average_size_m2, CAST(AVG(build_year) AS SIGNED) AS average_build_year
FROM
(
SELECT DISTINCT
city,
CASE 
WHEN market_type = 'wtórny' THEN advertiser_type
ELSE market_type END AS market, 
price_sqm, size_m2, build_year, link
FROM real_estate_data
WHERE market_type is not null) as src_tbl
group by city, market
"""

sql_age_comparison = """ 
SELECT
city, age_of_apartment, 
CAST(AVG(price_sqm) as SIGNED) AS average_price_sqm, CAST(avg(rent) AS SIGNED) AS average_rent
FROM
(
SELECT DISTINCT
CASE
WHEN build_year < 1990 THEN 'over 35 years'
WHEN build_year > 2015 THEN 'less than 10 years'
ELSE 'between 10 and 35 years' END AS age_of_apartment,
city, price_sqm, rent, link
FROM real_estate_data
WHERE build_year is not null
) AS derived
GROUP BY city, age_of_apartment
"""

sql_get_cities_data = """
SELECT city ,MIN(size_m2) as min ,MAX(size_m2) as max from real_estate_data GROUP BY city
"""

def get_entire_search(city, min_s, max_s):
    query = f""" 
    SELECT * FROM real_estate_data
    WHERE city = '{city}' AND size_m2 > {int(min_s)} AND size_m2 < {int(max_s)} ;
    """
    return query

def get_latest_search(city, min_s, max_s):
    query = f""" 
    SELECT * FROM real_estate_data
    WHERE city = '{city}' AND size_m2 > {int(min_s)} AND size_m2 < {int(max_s)} 
    AND scrap_time = (SELECT MAX(scrap_time) FROM real_estate_data WHERE city = '{city}');
    """
    return query


def get_prices_over_time(city, min_s, max_s):
    query = f""" 
    SELECT scrap_time as scrapped_time, CAST(AVG(price_sqm) AS SIGNED) AS average_price_sqm FROM real_estate_data
    WHERE city = '{city}' AND size_m2 > {min_s} AND size_m2 < {max_s}
    GROUP BY scrap_time 
    """
    return query

def get_price_change(city, min_s, max_s):
    query = f"""
    select changed_price_tbl.link, data_tbl.scrap_time, data_tbl.price
    FROM real_estate_data as data_tbl join 
    (
    SELECT link, count(price) FROM
    (select distinct link, price from real_estate_data
    WHERE city = '{city}' AND size_m2 > {min_s} AND size_m2 < {max_s}) as src_tbl
    group by link having count(price) > 1
    ) as changed_price_tbl
    on data_tbl.link = changed_price_tbl.link
    """
    return query


