import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

##---import file & data cleansing---##

###Benefits_Cost_Sharing_2016
scriptdir = os.path.dirname(os.path.abspath(__file__))
BenCS2016_csv = os.path.join(scriptdir, "Benefits_Cost_Sharing_PUF_2016.csv")
BenCS2016 = pd.read_csv(BenCS2016_csv, header=0, encoding='ISO-8859-1', parse_dates=['ImportDate'])
BenCS2016_2 = BenCS2016.drop(["IssuerId2", "StateCode2"], axis=1) #drop duplicate columns
BenCS2016_2 = BenCS2016_2.drop_duplicates() #drop duplicate records

##replace blank values to 'No'
blankno_col = ['IsEHB', 'IsStateMandate', 'IsCovered', 'QuantLimitOnSvc']
def blank_to_no(df, col):
    """turn blank values into "no" string"""
    for subcol in col:
        df[subcol] = df[subcol].fillna('No')
    return df

BenCS2016_2 = blank_to_no(BenCS2016_2, blankno_col)

BenCS2016_2.loc[:, 'IsCovered'][BenCS2016_2.loc[:, 'IsCovered'] == 'Covered'] = 'Yes' #convert string into boolean-like string first

##turn boolean columns into bool type
boolcol = ['IsEHB', 'IsStateMandate', 'IsCovered', 'QuantLimitOnSvc', 'IsExclFromInnMOOP', 'IsExclFromOonMOOP']
def bool_conv(df, col):
    """convert columns in a dataframe into boolean type"""
    for subcol in col:
        df[subcol] = pd.Series(np.where(df[subcol].values == 'No', 0, 1), df.index).astype('bool')
    return df
BenCS2016_2 = bool_conv(BenCS2016_2, boolcol)

##turn categorical columns into categories
catecol = ['StateCode', 'SourceName', 'BenefitName', 'CopayInnTier1', 'CopayInnTier2', 'CopayOutofNet', 'CoinsInnTier1', 'CoinsInnTier2', 'CoinsOutofNet', 'LimitUnit', 'Exclusions', 'Explanation', 'EHBVarReason']
def cate_conv(df, col):
    """convert columns in a dataframe into categorical type"""
    for subcol in col:
        df[subcol] = df[subcol].astype('category')
    return df
BenCS2016_2 = cate_conv(BenCS2016_2, catecol)

#print(BenCS2016_2.info(null_counts=True))
#BenCS2016_2.to_csv('BenCS2016_new.csv', chunksize=1000)

###Rate_2016
scriptdir = os.path.dirname(os.path.abspath(__file__))
Rate2016_csv = os.path.join(scriptdir, "Rate_PUF_2016.csv")
Rate2016 = pd.read_csv(Rate2016_csv, header=0, encoding='ISO-8859-1', parse_dates=['ImportDate'])
Rate2016[['RateEffectiveDate', 'RateExpirationDate']] = Rate2016[['RateEffectiveDate', 'RateExpirationDate']].astype('datetime64[ns]') #convert Date columns into datetime type
Rate2016_2 = Rate2016.drop(["IssuerId2"], axis=1) #drop duplicated column
Rate2016_2 = Rate2016_2.drop_duplicates() #drop duplicate records

##turn categorical columns into category
catecol2 = ['StateCode', 'SourceName', 'RatingAreaId', 'Tobacco', 'Age']
Rate2016_2 = cate_conv(Rate2016_2, catecol2)

##clean out "Rating Area" and append the state-specific integer to state code as a new column
Rate2016_2['RatingAreaId'] = Rate2016_2.RatingAreaId.apply(lambda x: x.replace('Rating Area', ' '))
Rate2016_2['StateRatingArea'] = Rate2016_2[['StateCode', 'RatingAreaId']].apply(lambda x: ''.join(x), axis=1).astype('category')

##some plans are identical except for the plan effective date and expiration date, keep only the last record of such repeated records
cols = [col for col in Rate2016_2.columns if col not in ['RateEffectiveDate', 'RateExpirationDate']]
Rate2016_2 = Rate2016_2.drop_duplicates(cols, keep='last')

#print(Rate2016_2.info(null_counts=True))

#Rate2016_2.to_csv('Rate2016_new2.csv', chunksize=1000)