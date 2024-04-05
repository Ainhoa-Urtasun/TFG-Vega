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
url = '{}{}'.format(fixed,'sdg_07_50')
metadata = requests.get(url).json()
print(metadata['label'])
data = pandas.Series(metadata['value']).rename(index=int).sort_index()
n = 1 # Initialize the result to 1
for num in metadata['size']:
  n *= num
data = data.reindex(range(0,n),fill_value=0)
structure = [pandas.DataFrame({key:val for key,val in metadata['dimension'][dim]['category'].items()}).sort_values('index')['label'].values for dim in metadata['id']]
data.index = pandas.MultiIndex.from_product(structure,names=metadata['id'])
mydata1 = data.reset_index()
mydata1 = mydata1[mydata1['siec']=='Total']
mydata1 = mydata1[mydata1.time=='2022']
mydata1 = mydata1[['geo',0]]
mydata1.rename(columns={'geo':'ADMIN'},inplace=True)
mydata1.rename(columns={0:'Energy'},inplace=True)

world = geopandas.read_file('/content/TFG-Vega/ne_110m_admin_0_countries.zip')[['ADMIN','geometry']]
polygon = Polygon([(-25,35),(40,35),(40,75),(-25,75)])
europe = geopandas.clip(world,polygon)

mydata1 = mydata1.merge(europe,on='ADMIN',how='right')
mydata1 = geopandas.GeoDataFrame(mydata1,geometry='geometry')
fig,ax = plt.subplots(1,figsize=(10,10))
mydata1.plot(column='Energy',alpha=0.8,cmap='viridis',ax=ax,legend=True)
ax.set_title('Energy import dependency by product, 2022 (Fuente: Eurostat, online datacode: sdg_07_50)')
ax.axis('off')
fig.savefig('/content/TFG-Vega/Europe.png')

url = '{}{}'.format(fixed,'ilc_pw01')
metadata = requests.get(url).json()
print(metadata['label'])
data = pandas.Series(metadata['value']).rename(index=int).sort_index()
n = 1 # Initialize the result to 1
for num in metadata['size']:
  n *= num
data = data.reindex(range(0,n),fill_value=0)
structure = [pandas.DataFrame({key:val for key,val in metadata['dimension'][dim]['category'].items()}).sort_values('index')['label'].values for dim in metadata['id']]
data.index = pandas.MultiIndex.from_product(structure,names=metadata['id'])
mydata2 = data.reset_index()
print(mydata2)
mydata = mydata2[mydata2['isced11'] == 'All ISCED 2011 levels']
mydata2 = mydata2[mydata2['indic_wb'] == 'Overall life satisfaction']
mydata2 = mydata2[mydata2['sex'] == 'Total']
mydata2 = mydata2[mydata2['age'] == '16 years or over']
mydata2 = mydata2[mydata2['time'] == '2022']
mydata2 = mydata2[['geo',0]]
mydata2.rename(columns={'geo':'ADMIN'},inplace=True)
mydata2.rename(columns={0:'Overall life satisfaction'},inplace=True)
print(mydata2)

mydata = mydata1.merge(mydata2,on='ADMIN',how='left')
mydata = mydata[['ADMIN','Overall life satisfaction','Energy']]
print(mydata)

