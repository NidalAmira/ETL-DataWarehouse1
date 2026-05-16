
import pandas as pd
from sqlalchemy import create_engine

engine_oltp = create_engine(
    "mysql+mysqlconnector://root:0000@localhost/movie_rental_oltp"
)

engine_dw = create_engine(
    "mysql+mysqlconnector://root:0000@localhost/movie_rental_dw"
)

print("Connected Successfully")
query_customer = """
SELECT
    c.customer_id AS Customer_ID,
    CONCAT(c.first_name, ' ', c.last_name) AS Full_Name,
    c.email AS Email,
    a.address AS Address,
    ci.city AS City,
    co.country AS Country,
    CASE
        WHEN c.active = 1 THEN 'Active'
        ELSE 'Inactive'
    END AS Active_Status
FROM customer c
JOIN address a
    ON c.address_id = a.address_id
JOIN city ci
    ON a.city_id = ci.city_id
JOIN country co
    ON ci.country_id = co.country_id
"""

df_customer = pd.read_sql(query_customer, engine_oltp)

print(df_customer.head())

df_customer.to_sql(
    "Dim_Customer",
    con=engine_dw,
    if_exists="append",
    index=False
)

query_film = """
SELECT
    film_id AS Film_ID,
    title AS Title,
    release_year AS Release_Year,
    rental_duration AS Rental_Duration,
    rental_rate AS Rental_Rate,
    length AS Length_Minutes,
    rating AS Rating
FROM film
"""

df_film = pd.read_sql(query_film, engine_oltp)

print(df_film.head())

df_film.to_sql(
    "Dim_Film",
    con=engine_dw,
    if_exists="append",
    index=False
)

query_store = """
SELECT
    s.store_id AS Store_ID,
    a.address AS Store_Address,
    ci.city AS City,
    co.country AS Country
FROM store s
JOIN address a
    ON s.address_id = a.address_id
JOIN city ci
    ON a.city_id = ci.city_id
JOIN country co
    ON ci.country_id = co.country_id
"""

df_store = pd.read_sql(query_store, engine_oltp)

print(df_store.head())

df_store.to_sql(
    "Dim_Store",
    con=engine_dw,
    if_exists="append",
    index=False
)

query_staff = """
SELECT
    staff_id AS Staff_ID,
    CONCAT(first_name, ' ', last_name) AS Full_Name,
    email AS Email,
    CASE
        WHEN active = 1 THEN 'Active'
        ELSE 'Inactive'
    END AS Active_Status
FROM staff
"""

df_staff = pd.read_sql(query_staff, engine_oltp)

print(df_staff.head())

df_staff.to_sql(
    "Dim_Staff",
    con=engine_dw,
    if_exists="append",
    index=False
)

query_rental = """
SELECT
    rental_id AS Rental_Key,
    customer_id AS Customer_Key,
    inventory_id AS Inventory_Key,
    staff_id AS Staff_Key
FROM rental
"""

df_rental = pd.read_sql(query_rental, engine_oltp)

print(df_rental.head())

df_rental.to_sql(
    "Fact_Rental",
    con=engine_dw,
    if_exists="append",
    index=False
)

query_payment = """
SELECT
    payment_id AS Payment_Key,
    customer_id AS Customer_Key,
    staff_id AS Staff_Key,
    rental_id AS Rental_Key,
    amount AS Payment_Amount
FROM payment
"""

df_payment = pd.read_sql(query_payment, engine_oltp)

print(df_payment.head())

df_payment.to_sql(
    "Fact_Payment",
    con=engine_dw,
    if_exists="append",
    index=False
)

query_inventory = """
SELECT
    inventory_id AS Inventory_Key,
    film_id AS Film_Key,
    store_id AS Store_Key
FROM inventory
"""

df_inventory = pd.read_sql(query_inventory, engine_oltp)

print(df_inventory.head())

df_inventory.to_sql(
    "Fact_Inventory",
    con=engine_dw,
    if_exists="append",
    index=False
)

print("ETL Completed Successfully")
