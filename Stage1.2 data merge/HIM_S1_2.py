import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

def cate_conv(df, col):
    """convert columns in a dataframe into categorical type"""
    for subcol in col:
        df[subcol] = df[subcol].astype('category')
    return df

###---some more cleaning, no need for this step if replicated because the previous scripts were already edited to drop these columns---###
BenCS2014 = pd.read_csv('BenCS2014_new.csv', header=0, encoding='ISO-8859-1', parse_dates=['ImportDate'])
BenCS2014 = BenCS2014.drop(['IsSubjToDedTier1', 'IsSubjToDedTier2'], axis=1)
#print(BenCS2014.info(null_counts=True))
BenCS2015 = pd.read_csv('BenCS2015_new.csv', header=0, encoding='ISO-8859-1', parse_dates=['ImportDate'])
BenCS2015 = BenCS2015.drop(['IsSubjToDedTier1', 'IsSubjToDedTier2'], axis=1)
#print(BenCS2015.info(null_counts=True))
BenCS2016 = pd.read_csv('BenCS2016_new.csv', header=0, encoding='ISO-8859-1', parse_dates=['ImportDate'])
list_bencs = [BenCS2014, BenCS2015, BenCS2016]

###---read all files & concat into one file---###
#BenCS_csv = glob.glob('BenCS*_new.csv')
#list_bencs = []
#for filename in BenCS_csv:
#    data = pd.read_csv(filename, header=0, parse_dates=['ImportDate'])
#    list_bencs.append(data)
BenCS = pd.concat(list_bencs)
catecol = ['StateCode', 'SourceName', 'BenefitName', 'CopayInnTier1', 'CopayInnTier2', 'CopayOutofNet', 'CoinsInnTier1', 'CoinsInnTier2', 'CoinsOutofNet', 'LimitUnit', 'Exclusions', 'Explanation', 'EHBVarReason']
BenCS = cate_conv(BenCS, catecol)
BenCS = BenCS.drop(['Unnamed: 0'], axis=1)
#BenCS.to_csv('BenCS_mer.csv', chunksize=1000)
#print(BenCS.info(null_counts=True))

Rate_csv = glob.glob('Rate*_new.csv')
list_rate = []
for filename in Rate_csv:
    data = pd.read_csv(filename, header=0, parse_dates=['ImportDate'])
    list_rate.append(data)
Rate = pd.concat(list_rate)
catecol2 = ['StateCode', 'SourceName', 'RatingAreaId', 'Tobacco', 'Age']
Rate = cate_conv(Rate, catecol2)
Rate[['RateEffectiveDate', 'RateExpirationDate']] = Rate[['RateEffectiveDate', 'RateExpirationDate']].astype('datetime64[ns]')
Rate = Rate.drop(['Unnamed: 0'], axis=1)
#print(Rate.info(null_counts=True))
Rate.to_csv('Rate_mer.csv', chunksize=1000)


