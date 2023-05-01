import psycopg2


conn = psycopg2.connect(
    "host=localhost dbname=postgres user=postgres password=postgres"
)
cur = conn.cursor()
with open(
    "C:/Dev/foodgram-project-react/data/ingredients.csv", "r", encoding="utf-8"
) as f:
    cur.copy_from(f, "recipes_ingridient(name,measurment_unit)", sep=",")
conn.commit()
