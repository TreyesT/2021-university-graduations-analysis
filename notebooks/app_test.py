import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd
import seaborn as sns

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


# merged_df['size_category'] = merged_df['total_awards'].apply(categorize_size)
#
# print("Size vs awards")
# print(merged_df.groupby('size_category')[group_totals])

################# PRIVATE/PUBLIC, ETC

ethnicity_columns = [
    'awards_native_american_total', 'awards_asian_total', 'awards_black_total',
    'awards_hispanic_total', 'awards_pacific_islander_total', 'awards_white_total'
]

# Aggregate data by control type using mean instead of sum
grouped_data_mean = merged_df.groupby('control')[ethnicity_columns].mean()

# Plot horizontal bar charts for each control type
for control_type in grouped_data_mean.index:
    plt.figure(figsize=(10, 6))
    grouped_data_mean.loc[control_type].plot(kind='barh', title=f'Average Awards by Ethnicity for {control_type} Institutions')
    plt.xlabel('Average Awards')
    plt.ylabel('Ethnicity')
    plt.grid(axis='x', linestyle='--', alpha=0.7)

plt.tight_layout()  # Adjust layout to prevent overlapping
plt.show()

################# FINANCIAL AID?

# All universities have financial aid

################# LOCATION - KEEP IT COMMENTED OUT TO NOT RERUN IT

# Group by state, summing awards for each ethnicity
# state_awards = merged_df.groupby('state')[ethnicity_columns].mean().reset_index()
#
# # Create a separate map for each ethnicity
# for eth_col in ethnicity_columns:
#     fig = px.choropleth(
#         state_awards,                      # DataFrame with state-level sums
#         locations="state",                 # Column with state abbreviations
#         locationmode="USA-states",         # Tells Plotly to use USA state abbreviations
#         color=eth_col,                     # Values to color by
#         color_continuous_scale="Blues",     # Choose any built-in color scale or custom
#         scope="usa",                       # Zoom in on the USA
#         title=f"Total {eth_col.replace('_', ' ').title()} by State"  # Figure title
#     )
#
#     # Display the figure
#     fig.show()

################# TOP 5 UNIVERSITIES

for eth_col in ethnicity_columns:
    # Group by institution and state, computing the mean of the chosen ethnicity column
    grouped = (
        merged_df
        .groupby(['institution_name', 'state'])[eth_col]
        .mean()
        .sort_values(ascending=False)
        .head(5)  # top 5
    )

    # Prepare a new DataFrame from this grouped result for plotting
    top_5_df = grouped.reset_index()

    # Create a new column combining institution name and state for the x-axis label
    top_5_df['institution_label'] = top_5_df['institution_name'] + " (" + top_5_df['state'] + ")"

    # Plot
    plt.figure(figsize=(8, 6))
    plt.bar(
        top_5_df['institution_label'],
        top_5_df[eth_col],
        color='skyblue'
    )
    plt.xticks(rotation=45, ha='right')
    plt.title(f'Top 5 Institutions by Mean {eth_col.replace("_", " ").title()}')
    plt.xlabel('Institution (State)')
    plt.ylabel(f'Mean {eth_col.replace("_", " ").title()}')

plt.tight_layout()
plt.show()