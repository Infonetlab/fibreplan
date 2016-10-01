import os
import sys
def cleardistfile():
	for filename in os.listdir("distfile"):
		if('dist' in filename):
			thefile="distfile/"+str(filename)
			print thefile
			f=open(thefile,'r')
			lines = list()
			N=2
			for i in range(N):
				line=f.next()
				lines.append(line)
			f.close
			delete=1
			for line in lines:
				if(float(line.split(",")[4].strip("\n"))!=1000000.0):
					delete=0
					break
				else:
					delete=1
			if(delete==1):
				try:	
					print filename.split("_")[3]
					print "delete", thefile
					print "waypoints/waypoints_eps_"+str(filename.split("_")[3])+".csv"
					os.remove(thefile)
					os.remove("waypoints/waypoints_eps_"+str(filename.split("_")[3])+".csv")
				except:
					continue	

			# print lines
			# for file in *; do mv "$file" "$file.csv"; done
cleardistfile()


