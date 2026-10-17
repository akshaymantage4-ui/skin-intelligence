import pandas as pd
df=pd.read_csv('ml/ingredient-flags.csv')
target_columns=[
    'fa_trigger',
    'comedogenic',
    'fragrance',
    'eu_allergen',
    'pregnancy_caution'
]
print('\n---target value counts---')
for column in target_columns:
    print(f'\n{column}')
    print(df[column].value_counts(dropna=False))
print('\n--Active Ingridients---')
print(df['is_active'].value_counts(dropna=False))

print('\n---Function Values---')
print(df['function'].value_counts(dropna=False).head(20))

print('\n ---duplicate ingridients names---')
print('duplicates:',df['inci_name'].duplicated().sum())