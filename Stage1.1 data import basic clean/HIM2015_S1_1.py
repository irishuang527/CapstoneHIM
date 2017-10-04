import os

import pandas as pd
from HIM_2016_S1 import blank_to_no
from HIM_2016_S1 import bool_conv
from HIM_2016_S1 import cate_conv

###Benefits_Cost_Sharing_2015
scriptdir = os.path.dirname(os.path.abspath(__file__))
BenCS2015_csv = os.path.join(scriptdir, "Benefits_Cost_Sharing_PUF_2015.csv")
BenCS2015 = pd.read_csv(BenCS2015_csv, header=0, encoding='ISO-8859-1', parse_dates=['ImportDate'])
BenCS2015_2 = BenCS2015.drop(["IssuerId2", "StateCode2", 'IsSubjToDedTier1', 'IsSubjToDedTier2'], axis=1) #drop duplicate and useless columns
BenCS2015_2 = BenCS2015_2.drop_duplicates() #drop duplicate records

blankno_col = ['IsEHB', 'IsStateMandate', 'IsCovered', 'QuantLimitOnSvc']
BenCS2015_2 = blank_to_no(BenCS2015_2, blankno_col)
BenCS2015_2.loc[:, 'IsCovered'][BenCS2015_2.loc[:, 'IsCovered'] == 'Covered'] = 'Yes' #convert string into boolean-like string first
boolcol2 = ['IsEHB', 'IsStateMandate', 'IsCovered', 'QuantLimitOnSvc', 'IsExclFromInnMOOP', 'IsExclFromOonMOOP', 'IsSubjToDedTier1', 'IsSubjToDedTier2']
BenCS2015_2 = bool_conv(BenCS2015_2, boolcol2)
catecol2 = ['StateCode', 'SourceName', 'BenefitName', 'CopayInnTier1', 'CopayInnTier2', 'CopayOutofNet', 'CoinsInnTier1', 'CoinsInnTier2', 'CoinsOutofNet', 'LimitUnit', 'Exclusions', 'Explanation', 'EHBVarReason']
BenCS2015_2 = cate_conv(BenCS2015_2, catecol2)

#print(BenCS2015_2.info(null_counts=True))

BenCS2015_2.to_csv('BenCS2015_new.csv', chunksize=1000)

###Rate2015
scriptdir = os.path.dirname(os.path.abspath(__file__))
Rate2015_csv = os.path.join(scriptdir, "Rate_PUF_2015.csv")
Rate2015 = pd.read_csv(Rate2015_csv, header=0, encoding='ISO-8859-1', parse_dates=['ImportDate'])
Rate2015[['RateEffectiveDate', 'RateExpirationDate']] = Rate2015[['RateEffectiveDate', 'RateExpirationDate']].astype('datetime64[ns]') #convert Date columns into datetime type
Rate2015_2 = Rate2015.drop(["IssuerId2"], axis=1) #drop duplicated column
Rate2015_2 = Rate2015_2.drop_duplicates() #drop duplicate records

##turn categorical columns into category
catecol = ['StateCode', 'SourceName', 'RatingAreaId', 'Tobacco', 'Age']
Rate2015_2 = cate_conv(Rate2015_2, catecol)

##clean out "Rating Area" and append the state-specific integer to state code as a new column
Rate2015_2['RatingAreaId'] = Rate2015_2.RatingAreaId.apply(lambda x: x.replace('Rating Area', ' '))
Rate2015_2['StateRatingArea'] = Rate2015_2[['StateCode', 'RatingAreaId']].apply(lambda x: ''.join(x), axis=1).astype('category')

##some plans are identical except for the plan effective date and expiration date, keep only the last record of such repeated records
cols = [col for col in Rate2015_2.columns if col not in ['RateEffectiveDate', 'RateExpirationDate']]
Rate2015_2 = Rate2015_2.drop_duplicates(cols, keep='last')

#print(Rate2015_2.info())

Rate2015_2.to_csv('Rate2015_new.csv', chunksize=1000)