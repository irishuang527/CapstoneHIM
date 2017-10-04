import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def cate_conv(df, col):
    """convert columns in a dataframe into categorical type"""
    for subcol in col:
        df[subcol] = df[subcol].astype('category')
    return df

def uniq_value(df, col_list):
    """find the unique values of a categorical column"""
    listofseries =  [df[col].value_counts(dropna=False) for col in col_list]
    uniq_dict = dict(zip(col_list, listofseries))
    return uniq_dict

###---exploratory data analysis---###

BenCS = pd.read_csv('BenCS_mer.csv', encoding='ISO-8859-1', header=0, index_col=['StandardComponentId', 'PlanId'], parse_dates=['ImportDate'])
BenCS = BenCS.drop(['Unnamed: 0'], axis=1)
catecol = ['BusinessYear', 'StateCode', 'SourceName', 'BenefitName', 'CopayInnTier1', 'CopayInnTier2', 'CopayOutofNet', 'CoinsInnTier1', 'CoinsInnTier2', 'CoinsOutofNet', 'LimitUnit', 'Exclusions', 'Explanation', 'EHBVarReason']
BenCS = cate_conv(BenCS, catecol)
BenCScate_uniq_val = uniq_value(BenCS, catecol)

TotalPlanNum = len(BenCS.reset_index().groupby('StandardComponentId').count())
TotalPlanVarNum = len(BenCS.reset_index().groupby('PlanId').count())

##
#y_pos = np.arange(len(BenCScate_uniq_val['StateCode'].keys()))
#busyr_val = BenCScate_uniq_val['StateCode'].values
#wid = 1/1.5
#plt.bar(y_pos, busyr_val, wid, color='blue', tick_label=BenCScate_uniq_val['StateCode'].keys())

#plt.show()

#print(BenCS.head(), BenCS.info())

Rate = pd.read_csv('Rate_mer.csv', encoding='ISO-8859-1', header=0, index_col=['PlanId'], parse_dates=['ImportDate'])
Rate = Rate.drop(['Unnamed: 0'], axis=1)
Rate[['RateEffectiveDate', 'RateExpirationDate']] = Rate[['RateEffectiveDate', 'RateExpirationDate']].astype('datetime64[ns]')
catecol2 = ['StateCode', 'SourceName', 'RatingAreaId', 'Tobacco', 'Age']
Rate = cate_conv(Rate, catecol2)
Ratecate_uniq_val = uniq_value(Rate, catecol2)

#seperate out Family demographics
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
family_plan_Rate = Rate.loc[Rate.Age == 'Family Option']
family_plan_Rate = family_plan_Rate.drop(['Age', 'VersionNum','FederalTIN', 'IndividualTobaccoRate', 'RowNumber'], axis=1) #IndividualTobaccoRate is an empty column
family_plan_Rate_option = ['IndividualRate', 'Couple', 'PrimarySubscriberAndOneDependent', 'PrimarySubscriberAndTwoDependents', 'PrimarySubscriberAndThreeOrMoreDependents', 'CoupleAndOneDependent', 'CoupleAndTwoDependents', 'CoupleAndThreeOrMoreDependents']
family_plan_Rate.boxplot(column=family_plan_Rate_option, ax=ax1)
ax1.set_xticklabels(['Individual', 'Couple', 'PrimSub_1_dep', 'PrimSub_2_dep', 'PrimSub_3+_dep', 'Couple_1_dep', 'Couple_2_dep', 'Couple_3+_dep'], rotation=25)
plt.ylabel('Plan Rate')
plt.xlabel('Family Option Categories')
#plt.show()
#print(family_plan_Rate.head(10))
#print(family_plan_Rate.describe())
plt.clf()

#seperate out Individuals demographics
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
indiv_plan_Rate = Rate.loc[Rate.Age != 'Family Option']
indiv_plan_Rate = indiv_plan_Rate.drop(['Couple', 'PrimarySubscriberAndOneDependent', 'PrimarySubscriberAndTwoDependents', 'PrimarySubscriberAndThreeOrMoreDependents', 'CoupleAndOneDependent', 'CoupleAndTwoDependents', 'CoupleAndThreeOrMoreDependents', 'VersionNum', 'FederalTIN', 'RowNumber'], axis=1)
indiv_plan_Rate_cat = indiv_plan_Rate.loc[(indiv_plan_Rate.Age == '0-20') | (indiv_plan_Rate.Age == '65 and over')]
indiv_plan_Rate_int = indiv_plan_Rate.loc[(indiv_plan_Rate.Age != '0-20') & (indiv_plan_Rate.Age != '65 and over')]
indiv_plan_Rate_int.loc[:, 'Age'] = indiv_plan_Rate_int.Age.astype('int')
age_bin = [i for i in range(20, indiv_plan_Rate_int.Age.max(), 5)]#binning age groups
age_bin.append(64)#61-65 was left off
indiv_plan_Rate_int.loc[:, 'Age'] = pd.cut(indiv_plan_Rate_int.Age, bins=age_bin)
indiv_plan_Rate_new = indiv_plan_Rate_int.append(indiv_plan_Rate_cat)
#print(indiv_plan_Rate_new[['Age', 'IndividualRate', 'IndividualTobaccoRate']].head(10), indiv_plan_Rate_new[['Age', 'IndividualRate', 'IndividualTobaccoRate']].tail(10))
age_list = indiv_plan_Rate_new.Age.tolist()

#ax2.set_xticklabels(age_list)
#plt.ylabel('Plan Rate')
#plt.xlabel('Individuals by Age Group')
#plt.show()



