import pandas as pd

df = pd.read_csv(r"C:\Users\user\Desktop\Project\customer_shopping_behavior.csv")
print(df.head())
print(df.info())
print(df.describe(include="all"))


# Remove null values
print(df.isnull().sum())
df['Review Rating']=df.groupby('Category')['Review Rating'].transform(lambda x:x.fillna(x.median())) 
print(df.isnull().sum())

# LOWER CASE AND REPLACE SPACE WITH _
df.columns=df.columns.str.lower()
df.columns=df.columns.str.replace(' ','_')
print(df.columns)

#change name of bad coloum name
df=df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})
print(df.columns)

#create a col name age group
labels=["Young Adult",'Adult','Middle_Aged','Senior']
df['age_group']=pd.qcut(df['age'],q=4,labels=labels)
print(df[['age','age_group']].head(10))
#create col purchase_frequency_days
frequency_mapping={
    'Fortnightly' : 14,
    'Weekly' : 7,
    'Minthly' : 30,
    'Quarterly' : 90,
    'Bi-Weekly' : 14,
    'Annually' : 365,
    'Every 3 Months' : 90
}
df['Purchase_frequency_days']=df['frequency_of_purchases'].map(frequency_mapping)
# df["Purchase_frequency_days"].fillna(90, inplace=True)
print(df[['Purchase_frequency_days','frequency_of_purchases']].head(10))

# #removing promocode
print(df[['discount_applied','promo_code_used']].head(10))
print(df['discount_applied']==df['discount_applied'].all())
df=df.drop('promo_code_used',axis=1)
print(df.columns)


#connect to postgre
from sqlalchemy import create_engine

username = "postgres"
password= "1412"
host="localhost"
port="5432"
database="customer_behaviour"

engine=create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

#load dataframe
table_name="customer"
df.to_sql(table_name,engine,if_exists="replace",index=False)
print(f"Data successfully loaded into table '{table_name}' in database '{database}'.")
