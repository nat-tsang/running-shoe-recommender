import pandas as pd

folderpath = 'C:/Users/natal/OneDrive/Documents/natalie-code/csv/shoe_neutral.csv'
df = pd.read_csv(folderpath)

list = []
for ind,shoe in enumerate(df['weight']):
    if shoe != 'None':
        #print(shoe,type(shoe))
        #list = shoe.split('/')
        #new_shoe = float(list[1].replace('g',''))
        list.append(float(shoe))
    else:
        list.append(None)
df['weight'] = list
# for ind,shoe in enumerate(df['price']):
#     if 'On Sale' not in shoe:
#         new_shoe = float(shoe.replace('$',''))
#         df['price'].iloc[ind] = new_shoe
#     elif 'On Sale' in shoe:
#         new_shoe = float(shoe.replace('On Sale $', ''))
#         df['price'].iloc[ind] = new_shoe
#         print(df['price'].iloc[ind])
#         print(type(new_shoe))

# for ind,shoe in enumerate(df['drop']):
#     if shoe != 'None':
#         new_shoe = float(shoe)
#         df['drop'].iloc[ind] = new_shoe

print(type(df['weight'][0]))
df.to_csv(folderpath, index=False)