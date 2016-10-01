import numpy as np
import datetime
DEBUG = True
import os

def read_csv_fields(filename, fields):
    
    ## Explicit declare : This is a custom function
    ## pass the input (csv) filename and list of column labels to extract
    ST_IDX =0
    DC_IDX=1

    t1 =  datetime.datetime.now()
    with open('input/'+filename+'.csv', 'r') as f:
        titles = f.readline()
        lines = f.readlines()
    titles = titles.strip().split(',')
    


    #print('Im Here : {}'.format(len(titles)))
    print titles 
    #exit()
    
    # Note: Not all fields are relevant 
    # So we pick those whicch are relevant
     
    indices = []
    i=0
    for elem in titles:
        if elem.strip('"') in fields:
            indices.append(i)
        i = i+1

    
    print 'indices : ',indices
    #exit()
    # Parse each line into meaningful data now

    data_mat = [] 
    i=0
    error_count = 0 
    for line in lines:
        row = line.strip()
        row = row.strip('"').split(',')
        try:
            data_mat.append( [ row[idx] for idx in indices ])
        except IndexError:
            print 'Error parsing index: ', i, ':', line, '>' , row
            error_count = error_count + 1
            pass
        i = i+1
        
        
    data_mat = np.array(data_mat)
    if DEBUG:
        #print len(titles), titles
        #print (indices)
        print('Parsed {} lines: \
        \r\n\tEncountered error on {} lines\
        \r\n\tTotal {} lines retreived '.format(i,error_count, data_mat.shape[0]))
        #print len(lines)
        
        print 'time taken :', datetime.datetime.now()-t1
        print ('shape of data_mat: {}'.format(data_mat.shape) )
    # parsing is complete/ Now seperate data into state data
    #exit() 
    rows, cols = data_mat.shape
    states = []
    ##data_mat[r,ST_IDX] refers to first column which has state information
    for r in range(rows):
        cur_state = data_mat[r,ST_IDX]
        # print cur_state
        if not cur_state in states:
            states.append(cur_state)
    print len(states), states
    
    district_data=[]
    k=0
    state_col = data_mat[:,ST_IDX]

    
    print('shape of state_col :{}'.format(state_col.shape))
    #exit()
    for state in states:
        
        bool_mat = np.where(state_col == state)
        bool_mat = list(bool_mat[0])
        #print len(bool_mat)
        res = np.copy(data_mat[bool_mat,:])

        ## Res has the state data

        ## Which district codes are there for this data?
        rr, cc = res.shape
        dCodes=[]
        # print res[:,DC_IDX]
        for i in range(rr):
            if not res[i,DC_IDX] in dCodes:
                dCodes.append(res[i,DC_IDX])

        ## dCodes has the list of all district codes
        rDC = res[:,DC_IDX]
        for dc in dCodes:   
            mask = np.where(rDC == dc)
            mask = list(mask[0])

            dRes = np.copy(res[mask,:])
            print('Processing dc:{} length is :{}'.format(dRes[0,DC_IDX], dRes.shape[0]))
            district_data.append(dRes)
        #print state,' has follow data :\r\n'
        #print res.shape, res[:10,:]
        #print '========'
        k = k+1
    if not os.path.exists('latlongraw'):
        os.makedirs('latlongraw')
    np.save('latlongraw/latlongRAW_'+filename,np.array([district_data,states]))
    print 'Total time taken :', datetime.datetime.now()-t1
    return 'latlongRAW_'+filename+'.npy'

if __name__ == '__main__':
    DEBUG = True
#    read_csv_fields('Cleaned_GP_data.csv', ['sequence_no', 'OLT_CODE', 'GP_Code', 'Lat', 'Long', 'St_Name', 'Dt_Code'])
#    read_csv_fields('thane_GP_data.csv', ['State_Code','District_Code','Block_Code','GP_Code', 'Latitude', 'Longitude','Phase','throughput'])
