import requests
import json
import pandas
import geopandas
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import pyproj
import warnings
warnings.filterwarnings("ignore")

fixed = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/'
url = '{}{}'.format(fixed,'nrg_ind_ren')
metadata = requests.get(url).json()
print(metadata['label'])
data = pandas.Series(metadata['value']).rename(index=int).sort_index()
n = 1 # Initialize the result to 1
for num in metadata['size']:
  n *= num
data = data.reindex(range(0,n))
structure = [pandas.DataFrame({key:val for key,val in metadata['dimension'][dim]['category'].items()}).sort_values('index')['label'].values for dim in metadata['id']]
data.index = pandas.MultiIndex.from_product(structure,names=metadata['id'])
mydata1 = data.reset_index()
mydata1 = mydata1[mydata1['nrg_bal']=='Renewable energy sources in electricity']
mydata1 = mydata1[(mydata1.time=='2022')|(mydata1.time=='2021')|(mydata1.time=='2020')]
mydata1 = mydata1[['geo',0]]
mydata1.rename(columns={'geo':'ADMIN'},inplace=True)
mydata1.rename(columns={0:'Renewable Energy'},inplace=True)

url = '{}{}'.format(fixed,'ilc_pw01')
metadata = requests.get(url).json()
print(metadata['label'])
data = pandas.Series(metadata['value']).rename(index=int).sort_index()
n = 1 # Initialize the result to 1
for num in metadata['size']:
  n *= num
data = data.reindex(range(0,n))
structure = [pandas.DataFrame({key:val for key,val in metadata['dimension'][dim]['category'].items()}).sort_values('index')['label'].values for dim in metadata['id']]
data.index = pandas.MultiIndex.from_product(structure,names=metadata['id'])
mydata2 = data.reset_index()
mydata2 = mydata2[mydata2['isced11'] == 'All ISCED 2011 levels']
mydata2 = mydata2[mydata2['indic_wb'] == 'Overall life satisfaction']
mydata2 = mydata2[mydata2['sex'] == 'Total']
mydata2 = mydata2[mydata2['age'] == '16 years or over']
mydata2 = mydata2[(mydata2.time=='2022')|(mydata2.time=='2021')|(mydata2.time=='2020')]
mydata2 = mydata2[['geo',0]]
mydata2.rename(columns={'geo':'ADMIN'},inplace=True)
mydata2.rename(columns={0:'Overall Life Satisfaction'},inplace=True)

url = '{}{}'.format(fixed,'sdg_08_60')
metadata = requests.get(url).json()
print(metadata['label'])
data = pandas.Series(metadata['value']).rename(index=int).sort_index()
n = 1 # Initialize the result to 1
for num in metadata['size']:
  n *= num
data = data.reindex(range(0,n))
structure = [pandas.DataFrame({key:val for key,val in metadata['dimension'][dim]['category'].items()}).sort_values('index')['label'].values for dim in metadata['id']]
data.index = pandas.MultiIndex.from_product(structure,names=metadata['id'])
mydata3 = data.reset_index()
mydata3 = mydata3[mydata3['sex'] == 'Total']
mydata3 = mydata3[(mydata3.time=='2021')|(mydata3.time=='2020')]
mydata3 = mydata3[['geo',0]]
mydata3.rename(columns={'geo':'ADMIN'},inplace=True)
mydata3.rename(columns={0:'Fatal Accidents'},inplace=True)

url = '{}{}'.format(fixed,'sdg_08_30a')
metadata = requests.get(url).json()
print(metadata['label'])
data = pandas.Series(metadata['value']).rename(index=int).sort_index()
n = 1 # Initialize the result to 1
for num in metadata['size']:
  n *= num
data = data.reindex(range(0,n))
structure = [pandas.DataFrame({key:val for key,val in metadata['dimension'][dim]['category'].items()}).sort_values('index')['label'].values for dim in metadata['id']]
data.index = pandas.MultiIndex.from_product(structure,names=metadata['id'])
mydata4 = data.reset_index()
mydata4 = mydata4[mydata4['citizen'] == 'Reporting country']
mydata4 = mydata4[(mydata4.time=='2022')|(mydata4.time=='2021')|(mydata4.time=='2020')]
mydata4 = mydata4[['geo',0]]
mydata4.rename(columns={'geo':'ADMIN'},inplace=True)
mydata4.rename(columns={0:'Employment Rate'},inplace=True)

mydata = mydata1.merge(mydata2,on='ADMIN',how='left')
mydata = mydata.merge(mydata3,on='ADMIN',how='left')
mydata = mydata.merge(mydata4,on='ADMIN',how='left')
mydata = mydata[['ADMIN','time','Overall Life Satisfaction','Renewable Energy','Fatal Accidents','Employment Rate']]
mydata = mydata[mydata['ADMIN']!='Bulgaria']
mydata = mydata.dropna()
mydata = mydata.reset_index()
data = mydata

world = geopandas.read_file('/content/TFG-Vega/ne_110m_admin_0_countries.zip')[['ADMIN','geometry']]
polygon = Polygon([(-25,35),(40,35),(40,75),(-25,75)])
europe = geopandas.clip(world,polygon)
mapdata = mydata.loc[mydata1.time=='2022','Renewable Energy']
mapdata = mapdata.merge(europe,on='ADMIN',how='right')
mapdata = geopandas.GeoDataFrame(mydata1,geometry='geometry')
fig,ax = plt.subplots(1,figsize=(10,10))
mapdata.plot(column='Renewable Energy',alpha=0.8,cmap='Greens',ax=ax,legend=True)
ax.set_title('Renewable energy sources in electricity, 2022')
ax.axis('off')
fig.savefig('/content/TFG-Vega/Figure1.png')

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

# Assuming 'mydata' is your DataFrame and it's already been defined
print(mydata)
x = mydata.loc[mydata.time=='2022','Fatal Accidents']
y = mydata.loc[mydata.time=='2022','Overall Life Satisfaction']
z = mydata.loc[mydata.time=='2022','Renewable Energy']
country = mydata.loc[mydata.time=='2022,'ADMIN']

# Create a colormap and normalize it based on the 'Energy' column
cmap = plt.get_cmap('Greens')
norm = Normalize(vmin=z.min(), vmax=z.max())

# Create a ScalarMappable object to map scalar data to colors
scalar_mappable = ScalarMappable(cmap=cmap, norm=norm)

# Plot the scatter plot with varying marker sizes and colors
plt.figure(figsize=(25,10))
for i in range(len(x)):
    plt.scatter(x[i], y[i], s=z[i]*100, color=scalar_mappable.to_rgba(z[i]), alpha=0.75, edgecolor='w')
    plt.annotate(country[i], (x[i], y[i]), textcoords="offset points", xytext=(0, 10), ha='center')

# Add colorbar
plt.colorbar(scalar_mappable, label='Renewable Energy')

# Set labels and title
plt.xlabel('Fatal Accidents At Work')
plt.ylabel('Overall Life Satisfaction')
plt.title('Scatter Plot with Energy Color Mapping')

# Adjusting plot limits and margins
plt.margins(0.15)
plt.grid(True)

# Save and show the plot
fig.savefig('/content/TFG-Vega/Figure2.png', dpi=300, bbox_inches='tight')
plt.show()


