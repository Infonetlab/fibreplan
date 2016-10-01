import pickle
import numpy as np
from pse_2 import rf_get
import os


def make_feas(REF_DIST,htListT,htListR,state,dist,input_file):
    all_data = np.load('adjmat/AD_mat_' +str(input_file)+'_' +str(REF_DIST)+'.npy')

    adjMats = all_data[0]         #adjacency
    States_list = all_data[1]     #Sate names ???It is giving district code
    GP_lists = all_data[2]        #GP codes
    Phase_lists = all_data[3]     #Phase of Bharatnet project
    DistMats = all_data[4]        #distance matrix for each district
    District_code = all_data[5]   #unique code for all districts
    LatLong = all_data[6]         #lat and long of GPs
    TPreq = all_data[7]           #Throughput required per GP
    GPNames = all_data[8]

    print "TPreq = ",TPreq
    
    NODE, NODE = np.shape(adjMats[0])
    
    def removeincominganddiagonal(status):
        for j in range(NODE):                                 ##for each node in that district

            if(Phase_lists[0][j] == status):                     ##if some node belongs to phase-1

                adjMats[0][:,j] = 0                           ##cut all the incoming connections for that

                for k in range(NODE):                  ##for that Phase-1 node

                    if(adjMats[0][j][k] == 1):             ##if there is any adjacent nodes

                        if(Phase_lists[0][k] == status):         ##if it belongs to phase-1 GP

                            adjMats[0][j][k] = 0              ## cut outgoing connection which go to that node

    removeincominganddiagonal(9)
    removeincominganddiagonal(21)
    removeincominganddiagonal(15)


    
    '''
    for j in range(NODE):                                 ##for each node in that district

        if(Phase_lists[0][j] == 2):                     ##if some node belongs to phase-1

            adjMats[0][:,j] = 0                           ##cut all the incoming connections for that
            
            for k in range(NODE):                         ##for that Phase-1 node
                
                if(adjMats[0][j][k] == 1):                ##if there is any adjacent nodes
                    
                    if(Phase_lists[0][k] == 2):         ##if it belongs to phase-1 GP

                        adjMats[0][j][k] = 0              ## cut outgoing connection which go to that node
     '''               


    feas=adjMats[0]
    TP=np.zeros(shape=(NODE,NODE))
    TxH=np.zeros(shape=(NODE,NODE))
    RxH=np.zeros(shape=(NODE,NODE))
    feasTP=np.identity(NODE)
    for j in range(NODE):                                    ##for each node in that district
        htListT= [10,15,20,30,40]
        for k in range(NODE):                            ##for that Phase-2 node
            if (adjMats[0][j][k] == 1):                  ##If there is any adjacent nodes
            #####Added to compare till differnt height for towers
                if Phase_lists[0][j]!=9:                              ###for all nodes except towers max. height will be 15m on both sides
                    htListT=htListR
                    print "gp",htListT                    
                else:
                    print "tower",htListT
                ress = rf_get([LatLong[j],LatLong[k]],htListT,htListR,state,dist)
                print "ress",ress
                if ress == 0:
                    continue
                if ress[0][0]==0:
                    feas[j][k] = 0
                    TP[j][k]= 0
                    TxH[j][k] =0
                    RxH[j][k] = 0
                else:
                    TP[j][k]= ress[0][0]
                    TxH[j][k] = ress[1][0]
                    RxH[j][k] = ress[2][0]
                    Tprequired=float(TPreq[0][k])/62.5
                    print TPreq[0][k]
                    
                    if(int(ress[0][0]) > Tprequired):
                        feasTP[j][k] = 1

    # fp=0 
    # fs=0
    # for i in range(NODE):
    #     for j in range(NODE):
    #         if(feas[i][j]==1):
    #             fs+=1
    #             if(feasTP[i][j]==1):
    #                 fp+=1
                
    # print "#########################################################################fp",fp
    # print "fs=",fs
    if not os.path.exists('feasmat'):
        os.makedirs('feasmat')
    name = 'feasmat/Feas_mat_{}_{}'.format(input_file,REF_DIST)
    np.save(name,np.array([feas,TP,TxH,RxH,feasTP]))
    return 0

# if __name__ == '__main__':
#     #print latlongdist([38.8985, -77.0378],[38.8971, -77.0439])a
#     # make_feas(5,[40,15])
