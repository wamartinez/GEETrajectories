# -*- coding: utf-8 -*-

import os
import ogr
import ee
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#This function performs a simple cloud masking using metadata
def maskS2clouds(image):
    # Bits 10 and 11 are clouds and cirrus, respectively.
    cloudBitMask = 1024
    cirrusBitMask = 2048
    #Get the pixel QA band.
    qa = image.select('QA60')
    #Both flags should be set to zero, indicating clear conditions.
    mask = qa.bitwiseAnd(cloudBitMask).eq(0) and qa.bitwiseAnd(cirrusBitMask).eq(0)
    return image.updateMask(mask)

#NDVI
def ndvi_S2(img):
    ndvi_i = img.normalizedDifference(['B8', 'B4'])
    d = ee.Date(ee.Number(img.get('system:time_start')))
    m = ee.Number(d.get('month'))
    y = ee.Number(d.get('year'))
    ym = d.format('YYYY M')
    return ndvi_i.set({'month':m,'year':y,'ym':ym})

#Metadata
def get_metadata(img):
    m = ee.Number(img.get('month'))
    y = ee.Number(img.get('year'))
    return img.set({'month':m,'year':y})


def get_series_ndvi(Lon,Lat):

    coords = [Lon,Lat]
    feature = ee.Geometry.Point(coords)
    #feature = ee.FeatureCollection(feature)

    #======================================================
    #importing imagery
    #======================================================
    dataset = ee.ImageCollection('COPERNICUS/S2')\
                  .filterDate('2017-01-01','2020-12-31')\
                  .map(maskS2clouds)\
                  .map(get_metadata)\
                  .map(ndvi_S2)\
                  .filterBounds(feature)

    #======================================================
    #Get medians per month
    #======================================================
    months = np.arange(1,13).tolist()

    years = np.arange(2017,2021).tolist()

    ym_list = []
    for y in years:
        for m in months:
            ym = str(y) + str(' ') + str(m)
            ym_list.append(ym)

    ym_list = ee.List(ym_list)

    def get_median_month(x):
        return dataset.filterMetadata('ym','equals',x)\
                        .select('nd').median()\
                        .set('ym',x)
                        
    median_month = ee.ImageCollection.fromImages(ym_list.map(get_median_month))
    composite = median_month.toBands()

    #=============================================================
    #Get values from composite
    #=============================================================
    bandnames = composite.bandNames().getInfo()
    sample_points_composite = composite.sampleRegions(collection= feature,scale= 10,geometries = True)
    #loop features gee object
    features_gee = sample_points_composite.getInfo()['features']

    list_values = []
    list_id = []
    list_ndvi = []
    for f in features_gee:
        for id, ndvi in f['properties'].items():
            list_id.append(int(id.split('_')[0]))
            list_ndvi.append(ndvi)
    dict_df = {
        'id' : list_id,
        'ndvi' : list_ndvi
    }
    #=============================================================
    #Plot
    #=============================================================
    df =  pd.DataFrame(dict_df)
    df_sort = df.sort_values(by = ['id'])
    df_plot = df_sort.reset_index(drop=True) 

    datetime_series = pd.Series(
        pd.date_range("2017-01-01", periods=48, freq="M")
    )
    df_plot["Date"] = datetime_series

    plt.plot(df_plot["Date"],df_plot['ndvi'], 'go-', label='line 1', linewidth=1, linestyle = 'dotted')
    plt.xlabel('Date')
    plt.ylabel('NDVI')
    plt.show()






