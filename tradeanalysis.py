import pandas as pd
import matplotlib.pyplot as plt
print('==================')
print('Raw from Stocktrak CSV')
df = pd.read_csv('TransactionHistory_3_14_2021.csv')

#print(df)
print('==================')



# select commodities traded by me
gold_df = df[df['Symbol'].str.contains('GC')]
btc_df = df[df['Symbol'].str.contains('BTC')]
wheat_df = df[df['Symbol'].str.contains('ZW')]
gas_df = df[df['Symbol'].str.contains('RB')]

# create dictionary of selected commodities
commodity_dict = {
                  'wheat': wheat_df,
                  'gas': gas_df,
                  'gold': gold_df,
                  'bitcoin': btc_df,}
# assign a multiplier to account for the leverage in each trade
commodity_multiplier = {
                  'wheat': 50,
                  'gas': 42000,
                  'gold': 100,
                  'bitcoin': 5,}

print('==================')
print('Max\'s commodities')

for key in commodity_dict.keys():
    # this stuff here dealing with the datetime could be extraneous. This is just a quick tool to help me see how I did during the assignment
    current_df = commodity_dict[key]
    current_df.index = pd.to_datetime(current_df['CreateDate'])
    #current_df = current_df.drop('CreateDate',axis=1)
    current_df = current_df.sort_index()
    current_df['Price'] = current_df['Price'].replace('[\$,]', '', regex=True).astype(float)

    # calculate the profit and loss for each trade taking in to account the leverage associated with each commodity and the comission fees
    current_df.loc[current_df['TransactionType'] == 'Market - Sell', 'PnL'] = (pd.to_numeric(current_df['Price']).diff())*commodity_multiplier[key] - 10
    current_df.loc[current_df['TransactionType'] == 'Limit - Sell', 'PnL'] = (pd.to_numeric(current_df['Price']).diff())*commodity_multiplier[key] - 10

    current_df.loc[current_df['TransactionType'] == 'Market - Cover', 'PnL'] = (-1*pd.to_numeric(current_df['Price']).diff())*commodity_multiplier[key] - 10
    current_df.loc[current_df['TransactionType'] == 'Limit - Cover', 'PnL'] = (-1*pd.to_numeric(current_df['Price']).diff())*commodity_multiplier[key] - 10
    current_df['PnL'] = current_df['PnL'].fillna(-10) # account for 10 comission on each trade
    #current_df['PnL'] =
    commodity_dict[key] = current_df
    print(commodity_dict[key])
print('==================')

# put all the commodities traded together
final_df = pd.concat(commodity_dict)


# clean up the date time index in preperation for plot
final_df.index = pd.to_datetime(final_df['CreateDate'])
final_df = final_df.sort_index(ascending=True)
final_df['Cumulative PnL'] = final_df['PnL'].cumsum()
print(final_df)

final_df.plot(y='Cumulative PnL', color='green')

# rotate labels
plt.xticks(rotation=45)
plt.axhline(y=0, linestyle='--', color='black')

# label periods for what I traded at what times
plt.axvline(x='2021-01-11', linestyle='--',alpha=0.4)
plt.text('2021-01-17', 8000, 'Wheat')
plt.axvline(x='2021-01-29', linestyle='--',alpha=0.4)

plt.axvline(x='2021-02-01', linestyle='--',alpha=0.4)
plt.text('2021-02-6', 8000, 'Gasoline')
plt.axvline(x='2021-02-19', linestyle='--',alpha=0.4)

plt.axvline(x='2021-02-22', linestyle='--',alpha=0.4)
plt.text('2021-02-24', 8000, 'Gold & Bitcoin')
plt.axvline(x='2021-03-12', linestyle='--',alpha=0.4)

# spruce things up
plt.title('Maximo DeLeon\'s Cumulative Realized PnL')
plt.ylabel('USD $')
plt.xlabel('Date')


plt.show()

final_df.to_csv('DATA_OUT.CSV')