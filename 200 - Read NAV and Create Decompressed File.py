# Example Using Python 3.x
import zlib, sys, struct
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import pyodbc
import codecs

# 1 -Create a connection string
Driver = "SQL Server"
Server = "OMSC-F01"
Database = "MIRUSNewTest"
ConnectionString = "Driver={" + Driver + "};Server="+Server+";Database="+Database+";Trusted_Connection=yes;"

conn = pyodbc.connect(ConnectionString)
# 2 - The query we want to use
SQLQuery = """
SELECT  meta.[Object ID] AS TableNo,
		obj.Name AS TableName,
		meta.Metadata
FROM	dbo.[Object Metadata] meta
		JOIN dbo.Object obj
			ON meta.[Object Type] = obj.Type
				AND meta.[Object ID] = obj.ID
WHERE obj.Type = 1
ORDER BY obj.ID"""
# 3 -Load the SQL to a Python Pandas Dataframe
ObjectMetaData = pd.read_sql(sql=SQLQuery,con=conn)#,params=params)
# 4 - loop throught the output (Note - in the initial test I have 
#     limited this to just table 15)
for Name, TableNo, TableName, MetaData in ObjectMetaData.itertuples():
    MetaDataToDecompress = bytearray(MetaData)
    # we need to skip the first four characters
    MetaDataToDecompress = MetaDataToDecompress[4:]
    # now we decompress the data
    output = zlib.decompress(MetaDataToDecompress,-15)
    # We can print it to the screen
    print(output.decode("utf-8"))
    # we can write it to an xml file
    OutputFileName = "NAVTable-" + str(TableNo) + ".xml"
    with codecs.open(OutputFileName, "w+", encoding="utf-8") as OutputFile:
        OutputFile.write(output.decode("utf-8"))