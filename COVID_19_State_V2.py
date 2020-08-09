# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 13:04:33 2020

@author: Dan Wilson
"""

import requests
from bs4 import BeautifulSoup 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime
     
date = '08-08-2020'
page = requests.get("https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_daily_reports_us/"+date+".csv")

savedir = 'C:\\Users\\dan.wilson\\Desktop\\Management\\Tracking_Documents\\COVID-19\\COVID_Figures'

try: 
    os.makedirs(savedir + '\\' + str(date))
except FileExistsError:
    pass

soup = BeautifulSoup(page.content, 'html.parser')
a = len(soup.find_all('tr', class_="js-file-line"))

b=[]
c=[]
series2=[]
 
state_cases, state_deaths, state_recovered, state_active, state_tested, state_hospital, state_testrate, state_hosprate, state_dchange = [],[],[],[],[],[],[],[],[]
  
count = 0

state_names = ['Alabama', 'Alaska', 'Arizona', 
            'Arkansas', 'California', 'Colorado',
            'Connecticut', 'Delaware', 'District of Columbia',
            'Florida', 'Georgia', 'Hawaii',
            'Idaho', 'Illinois', 'Indiana',
            'Iowa', 'Kansas', 'Kentucky',
            'Louisiana', 'Maine', 'Maryland',
            'Massachusetts', 'Michigan', 'Minnesota',
            'Mississippi','Missouri', 'Montana', 'Nebraska',
            'Nevada', 'New Hampshire', 'New Jersey',
            'New Mexico', 'New York', 'North Carolina',
            'North Dakota', 'Ohio', 'Oklahoma',
            'Oregon', 'Pennsylvania', 'Puerto Rico',
            'Rhode Island', 'South Carolina', 'South Dakota',
            'Tennessee', 'Texas', 'Utah', 'Vermont',
            'Virginia', 'Washington', 'West Virginia',
            'Wisconsin', 'Wyoming', 'Stop']

statecount = 0
for ii in range(0,a+1,1):
    
    if state_names[statecount] == 'Stop':
        print('Stopping')
        break
    list1=[]
    #Just grabbing the first header information.  
    if ii == 0:
        line = soup.find(id='LC1')
        colheads = line.find_all('th')
        
        for jj in range(0,len(colheads),1):
            b.append(str(colheads[jj].string))
        series1 = pd.Series(b)    
        
    else:
    #searching line-by-line until the end  Grab a new line each time, with a different ID.   
        line = soup.find(id='LC'+str(ii)+'')
        
        #colheads is a element result of the line.  it gives all the results in the td class, including the case values. 
        colheads = line.find_all('td')
        
        #Reset the variable of list1 and the series.  
        list1=[]
        series=[]
        #count = 0
        
        for kk in np.arange(0,len(colheads),1):
            
            if (colheads[kk].string == state_names[statecount]):
#                print(statecount)
#                print('true')
               
                state_cases.append(str(colheads[6].string))
                state_deaths.append(str(colheads[7].string))
                state_recovered.append(str(colheads[8].string))
                state_active.append(str(colheads[9].string))
                state_tested.append(str(colheads[12].string))
                state_hospital.append(str(colheads[13].string))
                state_testrate.append(str(colheads[17].string))
                state_hosprate.append(str(colheads[18].string))
                statecount += 1
                
for aa in range(0,len(state_recovered)):
    if state_recovered[aa] == 'None':
        state_recovered[aa] = 0
    if state_hospital[aa] == 'None':
        state_hospital[aa] = 0
        
prevsave = ('C:\\Users\\dan.wilson\\Desktop\\Management\\Tracking_Documents\\COVID-19\\State_by_State.xlsx')
prevdata = pd.read_excel(prevsave, sheet_name=None)
#Build the saved file.  Each county gets a different sheet.
prevdata = dict(prevdata)
#1.  Import previous data
#2.  Check current day and get correct row information for saving new data. 
#3.  Add new data to dictionary.
newcount=0  
newdate = (datetime.datetime.strptime(date, "%m-%d-%Y") + datetime.timedelta(days=1))
#for nn in range(0,len(prevdata[state_names[0]]['Date']),1):
for nn in range(0,len(prevdata['Alabama']['Date']),1):    
    if prevdata['Alabama']['Date'][nn].strftime("%m-%d-%Y") == date:
    
        for oo in range(0,len(state_names)-1,1):
#        for oo in range(0,1,1):
        
            prevdata[state_names[oo]].loc[nn,'Cases']                = float(state_cases[oo])
            prevdata[state_names[oo]].loc[nn,'Active']               = float(state_active[oo])
            prevdata[state_names[oo]].loc[nn,'Deaths']               = float(state_deaths[oo])
            prevdata[state_names[oo]].loc[nn,'Recovered']            = float(state_recovered[oo])
            prevdata[state_names[oo]].loc[nn,'Tested']               = float(state_tested[oo])
            prevdata[state_names[oo]].loc[nn,'Test Rate']            = float(state_testrate[oo])
            prevdata[state_names[oo]].loc[nn,'Hospitalized']         = float(state_hospital[oo])
            
            if prevdata[state_names[oo]].loc[nn,'Hospitalization Rate'] == 'None' or 'nan':
                prevdata[state_names[oo]].loc[nn,'Hospitalization Rate'] = 0
            elif prevdata[state_names[oo]].loc[nn,'Hospitalization Rate'] == 0:
                pass
            else:
                prevdata[state_names[oo]].loc[nn,'Hospitalization Rate'] = float(state_hosprate[oo])
                
            prevdata[state_names[oo]].loc[nn,'dChange']              = int(state_cases[oo])-int(prevdata[state_names[oo]].loc[nn-1,'Cases'])
            prevdata[state_names[oo]].loc[nn,'Case/Test']            = int(state_cases[oo])/int(state_tested[oo])
            state_dchange.append(int(state_cases[oo])-int(prevdata[state_names[oo]].loc[nn-1,'Cases']))
            
        prevdata['Totals'].loc[nn,'Cases']        = sum(pd.array(state_cases, dtype=float))
        prevdata['Totals'].loc[nn,'Active']       = sum(pd.array(state_active, dtype=float))
        prevdata['Totals'].loc[nn,'Deaths']       = sum(pd.array(state_deaths, dtype=float))
        prevdata['Totals'].loc[nn,'Recovered']    = sum(pd.array(state_recovered, dtype=float))
        prevdata['Totals'].loc[nn,'Tested']       = sum(pd.array(state_tested, dtype=float))
        prevdata['Totals'].loc[nn,'Hospitalized'] = sum(pd.array(state_hospital, dtype=float))
        prevdata['Totals'].loc[nn,'dChange']      = sum(pd.array(state_dchange, dtype = float))
        prevdata['Totals'].loc[nn,'Case/Test']    = int(prevdata['Totals'].loc[nn,'Cases'])/int(prevdata['Totals'].loc[nn,'Tested'])
        
        break
#if prevdata['Totals'].loc[nn+1,'Date']       == 'nan':
# prevdata['Totals'].loc[nn+1,'Date'] = newdate
writer = pd.ExcelWriter('C:\\Users\\dan.wilson\\Desktop\\Management\\Tracking_Documents\\COVID-19\\State_by_State.xlsx', engine='xlsxwriter')

for pp in np.arange(0,len(state_names)-1,1):

    prevdata[state_names[pp]].to_excel(writer, sheet_name=state_names[pp], index=False)

prevdata['Totals'].to_excel(writer, sheet_name = 'Totals', index=False)   
 
writer.save()    

#Plot All Data from that day by state
#for qq in np.arange(0,1,1):
for qq in np.arange(0,len(state_names)-1,1):
    
    fig, axes = plt.subplots(1,4,figsize=(19.2,10.8))

    axes[0]=plt.subplot2grid((2, 2), (0, 0))
    axes[1]=plt.subplot2grid((2, 2), (0, 1))
    axes[2]=plt.subplot2grid((2, 2), (1, 1))
    axes[3]=plt.subplot2grid((2, 2), (1, 0))
    fig.subplots_adjust(hspace=.5)
    fig.suptitle('State of '+str(state_names[qq])+' Data, As of '+str(date)+'', fontsize=16, fontweight='bold')
    
    im1 = axes[0].plot(prevdata[state_names[qq]]['Date'],prevdata[state_names[qq]]['Cases'],'b:',label = "Cases")
    im2 = axes[0].plot(prevdata[state_names[qq]]['Date'],prevdata[state_names[qq]]['Active'],'r:',label = "Active")
    im3 = axes[0].plot(prevdata[state_names[qq]]['Date'],prevdata[state_names[qq]]['Deaths'],'k:',label = "Deaths")
    im4 = axes[0].plot(prevdata[state_names[qq]]['Date'],prevdata[state_names[qq]]['Recovered'],'g:',label = 'Recovered')
#    im5 = axes[0].plot(prevdata[state_names[qq]]['Date'],prevdata[state_names[qq]]['Tested'],'p:',label = 'Tested')
    
    axes[0].set_xlabel('Date', fontsize=14,fontweight='bold',labelpad=5)
    axes[0].set_ylabel('Count (# of people)',fontsize=14,fontweight='bold',labelpad=10)
    axes[0].set_title('Raw Data',fontsize=14,fontweight='bold')
    axes[0].tick_params(axis='x', labelrotation=30)
    axes[0].legend()
    
    im5 = axes[1].plot(prevdata[state_names[qq]]['Date'],prevdata[state_names[qq]]['dChange'], 'b:',label = "dChange")
    axes[1].set_xlabel('Date', fontsize=14,fontweight='bold',labelpad=5)
    axes[1].set_ylabel('dChange in New Cases',fontsize=14,fontweight='bold',labelpad=10)
    axes[1].set_title('Rate of Change, New Cases',fontsize=14,fontweight='bold')
    axes[1].tick_params(axis='x', labelrotation=30)
    axes[1].legend()
    
    im6 = axes[2].plot(prevdata[state_names[qq]]['Cases'],prevdata[state_names[qq]]['dChange'],'r:',label = "New vs. Existing")
    axes[2].set_xlabel('Existing Cases', fontsize=14, fontweight='bold')
    axes[2].set_ylabel('New Cases', fontsize=14, fontweight='bold')
    axes[2].set_title('New vs Existing, Log/Log',fontsize=14,fontweight='bold')
    axes[2].set_yscale("log")
    axes[2].set_xscale("log")
    axes[2].legend()

    im7 = axes[3].plot(prevdata[state_names[qq]]['Cases'], prevdata[state_names[qq]]['Tested'],'k:',label = 'Cases/Tested')    
    axes[3].set_xlabel('Daily Cases', fontsize=14, fontweight='bold')
    axes[3].tick_params(axis='x', labelrotation=30)
    axes[3].set_ylabel('Daily Tests', fontsize=14, fontweight='bold')
    axes[3].set_title('Cases vs Tested',fontsize=14,fontweight='bold')
    axes[3].legend()
        
    fig.savefig(savedir + '\\' + str(date)+ '\\' + str(state_names[qq])+'_' + str(date)+'.png')
#    
fig, axes = plt.subplots(1,4,figsize=(19.2,10.8))

axes[0]=plt.subplot2grid((2, 2), (0, 0))
axes[1]=plt.subplot2grid((2, 2), (0, 1))
axes[2]=plt.subplot2grid((2, 2), (1, 1))
axes[3]=plt.subplot2grid((2, 2), (1, 0))
fig.subplots_adjust(hspace=.5)
fig.suptitle('United States Data, As of '+str(date)+'', fontsize=16, fontweight='bold')

ims = []

im1 = axes[0].plot(prevdata['Totals']['Date'],prevdata['Totals']['Cases'],'b:',label = "Cases")
im2 = axes[0].plot(prevdata['Totals']['Date'],prevdata['Totals']['Active'],'r:',label = "Active")
im3 = axes[0].plot(prevdata['Totals']['Date'],prevdata['Totals']['Deaths'],'k:',label = "Deaths")
im4 = axes[0].plot(prevdata['Totals']['Date'],prevdata['Totals']['Recovered'],'g:',label = 'Recovered')

axes[0].set_xlabel('Date', fontsize=14,fontweight='bold',labelpad=5)
axes[0].set_ylabel('Count (# of people)',fontsize=14,fontweight='bold',labelpad=10)
axes[0].set_title('Raw Data',fontsize=14,fontweight='bold')
axes[0].tick_params(axis='x', labelrotation=30)
axes[0].legend()

im5 = axes[1].plot(prevdata['Totals']['Date'],prevdata['Totals']['dChange'], 'b:',label = "dChange")
axes[1].set_xlabel('Date', fontsize=14,fontweight='bold',labelpad=5)
axes[1].set_ylabel('dChange in New Cases',fontsize=14,fontweight='bold',labelpad=10)
axes[1].set_title('Rate of Change, New Cases',fontsize=14,fontweight='bold')
axes[1].tick_params(axis='x', labelrotation=30)
axes[1].legend()

im6 = axes[2].plot(prevdata['Totals']['Cases'],prevdata['Totals']['dChange'], 'r:',label = "New vs. Existing")
axes[2].set_xlabel('Existing Cases', fontsize=14, fontweight='bold')
axes[2].set_ylabel('New Cases', fontsize=14, fontweight='bold')
axes[2].set_title('New vs Existing, Log/Log',fontsize=14,fontweight='bold')
axes[2].set_yscale("log")
axes[2].set_xscale("log")
axes[2].legend()

im7 = axes[3].plot(prevdata['Totals']['Cases'], prevdata['Totals']['Tested'],'k:',label = 'Cases/Tested')    
axes[3].set_xlabel('Daily Cases', fontsize=14, fontweight='bold')
axes[3].tick_params(axis='x', labelrotation=30)
axes[3].set_ylabel('Daily Tests', fontsize=14, fontweight='bold')
axes[3].set_title('Cases vs Tested',fontsize=14,fontweight='bold')
axes[3].legend()

fig.savefig(savedir + '\\' + str(date)+ '\\' + 'USA_' + str(date)+'.png')


