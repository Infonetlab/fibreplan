import simplejson
import urllib
import os
from maps_blk import road_dist_block,update_road_dist
from pse_2 import latlongdist
def get_direction(orig_coord,dest_coord,state,dist):

	if(os.path.exists('distfile/distFile_'+str(state)+'_'+str(dist))):
		with open('distfile/distFile_'+str(state)+'_'+str(dist), 'r+') as fo:
			lines = fo.readlines()
		for li in lines:
			if not li:
				print "hi"
				continue
			tokens = li.split(',')
			if ((orig_coord[0] == float(tokens[0])) \
			and (orig_coord[1] == float(tokens[1])) \
			and (dest_coord[0] == float(tokens[2])) \
			and (dest_coord[1] == float(tokens[3]))):
				distance  = float(tokens[4])

				# print 'distance was found in file',type(distance)
				return distance
		return get_distance(orig_coord,dest_coord,state,dist)	


	else:
		return get_distance(orig_coord,dest_coord,state,dist) 

		# if not os.path.exists('distance_file'):
		#     os.makedirs('distance_file')

def fetch_direction(orig_coord,dest_coord,state,dist):

	ELEVATION_BASE_URL='https://maps.googleapis.com/maps/api/directions/json'
	# orig_coord='40.6655101,-73.89188969999998'
	# dest_coord='40.6905615,-73.9976592'
	key = 'AIzaSyDtPhMwTJmzoTpR4_xyovrmFGa77VLeamQ'
	units = 'Imperial'
	travel= 'bicycling'
	#params = 'origins=origins&destinations=destinations&key=key'
	origin=str(orig_coord[0])+","+str(orig_coord[1])
	dest = str(dest_coord[0])+","+str(dest_coord[1])
	params = {'origin':origin,'destination':dest,'travel_mode':travel,'key':key, 'units': units }

	url = ELEVATION_BASE_URL + '?' + urllib.urlencode(params)
	print url
	f= simplejson.load(urllib.urlopen(url))
	# print f['rows'][0]['elements'][0]['distance']['text']
	
	llength = len(f['routes'][0]['legs'][0]['steps'])
	print "    "
	print "[" , f['routes'][0]['legs'][0]['start_location']['lat'] ,"," ,  f['routes'][0]['legs'][0]['start_location']['lng'] , "]" 
	print "    "
	for x in range(0,llength):

	    print "[" , f['routes'][0]['legs'][0]['steps'][x]['start_location']['lat'] ,"," ,  f['routes'][0]['legs'][0]['steps'][x]['start_location']['lng'] , "]" ,f['routes'][0]['legs'][0]['steps'][x]['distance']['value']

	print "    "
	print "[" , f['routes'][0]['legs'][0]['steps'][llength-1]['end_location']['lat'] ,"," ,  f['routes'][0]['legs'][0]['steps'][llength-1]['end_location']['lng'] , "]" 
	print "    "
	print f['routes'][0]['legs'][0]['distance']['value']
	

	print "    "# distance = f['rows'][0]['elements'][0]['distance']['text'].split(' ')[0]
	# distance = f['rows'][0]['elements'][0]['distance']['text'].split(' ')[0]
	if not os.path.exists('directfile'):
		os.makedirs('directfile')
	with open('directfile/directFile_'+str(state)+'_'+str(dist), 'a+') as fo:

		#fo.write('{},{},{},{},{}\n'.format(orig_coord[0],orig_coord[1],dest_coord[0],dest_coord[1]),distance)
		var = str(orig_coord[0]) + "," + str(orig_coord[1]) + "," + str(dest_coord[0]) + "," + str(dest_coord[1]) + "," + str(f)
		fo.write(var)
		fo.write("\n")		
	# return distance
	return f	

	# response = simplejson.load(urllib.urlopen(url))
	# print (response)


def get_waypoints(orig_coord,dest_coord,state,dist,blok,key):
### Open waypoints file and read lines ###
	if os.path.exists('waypoints/waypoints_eps_'+str(int(blok))+'.csv'):
		with open('waypoints/waypoints_eps_'+str(int(blok))+'.csv', 'r+') as fw1:
			lines = fw1.readlines()

		for li in lines: ### Empty file
			if not li:
				print "hi"
				continue

			tokens = li.split(',')
			if ((orig_coord[0] == dest_coord[0]) \
			and (orig_coord[1] == dest_coord[1])): # When both latlongs are same
				print "get_waypoints:::same Coordinates for Waypoints!!!"
				return [dest_coord]
			elif ((orig_coord[0] == float(tokens[0])) \
			and (orig_coord[1] == float(tokens[1])) \
			and (dest_coord[0] == float(tokens[2])) \
			and (dest_coord[1] == float(tokens[3]))): #Found in file
				wp_number = (len(tokens) - 4)/2 #Number of waypoints
				if wp_number <= 0:
					return [dest_coord]
				else:
					wp_list = [[float(tokens[2*x+4]),float(tokens[2*x+5])] for x in range(wp_number)]
					wp_list.append(dest_coord)
					return wp_list
			elif ((orig_coord[0] == float(tokens[2])) \
			and (orig_coord[1] == float(tokens[3])) \
			and (dest_coord[0] == float(tokens[0])) \
			and (dest_coord[1] == float(tokens[1]))): # Found in reverse order
					wp_number = (len(tokens) - 4)/2 #Number of waypoints
					if wp_number <= 0:
						return [dest_coord]
					else:
						wp_list = [[float(tokens[2*x+4]),float(tokens[2*x+5])] for x in range(wp_number)]
						wp_list.append(dest_coord)
						return wp_list
		

		# Get waypoints from the mighty Google
		print "Fetching Waypoints from Google!!!"
		DIRECTIONS_BASE_URL='https://maps.googleapis.com/maps/api/directions/json'
		units = 'Imperial'
		travel= 'driving'
		origin=str(orig_coord[0])+","+str(orig_coord[1])
		dest = str(dest_coord[0])+","+str(dest_coord[1])
		params = {'origin':origin,'destination':dest,'travel_mode':travel,'key':key, 'units': units }

		url = DIRECTIONS_BASE_URL + '?' + urllib.urlencode(params)
		print url
		f= simplejson.load(urllib.urlopen(url)) #
		print f['routes'][0]['legs'][0]['steps']
		print "get_waypoints:::number of waypoints = ",len(f['routes'][0]['legs'][0]['steps'])
		llength = len(f['routes'][0]['legs'][0]['steps'])
		if llength < 1:
			print "Jassi do something error in getting waypoints!!!!",orig_coord,dest_coord
			sys.exit()
		
		wp_list = [dest_coord]
		print "get_waypoints::: wp_list initial value",wp_list
		start_pt = orig_coord
		
		for x in range(llength):
			if x == 0: #This will always exist
				fw1_write_str = str(orig_coord[0])+','+str(orig_coord[1])+','+str(dest_coord[0])+','+str(dest_coord[1])

				# wp_lat = f['routes'][0]['legs'][0]['steps'][0]['start_location']['lat']
				# wp_long = f['routes'][0]['legs'][0]['steps'][0]['start_location']['lng']
				# wp_latlong = [float(start_wp_lat),float(start_wp_long)]

				# if wp_latlong != orig_coord:
				# 	fw1_write_str = fw1_write_str+','+str(wp_lat)+','+str(wp_long)
				# 	wp_list.append(wp_latlong)
				# 	fw1_write_str = fw1_write_str+','+str(wp_lat)+','+str(wp_long)
				# 	road_dist_block(start_pt,wp_latlong,state,dist,blok,float(f['routes'][0]['legs'][0]['steps'][llength-1]['distance']['value']))
				# 	add_dist = latlongdist(wp_latlong,dest_coord)
				# 	road_dist_block(wp_latlong,dest_coord,state,dist,blok,add_dist)
				# 	print "get_waypoints::: distance between two gp's-",f['routes'][0]['legs'][0]['distance']['value'],latlongdist(wp_latlong,dest_coord)
			else:
				wp_lat = f['routes'][0]['legs'][0]['steps'][x]['start_location']['lat']
				wp_long = f['routes'][0]['legs'][0]['steps'][x]['start_location']['lng']
				fw1_write_str = fw1_write_str+','+str(wp_lat)+','+str(wp_long)
				wp_latlong = [float(wp_lat),float(wp_long)]
				wp_list.append(wp_latlong)
				road_dist_block(start_pt,wp_latlong,state,dist,blok,float(f['routes'][0]['legs'][0]['steps'][x-1]['distance']['value']))
				start_pt = wp_latlong
				print "get_waypoints::: wp_list initial value",wp_list

		wp_lat = f['routes'][0]['legs'][0]['steps'][llength-1]['end_location']['lat']
		wp_long = f['routes'][0]['legs'][0]['steps'][llength-1]['end_location']['lng']
		wp_latlong = [float(wp_lat),float(wp_long)]

		if wp_latlong != dest_coord:
			fw1_write_str = fw1_write_str+','+str(wp_lat)+','+str(wp_long)
			#wp_latlong = [float(wp_lat),float(wp_long)]
			wp_list.append(wp_latlong)
			fw1_write_str = fw1_write_str+','+str(wp_lat)+','+str(wp_long)
			road_dist_block(start_pt,wp_latlong,state,dist,blok,float(f['routes'][0]['legs'][0]['steps'][llength-1]['distance']['value']))
			add_dist = latlongdist(wp_latlong,dest_coord)
			road_dist_block(wp_latlong,dest_coord,state,dist,blok,add_dist)
			print "get_waypoints::: distance between two gp's-",f['routes'][0]['legs'][0]['distance']['value'],latlongdist(wp_latlong,dest_coord)		
			print "update road sit is called for - ",orig_coord,dest_coord
			update_road_dist(orig_coord,dest_coord,state,dist,blok,int(f['routes'][0]['legs'][0]['distance']['value'])+add_dist)	
		else:
			road_dist_block(start_pt,dest_coord,state,dist,blok,float(f['routes'][0]['legs'][0]['steps'][llength-1]['distance']['value']))
		


		fw1_write_str = fw1_write_str+'\n'

		fw1 = open('waypoints/waypoints_eps_'+str(int(blok))+'.csv','a+')
		fw1.write(fw1_write_str)
		fw1.close()
		return(wp_list)

	else:
		fw1 = open('waypoints/waypoints_eps_'+str(int(blok))+'.csv','w')
		fw1.close()
		wp_list=get_waypoints(orig_coord,dest_coord,state,dist,blok,key)
		return(wp_list)


		## Remaining to add the waypoint distances




