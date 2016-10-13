import pickle
import numpy as np
import random
import math
import os
import sys
import time
from sets import Set
from random import randrange
from csv2npy import read_csv_fields
from adj_maker import make_adjacency
from pse_2 import rf_get
from pse_2 import get_elevation_profile
from feas_mkr import make_feas
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
#from directions import fetch_direction
from maps_blk import road_dist_block,road_dist_block_file
from sptgraph import spt,print_mst_links,build_Tcsr,fibre_saved_if_wireless,handle_no_road_cases,prun_leaf_wps
from pse_2 import latlongdist
from copy import copy, deepcopy
from directions import get_waypoints,build_latlng_dict
########################################



## '21' ---phase-1  [initial]
## '2' ---phase-1  [initial]
## '9' ---tower    [initial]
##----------------------------------
## '3' ---children of '2'
## '4' ---children of '3',state,dist   ---not used
## '5' ---New fibre --New ministers
## '6' ---children of '5' 
## '8' ---phase-2 GP within 300 mtr of tower  
## '10'---
## '11'---children of '10'   ---not used
## '12'---New ONT proposed because of throughput requirement  
## '13'---children of '12'
## '14'---children of '13'   not used
## '15'---Block HQ

########################################

##distance criteria for adjacency matrix
REF_DIST = 5						##km for adjacency matrix
htListT = [10,15,20,30,40]      ##Available heights of transmitting Towers
htListR = [3,6,9,15]            ##Available heights of receiving Towers

########################################
upper_limit = 100000
NUM_ZERO_HOP=0
NUMT_ZERO_HOP=0
NUM_FIRST_HOP=0
<<<<<<< HEAD

=======
MAX_ROUTE_LENGTH = 50000
GUARD_DISTANCE = 30000
BETA = 0.5

#KEY = 'AIzaSyBOynBGgDTlSNZCTO4_n9vvSrP9rk6zB4w'




>>>>>>> 0fdb1756875f015ed71d4c081089605f53ee20d7
# near_limit = 300
# rear_limit = 2000
########################################
def get_block_hq(dijkstralist,bhqsindx):
	bhq_to_nodes = []

	for bhqidxes in bhqsindx:
		#spt(dijkstralist,bhqidxes)
		bhq_to_nodes_dist = spt(dijkstralist,bhqidxes)
		print "total fibre in block",bhq_to_nodes_dist
		# sys.exit()
		bhq_to_nodes.append(bhq_to_nodes_dist)
		print "bhq_to_nodes",bhq_to_nodes.index(min(bhq_to_nodes))

	#print "Final bhq ",(bhq_to_nodes.index(min(bhq_to_nodes)))
	#return bhq[(bhq_to_nodes.index(min(bhq_to_nodes)))]		
	return (bhq_to_nodes.index(min(bhq_to_nodes)))



def do_something(input_file):

	dist_olts = 0
	if not os.path.exists('tower'):
		os.makedirs('tower')
	f1 = open('tower/tower_'+str(input_file)+'.csv','w')
	f1.write('GP Name,GP seq,GP lat,GP long,GP status,GP tower height' +  '\n')
	f1.close()
	f1 = open('tower/tower_'+str(input_file)+'.csv','a+')

	if not os.path.exists('stats.csv'): 
		f2 = open('stats.csv','w')
		f2.write('District Code,Phase 1, Phase 2,Rural Exchanges, Towers, Conn. to P1,Conn. to towers, Sat. recommendation, ONTs, OLTs,Problem Cases\n')
		f2.close()
		f2 = open('stats.csv','a+')
	else:    
		f2 = open('stats.csv','a+')
		next(f2,None)
		for row in f2:
			print (int(row.split(",")[0]),int(input_file))
			if (int(row.split(",")[0]) == int(input_file)):
				print ("district code already processed:",input_file)
				f2.close()
				#sys.exit()
				return

	if not os.path.exists('data_error.csv'): 
		f9 = open('data_error.csv','w')
		f9.write('District Code,GP Code, GP Name, GP Lat, GP_Lon,Status\n')
		f9.close()
	#else:    
	f9 = open('data_error.csv','a+')
	

	if not os.path.exists('fibre_all'):
		os.makedirs('fibre_all')
	f3=open('fibre_all/fibre_'+str(input_file)+'.csv','w')
	f3.write('Block Code,fibre length,max. link length,max. route length,No. of OLTs\n')
	f3.close()
	f3=open('fibre_all/fibre_'+str(input_file)+'.csv','a+')

	if not os.path.exists('sat'):
		os.makedirs('sat')
	f4=open('sat/sat_'+str(input_file)+'.csv','w')
	f4.write('Block Code,Sat. GP code, Sat. GP Name,Latitude, Longitude, population\n')
	f4.close()
	f4=open('sat/sat_'+str(input_file)+'.csv','a+')

	if not os.path.exists('fibre_all'):
		os.makedirs('fibre_all')
	f5=open('fibre_all/mst_'+str(input_file)+'.csv','w')
	f5.write('Block Code,FROM GP lat,FROM GP long,TO GP Lat , TO GP Long,link length(km)\n')
	f5.close()
	f5=open('fibre_all/mst_'+str(input_file)+'.csv','a+')


	if not os.path.exists('fibre'):
		os.makedirs('fibre')
	f6=open('fibre/fibre_'+str(input_file)+'.csv','w')
	f6.write('Block Code,fibre length, max. link length(km),max. route length,Length reduction,No. of OLTs\n')
	f6.close()
	f6=open('fibre/fibre_'+str(input_file)+'.csv','a+')

	f7=open('fibre/mst_link'+str(input_file)+'.csv','w')
	f7.write('Block Code,FROM GP lat,FROM GP long,TO GP Lat , TO GP Long,link length(km)\n')
	f7.close()
	f7=open('fibre/mst_link'+str(input_file)+'.csv','a+')


	f8=open('fibre_all/unconnected_'+str(input_file)+'.csv','w')
	f8.write('GP Code,GP Name, Block Code,GP lat,GP long,Population,Status\n')
	f8.close()
	f8=open('fibre_all/unconnected_'+str(input_file)+'.csv','a+')



	if not os.path.exists('olt_connect'):
		os.makedirs('olt_connect')
	


	if not os.path.exists('output'):
		os.makedirs('output')
	f = open('output/output_'+str(input_file)+'.csv','w')
	f.write('FROM GP Name,FROM GP seq, FROM Block_code, FROM GP lat,FROM GP long,FROM GP status,FROM GP tower height,LINK throughput,TO GP Name,TO GP seq, TO Block Code,TO GP lat,TO GP long,TO GP status,TO GP tower height' +  '\n')
	f.close()
	f = open('output/output_'+str(input_file)+'.csv' ,'a+')
	#####################################
	##thane_GP_data.csv gives the following informations
	# ['State_Code','District_Code','Block_Code','GP_Code', 'Latitude', 'Longitude','Phase','throughput']
	filename = read_csv_fields(str(input_file),['State Code','District_Code','Block_Code','GP Name','GP Code', 'Latitude', 'Longitude','Phase','population'])
	
	#####################################

	# # #create adjacency matrix
	# fname = make_adjacency(REF_DIST,filename,input_file) #############################
	# # ######################################

	
	all_data = np.load('adjmat/AD_mat_' +str(input_file)+ '_'+str(REF_DIST)+'.npy')


	States_list = all_data[1]     #Sate names ???It is giving district code
	GP_lists = all_data[2]        #GP codes
	GP_Names = all_data[9]
	Phase_lists = all_data[3]     #Phase of Bharatnet project
	DistMats = all_data[4]        #distance matrix for each district
	District_code = all_data[5]   #unique code for all districts
	Block_code = all_data[8]
	LatLong = all_data[6]         #lat and long of GPs
	reqTP_mat = all_data[7][0]    #throughput required for each GP It is a list

	Block_code=Block_code[0]
	state = np.unique(States_list[0])
	# print "Districts ",District_code[0]
	dist = np.unique(District_code[0])
	state=str(int(state[0]))
	dist= str(int(dist[0]))
	#####################################

	# ffname = make_feas(REF_DIST,htListT,htListR,state,dist,input_file) ######################################

	feas = np.load('feasmat/Feas_mat_'+str(input_file)+'_'+str(REF_DIST)+'.npy')
	feasibility_mat_raw = feas[0]
	throughPut_mat = feas[1]
	transHeight_mat = feas[2]
	receivHeight_mat = feas[3]
	adjMats = [feas[4]] ##this feasibility is according to throughput


	NODE, NODE = np.shape(adjMats[0])
	#print NODE
	

	########################################################
	tower_height = [0 for k in range(NODE)]
	availableTP_mat = [0 for i in range(NODE)]

	########################################################


	#print Phase_lists[0]
	blocks = []
	blocks=np.unique(Block_code)
	#print "blocksssss",blocks

	#......................................................................
	##In this adjacency matrix first remove "TO" connections to phase-1 GPs
	##then remove any interconnection between phase-1 GPs
	#......................................................................

	alc=0
	for j in range(NODE):                                                                     ##for each node in that district

		if(Phase_lists[0][j] == 9 or Phase_lists[0][j] == 8 or Phase_lists[0][j] == 21 or Phase_lists[0][j] == 15):       ##if some node belongs to tower                    
			alc+=1
			adjMats[0][:,j] = 0                                                               ##cut all the incoming connections for that
			
			for k in range(NODE):                                                             ##for that node
				
				if(adjMats[0][j][k] == 1):                                                    ##if there is any adjacent nodes
					
					if(Phase_lists[0][k] == 9 or Phase_lists[0][k] == 8 or Phase_lists[0][k] == 21 or Phase_lists[0][k] == 15):   ##if it belongs to tower

						adjMats[0][j][k] = 0                                                  ## cut outgoing connection which go to that node
	#print "Phasssesssss2=---\n",len(Phase_lists[0])
	#print "Phasssesssss2=---\n",Phase_lists
###Give satellite suggestion for GPs which do not have any incoming or outgoing feasible connections
	# satr=0
 #    for j in range(NODE):
 #    	if(Phase_lists[0][j] == 2):
 #    		if(sum(adjMats[0][j,:])<=1 and sum(adjMats[0][:,j])<=1):
 #    		# if(sum(adjMats[0][j,:])<=1):
 #    			m=min(i for i in DistMats[0][:,j] if i>0)
 #    			# print "minimum",m
 #    			if(m>2000):
	#     			x=np.where(adjMats[0][j,:]==1)
	#     			f4.write(str(Block_code[j])+','+str(GP_lists[0][j])+','+str(GP_Names[0][j])+ ',' +str(LatLong[j][0]) + ',' +str(LatLong[j][1])+','+str(reqTP_mat[j])+'\n')
	#     			satr+=1 
				# print "outgoing connections from ",GP_lists[0][j], "are ",sum(adjMats[0][j,:]),"to",  GP_lists[0][x[0]],"TP",reqTP_mat[j]

	###Connet unconnected GP to nearest tower or connected GP
	


	def connect(gp,status,blk_code):
		for m in range(NODE):  
		   ##for all nodes
			if (Phase_lists[0][m] == status):    ##check for phase 1 or towers    
				# degree3 = [0 for i in range(NODE)]
				# dist3 = [upper_limit for i in range(NODE)]                           
				if adjMats[0][m][gp] == 1:                       ##If any other node is adjacent to child of Status 3 node
					#print "phase ",Phase_lists[0][m]
					Phase_lists[0][gp] = status+1            ##GP is connected wirelessly from tower 

					#print "connected ",GP_Names[0][m], "to", GP_Names[0][gp]
					#print "connect with wireless",LatLong[m],LatLong[gp], reqTP_mat[gp],m,gp, Phase_lists[0][gp]
					#print "Transmission height", transHeight_mat[m][gp]
					f.write(str(GP_Names[0][m]) + ',' +str(GP_lists[0][m]) + ','+str(Block_code[m])+',' +str(LatLong[m][0]) + ',' +str(LatLong[m][1]) + ',' +str(Phase_lists[0][m]) + ',' + str(transHeight_mat[m][gp])+','+str(throughPut_mat[m][gp]) +','+str(GP_Names[0][gp]) + ',' +str(GP_lists[0][gp]) + ',' +str(blk_code)+','+str(LatLong[gp][0]) + ',' +str(LatLong[gp][1]) + ',' +str(Phase_lists[0][gp]) + ','+ str(receivHeight_mat[m][gp]) +',' +'\n' )
					# f.write(str(GP_Names[0][gp])+ ',' +str(GP_lists[0][m]) + ',' +str(LatLong[m][0]) + ',' +str(LatLong[m][1]) + ',' +str(Phase_lists[0][m]) + ',' + str(transHeight_mat[m][index3])+','+str(throughPut_mat[m][index3]) +','+str(GP_Names[0][index3]) + ',' +str(GP_lists[0][index3]) + ',' +str(LatLong[index3][0]) + ',' +str(LatLong[index3][1]) + ',' +str(Phase_lists[0][index3]) + ','+ str(receivHeight_mat[m][index3]) +',' +'\n' )
					if tower_height[m] < transHeight_mat[m][gp]:
						tower_height[m] = transHeight_mat[m][gp]

					if tower_height[gp] < receivHeight_mat[m][gp]:
						tower_height[gp] = receivHeight_mat[m][gp]

					adjMats[0][:,gp] = 0                  ##cut all the incoming connections
					return 1
			
		return 0    

	def connectwls(Tcsr,j):
		conncts=0
		#print "j = = = = ==== =",j
		for l in range(len(Tcsr)):
			if(Tcsr[:,l].sum()==0 and np.count_nonzero(Tcsr[l])==1 and l!=bhq): #prasanna
				val=[value for key,value in blkx_distx.items() if key ==l][0]
				#print "leaf node =",[l]
				#print Tcsr[l,:].sum()
				if(float(reqTP_mat[val]) <= 6250.0):
					conn=connect(val,9,j)
					if(conn ==1):
						block_phase[j][l] = 10
						Tcsr[l,:]=0
						conncts+=1
					else:
						conn=connect(val,21,j)#what 
						if(conn ==1):
							block_phase[j][l] = 22
							Tcsr[l,:]=0
							conncts+=1
			elif(Tcsr[l,:].sum()==0 and np.count_nonzero(Tcsr[:,l])==1 and l!=bhq):
				val=[value for key,value in blkx_distx.items() if key ==l][0]
				#print "leaf node =",[l]
				#print Tcsr[:,l].sum()
				if(float(reqTP_mat[val]) <= 6250.0):
					conn=connect(val,9,j)
					if(conn ==1):
						block_phase[j][l] = 10
						Tcsr[:,l]=0
						conncts+=1
					else:
						conn=connect(val,21,j)#what 
						if(conn ==1):
							block_phase[j][l] = 22
							Tcsr[:,l]=0
							conncts+=1
			elif(Tcsr[:,l].sum() == 0.0001 and l!=bhq):
				val=[value for key,value in blkx_distx.items() if key ==l][0]
				#print "Isolated node =",[l]
				#print Tcsr[:,l].sum()
				Tcsr[:,l]=0
				#if(float(reqTP_mat[val]) <= 6250.0):
				conn=connect(val,9,j)
				if(conn ==1):
					block_phase[j][l] = 10
					#Tcsr[:,l]=0
					conncts+=1
				else:
					conn=connect(val,21,j)#what 
					if(conn ==1):
						block_phase[j][l] = 22
						#Tcsr[:,l]=0
						conncts+=1
		return conncts

	ctt = 0

	block_idx=[]
	block_phase={}
	for j in blocks:
		blocks1={}
		for i in range(NODE):
			if int(Block_code[i])==j:
				blocks1.update({i:int(Phase_lists[0][i])}) #i is id as per district rows
		block_phase.update({j:blocks1})
		# block_idx.append(blocks1)
		blocks1=[]
	#print "blocks_phase",block_phase
	# print "block_adj = ",block_idx
	#print "length of block_adj = ",len(block_idx)
	#print "Block_IDX =    ",block_idx[2]

	##DistMats is distance matrix for all towers and GP's of the district
	DistMats=DistMats[0]
	# print "DistMats", DistMats
	##We create a distance matrix for fibre GP's & Block HQ of each block
	# block_dist_mat =[0 for k in range(len(blocks))]
	block_dist_mat={}
	block_adj_mat={}
	Block_MST=[]
	road_dr_array=[]
	LatLong_fibre=[0 for k in range(len(blocks))]
	#latlong_dict_array= {}

	##cut block distance matrix for fibre GPP's from distance matrix for whole district
	# for j in range(len(blocks)):
	for j in blocks: 
		# block_dist_mat[j]=DistMats[:,block_phase[j].keys()][block_phase[j].keys(),:]
		print "Processing block ============",j
		f10 = open('olt_connect/olt_connections_'+str(int(j))+'.csv','w')
		f10.write('Block Code,OLT Code,OLT Name,OLT Lat,OLT Lon,GP Name,GP Code,GP Lat,GP Lon,Route Length(km)\n')
		f10.close()
		f10 = open('olt_connect/olt_connections_'+str(int(j))+'.csv','a+')

		if not os.path.exists('waypoints'):
			os.makedirs('waypoints')
		
		if not os.path.exists('waypoints/waypoints_'+str(int(j))+'.csv'):
			fw=open('waypoints/waypoints_'+str(int(j))+'.csv','w')
			fw.write('Waypoint Code,Waypoint lat,Waypoint long\n')
			fw.close()
		fw=open('waypoints/waypoints_'+str(int(j))+'.csv','a+')

		
		# c1 = [28.032343,78.285034]
		# c2 = [28.081664, 78.324]

		# get_waypoints(c1,c2,state,dist,j,KEY)
		# sys.exit()


		bhq=[]
		status2 = []
		brk=0
		#print block_phase[j].items()
		for key,value in block_phase[j].items():
			if (value == 21):
				brk=1
				continue
			elif(value == 2 or value == 15):
				status2.append(key) #key = district wise id for GP
		if(brk):
			continue
		##Extract distance and adjacency matrix for that block GP's
		# block_dist_mat.update({j:DistMats[:,status2][status2,:]})
		blkx_distx={}
		#####Block index to district index mapping
		for k in range(len(status2)):
			blkx_distx.update({k:status2[k]})

		bhqs=([x for x,y in block_phase[j].items() if int(y) ==15])
		bhqsindx=[]
		for indx in bhqs:
			bhqsindx.append([x for x,y in blkx_distx.items() if int(y) ==indx][0])
		print "bhqsindx",bhqsindx,bhqs

		bhq = bhqsindx[0]
		print "UP bhq------------",bhq,status2[bhq],LatLong[status2[bhq]],LatLong[status2[bhq]],str(GP_Names[0][status2[bhq]]),str(GP_lists[0][status2[bhq]])
		
		
		print "Number of GPs::::",len(status2)
		road_d=[]
		latlng_in_file_dict = build_latlng_dict(state,dist,j)
		for l in range(len(status2)):
			road_dr=[]
			for m in range(len(status2)):
				if(l>=m):
					road_dr.append(0.0)
				else:
					sum_latlng = LatLong[status2[l]][0] + LatLong[status2[l]][1] + LatLong[status2[m]][0] + LatLong[status2[m]][1]
					try:
						x = latlng_in_file_dict[sum_latlng]
						wp_list = x[0]
						dis = x[1]
						#print "FOUND WAYPOINTS FROM THE DICT!!!!!!!!!!!!!!!!!!!!!!!!"
					except KeyError:
						try:
							wp_list,dis=get_waypoints(LatLong[status2[l]],LatLong[status2[m]],state,dist,j)
						except IOError, e:
							if e.errno == 101 or e.errno == 'socket error' or e.errno == -3 or e.errno == 2:
								print "Network Error"
								time.sleep(1)
								wp_list,dis=get_waypoints(LatLong[status2[l]],LatLong[status2[m]],state,dist,j)
							else:
								raise
						latlng_in_file_dict.update({sum_latlng:[wp_list,dis]})    
						
					if dis == 0.1: #same coordinates 
						print "Possible???", l,m,LatLong[status2[l]],LatLong[status2[m]],str(GP_Names[0][status2[m]]),str(GP_lists[0][status2[m]])
						f9.write(str(dist)+","+str(GP_lists[0][status2[m]])+","+str(GP_Names[0][status2[m]])+","+str(LatLong[status2[m]][0])+","+str(LatLong[status2[m]][1])+",Duplicate LatLong\n")
						f9.write(str(dist)+","+str(GP_lists[0][status2[l]])+","+str(GP_Names[0][status2[l]])+","+str(LatLong[status2[l]][0])+","+str(LatLong[status2[l]][1])+",Duplicate LatLong\n")
					road_dr.append(dis)
					#print "Getting inter GP distances: Processing out of ",	LatLong[status2[l]],LatLong[status2[m]],dis
					
			#sys.exit()
			road_d.append(road_dr) 
			#road_d is a list of list road_d[x][y] = road distance between gp's x and y if x < y and 0 otherwise

			#sys.exit()

		###############################
		# Get Waypoints for the block #
		###############################

		road_d_min = {}
		processed_nodes = [bhq]
		block_waypoints_list = list() #list of block waypoints  
		for l in range(len(status2)): #Initialization Loop
			if l > bhq:
				road_d_min.update({str(l)+','+','.join([str(x) for x in LatLong[status2[bhq]]]) : road_d[bhq][l]})
			elif l < bhq:
				road_d_min.update({str(l)+','+','.join([str(x) for x in LatLong[status2[bhq]]]) : road_d[l][bhq]})

		while len(road_d_min) > 0:
			print "Number of GP's still to be processed::",len(road_d_min)
			min_curr_road_d = 10000000000000
			for x,y in road_d_min.items(): #Find GP with the min distance from the set of points chosen already
				if y < min_curr_road_d:
					min_curr_road_d = y
					min_curr_road_d_key = x
			print "ROAD D MIN::::",min_curr_road_d_key,road_d_min[min_curr_road_d_key]
			del road_d_min[min_curr_road_d_key]

			if min_curr_road_d >= 1000000: #If road data not found then nothing can be done. Sorry!!
				continue

			x_list = min_curr_road_d_key.split(',')
			x_latlong = [float(x_list[1]),float(x_list[2])] #latlong of waypoint with the curr min distance

			sum_latlng = x_latlong[0] + x_latlong[1] + LatLong[status2[int(x_list[0])]][0] + LatLong[status2[int(x_list[0])]][1]
			try:
				x = latlng_in_file_dict[sum_latlng]
				waypoints_list = x[0]
				d = x[1]
			except KeyError:
				try:
					waypoints_list,d=get_waypoints(x_latlong,LatLong[status2[int(x_list[0])]],state,dist,j)
				except IOError, e:
					if e.errno == 101 or e.errno == 'socket error' or e.errno == -3 or e.errno == 2:
						print "Network Error"
						time.sleep(1)
						waypoints_list,d=get_waypoints(x_latlong,LatLong[status2[int(x_list[0])]],state,dist,j)
					else:
						raise
				latlng_in_file_dict.update({sum_latlng:[waypoints_list,d]})    
			

			print "Waypoints List:::",waypoints_list
			
			for w in waypoints_list:
				print "Check1:::",w
				if LatLong[status2[int(x_list[0])]] == w:
					continue
				else:
					if w not in block_waypoints_list:
						block_waypoints_list.append(w)
			
			for x,y in road_d_min.items():
				rd_min = y
				gp_latlong = LatLong[status2[int(x.split(',')[0])]] # Waypoint order does not matter


				
				for l in waypoints_list:

					sum_latlng = gp_latlong[0] + gp_latlong[1] + l[0] + l[1]
					try:
						z = latlng_in_file_dict[sum_latlng]
						wp_temp = z[0]
						rd = z[1]
					except KeyError:
						try:
							wp_temp,rd=get_waypoints(gp_latlong,l,state,dist,j)
						except IOError, e:
							if e.errno == 101 or e.errno == 'socket error' or e.errno == -3 or e.errno == 2:
								print "Network Error"
								time.sleep(1)
								wp_temp,rd=get_waypoints(gp_latlong,l,state,dist,j)
							else:
								raise
						latlng_in_file_dict.update({sum_latlng:[wp_temp,rd]})    
					
					#rd = road_dist_block(gp_latlong,l,state,dist,j,KEY)
					if rd < rd_min:
						rd_min = rd
						rd_min_latlong = l
	
				if rd_min < y:
					del road_d_min[x]
					road_d_min.update({x.split(',')[0]+','+','.join([str(u) for u in rd_min_latlong]):rd_min})
			
		############################################
		# Finished Getting Waypoints for the block #
		############################################

		print "All waypoints in the block",block_waypoints_list
		#sys.exit()

		##################################
		# Start Making the Spanning Tree #
		##################################

		## Make the underlyting graph with gps and wps ##
		# original_graph = dict()
		# #key = node and value = [ [node,road_dist] ]
		# #Creating nodes in the graph
		# for l in range(len(status2)):
		# 	original_graph.update({'gp,'+str(l):[]})
		# for l in range(len(block_waypoints_list)):
		# 	original_graph.update({'wp,'+str(l):[]})

		# for l in range(len(status2)):
		# 	l_key = 'gp,'+str(l)
			
		# 	for m in range(l+1,len(status2)):
		# 		m_key = 'gp,'+str(m)
		# 		#d_chk = road_dist_block_file(LatLong[status2[l]],LatLong[status2[m]],state,dist,j)
		# 		d_chk = road_dist_block(LatLong[status2[l]],LatLong[status2[m]],state,dist,j)
		# 		if d_chk > 0:
		# 			original_graph[l_key].append([m_key,d_chk])
		# 			original_graph[m_key].append([l_key,d_chk])
		# 	print "Done making gp to gp adjacency for",GP_Names[0][status2[l]]
			
		# 	for m in range(len(block_waypoints_list)):
		# 		m_key = 'wp,'+str(m)
		# 		d_chk = road_dist_block_file(LatLong[status2[l]],block_waypoints_list[m],state,dist,j)
		# 		if d_chk > 0:
		# 			original_graph[l_key].append([m_key,d_chk])
		# 			original_graph[m_key].append([l_key,d_chk])
		# 	print "Done making gp to wp adjacency!!!",GP_Names[0][status2[l]]

		# for l in range(len(block_waypoints_list)):
		# 	l_key = 'wp,'+str(l)
			
		# 	for m in range(l+1,len(block_waypoints_list)):
		# 		m_key = 'wp,'+str(m)
		# 		d_chk = road_dist_block_file(block_waypoints_list[l],block_waypoints_list[m],state,dist,j)
		# 		if d_chk > 0:
		# 			original_graph[l_key].append([m_key,d_chk])
		# 			original_graph[m_key].append([l_key,d_chk])	
		# print "Done making wp to wp adjacency!!!"		

		# print "original graph ------",len(original_graph)		

		# no_neighbor_nodes = []
		# for x,y in original_graph.items():
		# 	if y == []:
		# 		print "Node is not connected to anything::::", x
		# 		no_neighbor_nodes.append(x)

		# #sys.exit()

		
		# ## Building the Tree from the graph ##	

		# tree_with_wps = dict()
		# # key = node and value = parent id, link lenght, [children], route length from bhq
		# #node_status = dict() #whether nodes are in or out of the current tree
		
		# for x in original_graph.keys():
		# 	init_tree_value_list = [None,0,[],0]
		# 	if x == 'gp,'+str(bhq):
		# 		y = 'in'
		# 	else:
		# 		y = 'out'
		# 	init_tree_value_list.append(y)
		# 	tree_with_wps.update({x:init_tree_value_list})

		# # print "Tree with wps:::", tree_with_wps

		# last_added = 'gp,'+str(bhq)
		# not_yet_connected = [x for x in tree_with_wps.keys() if tree_with_wps[x][4] == 'out']

		# # print "Not yet connected 1:::",not_yet_connected

		# #while (len(not_yet_connected) > 0):
		# while (len(not_yet_connected) > len(no_neighbor_nodes) ):
		# 	#last_added_adj_list = original_graph[last_added]
		# 	for x in original_graph[last_added]: 
		# 		#print "Last added x==== ",x #original_graph[last_added]

		# 		x_id = x[0]
		# 		x_dist_from_last_added = x[1]

		# 		#if tree_with_wps[x_id][4] == 'in':
		# 		if x_id not in not_yet_connected:
		# 			continue
		# 		else:
		# 			if tree_with_wps[x_id][0] == None:
		# 				tree_with_wps[x_id][0] = last_added
		# 				tree_with_wps[x_id][1] = x[1]
		# 				tree_with_wps[x_id][3] = tree_with_wps[last_added][3] + x[1]
		# 			else:
		# 				if tree_with_wps[x_id][1] > x[1]:
		# 					tree_with_wps[x_id][1] = x[1]
		# 					tree_with_wps[x_id][0] = last_added
		# 					tree_with_wps[x_id][3] = tree_with_wps[last_added][3] + x[1]

		# 	min_length = 10000000000000000
		# 	for x in [y for y in not_yet_connected if tree_with_wps[y][0] != None]:
		# 		if tree_with_wps[x][1] < min_length:
		# 			min_length = tree_with_wps[x][1]
		# 			min_length_id = x

		# 	tree_with_wps[min_length_id][4] = 'in'
		# 	tree_with_wps[tree_with_wps[min_length_id][0]][2].append(min_length_id)

		# 	last_added = min_length_id
		# 	not_yet_connected = [x for x in tree_with_wps.keys() if tree_with_wps[x][4] == 'out']

		# print "Not yet connected:::",len(not_yet_connected),not_yet_connected,no_neighbor_nodes

		# tree_with_wps,sattelite_reco_list = handle_no_road_cases(tree_with_wps,LatLong,block_waypoints_list,status2,state,dist) 
		# #Handles no road data cases
		# tree_with_wps = prun_leaf_wps(tree_with_wps) #Removes leaf wp's

		# print "Satellite Recommendations:::",sattelite_reco_list


		# mst_link_list = list()
		# #mst_link_dict = print_mst_links('gp,'+str(bhq),tree_with_wps,mst_link_dict)

		# tot_mst_links = 0
		# for x in tree_with_wps.keys():
		# 	if tree_with_wps[x][2] != []:
		# 		tot_mst_links += len(tree_with_wps[x][2])
		# 		for y in tree_with_wps[x][2]:
		# 			mst_link_list.append([x,y])
		

		# print "mst_link_list::::::",len(mst_link_list),tot_mst_links,mst_link_list

		# ## Print MST links in the file ##
		# # ff = open('mst_links.csv','w')
		# # ff.write('Block code,From GP Name,From GP Lat,From GP Long,To GP Name,To GP Lat,To GP Long,Link Length(km)\n')
		# # ff.write()
		# for x in mst_link_list:
		# 	x_from = x[0].split(',')[0]
		# 	x_to = x[1].split(',')[0]
		# 	gp_from_name = ' '
		# 	gp_to_name = ' ' 
			
		# 	if x_from == 'wp':
		# 		from_latlong =  block_waypoints_list[int(x[0].split(',')[1])]
			
		# 	elif x_from == 'gp':
		# 		from_latlong = LatLong[status2[(int(x[0].split(',')[1]))]]
		# 		gp_from_name = GP_Names[0][status2[(int(x[0].split(',')[1]))]]
			
		# 	if x_to == 'wp':
		# 		to_latlong =  block_waypoints_list[int(x[1].split(',')[1])]
			
		# 	elif x_to == 'gp':
		# 		#print "Debug gp name printing problem:::",x
		# 		to_latlong = LatLong[status2[int(x[1].split(',')[1])]]
		# 		gp_to_name = GP_Names[0][status2[(int(x[1].split(',')[1]))]]

		# 	#print str(j),gp_from_name,str(from_latlong[0]),str(from_latlong[1]),gp_to_name,str(to_latlong[0]),str(to_latlong[1]),tree_with_wps[x[1]][1]
	
				
		# 	f5.write(str(j)+ ", " + gp_from_name +',' + str(from_latlong[0]) + ", "+ str(from_latlong[1]) + "," + gp_to_name + ',' + str(to_latlong[0]) + "," +str(to_latlong[1]) +',' + str(float(tree_with_wps[x[1]][1]/1000.0)) + '\n' )

# 		sys.exit()
# 		#list_of_connected_nodes = set( mst_link_dict.keys() + mst_link_dict.values() )
		 
# 		# list_of_connected_nodes.append(mst_link_dict.values())
# 		#print list_of_connected_nodes,len(list_of_connected_nodes)

# 		# for x in original_graph.keys():
# 		# 	if x not in list_of_connected_nodes:
# 		# 		# print "not in tree", x
# 		# 		print "details of node not in tree ", tree_with_wps[x],"parent details -------", tree_with_wps[tree_with_wps[x][0]]
# 		# unique_nodes = set(list_of_connected_nodes)

# 		# print unique_nodes,len(unique_nodes)

		
# 		# print "latlong_dict_array",latlong_dict_array  
# 		#road_dr_array=np.array(road_d)
# 		#road_dr_array=np.reshape(road_dr_array,(len(status2),len(status2)))
# 		#print "length of road_dr_array------",len(road_dr_array)
# 		#X=csr_matrix(road_dr_array)

# 		#Tcsr1= minimum_spanning_tree(X)
# 		#print "mst===========",Tcsr1
# 		#Tcsr=Tcsr1.toarray().astype(float)
		
# 		#################
# 		# Building Tcsr #
# 		#################
# 		#print "Treeeeeee dicttttt",tree_dict

# 		#Tcsr = list()


# 		# print "TREEE  ",tree_with_wps
# 		# sys.exit()	
# 		u = 0

# 		Tcsr = list()
# 		for x in range(len(status2)):
# 			Tcsr.append([])
# 			for y in range(len(status2)):
# 				Tcsr[x].append(0)

# 		Tcsr = build_Tcsr('gp,'+str(bhq),tree_with_wps,Tcsr,'gp,'+str(bhq))
# 		Tcsr = np.array(Tcsr)
# 		for x in range(len(status2)):
# 			for y in range(len(status2)):
# 				if Tcsr[x][y] > 0 :
# 					u += 1
# 					print "Printing Tcsr === ",LatLong[status2[x]],LatLong[status2[y]],Tcsr[x][y]


# 		Orig_Tcsr=deepcopy(Tcsr)


# 		#print Tcsr
# 		print "Correct Tcsr?",u, len(status2)

# 		sys.exit()


# 		if not os.path.exists('fibre_all/mstnpy'):
# 			os.makedirs('fibre_all/mstnpy')
# 		np.save('./fibre_all/mstnpy/mst_'+str(input_file),np.array(Tcsr))



# 		#print "TCSR = ", Tcsr
# 		dijkstralist=list()
# 		count = 0
# 		#print status2, len(status2),range(len(status2))
# 		for l in range(len(status2)):
# 			for m in range(len(status2)):
# 				if Tcsr[l][m] > 0:
# 					count +=1
# 					smalllist=list()
# 					smalllistrev=list()
# 					smalllist.append(l)
# 					smalllist.append(m)
# 					smalllist.append(Tcsr[l][m])
# 					smalllistrev.append(m)
# 					smalllistrev.append(l)
# 					smalllistrev.append(Tcsr[l][m])
# 					dijkstralist.append(smalllist)
# 					dijkstralist.append(smalllistrev)
# 		print "count ======",count
# 		#bhq=get_block_hq(dijkstralist,bhqsindx)
# 		tree_dist=list()
# 		over_sixty=list()
# 		print "Entering SPT ##############",len(bhqsindx),bhqsindx
# 		for l in range(len(bhqsindx)):
# 			tree_dist_temp,over_sixty_temp = spt(dijkstralist,str(bhqsindx[l]),1)
# 			tree_dist.append(tree_dist_temp)
# 			over_sixty.append(over_sixty_temp)
# 			print tree_dist[l], len(tree_dist[l]), len(status2), over_sixty[l]
# 		# bhq = bhqsindx[0]
# 		# print "UP bhq------------",bhq,status2[bhq],LatLong[status2[bhq]],LatLong[status2[bhq]],str(GP_Names[0][status2[bhq]]),str(GP_lists[0][status2[bhq]])
# 		# #bhq = bhqsindx[over_sixty.index(min(over_sixty))] # selecting bhq based on minimum oversixty route-lengths
# 		all_olts = [bhq]
# 		#check tree distance from bhq > 1000000 call satellite 
# 		print "BHQ (finally!) ===== ",bhq,over_sixty.index(min(over_sixty))
# 		#sys.exit()

# 		# no_road_data_list = [x for x in range(len(tree_dist[0])) if (tree_dist[0][x] > 1000000) and (Phase_lists[0][status2[x]] == 2)]

# 		# new_association = satellite_recommendation(no_road_data_list) #getting dict with key i (in no_road_data) and value k,dist(i,k)*1.2
		
# 		# for i in new_association.keys():
# 		# 	k = int(new_association[i][0])
# 		# 	if i < k:
# 		# 		Tcsr[i][k] = new_association[i][1]
# 		# 	else:
# 		# 		Tcsr[k][i] = new_association[i][1]

# 		# 	for l in range(len(bhqsindx)):
# 		# 		if tree_dist[l][i] < 1000000:
# 		# 			print "====ERROR in tree_dist update===",j,l,i,tree_dist[l][i]
# 		# 			sys.exit()
					
# 		# 		tree_dist[l][i] = tree_dist[l][k] + new_association[i][1]
		
# 		no_road_data_list = [x for x in range(len(tree_dist[0])) if (tree_dist[0][x] > 1000000) and (Phase_lists[0][status2[x]] == 2)]

# 		# Prasanna



# 		print "No road data list::", no_road_data_list
# 		if no_road_data_list != []:
# 			new_association = satellite_recommendation(no_road_data_list) #getting dict with key i (in no_road_data) and value k,dist(i,k)*1.2
# 			print "Print New Association::", new_association
# 			print "New association Keys!!",new_association.keys()
# 			#sys.exit()
			
		
# 			for i in new_association.keys():
# 				k = int(new_association[i][0])
# 				Tcsr[i,:] = 0
# 				Tcsr[:,i] = 0
# 				print "New association:::",i,new_association[i],k
# 				if float(new_association[i][1]) == 0:
# 					print "Error:: Zero arial distance!!!!!!"
# 					sys.exit()
# 				if int(i) < int(k):
# 					Tcsr[i][k] = float(new_association[i][1])
# 				elif int(k) < int(i):
# 					Tcsr[k][i] = float(new_association[i][1])
# 				else: #eRROR HANDLING
# 					print "Error::i cannot be same as k!!!", i,k
# 					sys.exit()

# 				#print "New TCSR:::",Tcsr
# 				# sys.exit()

# 				for l in range(len(bhqsindx)):
# 					if tree_dist[l][i] < 1000000: #Error Handling
# 						print "====ERROR in tree_dist update===",j,l,i,tree_dist[l][i]
# 						sys.exit()
						
# 					tree_dist[l][i] = tree_dist[l][k] + new_association[i][1]


# 		print tree_dist[0], len(tree_dist[0])
# 		#min_route_length = [None]*len(tree_dist[0])
# 		min_route_length = [10000000000 for x in range(len(tree_dist[0]))]
# 		olt_assigned = [bhq for x in range(len(tree_dist[0]))] #initial bhq assigned for those GPs which are 
# 		problem_cases = [x for x in range(len(tree_dist[0])) if (tree_dist[bhqsindx.index(bhq)][x] > MAX_ROUTE_LENGTH and tree_dist[bhqsindx.index(bhq)][x] < 1000000)]
# 		sys.exit()

# 		#for l in range(len(tree_dist[0])):
# 			# for i in range(len(bhqsindx)):
# 			#     min_route_length[l] = min([tree_dist[i][l],min_route_length[l]])
# 		while True:
# 			res_cases = []
# 			max_res = -1
# 			max_res_index = 0  
# 			print "Problem Cases",problem_cases
			  
# 			for i in range(len(bhqsindx)):
# 				res_cases.append([x for x in problem_cases if tree_dist[i][x]< MAX_ROUTE_LENGTH])
# 				print res_cases[i]

# 					#if tree_dist[i][l] > MAX_ROUTE_LENGTH and min_route_length[l] < 1000000:
# 					# if (int(l) == 124):
# 					#     print "Road Distance", road_dist(LatLong[status2[l]],LatLong[status2[bhqsindx[i]]],state,dist
# 				# if min_route_length[l] > MAX_ROUTE_LENGTH and min_route_length[l] < 1000000:
# 				#     print "Can not be less than 60",l,LatLong[status2[l]],LatLong[status2[bhqsindx[i]]]
# 				#     #problem_cases.append(l)
			
# 				if len(res_cases[i]) > max_res:
# 					max_res_index = i
# 					max_res = len(res_cases[i])

# 			if res_cases[max_res_index] == []:
# 				break
# 			else:
# 				problem_cases = [x for x in problem_cases if x not in res_cases[max_res_index]]
# 				all_olts.append(bhqsindx[max_res_index])

# 		print "Final OLT List -----------",all_olts 
# 		for l in problem_cases:
# 			print "Putting problem case in file ---->",l
# 			f9.write(str(dist)+","+str(GP_lists[0][status2[l]])+","+str(GP_Names[0][status2[l]])+","+str(LatLong[status2[l]][0])+","+str(LatLong[status2[l]][1])+",Suspect LatLong\n")
# 			# res_cases.index(max([len(x) for x in res_cases])) 
# 		olt_connect = dict() 
# 		for olt in all_olts:
# 			olt_connect.update({olt:[]})

# 		for l in range(len(tree_dist[0])):
# 			min_olt = 0
# 			min_tree_dist = 100000000000000
# 			#if (l not in problem_cases) or (tree_dist[bhqsindx.index(bhq)][l] >= 1000000): 
# 			if (l not in problem_cases) and (tree_dist[bhqsindx.index(bhq)][l] < 1000000): #All OLTs with distance less than 40Km
# 				for olt in all_olts:
# 					olt_index = bhqsindx.index(olt)
# 					if (tree_dist[olt_index][l] < min_tree_dist):
# 						min_tree_dist = tree_dist[olt_index][l]
# 						min_olt = olt
# 				olt_connect[min_olt].append(l)
# 				min_route_length[l] = min_tree_dist
# 				f10.write(str(j)+","+str(GP_lists[0][status2[min_olt]])+','+str(GP_Names[0][status2[min_olt]])+","+str(LatLong[status2[min_olt]][0])+","+str(LatLong[status2[min_olt]][1])+','+str(GP_lists[0][status2[l]])+","+str(GP_Names[0][status2[l]])+","+str(LatLong[status2[l]][0])+","+str(LatLong[status2[l]][1])+','+str(min_tree_dist/1000)+'\n')
# 		print "OLT Connect======", olt_connect



# 		#exit()        

# 		# for i in range(len(tree_dist)):
# 		#     ucount = 0
# 		#     if i == over_sixty.index(min(over_sixty)):
# 		#         continue
# 		#     else:    
# 		#         for l in range(len(tree_dist[0])):
# 		#             min_route_length[l] = min([])
# 		#             print "Vinoo I came here!!!"
# 		#             if tree_dist[0][l] > MAX_ROUTE_LENGTH and tree_dist[i][l] < MAX_ROUTE_LENGTH:
# 		#                 ucount += 1
# 		#                 print l ,tree_dist[0][l],tree_dist[2][l]
# 		#     print "counting difference in nodes ------------",i,ucount        
# 		# # sys.exit()
# 		#print "bhq ===================================================",bhqsindx[bhq],blkx_distx[bhqsindx[bhq]]
# 		# ,str(GP_lists[0][blkx_distx[bhqsindx[bhq]]])
# 		# ,str(GP_Names[0][blkx_distx[bhqsindx[bhq]]]),str(LatLong[blkx_distx[bhqsindx[bhq]]][0]),str(LatLong[blkx_distx[bhqsindx[bhq]]][1])
# 		#exit()

# 		for l in range(len(status2)):#unconnected because route length > 1000km or unable to connect from any OLT
# 			if (tree_dist[bhqsindx.index(bhq)][l] >= 1000000):
# 				f8.write(str(GP_Names[0][status2[l]])+','+str(GP_lists[0][status2[l]])+','+str(j)+','+str(LatLong[status2[l]][0])+','+str(LatLong[status2[l]][1])+','+str(reqTP_mat[status2[l]])+',Road data not found\n')
# 				Tcsr[l,:] = 0
# 				Tcsr[:,l] = 0
# 				Tcsr[int(bhq),l] = 0.0001 #Required in wireless connectivity function
# 				continue
# 			elif (l in problem_cases):
# 				f8.write(str(GP_Names[0][status2[l]])+','+str(GP_lists[0][status2[l]])+','+str(j)+','+str(LatLong[status2[l]][0])+','+str(LatLong[status2[l]][1])+','+str(reqTP_mat[status2[l]])+',Too far from block HQ\n')
# 				Tcsr[l,:] = 0
# 				Tcsr[:,l] = 0
# 				Tcsr[int(bhq),l] = 0.0001 #Required in wireless connectivity function
# 				continue

# 			for m in range(len(status2)):
# 				if Tcsr[l][m] > 0:
# 					if min_route_length[l] < 1000000 and min_route_length[m] < 1000000:
# 						for i in all_olts:
# 							if (l in olt_connect[i]) and (m in olt_connect[i]):
# 								#f5.write(str(j)+','+str(latlong_dict_array[j][l][0])+','+str(latlong_dict_array[j][l][1])+','+str(latlong_dict_array[j][m][0])+','+str(latlong_dict_array[j][m][1])+','+str(Tcsr[l][m]/1000)+'\n'),
# 								f5.write(str(j)+','+str(LatLong[status2[l]][0])+','+str(LatLong[status2[l]][1])+','+str(LatLong[status2[m]][0])+','+str(LatLong[status2[m]][1])+','+str(Tcsr[l][m]/1000)+'\n'),


# 		# print "bhq ===================================================",bhqsindx[bhq],blkx_distx[bhqsindx[bhq]],str(GP_lists[0][blkx_distx[bhqsindx[bhq]]]),str(GP_Names[0][blkx_distx[bhqsindx[bhq]]]),str(LatLong[blkx_distx[bhqsindx[bhq]]][0]),str(LatLong[blkx_distx[bhqsindx[bhq]]][1])
# 		#exit()

# 		#f10.write()

# 		# sys.exit()
# 		# Block_MST.append(Tcsr)
# 		#print Tcsr
# 		# print Orig_Tcsr
# 		distan=Tcsr.sum()
# 		distan_all = distan
# 		if(distan !=0):
# 			maxi=Tcsr.max()
# 			f3.write(str(j)+','+str(distan/1000)+'km,'+str(maxi/1000)+'km,' + str(max([x for x in min_route_length if x < 1000000.0 ])/1000)+'km' + ','+ str(len(all_olts)) +'\n')
# 		#sys.exit()
# 		limit_leafnode_iterations = 0
# 		while(1):#what 200
# 			limit_leafnode_iterations += 1
# 			#print "iteration======",limit_leafnode_iterations
# 			conn=connectwls(Tcsr,j)
# 			if (conn==0):
# 				break;
# 			if limit_leafnode_iterations >= 100:
# 				print "Warning: No of iterations for removing leaf nodes in the mst has crosses limit = 200, please ckeck the code"
# 				exit()

# 		# print "reduced mst after removing connected leafnodes"  
# 		# satellite_test = []      
# 		# for l in range(len(status2)):
# 		# 	if (min_route_length[l]>=1000000 and int(Phase_lists[0][status2[l]]) == 2):
# 		# 		satellite_test.append(l)


# 		# satellite_recommendation(satellite_test)	
# 		# exit()	




# 		max_reduced_route_len = 0
# 		for l in range(len(status2)):
# 			if l in problem_cases and int(Phase_lists[0][status2[l]]) == 2:
# 				Phase_lists[0][status2[l]]=30
# 				print "Node discarded",j,l
# 				continue
# 			elif(min_route_length[l]>=1000000 and int(Phase_lists[0][status2[l]]) == 2):            	
# 				f4.write(str(j)+','+str(GP_lists[0][status2[l]])+','+str(GP_Names[0][status2[l]])+ ',' +str(LatLong[status2[l]][0]) + ',' +str(LatLong[status2[l]][1])+','+str(reqTP_mat[status2[l]])+'\n')
# 				Phase_lists[0][status2[l]]=20
# 				print "Node for Satellite", j,l 
# 				continue
			

# 			for m in range(len(status2)):
# 				if Tcsr[l][m] > 0:
# 					if min_route_length[l] < 1000000 and min_route_length[m] < 1000000:
# 						if Tcsr[l][m] >= 1000000:
# 							print "ERROR:: link length > 1000Km", l,m,Tcsr
# 							sys.exit()
# 						#f7.write(str(j)+','+str(latlong_dict_array[j][l][0])+','+str(latlong_dict_array[j][l][1])+','+str(latlong_dict_array[j][m][0])+','+str(latlong_dict_array[j][m][1])+','+str(Tcsr[l][m]/1000)+'\n')    
# 						f7.write(str(j)+','+str(LatLong[status2[l]][0])+','+str(LatLong[status2[l]][1])+','+str(LatLong[status2[l]][0])+','+str(LatLong[status2[l]][1])+','+str(Tcsr[l][m]/1000)+'\n')    

# 						max_reduced_route_len = max(max_reduced_route_len,min_route_length[l],min_route_length[m])

# 		distan=Tcsr.sum()
# 		if(distan !=0):
# 			maxi=Tcsr.max()
# 			#print "Maximum length for Block",blocks[j],"= ",maxi/1000,"km"

# 			f6.write(str(j)+','+str(distan/1000)+'km,'+str(maxi/1000)+'km,' + str(max_reduced_route_len/1000)+'km,'+str((distan_all-distan)/1000)+'km,'+str(len(all_olts))+'\n')
		
# 		dist_olts += len(all_olts)
# # Block Loop Ends #

# 	for k in range(NODE):
# 		f1.write(str(GP_Names[0][k]) + ',' +str(GP_lists[0][k]) + ',' + str(LatLong[k][0]) + ',' + str(LatLong[k][1]) + ',' + str(Phase_lists[0][k]) +','+ str(tower_height[k]) + '\n')

# 	#print "Phasssesssss2=---\n",Phase_lists
# 	#exit()

# 	p1 = 0
# 	t=0
# 	rex=0
# 	blhq=0
# 	tp=0
# 	p1c=0
# 	cont=0
# 	nfibre=0
# 	satr=0
# 	pr_cases=0
# 	for i in range(NODE):
# 		if Phase_lists[0][i] == 21:
# 			p1+=1
# 		elif Phase_lists[0][i] == 15:
# 			rex+=1
# 		elif Phase_lists[0][i] == 9:
# 			t+=1
# 		elif Phase_lists[0][i] == 19:
# 			blhq+=1  
# 		elif Phase_lists[0][i] == 22:
# 			print "connected to phase 1 (wireless)"
# 			p1c+=1 
# 		elif Phase_lists[0][i] == 10:
# 			print "connected to phase 9 (wireless tower)"
# 			cont+=1 
# 		elif Phase_lists[0][i] == 2 or Phase_lists[0][i] == 3 :
# 			nfibre+=1
# 		elif Phase_lists[0][i] == 20:
# 			satr+=1
# 		elif Phase_lists[0][i] == 30:
# 			pr_cases+=1        
# 	p2=cont+p1c+nfibre+satr+pr_cases
	
# 	f2.write(str(input_file)+','+str(p1)+','+str(p2)+','+str(rex)+','+str(t)+','+str(p1c)+','+str(cont)+','+str(satr)+','+str(nfibre)+','+str(dist_olts)+','+str(pr_cases)+'\n')
# 	print ("Closing everything!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
# 	#closeall()
	
# 	# print dist_olts
# 	# sys.exit()

def removecsv(dis_code):
    for filename in os.listdir("input"):
        print filename
        if filename.startswith(str(dis_code)):
            os.rename("input/"+str(dis_code)+".csv","input/"+str(dis_code))

for file in os.listdir("input"):
	if file.endswith(".csv"):
		do_something(file.split(".")[0])
		removecsv(file.split(".")[0])

print "Congratulations IITB Team for the AWESOME results!!!!"

# do_something(245)

# print "Towers ",t
# print "Unconnected GPs ",ug
# print "connected to phase 1 status 22--- ",p1c
# print "close to tower   --status 8",ct
# print "Throughput req. more than 150mbps status 12----",tp
# print "connected to 12--status 13 -s",c12
# print "connected to tower i.e 10-s",cont
# print "new fibre provided i.e. status 5-s",nfibre
# print "connected to new fibre i.e status  6 -s",conf



# degreeGp = np.sum(adjMats[0], axis = 1)
# sumAllElementsAdjMat = np.sum(degreeGp)
# print degreeGp[np.argmax(degreeGp)]
# print sumAllElementsAdjMat
  
