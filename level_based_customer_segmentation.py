import pandas as pd

def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)

    print("##################### Types #####################")
    print(dataframe.dtypes)

    print("##################### Head #####################")
    print(dataframe.head(head))

    print("##################### Tail #####################")
    print(dataframe.tail(head))

    print("##################### NA #####################")
    print(dataframe.isnull().sum())

    print("##################### Quantiles #####################")
    print(df.describe().T)

    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)


df = pd.read_csv("datasets/persona.csv")

# Veriyi inceleyelim.
check_df(df)

# Kaç unique SOURCE vardır? Frekansları nedir?

print(df["SOURCE"].value_counts())
print(df["SOURCE"].nunique())

# Kaç unique PRICE vardır?
print(df["PRICE"].nunique())

# Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
print(df["PRICE"].value_counts())

# Hangi ülkeden kaçar tane satış olmuş?
print(df["COUNTRY"].value_counts())

# Ülkelere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("COUNTRY")["PRICE"].agg("sum")

# SOURCE türlerine göre göre satış sayıları nedir?
df.groupby("SOURCE")["PRICE"].agg("count")

# Ülkelere göre PRICE ortalamaları nedir?
df.groupby("COUNTRY")["PRICE"].agg("mean")

# SOURCE'lara göre PRICE ortalamaları nedir?
df.groupby("SOURCE")["PRICE"].agg("mean")

# COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
df.groupby(["COUNTRY","SOURCE"])["PRICE"].agg("mean")

# COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
df.groupby(["COUNTRY","SOURCE","SEX","AGE"])["PRICE"].agg("mean")

agg_df = pd.DataFrame(df.groupby(["COUNTRY","SOURCE","SEX","AGE"])["PRICE"].agg("mean")).sort_values("PRICE",ascending=False)

agg_df.reset_index(inplace=True)

# age değişkenini kategorik değişkene çevirelim ve agg_df’e ekleyelim.
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], [0, 18, 25, 30,40,50,agg_df["AGE"].max()],
                           labels=["0_18","19_25","26_30","31_40","41_50","50_50+"])

# Yeni seviye tabanlı müşterileri (persona) tanımlayalım.

agg_df["customers_level_based"] = [row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" +
                                   str(row[5]).upper() for row in agg_df.values]


agg_df["customers_level_based"].value_counts()

agg_df_new = agg_df.groupby("customers_level_based")["PRICE"].agg("mean")
agg_df_new = pd.DataFrame(agg_df_new.reset_index())

# Personaları price göre segmentlere ayıralım

agg_df_new["SEGMENT"] = pd.qcut(agg_df_new["PRICE"],4,["D","C","B","A"])

print(agg_df_new["SEGMENT"].value_counts())
agg_df_new.groupby("SEGMENT")["PRICE"].agg(["mean","max","sum"])

agg_df_new[agg_df_new['SEGMENT'] =='C']["PRICE"].agg(["mean","max","sum"])

# 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?


new_customer1 = "TUR_ANDROID_FEMALE_31_40"

agg_df_new[agg_df_new['customers_level_based'] ==new_customer1]

# 35 yaşında IOS kullanan bir Fransız kadını hangi segmente ve ortalama ne kadar gelir kazandırması beklenir?

new_customer2 = "FRA_IOS_FEMALE_31_40"

agg_df_new[agg_df_new['customers_level_based'] ==new_customer2]