import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import pyodbc           # 4.0.26
import sqlalchemy as sa # 1.3.6
import urllib.parse          # 1.25.3

# Creating empty dataframe one for each table we will eventually write
dfNAVFieldNames = pd.DataFrame(columns=['TableNo','TableName','FieldNo','FieldName'])
dfNAVFieldOptions = pd.DataFrame(columns=['TableNo','TableName','FieldNo','FieldName','OptionNo','OptionName'])

with open('NAVTable-15.xml', 'r') as xml_file:
    tree = ET.parse(xml_file)
root = tree.getroot()
TableNo = root.get("ID")
TableName = root.get("Name")

# this gets me all the field level attributes from the XML. It creates row in our
# dataframe.  One row for each distinct field name and one row for each option

for child in root.iter('{urn:schemas-microsoft-com:dynamics:NAV:MetaObjects}Field'):
    dfNAVFieldNames = dfNAVFieldNames.append(
             {'TableNo': TableNo,
              'TableName': TableName,
              'FieldNo': child.attrib.get('ID'),
              'FieldName': child.attrib.get('Name')},ignore_index=True)
    OptionString = child.attrib.get('OptionString') 
    if OptionString is not None:
        # print(OptionString.split(","))
        OptionNo = 0        
        for Option in OptionString.split(","):
            dfNAVFieldOptions = dfNAVFieldOptions.append(
             {'TableNo': TableNo,
              'TableName': TableName,
              'FieldNo': child.attrib.get('ID'),
              'FieldName': child.attrib.get('Name'),
              'OptionNo': OptionNo,
              'OptionName': Option},ignore_index=True)
            OptionNo += 1    
# the below just show examples
print(dfNAVFieldNames.head())
print(dfNAVFieldOptions.head())
# # We have our Dataframe and we want to load them into SQL server
# # Create Our Connection String-
Driver = "SQL Server"
Server = "OMSC-F01"
Database = "MIRUSNewTest"
ConnectionString = "Driver={" + Driver + "};Server="+Server+";Database="+Database+";Trusted_Connection=yes;"
Schema = "dbo"
params = urllib.parse.quote_plus(ConnectionString)
engine = sa.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params, fast_executemany=True)
# # ConnectionString = "Driver={" + Driver + "};Server="+Server+";Database="+Database+";Trusted_Connection=yes;"
# # connection = pyodbc.connect(ConnectionString)
# # here we take our dataframes and put them into SQL
#
#
dfNAVFieldNames.to_sql("NAVFieldNames", con=engine, schema=None, if_exists="append", index=False)
dfNAVFieldOptions.to_sql("NAVFieldOptions", con=engine, schema=None, if_exists="append", index=False)