from django.db import connection

cursor = connection.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS presencas_configuracaopresenca (id bigserial PRIMARY KEY);"
)
cursor.execute("select to_regclass('presencas_configuracaopresenca');")
print(cursor.fetchone())
