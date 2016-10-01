import pickle
import numpy as np
import random
import math
from random import randrange
from csv2npy import read_csv_fields
from adj_maker import make_adjacency
from pse_2 import rf_get
from feas_mkr import make_feas
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
import geocoder
########################################

## '1' ---phase-2  [initial]
## '2' ---phase-1  [initial]
## '9' ---tower    [initial]
##----------------------------------
## '3' ---children of '2'
## '4' ---children of '3'
## '5' ---fibre children of '9'
## '6' ---children of '5'
## '8' ---phase-2 GP within 300 mtr of tower
## '10'---children of '9'
## '11'---children of '10'
## '12'---New ONT proposed because of throughput requirement
## '13'---children of '12'
## '14'---children of '13'

########################################

##distance criteria for adjacency matrix
REF_DIST = 1
htListT = [15,20,30,40]      ##Available heights of transmitting Towers
htListR = [3,6,9,15]            ##Available heights of receiving Towers
POP=6
########################################
upper_limit = 100000
NUM_ZERO_HOP=3
NUM_FIRST_HOP=0



# near_limit = 300
# rear_limit = 2000
########################################

'''
f1 = open('thane_tower_height_'+str(REF_DIST) + str(POP)+'.csv','w')

f1.write('GP seq' + ',' + 'GP lat' + ',' + 'GP long' + ',' + 'GP status' + ',' +\
'GP tower height' +  '\n')

f1.close()

f1 = open('thane_tower_height_'+str(REF_DIST) + str(POP)+'.csv','a+')

f = open('thane_all_Status_'+str(REF_DIST) + str(POP)+'.csv','w')

f.write('FROM GP seq' + ',' + 'FROM GP lat' + ',' + 'FROM GP long' + ',' + 'FROM GP status' + ',' +\
'FROM GP tower height' + ',' + 'LINK throughput' + ','+\

'TO GP seq' + ',' + 'TO GP lat' + ',' + 'TO GP long' + ',' + 'TO GP status' + ',' + 'TO GP tower height' +  '\n')

f.close()
f = open('thane_all_Status_'+str(REF_DIST) + str(POP)+'.csv','a+')
#####################################
print "POPOPOP",str(POP)


'''


##thane_GP_data.csv gives the following informations
##['State_Code','District_Code','Block_Code','GP_Code', 'Latitude', 'Longitude','Phase','throughput']
def getele(filname):

    # filename = read_csv_fields(filname,['State Code','District_Code','Block_Name','GP Code', 'Latitude', 'Longitude','Phase','throughput'])

    #####################################

    # # #create adjacency matrix
    # fname = make_adjacency(REF_DIST,filename,POP)
    # # ######################################


    # all_data = np.load('AD_mat_'+str(REF_DIST) + str(POP)+'.npy')
    all_data = np.load('AD_mat_' + str(filname)+ '_5'+'.npy')

    States_list = all_data[1]     #Sate names '''???It is giving district code'''
    GP_lists = all_data[2]        #GP codes
    Phase_lists = all_data[3]     #Phase of Bharatnet project
    DistMats = all_data[4]        #distance matrix for each district
    District_code = all_data[5]   #unique code for all districts
    Block_code = all_data[8]
    LatLong = all_data[6]         #lat and long of GPs
    reqTP_mat = all_data[7][0]    #throughput required for each GP It is a list

    state = np.unique(States_list[0])
    dist = np.unique(District_code)
    state=state[0]
    dist= dist[0]
    #####################################

    blocks=np.unique(Block_code[0])
    blocks=np.char.strip(str(blocks))

    # print Block_code[0]
    print blocks

    blocks_lat=[]
    blocks_long=[]
    for j in blocks:
        location = geocoder.google(j)
        print location.latlng
        # blocks_lat.append(location.latitude)
        # blocks_long.append(location.longitude)

    print "latitude",blocks_lat
    print "longitude",blocks_long
    # ffname = make_feas(REF_DIST,htListT,htListR,POP,state,dist)
getele('143')
# getele('498.csv')
# getele('499.csv')
# getele('500.csv')
# getele('501.csv')
# getele('505.csv')
# getele('503.csv')
# getele('512.csv')
# getele('521.csv')
# getele('522.csv')
# getele('523.csv')
# getele('524.csv')
# getele('525.csv')
# getele('527.csv')
# getele('528.csv')
# getele('530.csv')
# getele('531.csv')


'''

feas = np.load('Feas_mat_' + str(state)+'_'+ str(district)+'_'+str(REF_DIST)+'_' +str(POP)+'.npy')
feasibility_mat_raw = feas[0]
throughPut_mat = feas[1]
transHeight_mat = feas[2]
receivHeight_mat = feas[3]
adjMats = [feas[4]] ##this feasibility is according to throughput




NODE, NODE = np.shape(adjMats[0])

########################################################
tower_height = [0 for k in range(NODE)]
availableTP_mat = [0 for i in range(NODE)]

########################################################

# print GP_lists[0]
# print Phase_lists[0]
# print LatLong

# degreeGp = np.sum(adjMats[0], axis = 1)
# sumAllElementsAdjMat = np.sum(degreeGp)
# print degreeGp[np.argmax(degreeGp)]
# print sumAllElementsAdjMat


########################################################    

##Adjacency matrix is having 
##phase-1 GP
##phase-2 GP
##block HQ

print Phase_lists[0]
blocks = []
blocks=np.unique(Block_code)
print "blocksssss",blocks

#......................................................................
##In this adjacency matrix first remove "TO" connections to phase-1 GPs
##then remove any interconnection between phase-1 GPs
#......................................................................


for j in range(NODE):                                                                     ##for each node in that district

    if(Phase_lists[0][j] == 9 or Phase_lists[0][j] == 8 or Phase_lists[0][j] == 2):       ##if some node belongs to tower                    

        adjMats[0][:,j] = 0                                                               ##cut all the incoming connections for that
        
        for k in range(NODE):                                                             ##for that node
            
            if(adjMats[0][j][k] == 1):                                                    ##if there is any adjacent nodes
                
                if(Phase_lists[0][k] == 9 or Phase_lists[0][k] == 8 or Phase_lists[0][k] == 2):   ##if it belongs to tower

                    adjMats[0][j][k] = 0                                                  ## cut outgoing connection which go to that node


##Now adjacency matrix is not having any inter-connection between phase-1 GPs
##towers and there is no incoming connection to phase-1 GPs and towers also

##----------------------------------------
# name1 = 'Latlong_22_{}'.format(REF_DIST)
# np.save(name1, LatLong)

# name2 = 'AdjMats_22_{}'.format(REF_DIST)
# np.save(name2, adjMats)
##----------------------------------------






# ###############connect 300 mtr to 2km GPs of a tower through fibre######################

# for n in range(NODE):

#     if Phase_lists[0][n] == 9:

#         tower_height[n] = 'NA'

#         dist5 = [upper_limit for i in range(NODE)]

#         for l in range(NODE):

#             if Phase_lists[0][l] == 1:

#                 dist5[l] = DistMats[0][n][l]

#                 if dist5[l] >near_limit and dist5[l] <rear_limit:

#                     Phase_lists[0][l] = 5

#                     f.write(str(GP_lists[0][n]) + ',' +str(LatLong[n][0]) + ',' +str(LatLong[n][1]) + ',' +str(Phase_lists[0][n]) + ',' + 'Distance' +',' + str(dist5[l]) + ',' +str(GP_lists[0][l]) + ',' +str(LatLong[l][0]) + ',' +str(LatLong[l][1]) + ',' +str(Phase_lists[0][l]) +','+ 'NA' + ',' +'\n' )

#                     adjMats[0][:,l] = 0
 

# for j in range(NODE):                                                                     ##for each node in that district

#     if(Phase_lists[0][j] == 5):       ##if some node belongs to tower                    

#         adjMats[0][:,j] = 0                                                               ##cut all the incoming connections for that
        
#         for k in range(NODE):                                                             ##for that node
            
#             if(adjMats[0][j][k] == 1):                                                    ##if there is any adjacent nodes
                
#                 if(Phase_lists[0][k] == 5):   ##if it belongs to tower

#                     adjMats[0][j][k] = 0                                                  ## cut outgoing connection which go to that node

#########################################To grow from towers#########################################
def ont_zero_hop(status):

    for j in range(NODE):                                    ##for each node in that district

        if (Phase_lists[0][j] == status):                       ##for a phase-1 tower('9') node

            # degree1 = [upper_limit for m in range(NODE)]
            dist1 = [upper_limit for m in range(NODE)]       ##Initial distance is set to be very high

            for k in range(NODE):                            ##for a Phase-2 node

                if (adjMats[0][j][k] == 1):                  ##If there is a feasible link       
                                        
                    # degree1[k] = np.sum(adjMats[0][:,k])     ##incoming degree of that phase-9 node is calculated
                    dist1[k] = DistMats[0][j][k]             ##distance for adjacent nodes are calculated

            limit1 = NUM_ZERO_HOP                                      ##minister (phase-1 node) can have 3 children
            
            while limit1 >  0 :                              ##if children constraint and throughput are available

                # index1 = np.argmin(degree1)                ##choose phase-2 node with minimum connectivity
                index1 = np.argmin(dist1)                    ##choose minimum distance from phse-2 nodes

                
                if dist1[index1] == upper_limit:             ##if no close distance then come out of the loop
                    break

                else:
                
                    Phase_lists[0][index1] = status+1            ##If a phase-2 GP is connected with tower
                                                             ##modify that GP the phase sequence to '10'

                    f.write(str(GP_lists[0][j]) + ',' +str(LatLong[j][0]) + ',' +str(LatLong[j][1]) + ',' +str(Phase_lists[0][j]) + ',' + str(transHeight_mat[j][index1]) +',' + str(throughPut_mat[j][index1]) + ',' +str(GP_lists[0][index1]) + ',' +str(LatLong[index1][0]) + ',' +str(LatLong[index1][1]) + ',' +str(Phase_lists[0][index1]) +','+ str(receivHeight_mat[j][index1]) + ',' +'\n' )

                    if tower_height[j] < transHeight_mat[j][index1]:
                        tower_height[j] = transHeight_mat[j][index1]

                    if tower_height[index1] < receivHeight_mat[j][index1]:
                        tower_height[index1] = receivHeight_mat[j][index1]


                    adjMats[0][:,index1] = 0                 ##cut all the incoming connections

                    limit1 -= 1

                    dist1[index1] = upper_limit                    
                    availableTP_mat[index1] = float(throughPut_mat[j][index1]) - float(reqTP_mat[index1])                  

ph12=0
for m in range(NODE):                   ##for all nodes which are unconnected and have more than 150mbps bandwidth reqt.

    if Phase_lists[0][m] == 1:
        if(float(reqTP_mat[m]) > 100.0):   
            Phase_lists[0][m] = 12              ##Mark them as phase 12 and grow from there to unconnected GP's
            f.write(str(GP_lists[0][m]) +',' + str(LatLong[m][0]) +',' + str(LatLong[m][1]) + ',' + str(Phase_lists[0][m]) + ',' + 'NOT' + ',' + str(reqTP_mat[m])+ ',' + 'NOT'+ ',' + 'NOT'+ ',' + 'NOT'+ ',' + 'NOT'+','+ 'NOT'+','+'\n')
            ph12+=1

for j in range(NODE):                                                                     ##for each node in that district

    if(Phase_lists[0][j] == 12):       ##if some node belongs to tower                    

        adjMats[0][:,j] = 0                                                               ##cut all the incoming connections for that
        
        for k in range(NODE):                                                             ##for that node
            
            if(adjMats[0][j][k] == 1):                                                    ##if there is any adjacent nodes
                
                if(Phase_lists[0][k] == 12):   ##if it belongs to tower

                    adjMats[0][j][k] = 0    


ont_zero_hop(12)


ont_zero_hop(5)
ont_zero_hop(9)
ont_zero_hop(2)


####################to grow from '10' nodes######################


def parenttochild(status):
    for m in range(NODE):                                       ##for all nodes

        
        if Phase_lists[0][m] == status:                           ##If node is child of tower

            # degree3 = [0 for i in range(NODE)]
            dist3 = [upper_limit for i in range(NODE)]
        
            for n in range(NODE):                               
        
                if adjMats[0][m][n] == 1:                       ##If any other node is adjacent to child of Status 3 node
        
                    # degree3[n] = np.sum(adjMats[0][n,:])      ##Calculate it's outgoing degree
                    dist3[n] = DistMats[0][m][n]


            limit3 = NUM_FIRST_HOP                                           ##children of minister can have 2 children
            while limit3 > 0 and availableTP_mat[m]>0:

                index3 = np.argmin(dist3)                        ##choose minimum distance node
                                                   
                if dist3[index3] == upper_limit:
                    break

                else:

                    if float(availableTP_mat[m]) - float(reqTP_mat[index3])>0:  ##available throughput of the link is decreasing


                        Phase_lists[0][index3] = status+1            ##Mark it as grand-child of '9'           

                        f.write(str(GP_lists[0][m]) + ',' +str(LatLong[m][0]) + ',' +str(LatLong[m][1]) + ',' +str(Phase_lists[0][m]) + ',' + str(transHeight_mat[m][index3])+','+str(throughPut_mat[m][index3]) +','+str(GP_lists[0][index3]) + ',' +str(LatLong[index3][0]) + ',' +str(LatLong[index3][1]) + ',' +str(Phase_lists[0][index3]) + ','+ str(receivHeight_mat[m][index3]) +',' +'\n' )

                        if tower_height[m] < transHeight_mat[m][index3]:
                            tower_height[m] = transHeight_mat[m][index3]

                        if tower_height[index3] < receivHeight_mat[m][index3]:
                            tower_height[index3] = receivHeight_mat[m][index3]

                        adjMats[0][:,index3] = 0                  ##cut all the incoming connections

                        limit3 -= 1
                        dist3[index3] = upper_limit
                        availableTP_mat[m] -= float(reqTP_mat[index3])

                    else:
                        break


parenttochild(10)

#################################to grow from '3' nodes##############################################

parenttochild(3)
#################################to grow from '6' nodes##############################################
parenttochild(6)




# parenttochild(13)


print "Phase 2 GP's to be connected with fibre",ph12
print "Status of all the nodes\n",Phase_lists[0]



for k in range(NODE):
    f1.write(str(GP_lists[0][k]) + ',' + str(LatLong[k][0]) + ',' + str(LatLong[k][1]) + ',' + str(Phase_lists[0][k]) +','+ str(tower_height[k]) + '\n')

#######for satellite connection

# for m in range(NODE):                                       ##for all nodes

#     degreesat = [0 for i in range(NODE)]
    
#     if Phase_lists[0][m] == '2':                            ##If node is unconnected
    
#         degreesat[m] = np.sum(adjMats[0][:,n])        ##Calculate it's incoming degree

#         if (degreesat[m] == 1 ):
#             print "incoming degree 0 and throughput ", reqTP_mat[m]
#             if(reqTP_mat[m] <= 40):
#                 f.write(str(GP_lists[0][m]) +',' + str(LatLong[m][0]) +',' + str(LatLong[m][1]) + ',' + str(Phase_lists[0][m]) + ',' + 'SAT'+ ',' + ''+ ',' + str(reqTP_mat[m])+ ',' + 'SAT'+ ',' + 'SAT'+ ',' + 'SAT'+ ',' + 'SAT'+','+'\n')



#############################################################

####Connecting GP's by giving new ONT's
p = 0
while True:
    p +=1
    print "iteration",p

    degreeGp = np.sum(adjMats[0], axis = 1)

    sumAllElementsAdjMat = np.sum(degreeGp)
    print "1's in adjmat", sumAllElementsAdjMat
            
    if sumAllElementsAdjMat == 0:
        break

#########################################################################################################

    temp_reqTP=reqTP_mat
    for i in range(NODE):

        if not Phase_lists[0][i] == 1:

            temp_reqTP[i] = 0               ##Make requirement of all connected nodes 0

    index3 = np.argmax(temp_reqTP)          ##Unconnected node with max. requirement will be selected

    if not temp_reqTP[index3] == 0:

        Phase_lists[0][index3] = 5      ##If its requirement is more than 0, mark it as ONT

    adjMats[0][:,index3] = 0                ##Make all incoming connections 0

######################################################################################################
    ##index3 keeps node which just got status 5

    degree4 = [0 for k in range(NODE)]

    for k in range(NODE):

        if adjMats[0][index3][k] == 1 and Phase_lists[0][k]==1 :    ##If it is possible to give to any unconnected node from status 5 node

            degree4[k] = np.sum(adjMats[0][k,:])                      ##check outgoing links from that

    if np.sum(degree4)== 0:                                           ## If no links are there add it to file as a status 5 GP with no outgoing links

        f.write(str(GP_lists[0][index3]) +',' + str(LatLong[index3][0]) +',' + str(LatLong[index3][1]) + ',' + str(Phase_lists[0][index3]) + ',' + 'NA'+ ',' + 'NA'+ ',' + 'NA'+ ',' + 'NA'+ ',' + 'NA'+ ',' + 'NA'+ ',' + 'NA'+','+'\n')

    limit3 = 3

    while limit3 > 0:

        index4 = np.argmax(degree4)                 ##choose maximum degree node
        if degree4[index4] == 0:
            break

        else:

            Phase_lists[0][index4] = 6            ##Mark it as child of phase-1 minister            

            f.write(str(GP_lists[0][index3]) + ',' +str(LatLong[index3][0]) + ',' +str(LatLong[index3][1]) + ',' +str(Phase_lists[0][index3]) +',' + str(transHeight_mat[index3][index4])+','+str(throughPut_mat[index3][index4]) +',' +str(GP_lists[0][index4]) + ',' +str(LatLong[index4][0]) + ',' +str(LatLong[index4][1]) + ',' +str(Phase_lists[0][index4]) +','+ str(receivHeight_mat[index3][index4]) + ',' +'\n' )

            if tower_height[m] < transHeight_mat[m][index3]:
                tower_height[m] = transHeight_mat[m][index3]

            if tower_height[index3] < receivHeight_mat[m][index3]:
                tower_height[index3] = receivHeight_mat[m][index3]

            adjMats[0][:,index4] = 0                ##cut all the incoming connections

            limit3 -= 1
            degree4[index4] = 0
            availableTP_mat[index4] = float(throughPut_mat[index3][index4]) - float(reqTP_mat[index4])                  






ctt = 0
tt = 0

for m in range(NODE):                                       ##for all nodes

    if Phase_lists[0][m] == 1:
        f.write(str(GP_lists[0][m]) +',' + str(LatLong[m][0]) +',' + str(LatLong[m][1]) + ',' + str(Phase_lists[0][m]) + ',' + 'NOT' + ',' + str(reqTP_mat[m])+ ',' + 'NOT'+ ',' + 'NOT'+ ',' + 'NOT'+ ',' + 'NOT'+','+ 'NOT'+','+'\n')
        tt +=1
    if Phase_lists[0][m] == 8:
        ctt +=1
        f.write(str(GP_lists[0][m]) +',' + str(LatLong[m][0]) +',' + str(LatLong[m][1]) + ',' + str(Phase_lists[0][m]) + ',' + 'close to tower' + ',' + str(reqTP_mat[m])+ ',' + 'NOT'+ ',' + 'NOT'+ ',' + 'NOT'+ ',' + 'NOT'+','+ 'NOT'+','+'\n')

print "Unconnected GPs",tt
print "GP's within 300m of tower ",ctt
##Now all the phase-1 GPs which are grandchildren of phase-1 are co
##phase-1 connectivity has been exhausted at this stage                    


# print "Status of every node",Phase_lists
# print adjMats[0]
# exit()


block_idx=[]
blocks1=[]
k=0
for j in blocks:
    for i in range(NODE):
        if(Phase_lists[0][i] == 12 or Phase_lists[0][i] == 5):
            if Block_code[i]==j:
                blocks1.append(i)
                print "i,j=",i,j
    block_idx.append(blocks1)
    blocks1=[]
print "block_adj = ",block_idx
print "length of block_adj = ",len(block_idx)
print block_idx[2]
sel=[3,4,7]
DistMats=DistMats[0]
print "DistMats", DistMats
block_dist_mat =[0 for k in range(len(blocks))]
for j in range(len(blocks)):
    # block_adj_mat = adjMats[:,block_idx[j]][block_idx,:]
    block_dist_mat[j]=DistMats[:,block_idx[j]][block_idx[j],:]
    # print "block_dist_mat",block_dist_mat
    X=csr_matrix(block_dist_mat[j])
    Tcsr= minimum_spanning_tree(X)
    Tcsr.toarray().astype(int)
    if(Tcsr.sum() !=0):
        maxi=Tcsr.max()
        print "Maximum length for Block",blocks[j],"= ",maxi/1000, "km"
    dist=Tcsr.sum()
    print "Spanning tree length for Block",blocks[j],"= ",dist/1000, "km"
    

# print "Status\n", Phase_lists


ug = 0
t=0
ct=0
c12=0
tp=0
p1c=0
cont=0
nfibre=0
conf=0
for i in range(NODE):
    if Phase_lists[0][i] == 1:
        ug +=1
    elif Phase_lists[0][i] == 8:
        ct+=1
    elif Phase_lists[0][i] == 9:
        t+=1
    elif Phase_lists[0][i] == 12:
        tp+=1  
    elif Phase_lists[0][i] == 13:
        c12+=1 
    elif Phase_lists[0][i] == 3:
        p1c+=1 
    elif Phase_lists[0][i] == 10:
         cont+=1 
    elif Phase_lists[0][i] == 5:
         nfibre+=1
    elif Phase_lists[0][i] == 6:
         conf+=1
print "Towers ",t
print "Unconnected GPs ",ug
print "connected to phase 1--- ",p1c
print "close to tower ",ct
print "Throughput req. more than 150mbps status 12----",tp
print "connected to 12--status 13 -s",c12
print "connected to tower -s",cont
print "new fibre provided-s",nfibre
print "connected to fibre -s",conf



# degreeGp = np.sum(adjMats[0], axis = 1)
# sumAllElementsAdjMat = np.sum(degreeGp)
# print degreeGp[np.argmax(degreeGp)]
# print sumAllElementsAdjMat'''



