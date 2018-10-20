'''
    Conversions between date and time representations
    Brett Hosking 2018

'''
import datetime
import numpy as np
import pandas as pd
import sys

def ticks(df):
    '''
        Given the number of samples in each year and month, produce xticks
        and positions
    '''
    mon_labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    # months in each year
    ysamples    = df['year'].value_counts().sort_index()
    years       = list(ysamples.index)
    mlabels = []
    midx = []
    for i in range(len(ysamples)):
        if i == 0:
            unqmon  = df['month'].iloc[0:ysamples.iloc[i]].unique().T
            ylist   = [years[i]]*len(unqmon)
            midx    = np.asarray((ylist, unqmon)).T
        else:
            unqmon  = df['month'].iloc[ysamples.iloc[i-1]:ysamples.iloc[i-1]+ysamples.iloc[i]].unique().T
            ylist   = [years[i]]*len(unqmon)
            arr     = np.asarray((ylist, unqmon)).T
            midx    = np.concatenate((midx,arr), axis=0)

    # for each month index, asign a label
    for m in midx[:,1]:
        mlabels.append(mon_labels[m-1])

    mlocs = []
    mlocs.append(0)
    cloc = 0
    for m in range(1,len(mlabels)):
        # for each month, calculate the number of seconds
        cloc+=(datetime.datetime(midx[m][0],midx[m][1],1)-datetime.datetime(midx[m-1][0],midx[m-1][1],1)).total_seconds()
        mlocs.append(cloc)

    cloc = 0
    ylocs = []
    ylabels = []
    for y in range(1,len(years)):
        # For each year calculate the number of seconds
        if y == 1:
            # start from 1st recorded month
            cloc+=(datetime.datetime(years[y],1,1)-datetime.datetime(midx[0][0],midx[0][1],1)).total_seconds()
        ylocs.append(cloc)
        ylabels.append(years[y])

    return  mlabels,mlocs,ylabels,ylocs

# def yearticks(df):

def datetime2arr(date,time):
    '''
        Reformat date of DD/MM/YY to [YY, MM, DD]
        Reformat time of hh:mm:ss to [hh, mm, ss]
    '''
    N               = np.shape(date)[0]
    datetime_arr    = np.array(np.zeros((N,6)))
    for d in range(N):
        datetime_arr[d,:3] = date[d].split('/')[::-1]
        datetime_arr[d,3:] = time[d].split(':')
    return datetime_arr.astype(int)


def dt2pd(date,time):
    '''
        Reformat date of DD/MM/YY to [YY, MM, DD]
        Reformat time of hh:mm:ss to [hh, mm, ss]

        convert to pandas dataframe
    '''
    df  = pd.DataFrame(columns=[    'year','month','day','hour','minute','second',
                                    'elapsed_1970/1/1','elapsed_sample','elapsed_month'])
    N   = np.shape(date)[0]

    epoch = datetime.datetime(1970,1,1)
    yrlist, mthlist, dylist, hlist, mlist, slist, epochlist = [],[],[],[],[],[],[]
    for i in range(N):
        year,month,day      = date[i].split('/')[::-1]
        hour,minute,second  = time[i].split(':')
        yrlist.append(int(year));mthlist.append(int(month));dylist.append(int(day))
        hlist.append(int(hour));mlist.append(int(minute));slist.append(int(second))
        epochlist.append((datetime.datetime(int(year),int(month),int(day),
                                            hour=int(hour),
                                            minute=int(minute),
                                            second=int(second) ) - epoch).total_seconds())

    df['year']      = yrlist
    df['month']     = mthlist
    df['day']       = dylist
    df['hour']      = hlist
    df['minute']    = mlist
    df['second']    = slist

    ## elapsed
    offset = (datetime.datetime(    int(df['year'].iloc[0]),
                                    int(df['month'].iloc[0]),
                                    int(df['day'].iloc[0]),
                                    hour=int(df['hour'].iloc[0]),
                                    minute=int(df['minute'].iloc[0]),
                                    second=int(df['second'].iloc[0])) - datetime.datetime( int(df['year'].iloc[0]),
                                                                                    int(df['month'].iloc[0]),1,
                                                                                    hour=0,
                                                                                    minute=0,
                                                                                    second=0)).total_seconds()

    df['elapsed_1970/1/1']             = epochlist
    df['elapsed_sample']               = np.subtract(epochlist,epochlist[0])
    df['elapsed_month']                = np.add(df['elapsed_sample'],offset)
    return df




def datetime2epoch(datetime_arr):
    '''
        Convert date and time into seconds past since 1970

        First data point - elapsed time from 1st of the month

        Parameters
        ----------
        datetime_arr : array
            array of shape (N, 6), where N is the number of timestamps with values
            Year, Month, Day, Hour, Minute, Second

        Returns
        -------
        epoch time since 1970

    '''
    N               = np.shape(datetime_arr)[0]
    epochtime       = np.array(np.zeros(N))
    second_arr      = np.array(np.zeros(N))
    epoch = datetime.datetime(1970,1,1)
    offset = (datetime.datetime(    datetime_arr[0][0],
                                    datetime_arr[0][1],
                                    datetime_arr[0][2],
                                    hour=datetime_arr[0][3],
                                    minute=datetime_arr[0][4],
                                    second=datetime_arr[0][5]) - datetime.datetime( datetime_arr[0][0],
                                                                                    datetime_arr[0][1],1,
                                                                                    hour=0,
                                                                                    minute=0,
                                                                                    second=0)).total_seconds()
    for d in range(N):
        epochtime[d] = (datetime.datetime(  datetime_arr[d][0],
                                            datetime_arr[d][1],
                                            datetime_arr[d][2],
                                            hour=datetime_arr[d][3],
                                            minute=datetime_arr[d][4],
                                            second=datetime_arr[d][5]) - epoch).total_seconds()

        second_arr[d] = epochtime[d] - epochtime[0] + offset

    return epochtime,second_arr

##### Do not use ###
def datecount0(year,month):
    '''
        Determine the number of samples in each month and year

        Has a bug...

        Returns
        -------
        Two array of shape (nYears,2) and (nMonths,3) which indicate the number
        of samples in each year and month, respectively. The second array also
        indicates the corresponding year in index 0 axis=0
    '''
    # samples in each year
    unique, counts  = np.unique(year, return_counts=True)
    ycount          = np.asarray((unique, counts)).T
    mcount          = []
    for i in range(np.shape(ycount)[0]):
        unique, counts  = np.unique(month[i:ycount[i,1]], return_counts=True)
        yeararr         = [ycount[i,0]]*len(unique)
        if i ==0:
            mcount    = np.asarray((yeararr,unique, counts)).T
        else:
            arr       = np.asarray((yeararr,unique, counts)).T
            mcount    = np.concatenate((mcount,arr), axis=0)

    print ycount,mcount
    raise NotYetImplented

def ticks0(mcount):
    '''
        Given the number of samples in each year and month, produce xticks
        and positions
    '''
    mon_labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    mlabels =[]
    for x in range(len(mcount)):
        mlabels.append(mon_labels[(mcount[x,1]-1)])

    mlocs = []
    mlocs.append(0)
    cloc = 0
    for m in xrange(1,len(mlabels)-1):
        # for each month, calculate the number of seconds
        cloc+=(datetime.datetime(mcount[m][0],mcount[m][1],1)-datetime.datetime(mcount[m-1][0],mcount[m-1][1],1)).total_seconds()
        mlocs.append(cloc)

    return  mlabels,mlocs


def elapsed0(dfstamp):
    '''
        Given the time stamp, add the elapsed time to dataframe
        Perhaps combine with dt2pd() to reduce for loops

        Very slow...
    '''
    N               = np.shape(dfstamp)[0]
    epochtime       = np.array(np.zeros(N)) # elapsed from 1970/1/1
    epoch = datetime.datetime(1970,1,1)

    offset = (datetime.datetime(    int(dfstamp['year'].iloc[0]),
                                    int(dfstamp['month'].iloc[0]),
                                    int(dfstamp['day'].iloc[0]),
                                    hour=int(dfstamp['hour'].iloc[0]),
                                    minute=int(dfstamp['minute'].iloc[0]),
                                    second=int(dfstamp['second'].iloc[0])) - datetime.datetime( int(dfstamp['year'].iloc[0]),
                                                                                    int(dfstamp['month'].iloc[0]),1,
                                                                                    hour=0,
                                                                                    minute=0,
                                                                                    second=0)).total_seconds()

    for i in range(N):
        epochtime[i] = (datetime.datetime(  int(dfstamp.iloc[i]['year']),
                                            int(dfstamp.iloc[i]['month']),
                                            int(dfstamp.iloc[i]['day']),
                                            hour=int(dfstamp.iloc[i]['hour']),
                                            minute=int(dfstamp.iloc[i]['minute']),
                                            second=int(dfstamp.iloc[i]['second'])) - epoch).total_seconds()

    dfstamp['elapsed_1970/1/1']             = epochtime
    dfstamp['elapsed_sample']               = np.subtract(epochtime,epochtime[0])
    dfstamp['elapsed_month']                = np.add(dfstamp['elapsed_sample'],offset)

    return dfstamp
