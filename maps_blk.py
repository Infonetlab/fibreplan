try:
	import simplejson
except:
	import json	as simplejson
import urllib
import os
import time
import sys
from goapi import sign_url

def road_dist_block_file(orig_coord,dest_coord,state,dist,block=-1,distance=-1):
	orig_coord[0] = float(str(orig_coord[0]))
	orig_coord[1] = float(str(orig_coord[1]))
	dest_coord[0] = float(str(dest_coord[0]))
	dest_coord[1] = float(str(dest_coord[1]))

	
	#print "road_dist_block_file::::",orig_coord,dest_coord,state,dist,block,distance,type(state),type(block)
	if (int(block) > -1):
		#print "road_dist_block::::Searching Block files for --",orig_coord,dest_coord
		if(os.path.exists('distfile/distFile_'+str(state)+'_'+str(dist)+'_'+str(block))):
			with open('distfile/distFile_'+str(state)+'_'+str(dist)+'_'+str(block), 'r+') as fo:
				lines = fo.readlines()
			for li in lines:
				if not li:
					print "hi"
					continue
				tokens = li.split(',')
				if ((orig_coord[0] == dest_coord[0]) \
				and (orig_coord[1] == dest_coord[1])):
					print "Same Coordinates!!!"
					print "road_dist_block_file::::",orig_coord,dest_coord,state,dist,block,distance,type(state),type(block)
	
					distance=float(0.1)
					#return float(distance)
				elif ((orig_coord[0] == float(tokens[0])) \
				and (orig_coord[1] == float(tokens[1])) \
				and (dest_coord[0] == float(tokens[2])) \
				and (dest_coord[1] == float(tokens[3]))):
					if len(tokens) == 5:
						distance  = float(tokens[4])
					else:
						distance  = float(tokens[5])
					#print "Found Coordinates!!!"
					#return float(distance)
				elif ((orig_coord[0] == float(tokens[2])) \
				and (orig_coord[1] == float(tokens[3])) \
				and (dest_coord[0] == float(tokens[0])) \
				and (dest_coord[1] == float(tokens[1]))):
					if len(tokens) == 5:
						distance  = float(tokens[4])
					else:
						distance  = float(tokens[5])
					#print "Found Coordinates 2!!!"		
					#return float(distance)

		return(distance)


def road_dist_block(orig_coord,dest_coord,state,dist,block=-1,key='AIzaSyD9-tRX5bAWeZbApETlNDRFgeHB3kgBGwI',distance=-1):

	orig_coord[0] = float(str(orig_coord[0]))
	orig_coord[1] = float(str(orig_coord[1]))
	dest_coord[0] = float(str(dest_coord[0]))
	dest_coord[1] = float(str(dest_coord[1]))

	
	#print "road_dist_block::::",orig_coord,dest_coord,state,dist,block,distance,type(state),type(block)
	#print "road_dist_block::::"
	if (int(block) > -1):
		#print "road_dist_block::::Searching Block files for --",orig_coord,dest_coord
		if(os.path.exists('distfile/distFile_'+str(state)+'_'+str(dist)+'_'+str(block))):
			with open('distfile/distFile_'+str(state)+'_'+str(dist)+'_'+str(block), 'r+') as fo:
				lines = fo.readlines()
			for li in lines:
				if not li:
					print "hi"
					continue
				tokens = li.split(',')
				#print "Tokens:::",tokens
				if ((orig_coord[0] == dest_coord[0]) \
				and (orig_coord[1] == dest_coord[1])):
					print "Same Coordinates!!!"
					distance=float(0.1)
					return float(distance)
				elif ((orig_coord[0] == float(tokens[0])) \
				and (orig_coord[1] == float(tokens[1])) \
				and (dest_coord[0] == float(tokens[2])) \
				and (dest_coord[1] == float(tokens[3]))):
					if len(tokens) == 5:
						distance  = float(tokens[4])
					else:
						distance  = float(tokens[5])
					#print "Found Coordinates!!!"
					return float(distance)
				elif ((orig_coord[0] == float(tokens[2])) \
				and (orig_coord[1] == float(tokens[3])) \
				and (dest_coord[0] == float(tokens[0])) \
				and (dest_coord[1] == float(tokens[1]))):
					if len(tokens) == 5:
						distance  = float(tokens[4])
					else:
						distance  = float(tokens[5])
					#print "Found Coordinates 2!!!"		
					return float(distance)

		if (distance == -1): #Need to get the distance
			#print "road_dist_block:::: Need to get the distance"
			road_dist_from_district = road_dist(orig_coord,dest_coord,state,dist) #Check in district file
			#print "road_dist_block:::Return value from road_dist", road_dist_from_district
			if (road_dist_from_district == -1): #Not found in district  distance files, so get from the mighty Google
				#print "road_dist_block::::Not found in district  distance files, so get from the mighty Google"
				#sys.exit()
				try:
					#print "distance not there in file"
					return get_distance(orig_coord,dest_coord,state,dist,block,key)
				except IOError, e:
						if e.errno == 101 or e.errno == 'socket error' or e.errno == -3 or e.errno == 2 or e.errno == 1 or e.errno == -2:
							print "Network Error"
							time.sleep(1)
							return get_distance(orig_coord,dest_coord,state,dist,block,key)		
						else:
							raise    
			else: #found in district files and has to be copied in block file for future use, Hence flag = -1
				return get_distance(orig_coord,dest_coord,state,dist,block,key,road_dist_from_district)
		else: #Distance already known, put it in block file
			return get_distance(orig_coord,dest_coord,state,dist,block,key,distance) 



def road_dist(orig_coord,dest_coord,state,dist):

	orig_coord[0] = float(str(orig_coord[0]))
	orig_coord[1] = float(str(orig_coord[1]))
	dest_coord[0] = float(str(dest_coord[0]))
	dest_coord[1] = float(str(dest_coord[1]))

	
	print "road_dist::::"
	if(os.path.exists('distfile/distFile_'+str(state)+'_'+str(dist))):
		with open('distfile/distFile_'+str(state)+'_'+str(dist), 'r+') as fo:
			lines = fo.readlines()
		for li in lines:
			if not li:
				print "hi"
				continue
			tokens = li.split(',')
			#print "road_dist:::: Tokens", tokens
			if ((orig_coord[0] == dest_coord[0]) \
			and (orig_coord[1] == dest_coord[1])):
				print "Same Coordinates!!!"
				distance=float(0.1)
				return float(distance)
			elif ((orig_coord[0] == float(tokens[0])) \
			and (orig_coord[1] == float(tokens[1])) \
			and (dest_coord[0] == float(tokens[2])) \
			and (dest_coord[1] == float(tokens[3]))):
				if len(tokens) == 5:
					#print "Forward Tokens === ", tokens
					distance  = float(tokens[4])
					#print "Dist === ", distance
				else:
					#print "Forward Tokens === ", tokens
					distance  = float(tokens[5])
					#print "Dist === ", distance
				print 'distance was found in file',distance
				return float(distance)
			elif ((orig_coord[0] == float(tokens[2])) \
			and (orig_coord[1] == float(tokens[3])) \
			and (dest_coord[0] == float(tokens[0])) \
			and (dest_coord[1] == float(tokens[1]))):
				if len(tokens) == 5:
					#print "Forward Tokens === ", tokens
					distance  = float(tokens[4])
					#print "Dist === ", distance
				else:
					#print "Forward Tokens === ", tokens
					distance  = float(tokens[5])
					#print "Dist === ", distance
				print 'distance was found in file',distance
				return float(distance)
		#else:
		return(-1)



	# 	try:		
	# 		return get_distance(orig_coord,dest_coord,state,dist)
	# 	except IOError, e:

	# 			if e.errno == 101 or e.errno == 'socket error' or e.errno == -3 or e.errno == 2:
	# 				print "Network Error"
	# 				time.sleep(1)
	# 				return get_distance(orig_coord,dest_coord,state,dist)		
	# 			else:
	# 				raise    
	# else:
	# 	try:		
	# 		return get_distance(orig_coord,dest_coord,state,dist)
	# 	except IOError, e:
	# 			if e.errno == 101 or e.errno == 'socket error' or e.errno == -3 or e.errno == 2:
	# 				print "Network Error"
	# 				time.sleep(1)
	# 				return get_distance(orig_coord,dest_coord,state,dist)		
	# 			else:
	# 				raise 
		

		# if not os.path.exists('distance_file'):
		#     os.makedirs('distance_file')

def update_road_dist(orig_coord,dest_coord,state,dist,block,distance_new):

	orig_coord[0] = float(str(orig_coord[0]))
	orig_coord[1] = float(str(orig_coord[1]))
	dest_coord[0] = float(str(dest_coord[0]))
	dest_coord[1] = float(str(dest_coord[1]))

	print orig_coord,dest_coord

	
	if not os.path.exists('distfile'):
		os.makedirs('distfile')
	fo = open('distfile/distFile_'+str(state)+'_'+str(dist)+'_'+str(block), 'r+')
	# distance = 0.1
	lines = fo.readlines()
	fo.close()
	flag = False # matched the line
	flag1 = False # exists in the file
	fo =  open('distfile/distFile_'+str(state)+'_'+str(dist)+'_'+str(block), 'w')
	print "update dist block called"
	for li in lines:
		if not li:
			print "hi"
			continue
		print li
		tokens = li.split(',')
		#print "road_dist:::: Tokens", tokens
		if ((orig_coord[0] == dest_coord[0]) \
		and (orig_coord[1] == dest_coord[1])):
			#print "Same Coordinates!!!"
			distance=float(0.1)
			#return float(distance)
		elif ((orig_coord[0] == float(tokens[0])) \
		and (orig_coord[1] == float(tokens[1])) \
		and (dest_coord[0] == float(tokens[2])) \
		and (dest_coord[1] == float(tokens[3]))):
			if len(tokens) == 5:
				distance  = float(tokens[4])
			else:
				distance  = float(tokens[5])
			flag=True
			flag1 = True
			# if int(distance) != int(distance_new):
			# 	flag = True
			# 	tokens[4] = str(distance_new)
			# 	li = tokens[0]+','+tokens[1]+','+tokens[2]+','+tokens[3]+','+tokens[4]+'\n'					

		elif ((orig_coord[0] == float(tokens[2])) \
		and (orig_coord[1] == float(tokens[3])) \
		and (dest_coord[0] == float(tokens[0])) \
		and (dest_coord[1] == float(tokens[1]))):
			if len(tokens) == 5:
				distance  = float(tokens[4])
			else:
				distance  = float(tokens[5])
			flag=True
			flag1=True


		if(flag==True):
			print "cordinates matched"
			if int(distance) != int(distance_new):
				distance = distance_new
				flag=False
		else:
			if len(tokens) == 5:
				distance  = float(tokens[4])
			else:
				distance  = float(tokens[5]) 

		li = tokens[0]+','+tokens[1]+','+tokens[2]+','+tokens[3]+','+"{:0.2f}".format(distance)+'\n'	

		print li

		# print "update_road_dist::::",orig_coord,dest_coord,distance

		fo.write(li)

	if flag1 == False: #record not in file
		li = str(orig_coord[0])+','+str(orig_coord[1])+','+str(dest_coord[0])+','+str(dest_coord[1])+','+"{:0.2f}".format(distance_new)+'\n'
		fo.write(li)
	
	fo.close()

			

def get_distance(orig_coord,dest_coord,state,dist,block,key='AIzaSyD9-tRX5bAWeZbApETlNDRFgeHB3kgBGwI',distance=-1):

	orig_coord[0] = float(str(orig_coord[0]))
	orig_coord[1] = float(str(orig_coord[1]))
	dest_coord[0] = float(str(dest_coord[0]))
	dest_coord[1] = float(str(dest_coord[1]))

	print "get_distance::::",orig_coord,dest_coord,distance
	#sys.exit()
	if not os.path.exists('distfile'):
		os.makedirs('distfile')
	fo = open('distfile/distFile_'+str(state)+'_'+str(dist)+'_'+str(block), 'a+')

	if (distance > -1):
		var = str(orig_coord[0]) + "," + str(orig_coord[1]) + "," + str(dest_coord[0]) + "," + str(dest_coord[1]) + "," + str(float(distance)) + "\n"
		fo.write(var)
		fo.close()
		return(distance)
	elif (distance == -1):
		wp_list,distance = fetch_waypoints(orig_coord,dest_coord,state,dist,blok,key)
		# ELEVATION_BASE_URL='https://maps.googleapis.com/maps/api/distancematrix/json'
		

		# # units = 'Imperial'
		# # walking = 'walking'
		# # #params = 'origins=origins&destinations=destinations&key=key'
		# # origin=str(orig_coord[0])+","+str(orig_coord[1])
		# # dest = str(dest_coord[0])+","+str(dest_coord[1])
		# # params = {'origins':origin,'destinations':dest,'key':key, 'units': units }
		# # params1 = {'origins':origin,'destinations':dest,'key':key, 'units': units, 'mode': walking }
		# # url = ELEVATION_BASE_URL + '?' + urllib.urlencode(params)
		# # print url
		# # url1 = ELEVATION_BASE_URL + '?' + urllib.urlencode(params1)
		# # DIRECTIONS_BASE_URL='https://maps.googleapis.com/maps/api/directions/json'
		# units = 'Imperial'
		# # travel= 'driving'
		# walking = 'walking'

		# secret = 'xghu9DIoNr63z8_al_oJCSPWQh0='
		# client='gme-leptonsoftwareexport4'
		# origin=str(orig_coord[0])+","+str(orig_coord[1])
		# dest = str(dest_coord[0])+","+str(dest_coord[1])
		# # params = {'client':client,'origin':origin,'destination':dest,'travel_mode':travel,'key':key, 'units': units,}
		# params = {'client':client,'origins':origin,'destinations':dest, 'units': units }
		# params1 = {'client':client,'origins':origin,'destinations':dest, 'units': units, 'mode': walking }
		# url = ELEVATION_BASE_URL + '?' + urllib.urlencode(params)
		# url1 = ELEVATION_BASE_URL + '?' + urllib.urlencode(params1)
		# # url = DIRECTIONS_BASE_URL + '?' + urllib.urlencode(params)
		# # print url
		# signedurl=sign_url(url, secret)
		# print signedurl
		# signedurl1=sign_url(url1, secret)

		# f= simplejson.load(urllib.urlopen(signedurl))
		# # print f['rows'][0]['elements'][0]['distance']['text']
		# print "Why distance Matrix???",orig_coord, dest_coord, f
		# if(f['rows'][0]['elements'][0]['status']=='ZERO_RESULTS'):
		# 	f1= simplejson.load(urllib.urlopen(signedurl1))
		# 	if(f1['rows'][0]['elements'][0]['status']=='ZERO_RESULTS'):
		# 		distance = 1000000
		# 	else:
		# 		distance = float("{:0.2f}".format(f1['rows'][0]['elements'][0]['distance']['value']))
		# else:
		# 	distance = float("{:0.2f}".format(f['rows'][0]['elements'][0]['distance']['value']))
		# status = f['rows'][0]['elements'][0]['status']
		# print status,str(orig_coord[0]) + "," + str(orig_coord[1]),str(dest_coord[0]) + "," + str(dest_coord[1])

		var = str(orig_coord[0]) + "," + str(orig_coord[1]) + "," + str(dest_coord[0]) + "," + str(dest_coord[1]) + "," + str(float(distance)) + "\n"
		fo.write(var)
		fo.close()
		#sys.exit()
		
		return float(distance)




	# response = simplejson.load(urllib.urlopen(url))
	# print (response)
