import pyodbc
import psycopg2

conn = psycopg2.connect(database="postgres", user = "postgres", password = "alan7474", host = "127.0.0.1", port = "5433")

print("Opened database successfully")

cur = conn.cursor()

###########################################################################################################################

#cur.execute('''CREATE TABLE Influenza
 #     (ID SERIAL PRIMARY KEY     NOT NULL,
  #    Ano           TEXT    ,
   #   N_de_casos            TEXT     
    #  );''')
#print("Table created successfully")


#cur.execute("INSERT INTO Influenza (Ano, N_de_casos) \
  #    VALUES ('1965','80')");

cur.execute("SELECT * FROM Influenza")

rows = cur.fetchall()
for row in rows:
   print("ID = ", row[0])
   print("Ano = ", row[1])
   print("N_de_casos = ", row[2])
  

print("Operation done successfully")

#cur.execute("SELECT * from hepatites")



conn.commit()


conn.close()

#cur.execute("SELECT id, name, address, salary  from COMPANY")





