
import pandas as pd
import mysql.connector as msql
from mysql.connector import Error
try:
    conn = msql.connect(host='localhost', user='root',  
                        password='')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE employee")
        print("Database is created")
except Error as e:
    print("Error while connecting to MySQL", e)

empdata = pd.read_csv('./FinishedProduct.csv', index_col=False, delimiter = ',')
empdata.head()
print (empdata)

try:
    conn = msql.connect(host='localhost', database='employee', user='root', password='')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS employee_data;')
        print('Creating table....')

        cursor.execute("CREATE TABLE employee_data(Est_number varchar(100),Company varchar(100),	Production_Date varchar(100)	,\
                       Lot_Number bigint,Material_Description bigint,	Sample_Selection varchar(100),	Sublot_Number bigint,\
                       	Pounds_Produced bigint	,Sample_Number varchar(100) 	,APC bigint,	APC_CPU double,	Coliform bigint,\
                       	Coliform_CPU bigint,	Generic_E_coli bigint,	Generic_E_coli_CPU bigint,	S_aureus bigint,\
                       	S_aureus_2 bigint,	Potential_E_coli_O157_H7 bigint,	Presumptive_E_coli_O157_H7 bigint,\
                       	E_coli_O157_H7 bigint,	E_Coli_O157_H7_Cl bigint,	Potential_Salmonella bigint,\
                       	Salmonella bigint,	Salmonella_Cl bigint,	Status char(100))")
        print("Table is created....")
        #loop through the data frame
        for i,row in empdata.iterrows():
            #here %S means string values 
            sql = "INSERT INTO employee.employee_data VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            # the connection is not auto committed by default, so we must commit to save our changes
            conn.commit()
except Error as e:
            print("Error while connecting to MySQL", e)
