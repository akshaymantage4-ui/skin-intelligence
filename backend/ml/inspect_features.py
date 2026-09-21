import pandas as pd
df=pd.read_csv('ml/ingredient-flags.csv')

print('\n---sample ingredients and functions---')
print(
    df[['inci_name','function','fragrance']].head(20).to_string(index=False)

)
print('\n--- Fragrance counts by function---')
print(
    df.groupby('function',dropna=False)['fragrance'].agg(['count','sum','mean']).sort_values('sum',ascending=False).head(20)
)

print('\n---FRAGRANCE label balancere---')
print(df['fragrance'].value_counts(normalize=True))