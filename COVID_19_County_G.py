# -*- coding: utf-8 -*-
"""
Created on Wed May  6 15:30:46 2020

@author: Dan Wilson
"""

import requests
from bs4 import BeautifulSoup 
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import time
import datetime

date = '08-07-2020'
page = requests.get("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"+date+".csv")

savedir = 'C:\\Users\\###\\####s\\COVID-19\\COVID_Figures'

try: 
    os.makedirs(savedir + '\\' + str(date))
except FileExistsError:
    pass

soup = BeautifulSoup(page.content, 'html.parser')
df = pd.DataFrame(soup)
data = df.to_csv()
data2 = data.splitlines()

b=[]
c=[]
series2=[]
state1 = 'Virginia'
state2 = 'Maryland'
state3 = 'District of Columbia'

VA, MD, = [[]],[[]]
Alex, Arli, Fair, DC, PG, Char, Anne, KG = [],[],[],[],[],[],[],[]
VAcases,     MDcases,     DCcases     = [],[],[]
VAactive,    MDactive,    DCactive    = [],[],[]
VAdeaths,    MDdeaths,    DCdeaths    = [],[],[]
VArecovered, MDrecovered, DCrecovered = [],[],[]
VAcount,     MDcount,     DCcount     = 0, 0, 0
count = 0

county_names = ['Alexandria', 'Arlington', 'Fairfax',
                'DC', 'PG County', 'Charles',
                'Anne Arundel', 'King George']

for nn in range(0,len(data2),1):
    
    a=data2[nn].split(',')
    
    for mm in range(0,len(a),1):
        
        if a[mm] == state1 and a[mm-1] == 'Alexandria':
            
            Alex.append(a[7])
            Alex.append(a[10])
            Alex.append(a[8])
            Alex.append(a[9])
            print('Alexandria Found!')
            count += 1

        if a[mm] == state1 and a[mm-1] == 'Arlington':
            
            Arli.append(a[7])
            Arli.append(a[10])
            Arli.append(a[8])
            Arli.append(a[9])
            print('Arlington Found!')
            count += 1

        if a[mm] == state1 and a[mm-1] == 'Fairfax':
            
            Fair.append(a[7])
            Fair.append(a[10])
            Fair.append(a[8])
            Fair.append(a[9])
            print('Fairfax Found!')
            count += 1 
            
        if a[mm] == state1 and a[mm-1] == 'King George':
            
            KG.append(a[7])
            KG.append(a[10])
            KG.append(a[8])
            KG.append(a[9])
            print('King George Found!')
            count += 1 
            
        if a[mm] == state2 and a[mm-1] == 'Prince George\'s':
            
            PG.append(a[7])
            PG.append(a[10])
            PG.append(a[8])
            PG.append(a[9])   
            print('PG County Found!')
            count += 1
            
        if a[mm] == state2 and a[mm-1] == 'Charles':
            
            Char.append(a[7])
            Char.append(a[10])
            Char.append(a[8])
            Char.append(a[9])    
            print('Charles County Found!')
            count += 1
            
        if a[mm] == state2 and a[mm-1] == 'Anne Arundel':
            
            Anne.append(a[7])
            Anne.append(a[10])
            Anne.append(a[8])
            Anne.append(a[9])
            print('Anne Arundel County Found!')
            count += 1
            
        if a[mm] == state3:
            
            DC.append(a[7])
            DC.append(a[10])
            DC.append(a[8])
            DC.append(a[9])
            print('DC Found!')
            count += 1
        
    if count == 9:
        break
            
frame1 = pd.DataFrame(VA)
frame1.to_csv('C:\\Users\\####\\COVID-19\\'+date+'.csv')

prevsave = ('C:\\Users\\####\\COVID-19\\COVID19Track.xlsx')
prevdata = pd.read_excel(prevsave, sheet_name=None)
#Build the saved file.  Each county gets a different sheet.
prevdata = dict(prevdata)

dataWork = prevdata['Worksheet Information']
dataAlex = prevdata['Alexandria']
dataArli = prevdata["Arlington"]
dataFair = prevdata["Fairfax"]
dataDC   = prevdata["DC"]
dataPG   = prevdata['PG County']
dataChar = prevdata['Charles']
dataAnne = prevdata['Anne Arundel']
dataTota = prevdata['Totals']
dataKG   = prevdata['King George']

#1.  Import previous data
#2.  Check current day and get correct row information for saving new data. 
#3.  Add new data to dictionary.  
#4.  Add in new date for next iteration. 

newdate = (datetime.datetime.strptime(date, "%m-%d-%Y") + datetime.timedelta(days=1))

for ii in np.arange(0,len(dataAlex['Date']),1):
    
    if dataAlex['Date'][ii].strftime("%m-%d-%Y") == date:
        
        dataAlex.loc[ii,'Cases']     = int(Alex[0])
        dataAlex.loc[ii,'Active']    = int(Alex[1])
        dataAlex.loc[ii,'Deaths']    = int(Alex[2])
        dataAlex.loc[ii,'Recovered'] = int(Alex[3])
        dataAlex.loc[ii+1,'Date']    = newdate
        
        
        dataArli.loc[ii,'Cases']     = int(Arli[0])
        dataArli.loc[ii,'Active']    = int(Arli[1])
        dataArli.loc[ii,'Deaths']    = int(Arli[2])
        dataArli.loc[ii,'Recovered'] = int(Arli[3])
        dataArli.loc[ii+1,'Date']    = newdate
        
        dataFair.loc[ii,'Cases']     = int(Fair[0])
        dataFair.loc[ii,'Active']    = int(Fair[1])
        dataFair.loc[ii,'Deaths']    = int(Fair[2])
        dataFair.loc[ii,'Recovered'] = int(Fair[3])
        dataFair.loc[ii+1,'Date']    = newdate
        
        dataDC.loc[ii,'Cases']       = int(DC[0])
        dataDC.loc[ii,'Active']      = int(DC[1])
        dataDC.loc[ii,'Deaths']      = int(DC[2])
        dataDC.loc[ii,'Recovered']   = int(DC[3])
        dataDC.loc[ii+1,'Date']      = newdate
        
        dataPG.loc[ii,'Cases']       = int(PG[0])
        dataPG.loc[ii,'Active']      = int(PG[1])
        dataPG.loc[ii,'Deaths']      = int(PG[2])
        dataPG.loc[ii,'Recovered']   = int(PG[3])
        dataPG.loc[ii+1,'Date']      = newdate
        
        dataChar.loc[ii,'Cases']     = int(Char[0])
        dataChar.loc[ii,'Active']    = int(Char[1])
        dataChar.loc[ii,'Deaths']    = int(Char[2])
        dataChar.loc[ii,'Recovered'] = int(Char[3])
        dataChar.loc[ii+1,'Date']    = newdate
        
        dataAnne.loc[ii,'Cases']     = int(Anne[0])
        dataAnne.loc[ii,'Active']    = int(Anne[1])
        dataAnne.loc[ii,'Deaths']    = int(Anne[2])
        dataAnne.loc[ii,'Recovered'] = int(Anne[3])
        dataAnne.loc[ii+1,'Date']    = newdate
        
        dataKG.loc[ii,'Cases']       = int(KG[0])
        dataKG.loc[ii,'Active']      = int(KG[1])
        dataKG.loc[ii,'Deaths']      = int(KG[2])
        dataKG.loc[ii,'Recovered']   = int(KG[3])
        dataKG.loc[ii+1,'Date']      = newdate
        
        dataTota.loc[ii,'Cases']     = float(Alex[0])+float(Arli[0])+float(Fair[0])+float(DC[0])+float(PG[0])+float(Char[0])+float(Anne[0])
        dataTota.loc[ii,'Active']    = float(Alex[1])+float(Arli[1])+float(Fair[1])+float(DC[1])+float(PG[1])+float(Char[1])+float(Anne[1])
        dataTota.loc[ii,'Deaths']    = float(Alex[2])+float(Arli[2])+float(Fair[2])+float(DC[2])+float(PG[2])+float(Char[2])+float(Anne[2])
        dataTota.loc[ii,'Recovered'] = float(Alex[3])+float(Arli[3])+float(Fair[3])+float(DC[3])+float(PG[3])+float(Char[3])+float(Anne[3])
        dataTota.loc[ii+1,'Date']    = newdate
#Create new Dictionary
dataWork = list(dataWork)
dataWork.append('Last Update:')
dataWork.append(time.asctime(time.localtime()))
dataWork = pd.DataFrame(dataWork)

writer = pd.ExcelWriter('C:\\Users\\####\\COVID-19\\COVID19Track.xlsx', engine='xlsxwriter')
dataWork.to_excel(writer, sheet_name='Worksheet Information', index=False)
dataAlex.to_excel(writer, sheet_name='Alexandria', index=False)
dataArli.to_excel(writer, sheet_name='Arlington', index=False)
dataFair.to_excel(writer, sheet_name='Fairfax', index=False)
dataDC.to_excel(writer, sheet_name='DC', index=False)
dataPG.to_excel(writer, sheet_name='PG County', index=False)
dataChar.to_excel(writer, sheet_name='Charles', index=False)
dataAnne.to_excel(writer, sheet_name='Anne Arundel', index=False)
dataTota.to_excel(writer, sheet_name='Totals', index=False)
dataKG.to_excel(writer, sheet_name='King George', index=False)
writer.save()

for qq in np.arange(0,count-1,1):
    
    fig, axes = plt.subplots(figsize=(19.2,10.8))

    fig.suptitle(str(county_names[qq])+' Data, As of '+str(date)+'', fontsize=16, fontweight='bold')
    
    im1 = axes.plot(prevdata[county_names[qq]]['Date'],prevdata[county_names[qq]]['Cases'],'b:',label = "Cases")
    im2 = axes.plot(prevdata[county_names[qq]]['Date'],prevdata[county_names[qq]]['Active'],'r:',label = "Active")
    im3 = axes.plot(prevdata[county_names[qq]]['Date'],prevdata[county_names[qq]]['Deaths'],'k:',label = "Deaths")
    im4 = axes.plot(prevdata[county_names[qq]]['Date'],prevdata[county_names[qq]]['Recovered'],'g:',label = 'Recovered')

    axes.set_xlabel('Date', fontsize=14,fontweight='bold',labelpad=5)
    axes.set_ylabel('Count (# of people)',fontsize=14,fontweight='bold',labelpad=10)
    axes.set_title('Raw Data',fontsize=14,fontweight='bold')
    axes.tick_params(axis='x', labelrotation=30)
    axes.legend()

    fig.savefig(savedir + '\\' + str(date)+ '\\' + str(county_names[qq])+'_' + str(date)+'.png')                  