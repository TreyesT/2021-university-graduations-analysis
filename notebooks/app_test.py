import pandas as pd

dc_df = pd.read_csv("../data/degree completions.csv")
uni_df = pd.read_csv("../data/university info.csv", encoding='latin')

#Change the names of the columns for both datasets
dc_df.rename(columns={
    'UNITID': 'institution_id',
    'CSTOTLT': 'total_awards',
    'CSTOTLM': 'awards_men',
    'CSTOTLW': 'awards_women',
    'CSAIANT': 'awards_native_american_total',
    'CSAIANM': 'awards_native_american_men',
    'CSAIANW': 'awards_native_american_women',
    'CSASIAT': 'awards_asian_total',
    'CSASIAM': 'awards_asian_men',
    'CSASIAW': 'awards_asian_women',
    'CSBKAAT': 'awards_black_total',
    'CSBKAAM': 'awards_black_men',
    'CSBKAAW': 'awards_black_women',
    'CSHISPT': 'awards_hispanic_total',
    'CSHISPM': 'awards_hispanic_men',
    'CSHISPW': 'awards_hispanic_women',
    'CSNHPIT': 'awards_pacific_islander_total',
    'CSNHPIM': 'awards_pacific_islander_men',
    'CSNHPIW': 'awards_pacific_islander_women',
    'CSWHITT': 'awards_white_total',
    'CSWHITM': 'awards_white_men',
    'CSWHITW': 'awards_white_women',
    'CS2MORT': 'awards_two_or_more_races_total',
    'CS2MORM': 'awards_two_or_more_races_men',
    'CS2MORW': 'awards_two_or_more_races_women',
    'CSUNKNT': 'awards_unknown_total',
    'CSUNKNM': 'awards_unknown_men',
    'CSUNKNW': 'awards_unknown_women',
    'CSNRALT': 'awards_nonresident_alien_total',
    'CSNRALM': 'awards_nonresident_alien_men',
    'CSNRALW': 'awards_nonresident_alien_women'
}, inplace=True)

uni_df.rename(columns={
    'UNITID': 'institution_id',
    'INSTNM': 'institution_name',
    'CITY': 'city',
    'STABBR': 'state',
    'ZIP': 'zip_code',
    'SECTOR': 'sector',
    'CONTROL': 'control',  # Public/Private
    'HBCU': 'hbcu',  # Historically Black College or University
    'TRIBAL': 'tribal_college',
    'LOCALE': 'locale_code',
    'WEBADDR': 'website',
    'ADMINURL': 'admin_url',
    'FAIDURL': 'faid_url',  # Financial Aid URL
    'INSTSIZE': 'institution_size',
    'CARNEGIE': 'carnegie_classification',
    'LATITUDE': 'latitude',
    'LONGITUD': 'longitude'
}, inplace=True)

# Join the two datasets based on the institution_id
merged_df = pd.merge(dc_df, uni_df, on='institution_id')

################# NATIONAL AVERAGES

group_totals = merged_df[['awards_native_american_total', 'awards_asian_total', 'awards_black_total', 'awards_hispanic_total', 'awards_pacific_islander_total', 'awards_white_total']].sum()
total_awards = merged_df['total_awards'].sum()
national_averages = group_totals / total_awards

print("National averages:")
print(national_averages)

################# SIZE

def categorize_size(total_awards):
    if total_awards < 500:
        return 'Small'
    elif 500 <= total_awards <= 2000:
        return 'Medium'
    else:
        return 'Large'

merged_df['size_category'] = merged_df['total_awards'].apply(categorize_size)

print("Size vs awards")
print(merged_df.groupby('size_category')[group_totals])

################# PRIVATE/PUBLIC, ETC