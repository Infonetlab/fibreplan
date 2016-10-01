import pickle
import numpy as np
import random
import math
import os
import sys
from random import randrange
from csv2npy import read_csv_fields
from adj_maker import make_adjacency
from pse_2 import rf_get
from pse_2 import get_elevation_profile
from feas_mkr import make_feas
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
#from directions import fetch_direction
from maps import road_dist
from sptgraph import spt
from pse_2 import latlongdist
from copy import copy, deepcopy
from sptgraph import fibre_saved_if_wireless

def get_towers_list(phase_list,number_of_nodes):
	towers_list = list()
	for m in range(number_of_nodes):
		if phase_list[m] == 9:
			towers_list.append(m)
	return towers_list

def get_phase1_list(phase_list,number_of_nodes):
	phase1_list = list()
	for m in range(number_of_nodes):
		if phase_list[m] == 21:
			phase1_list.append(m)
	return phase1_list

def make_tower_connection(tree_dict,curr_leaf_nodes,towers_list,adj,req_throuput,status2,process_flag=''):

	possible_connections = dict()
	link = dict()

	
	# for m in curr_leaf_nodes:
	for m in (curr_leaf_nodes):
		if m.split(',')[0] == 'wp':
			continue
		m_id = int(m.split(',')[1])
		possible_connections.update({m:[]})
		for n in towers_list:
			if adj[n][status2[m_id]] == 1:
				possible_connections[m].append(n)

	gps_connectable = [x for x,y in possible_connections.items() if len(y) > 0]

	if gps_connectable == []:
		return link

	if process_flag == 'TREE':
		max_fibre_saved = 0

		for x in gps_connectable:
			fibre_saved = fibre_saved_if_wireless(tree_dict,x)
			if fibre_saved > max_fibre_saved:
				max_fibre_saved = fibre_saved
				max_fibre_saving_gp = x

		if max_fibre_saved > 0:
			link.update({max_fibre_saving_gp:possible_connections[max_fibre_saving_gp]})
	else:
		min_connect_possible = 10000000000000
		for m,value_list in possible_connections.items():
			if len(value_list) < min_connect_possible and len(value_list) > 0:
				min_connect_possible = len(value_list)
				min_connect_gp = m

		link.update({min_connect_gp:possible_connections[min_connect_gp]})



	return link



def make_phase1_connection(tree_dict,curr_leaf_nodes,phase1_list,adj,req_throuput,status2,process_flag=''):

	# print "Adjacency === ",adj

	possible_connections = dict()
	link = dict()

	#curr_leaf_nodes = [x for x in tree_dict.keys() if tree_dict[x][2]==[] and float(req_throuput[int(x.split(',')[1])]) <= 6250.0]

	for m in curr_leaf_nodes:
		if m.split(',')[0] == 'wp':
			continue
		m_id = int(m.split(',')[1])
		# print "M ID == ",m_id
		possible_connections.update({m:[]})
		for n in phase1_list:
			if adj[n][status2[m_id]] == 1:
				possible_connections[m].append(n)

	gps_connectable = [x for x,y in possible_connections.items() if len(y) > 0]

	if gps_connectable == []:
		return link
	
	if process_flag == 'TREE':
		max_fibre_saved = 0

		for x in gps_connectable:
			fibre_saved = fibre_saved_if_wireless(tree_dict,x)
			if fibre_saved > max_fibre_saved:
				max_fibre_saved = fibre_saved
				max_fibre_saving_gp = x

		if max_fibre_saved > 0:
			link.update({max_fibre_saving_gp:possible_connections[max_fibre_saving_gp]})
	else:
		min_connect_possible = 10000000000000
		for m,value_list in possible_connections.items():
			if len(value_list) < min_connect_possible and len(value_list) > 0:
				min_connect_possible = len(value_list)
				min_connect_gp = m

		link.update({min_connect_gp:possible_connections[min_connect_gp]})



	return link