import json
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import re

%matplotlib auto

prov = gpd.read_file('C:/Users/santpi01/Documents/pim/cbsgebiedsindelingen_2021_v1.gpkg' ,
 layer='cbs_provincie_2020_gegeneraliseerd')

def prepare_gdf(json_file):
    plaatsen=pd.read_json(json_file, typ='series')
    geometry=plaatsen.apply(lambda x:Point(x[1],x[0]))
    gdf = gpd.GeoDataFrame(plaatsen, geometry=geometry)
    gdf = gdf.set_crs(epsg=4326)
    gdf=gdf.to_crs(epsg=28992)
    gdf.index.name='name'
    gdf=gdf.reset_index()
    gdf['capital']=gdf['name'].apply(
        lambda x: re.search('[A-Z]',x).group())
    gdf.loc[gdf['name'].str[:2]=='IJ','capital']='IJ'
    return gdf


def collect_routes(start_places):
#start with first letter and find closest place with next letter
    routes={}
    for _,row in start_places.iterrows():
        sub=naam_plaatsen.copy()
        # sub=sub.drop(sub.loc[sub['name']=='Emmaberg'].index)
        route=row['name']
        pos=row['geometry']
        cumdist=0
        for nn in [t for t in naam[1:]]:
            cumdist+=sub.loc[sub['capital']==nn].distance(pos).min()
            index=sub.loc[sub['capital']==nn].distance(pos).idxmin()
            route+=f"_{naam_plaatsen.loc[index,'name']}"
            pos=sub.loc[index,'geometry']
            sub=sub.drop(index=index)
        routes[route]=cumdist    
    return routes

def get_closest_start_finish(naam):
    s=naam[0]
    f=naam[-1].upper()
    dist=1000
    for _,row in naam_plaatsen.loc[naam_plaatsen['capital']==s].iterrows():
        dist_new=naam_plaatsen.loc[naam_plaatsen['capital']==f].distance(row['geometry']).min()
        f_plaats=naam_plaatsen.loc[naam_plaatsen.loc[naam_plaatsen['capital']==f].distance(row['geometry']).idxmin(),'name']
        if dist_new<dist:
            combi=row['name']+'_'+f_plaats
    return combi

def places_in_circle(places):
    #get letter with the least places.make a list for every place of this letter
    #with places closest by and at least one place for every letter
    least_letter=places.groupby('capital').count().idxmin()[0]
    lijst=[]
    buf=1000
    while len(lijst)==0:
        for _,row in places.loc[places['capital']==least_letter].iterrows():
            sub=places.loc[places.within(row['geometry'].buffer(buf))]
            if all([r in list(sub['capital']) for r in [t for t in naam]]):
                lijst.append(sub)
        buf+=1000
    return lijst

test=gek 
min(routes.values())
#plaatsen Limburg uit Nederland wiki pagina
gdf=prepare_gdf('plaatsen.json')
sub_gdf=gdf.copy()

# Limburg = prov.loc[prov['statnaam']=='Limburg','geometry'].iloc[0]
# sub_gdf=gdf.loc[gdf.within(Limburg)]

#plaatsen Limburg uit Limburg wiki pagina
# Lim_plaatsen=prepare_gdf('plaatsen_limburg.json')

naam='Wilhelmus'.upper()
naam_plaatsen = sub_gdf.loc[sub_gdf['capital'].isin([t for t in naam])]



fl=naam[0]
places=naam_plaatsen.loc[naam_plaatsen['capital']==fl]
routes=collect_routes(pd.concat([lijst[0],naam_plaatsen.loc[naam_plaatsen['capital']=='L']]))
routes=collect_routes(places)

collect_routes(naam_plaatsen.loc[
    naam_plaatsen['name']==get_closest_start_finish('Wilhelmus').split('_')[0]])


