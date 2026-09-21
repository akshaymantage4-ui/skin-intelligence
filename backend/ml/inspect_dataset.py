import pandas as pd
df=pd.read_csv('ml/ingredient-flags.csv')
print('first 5 rowa')
# print(df)

print(df.head())
#show dataset dimensions

print('rows',df.shape[0])
print('columns:',df.shape[1])

#show column names
print(df.columns.tolist())

#show data types
print(df.dtypes)

#count missing values
print(df.isnull().sum())

#6.show basic statistics
print(df.describe())
 