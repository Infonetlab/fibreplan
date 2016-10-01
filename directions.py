try:
	import simplejson
except:
	import json as simplejson
import urllib
import os
import time
from maps_blk import road_dist_block
import sys
from pse_2 import latlongdist 



def get_waypoints(orig_coord,dest_coord,state,dist,blok,key):

	orig_coord[0] = float(str(orig_coord[0]))
	orig_coord[1] = float(str(orig_coord[1]))
	dest_coord[0] = float(str(dest_coord[0]))
	dest_coord[1] = float(str(dest_coord[1]))

	#print "Get Waypoints::::",orig_coord,dest_coord

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
				return [dest_coord],0.1
			elif ((orig_coord[0] == float(tokens[0])) \
			and (orig_coord[1] == float(tokens[1])) \
			and (dest_coord[0] == float(tokens[2])) \
			and (dest_coord[1] == float(tokens[3]))): #Found in file
				wp_number = (len(tokens) - 4)/2 #Number of waypoints
				if wp_number <= 0:
					#print "ONE"
					return [dest_coord],road_dist_block(orig_coord,dest_coord,state,dist,blok,key)
				else:
					wp_list = [[float(tokens[2*x+4]),float(tokens[2*x+5])] for x in range(wp_number)]
					wp_list.append(dest_coord)
					#print "TWO"
					return wp_list,road_dist_block(orig_coord,dest_coord,state,dist,blok,key)
			elif ((orig_coord[0] == float(tokens[2])) \
			and (orig_coord[1] == float(tokens[3])) \
			and (dest_coord[0] == float(tokens[0])) \
			and (dest_coord[1] == float(tokens[1]))): # Found in reverse order
					wp_number = (len(tokens) - 4)/2 #Number of waypoints
					if wp_number <= 0:
						return [dest_coord],road_dist_block(orig_coord,dest_coord,state,dist,blok,key)
					else:
						wp_list = [[float(tokens[2*x+4]),float(tokens[2*x+5])] for x in range(wp_number)]
						wp_list.append(dest_coord)
						#print "THREE"
						return wp_list,road_dist_block(orig_coord,dest_coord,state,dist,blok,key)
		

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
		#print f['routes'][0]['legs'][0]['steps']
		try:
			llength = len(f['routes'][0]['legs'][0]['steps'])
		except:
			if f['status'] == 'OVER_QUERY_LIMIT':
				print "OVER QUERY LIMIT -- CHANGE KEY!!"
				sys.exit()
			elif f['status'] == 'ZERO_RESULTS':
				print "Jassi do something error in getting waypoints!!!!",orig_coord,dest_coord
				road_dist_block(orig_coord,dest_coord,state,dist,blok,key,1000000.0)
				fw1 = open('waypoints/waypoints_eps_'+str(int(blok))+'.csv','a+')
				fw1.write(str(orig_coord[0])+','+str(orig_coord[1])+','+str(dest_coord[0])+','+str(dest_coord[1])+'\n')
				fw1.close()
				return [dest_coord],1000000.0


		if f['status'] != 'OK':
			print "STATUS != OK... CHECK"
			sys.exit()

		print "get_waypoints:::number of waypoints = ",len(f['routes'][0]['legs'][0]['steps'])
		
		
		if llength < 1:
			print "Jassi do something error in getting waypoints!!!!",orig_coord,dest_coord
			road_dist_block(orig_coord,dest_coord,state,dist,blok,key,1000000.0)
			fw1 = open('waypoints/waypoints_eps_'+str(int(blok))+'.csv','a+')
			fw1.write(str(orig_coord[0])+','+str(orig_coord[1])+','+str(dest_coord[0])+','+str(dest_coord[1])+'\n')
			fw1.close()
			return [dest_coord],1000000.0
			#sys.exit()
		
		wp_list = [dest_coord]
		print "get_waypoints::: wp_list initial value",wp_list
		start_pt = orig_coord
		add_dist = 0
		add_dist_wpd = 0
		
		for x in range(llength):
			if x == 0: #This will always exist
				fw1_write_str = str(orig_coord[0])+','+str(orig_coord[1])+','+str(dest_coord[0])+','+str(dest_coord[1])

				wp_lat = str(float(f['routes'][0]['legs'][0]['steps'][0]['start_location']['lat']))
				wp_long = str(float(f['routes'][0]['legs'][0]['steps'][0]['start_location']['lng']))
				wp_latlong = [float(wp_lat),float(wp_long)]

				if wp_latlong != orig_coord:
				 	wp_list.append(wp_latlong)
				 	fw1_write_str = fw1_write_str+','+str(wp_lat)+','+str(wp_long)
				 	add_dist = float("{:0.2f}".format(latlongdist(wp_latlong,orig_coord)))
				 	print "Entering Road_dist_block ::::",x+1,orig_coord,wp_latlong,add_dist
				 	road_dist_block(orig_coord,wp_latlong,state,dist,blok,key,add_dist)
					start_pt = wp_latlong
					print "get_waypoints::: wp_list initial value",wp_list
				# 	print "get_waypoints::: distance between two gp's-",f['routes'][0]['legs'][0]['distance']['value'],latlongdist(wp_latlong,dest_coord)
			else:
				print "start point:::",start_pt
				wp_lat = str(float(f['routes'][0]['legs'][0]['steps'][x]['start_location']['lat']))
				wp_long = str(float(f['routes'][0]['legs'][0]['steps'][x]['start_location']['lng']))
				fw1_write_str = fw1_write_str+','+str(wp_lat)+','+str(wp_long)
				wp_latlong = [float(wp_lat),float(wp_long)]
				wp_list.append(wp_latlong)
				formatted_distance = float("{:0.2f}".format(float(f['routes'][0]['legs'][0]['steps'][x-1]['distance']['value'])))	
				print "Entering Road_dist_block ::::",x+1,start_pt,wp_latlong,formatted_distance
				road_dist_block(start_pt,wp_latlong,state,dist,blok,key,formatted_distance)
				start_pt = wp_latlong
				print "get_waypoints::: wp_list initial value",wp_list

		wp_lat = str(float(f['routes'][0]['legs'][0]['steps'][llength-1]['end_location']['lat']))
		wp_long = str(float(f['routes'][0]['legs'][0]['steps'][llength-1]['end_location']['lng']))
		wp_latlong = [float(wp_lat),float(wp_long)]

		if wp_latlong != dest_coord:
			print "start point:::",start_pt
			wp_list.append(wp_latlong)
			fw1_write_str = fw1_write_str+','+str(wp_lat)+','+str(wp_long)
			print "Entering Road_dist_block ::::",x+1,start_pt,wp_latlong,float("{:0.2f}".format(float(f['routes'][0]['legs'][0]['steps'][llength-1]['distance']['value'])))
			road_dist_block(start_pt,wp_latlong,state,dist,blok,key,float("{:0.2f}".format(float(f['routes'][0]['legs'][0]['steps'][llength-1]['distance']['value']))))
			add_dist_wpd = float("{:0.2f}".format(latlongdist(wp_latlong,dest_coord)))
			print "get_waypoints::: wp_list initial value",wp_list

			#print "SEVEN"		
			print "Entering Road_dist_block ::::",llength,wp_latlong,dest_coord,add_dist_wpd
			road_dist_block(wp_latlong,dest_coord,state,dist,blok,key,add_dist_wpd)
			add_dist += add_dist_wpd
			print "get_waypoints::: distance between two gp's-",f['routes'][0]['legs'][0]['distance']['value'],latlongdist(wp_latlong,dest_coord)		
			print "update road sit is called for - ",orig_coord,dest_coord
			print "Entering Update_oad_dist ::::",llength,orig_coord,dest_coord,float(f['routes'][0]['legs'][0]['distance']['value'])+add_dist
			road_dist_block(orig_coord,dest_coord,state,dist,blok,key,float("{:0.2f}".format(float(f['routes'][0]['legs'][0]['distance']['value'])+add_dist)))
		else:
			formatted_distance = float("{:0.2f}".format(float(f['routes'][0]['legs'][0]['steps'][llength-1]['distance']['value'])))
			print "Entering Road_dist_block ::::",llength,start_pt,dest_coord,formatted_distance
			road_dist_block(start_pt,dest_coord,state,dist,blok,key,formatted_distance)

		print "get_waypoints::: distance between two gp's-",f['routes'][0]['legs'][0]['distance']['value'],latlongdist(wp_latlong,dest_coord)		
		print "update road sit is called for - ",orig_coord,dest_coord
		print "Entering Update_oad_dist ::::",llength,orig_coord,dest_coord,float(f['routes'][0]['legs'][0]['distance']['value'])+add_dist
		road_dist_block(orig_coord,dest_coord,state,dist,blok,key,float("{:0.2f}".format(float(f['routes'][0]['legs'][0]['distance']['value'])+add_dist)))
	


		fw1_write_str = fw1_write_str+'\n'

		fw1 = open('waypoints/waypoints_eps_'+str(int(blok))+'.csv','a+')
		fw1.write(fw1_write_str)
		fw1.close()
		return wp_list,int(f['routes'][0]['legs'][0]['distance']['value'])+add_dist

	else:
		fw1 = open('waypoints/waypoints_eps_'+str(int(blok))+'.csv','w')
		fw1.close()
		try:
			wp_list,d=get_waypoints(orig_coord,dest_coord,state,dist,blok,key)
		except IOError, e:
						if e.errno == 101 or e.errno == 'socket error' or e.errno == -3 or e.errno == 2:
							print "Network Error"
							time.sleep(1)
							wp_list,d=get_waypoints(orig_coord,dest_coord,state,dist,blok,key)
						else:
							raise    
		return wp_list,d


def update_block_waypoint(block_waypoints_list,wp_list):
	
	for w in wp_list:
		#print "Check1:::",w
		if w not in block_waypoints_list:
			block_waypoints_list.append(w)

	return block_waypoints_list
	


