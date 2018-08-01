# Import pandas
import pandas as pd

import re
# Load a sheet into a DataFrame by name: df1
df1 = pd.read_csv('765_Track_statistics.csv')

# creating table with columns names and types:
columns_names_types='ID INT PRIMARY KEY AUTO_INCREMENT, '
for column_name in list(df1):
    if re.compile('[A-Z]').search(column_name) or re.compile('[a-z]').search(column_name):  #if column has name
        if column_name == list(df1)[-1]:                                      #if last column
            if len(re.findall('[aA-zZ]', str(df1.at[0, str(column_name)]))) == 0:  #if first value in column is int
                columns_names_types += column_name + " DECIMAL(18,6)"
            else:                                                #if first value in column is string
                columns_names_types += column_name + " TEXT"
        else:                                                  #other columns (...)
            if len(re.findall('[aA-zZ]', str(df1.at[0, str(column_name)]))) == 0:
                columns_names_types += column_name + " DECIMAL(18,6), "
            else:
                columns_names_types += column_name + " TEXT, "
    else:
        pass

# print(columns_names_types)

print('CREATE TABLE 765_Track_statistics '+'('+columns_names_types+');')


#collecting not null column names:

list_of_notNULL_column_names=[]
for column_name in list(df1):
    if re.compile('[A-Z]').search(column_name) or re.compile('[a-z]').search(column_name):
        list_of_notNULL_column_names.append(column_name)
    else:
        pass
# re.search('[A-Z]', column_name)

# inserting values into the right columns:
rows_values = ''
for j in range(len(df1.index)):  #rows
    for column_name in list(df1):  #columns
        if re.compile('[A-Z]').search(column_name) or re.compile('[a-z]').search(column_name):  #if any letters in column_name
            if column_name == list(df1)[-1]:  #if last column
                if len(re.findall('[aA-zZ]', str(df1.at[0, str(column_name)]))) == 0:  #if column values are ints
                    rows_values += str(df1.at[j, str(column_name)])
                else:
                    rows_values += "'" + str(df1.at[j, str(column_name)]) + "'"  #if column values are strings
            else:
                if str(df1.at[j, str(column_name)]) == 'nan' or str(df1.at[j, str(column_name)]) == 'NaN':             #if column value=='nan'
                    rows_values += 'NULL, '
                elif len(re.findall('[aA-zZ]', str(df1.at[0, str(column_name)]))) == 0:  #if column_values are ints
                    rows_values += str(df1.at[j, str(column_name)]) + ', '
                else:
                    rows_values += "'" + str(df1.at[j, str(column_name)]) + "'" + ', '  #if column values are strings
        else:
            pass  # skips columns without name
    print('INSERT INTO 765_Track_statistics ('+', '.join(list_of_notNULL_column_names)+')' + ' VALUES ('+ rows_values + ');')
    rows_values = ''

# len(df1.index)


# S="""_a-,?/":.5F"""
# print(re.findall('[aA-zZ]',S))
# print(re.findall('[a-z]',S))
# if len(re.findall('[a-z]',S))>0:
#     print(True)

# print(re.findall('[aA-zZ]', str(list(df1)[0])))

# for column_name in list(df1):
#     if re.compile('[A-Z]').search(column_name):
#         print(True)
#     else:
#         print(False)

# print(type(df1.at[5, 'TRACK_MEDIAN_QUALITY'])) # its numpy.float64