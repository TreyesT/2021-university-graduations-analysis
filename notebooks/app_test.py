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

################# Count of students

print("Total Degrees earned:")
print(total_awards)
print(group_totals)

################# PRIVATE/PUBLIC, ETC

# Create a copy of the original DataFrame to work with
df = merged_df.copy()

# Sum up the minority columns into a single column
df['minorities'] = (
        df['awards_native_american_total'] +
        df['awards_asian_total'] +
        df['awards_black_total'] +
        df['awards_hispanic_total'] +
        df['awards_pacific_islander_total']
)

# Rename the white column (optional, just for clarity)
df.rename(columns={'awards_white_total': 'white'}, inplace=True)

# Group by 'control' and calculate the mean of 'white' and 'minorities'
grouped_data_mean = df.groupby('control')[['white', 'minorities']].mean()

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

fig.patch.set_facecolor('#FEFCF5')  # Background of the entire figure
ax.set_facecolor('#FEFCF5')         # Background of the plot area

# Plot a grouped bar chart
# Note: If you'd like 'white' first (green), 'minorities' second (gray),
# make sure the DataFrame columns are in the order [white, minorities].
grouped_data_mean = grouped_data_mean[['white', 'minorities']]  # ensure column order
grouped_data_mean.plot(
    kind='bar',
    ax=ax,
    color=['#43A047', '#BDBDBD'],  # white (green), minorities (gray)
    legend=True  # You may set False if you don’t want a legend
)

# Custom x-axis labels
ax.set_xticklabels([
    "Public Institution",
    "Private Non-for-profit Institution",
    "Private For-profit Institution"
], rotation=0, fontsize=14)

# Remove gridlines
ax.grid(False)

ax.set_xlabel('')

# Remove the title
ax.set_title('')

ax.legend(fontsize=14)

plt.tight_layout()
plt.show()

#
ethnicity_columns = [
    'awards_native_american_total', 'awards_asian_total', 'awards_black_total',
    'awards_hispanic_total', 'awards_pacific_islander_total', 'awards_white_total'
]

# Aggregate data by control type using mean instead of sum
grouped_data_mean = merged_df.groupby('control')[ethnicity_columns].mean()
#
# # Plot horizontal bar charts for each control type
# for control_type in grouped_data_mean.index:
#     plt.figure(figsize=(10, 6))
#     grouped_data_mean.loc[control_type].plot(kind='barh', title=f'Average Awards by Ethnicity for {control_type} Institutions')
#     plt.xlabel('Average Awards')
#     plt.ylabel('Ethnicity')
#     plt.grid(axis='x', linestyle='--', alpha=0.7)
#
# plt.tight_layout()  # Adjust layout to prevent overlapping
# plt.show()

################# LOCATION - KEEP IT COMMENTED OUT TO NOT RERUN IT

# state_awards = df.groupby('state')[['minorities', 'white']].mean().reset_index()
#
# # Create the choropleth map for minorities
# fig_minorities = px.choropleth(
#     state_awards,
#     locations="state",
#     locationmode="USA-states",
#     color="minorities",
#     color_continuous_scale="Greens",
#     scope="usa",
#     title="Average Awards for Minority Students by State"
# )
# fig_minorities.show()
#
# # Create the choropleth map for white students
# fig_white = px.choropleth(
#     state_awards,
#     locations="state",
#     locationmode="USA-states",
#     color="white",
#     color_continuous_scale="Blues",
#     scope="usa",
#     title="Average Awards for White Students by State"
# )
# fig_white.show()
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

# for eth_col in ethnicity_columns:
#     # Group by institution and state, computing the mean of the chosen ethnicity column
#     grouped = (
#         merged_df
#         .groupby(['institution_name', 'state'])[eth_col]
#         .mean()
#         .sort_values(ascending=False)
#         .head(5)  # top 5
#     )
#
#     # Prepare a new DataFrame from this grouped result for plotting
#     top_5_df = grouped.reset_index()
#
#     # Create a new column combining institution name and state for the x-axis label
#     top_5_df['institution_label'] = top_5_df['institution_name'] + " (" + top_5_df['state'] + ")"
#
#     # Plot
#     plt.figure(figsize=(8, 6))
#     plt.bar(
#         top_5_df['institution_label'],
#         top_5_df[eth_col],
#         color='skyblue'
#     )
#     plt.xticks(rotation=45, ha='right')
#     plt.title(f'Top 5 Institutions by Mean {eth_col.replace("_", " ").title()}')
#     plt.xlabel('Institution (State)')
#     plt.ylabel(f'Mean {eth_col.replace("_", " ").title()}')
#
# plt.tight_layout()
# plt.show()

################# HBCU VS NON HBCU
# Define the columns that make up "minorities"
minority_cols = [
    'awards_native_american_total',
    'awards_asian_total',
    'awards_black_total',
    'awards_hispanic_total',
    'awards_pacific_islander_total'
]
non_minority_col = 'awards_white_total'

# Sum minority awards per row
merged_df['minorities'] = merged_df[minority_cols].sum(axis=1)
# White (non-minority)
merged_df['white'] = merged_df[non_minority_col]

# Convert HBCU column into a user-friendly label
# If your 'hbcu' column is 0/1, do this:
merged_df['hbcu_status'] = merged_df['hbcu'].map({1: 'HBCU', 2: 'Non-HBCU'})

# Compute the mean for minorities and white students by HBCU status
grouped_data_mean = merged_df.groupby('hbcu_status')[['white', 'minorities']].mean()

# Create a figure and axis
fig, ax = plt.subplots(figsize=(8, 6))

# Set background color
fig.patch.set_facecolor('#FEFCF5')  # Background of the entire figure
ax.set_facecolor('#FEFCF5')         # Background of the plot area

# Plot a grouped bar chart
grouped_data_mean = grouped_data_mean[['white', 'minorities']]  # Ensure column order
grouped_data_mean.plot(
    kind='bar',
    ax=ax,
    color=['#43A047', '#BDBDBD'],  # white (green), minorities (gray)
    legend=True
)

# Custom x-axis labels (HBCU status)
ax.set_xticklabels(["HBCU", "Non-HBCU"], rotation=0, fontsize=14)

# Remove gridlines
ax.grid(False)

# Remove x-axis label
ax.set_xlabel('')

# Remove the title
ax.set_title('')
ax.legend(fontsize=14)
plt.tight_layout()
plt.show()
# # Define the columns that make up "minorities"
# minority_cols = [
#     'awards_native_american_total',
#     'awards_asian_total',
#     'awards_black_total',
#     'awards_hispanic_total',
#     'awards_pacific_islander_total'
# ]
# non_minority_col = 'awards_white_total'
#
# # Sum minority awards per row
# merged_df['minorities_total'] = merged_df[minority_cols].sum(axis=1)
# # White (non-minority)
# merged_df['non_minorities_total'] = merged_df[non_minority_col]
#
# # Convert HBCU column into a user-friendly label if needed
# # If your 'hbcu' column is 0/1, do this:
# merged_df['hbcu_status'] = merged_df['hbcu'].map({1: 'HBCU', 2: 'Non-HBCU'})
#
# # Compute the mean for minorities_total by HBCU status
# minority_means = merged_df.groupby('hbcu_status')['minorities_total'].mean()
#
# # Compute the mean for non_minorities_total (White) by HBCU status
# white_means = merged_df.groupby('hbcu_status')['non_minorities_total'].mean()
#
# # 1) Plot the chart for Minorities
# plt.figure(figsize=(6, 4))
# minority_means.plot(kind='bar', color=['teal', 'gold'],
#                     title='Mean Awards (Minorities) by HBCU Status')
# plt.ylabel('Mean Awards')
# plt.xlabel('HBCU Status')
# plt.xticks(rotation=0)
# plt.tight_layout()
# plt.show()
#
# # 2) Plot the chart for White (non-minorities)
# plt.figure(figsize=(6, 4))
# white_means.plot(kind='bar', color=['teal', 'gold'],
#                  title='Mean Awards (White) by HBCU Status')
# plt.ylabel('Mean Awards')
# plt.xlabel('HBCU Status')
# plt.xticks(rotation=0)
# plt.tight_layout()
# plt.show()

################# SIZE FOR MINORITIES -- NOT RELEVANT AFTER ANALYSIS

# Define which ethnicity columns count as "minorities" (all except white)
minority_cols = [
    'awards_native_american_total',
    'awards_asian_total',
    'awards_black_total',
    'awards_hispanic_total',
    'awards_pacific_islander_total'
]
non_minority_col = 'awards_white_total'

# 1) Create two new columns for each row: total minority awards, and white awards
merged_df['awards_minority'] = merged_df[minority_cols].sum(axis=1)
merged_df['awards_non_minority'] = merged_df[non_minority_col]

# 2) Group by institution_size and get the mean of these two new columns
minority_by_size = (
    merged_df
    .groupby('institution_size')[['awards_minority', 'awards_non_minority']]
    .mean()
    .reset_index()
)

# 3) Melt for Plotly
minority_by_size_long = pd.melt(
    minority_by_size,
    id_vars='institution_size',
    value_vars=['awards_minority', 'awards_non_minority'],
    var_name='group',
    value_name='mean_awards'
)

# Optional: rename the group values for clarity
minority_by_size_long['group'] = minority_by_size_long['group'].replace({
    'awards_minority': 'Minority',
    'awards_non_minority': 'White'
})

# 4) Create grouped bar chart for "Minority" vs. "White"
fig_minority = px.bar(
    minority_by_size_long,
    x='institution_size',
    y='mean_awards',
    color='group',
    barmode='group',
    title='Mean Awards by Institution Size: Minorities vs. White',
    labels={
        'institution_size': 'Institution Size',
        'mean_awards': 'Mean Number of Awards',
        'group': 'Group'
    },
    color_discrete_sequence=['purple', 'orange']  # optional color choice
)

fig_minority.update_layout(
    xaxis_tickangle=-45,
    xaxis_title='Institution Size',
    yaxis_title='Mean Number of Awards'
)

fig_minority.show()

# 1) Map numeric HBCU column to labels (if needed)
merged_df['hbcu_status'] = merged_df['hbcu'].map({1: 'HBCU', 2: 'Non-HBCU'})

# 2) Create a cross-tab by (hbcu_status x control)
#    normalize='columns' => each column sums to 1.0, so you get % distribution within each control type
counts = pd.crosstab(merged_df['hbcu_status'], merged_df['control'])
counts_perc = counts.div(counts.sum(axis=0), axis=1) * 100  # convert to percentages

# 3) Plot heatmap
fig, ax = plt.subplots(figsize=(6, 4))

sns.heatmap(
    data=counts_perc,
    cmap='Blues',
    annot=True,         # show numbers on each cell
    fmt='.1f',          # one decimal place
    vmin=0, vmax=100,   # color scale from 0% to 100%
    cbar_kws={'label': 'Percentage (%)'}
)

# 4) Format and label the plot
ax.set_title('Distribution of HBCU Status by Control Type', fontsize=14, pad=12)
ax.set_xlabel('Control Type', fontsize=12)
ax.set_ylabel('HBCU Status', fontsize=12)

plt.tight_layout()
plt.show()