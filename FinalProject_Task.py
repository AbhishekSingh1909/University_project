import pandas as pd
# Load the CSV file again with the correct delimiter
df_electricity = pd.read_csv("./Electricity_20-09-2024.csv", delimiter=';')
df_price = pd.read_csv("./sahkon-hinta-010121-240924.csv")

# Rename the columns for easier access and clean-up
df_electricity.columns = [
    'Time', 'Energy (kWh)', 'Energy night (kWh)', 'Energy day (kWh)', 'Temperature']

df_electricity['Energy (kWh)'] = df_electricity['Energy (kWh)'].str.replace(
    ',', '.').astype(float)
df_electricity['Energy night (kWh)'] = df_electricity['Energy night (kWh)'].str.replace(
    ',', '.').astype(float)
df_electricity['Energy day (kWh)'] = df_electricity['Energy day (kWh)'].str.replace(
    ',', '.').astype(float)
df_electricity['Temperature'] = df_electricity['Temperature'].str.replace(
    ',', '.').astype(float)

df_price.columns = ['Time', 'Price(cent/kWh)']

# Convert 'Time' column to datetime
df_electricity['Time'] = pd.to_datetime(pd.to_datetime(
    df_electricity['Time'].str.strip(), format='%d.%m.%Y %H:%M', errors='coerce'))

df_price['Time'] = pd.to_datetime(df_price['Time'], format='%d-%m-%Y %H:%M:%S')


# Merge the data frames on the 'Time' column
df_merged = pd.merge(df_electricity, df_price, on='Time', how='inner')

# # Calculate the hourly bill
df_merged['Hourly Bill (€)'] = (df_merged['Energy (kWh)'] *
                                (df_merged['Price(cent/kWh)'] / 100)).round(2)


# Convert 'Time' column to datetime for proper grouping
df_merged['Time'] = pd.to_datetime(df_merged['Time'])


# Group by daily, weekly, and monthly using resample
daily_hourly_bill = df_merged.groupby(pd.Grouper(key='Time', freq='d')).agg({
    'Energy (kWh)': 'sum',
    'Hourly Bill (€)': 'sum',
    'Price(cent/kWh)': 'mean',
    'Temperature': 'mean'
}).reset_index()

# Display the results grouped by Year-Month-Week
print("Daily Consumption and Hourly Bill in Euro of each day:")

print(daily_hourly_bill)

weekly_hourly_bill = df_merged.groupby(pd.Grouper(key='Time', freq='W')).agg({
    'Energy (kWh)': 'sum',
    'Hourly Bill (€)': 'sum',
    'Price(cent/kWh)': 'mean',
    'Temperature': 'mean'
}).reset_index()

# Display the results grouped by Year-Month-Week
print("Weekly Consumption and Hourly Bill in Euro for every week:")

print(weekly_hourly_bill)

monthly_hourly_bill = df_merged.groupby(pd.Grouper(key='Time', freq='ME')).agg({
    'Energy (kWh)': 'sum',
    'Hourly Bill (€)': 'sum',
    'Price(cent/kWh)': 'mean',
    'Temperature': 'mean'
}).reset_index()

# Display the results grouped by Year-Month-Week
print("Monthly Consumption and Hourly Bill in Euro of each Month:")

print(monthly_hourly_bill)
