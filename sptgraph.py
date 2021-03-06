import sys
from collections import defaultdict, deque
from pse_2 import latlongdist,get_elevation_profile
# from spt_test 
MAX_ROUTE_LENGTH = 20000


class Graph(object):
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance


# def print_mst_links(node_id,tree_dict,links_dict):
#     for x in tree_dict[node_id][2]:
#         links_dict = print_mst_links(x,tree_dict,links_dict)
#         links_dict.update{node_id:x}
#         return links_dict



def print_mst_links(node_id,tree_dict,links_dict):
    

    if tree_dict[node_id][2] == []:
        print "No children found"
        return links_dict


    for x in tree_dict[node_id][2]:
        print "childrens",x,node_id
        links_dict.update({node_id:x})
        links_dict = print_mst_links(x,tree_dict,links_dict)
    return links_dict


def build_Tcsr(node,tree_with_wps,Tcsr,gp_parent=None):
    print "Entering Build TCR with node_id and parent id ====", node,gp_parent
    node_type = node.split(',')[0]
    node_index = int(node.split(',')[1])
    if gp_parent != None:
        gp_parent_index = int(gp_parent.split(',')[1]) 
    else:
        sys.exit() 
    if gp_parent.split(',')[1] == 'wp':
        print "ERROR:::: Parent GP cannot be WP!!",gp_parent
        sys.exit()
    if tree_with_wps[node][2] == []:
        print "No Children here!!",node
        return Tcsr

    #if node_type == 'gp':
    for x in tree_with_wps[node][2]: 
        #print "processing node ->", x
        x_type = x.split(',')[0]
        x_index = int(x.split(',')[1])
        if x_type == 'wp':
            print "wp processing  ->", x
            Tcsr = build_Tcsr(x,tree_with_wps,Tcsr,gp_parent)
        else:
            #print "Tcsr",Tcsr
            #print "gp processing - >",x,gp_parent_index
            if (x_index < gp_parent_index):
                print "updating TCSR for nodes",x_index,gp_parent_index
                Tcsr[x_index][gp_parent_index] = int(tree_with_wps[x][3] - tree_with_wps[gp_parent][3])
            else:
                print "updating TCSR for nodes*",gp_parent_index,x_index
                Tcsr[gp_parent_index][x_index] = int(tree_with_wps[x][3] - tree_with_wps[gp_parent][3])

            #gp_parent = x
            #print Tcsr
            
            Tcsr = build_Tcsr(x,tree_with_wps,Tcsr,x)


    return Tcsr


# def print_mst_links(node_id,tree_dict,links_dict):
    
#     # print "tree dict",tree_dict
#     # print "node_id",node_id

#     for x in tree_dict[node_id][2]:
#         print "childrens",x,node_id
#         links_dict.update({node_id:x})
#         links_dict = print_mst_links(x,tree_dict,links_dict)
#     return links_dict







def dijkstra(graph, initial):
    visited = {initial: 0}

    nodes = set(graph.nodes)
    path = {}

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node
        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge in graph.edges[min_node]:
            try:
                weight = current_weight + graph.distances[(min_node, edge)]
            except:
                continue
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    return visited, path


def shortest_path(graph, origin, destination):
    visited, paths = dijkstra(graph, origin)
    full_path = deque()
    _destination = paths[destination]

    while _destination != origin:
        full_path.appendleft(_destination)
        _destination = paths[_destination]

    full_path.appendleft(origin)
    full_path.append(destination)

    return visited[destination], list(full_path)

# if __name__ == '__main__':
def spt(l,bhq,flag=0):
    graph = Graph()
    r = len(l)
    k= list()
    for t in range(0,r):
        k.append(str(t))
    #print "calling spt ================="
    ##print (k[1] +k[2])
    for node in k:
        graph.add_node(node)
    #print "r=",r
    for d in range(0,r):
    	##print "'" + str(l[d][0])+ "'", str(l[d][1]), l[d][2]
        # graph.add_edge("'" + str(l[d][0]) + "'", "'" +str(l[d][1]) + "'", l[d][2])
        graph.add_edge(str(l[d][0]),str(l[d][1]), l[d][2])

    kk= list()
    for t in range(0,r):
        # kk.append("'" + str(t) + "'")
        kk.append(str(t))
    more_than_sixty_count= 0
    count = 0
    #print "kklen", len(kk)
    all_links_in_mst = []
    error_nodes = []
    tree_dist = []
    total_dist_bhq_to_nodes = 0
    for node in range(len(kk)/2+1):
        #print "bhq=",bhq
    	#print "node = ",node
    	# if(node != str(bhq[0])):
        if(int(str(node)) != int(str(bhq))):
            count+=1
            #print "CHECKING", node, bhq,count
    		##print(shortest_path(graph,str(31),node))
            #if shortest_path(graph,str(bhq[0]),node)[0] < MAX_ROUTE_LENGTH:
            #mst_link = shortest_path(graph,str(bhq),node)
            try:
                mst_link = shortest_path(graph,str(bhq),str(node))
                ##print mst_link
                #sys.exit()
                tree_dist.append(mst_link[0])
                total_dist_bhq_to_nodes += mst_link[0]
                #[x for x in tree_dist if tree_dist < 1000000]
            except KeyError, e:    
                error_nodes.append(node)
                #print "keyerror for node",node,"error ",e
                continue     
            #print mst_link

            all_links_in_mst.append(mst_link[1])
            if mst_link[0] > MAX_ROUTE_LENGTH and mst_link[0] < 1000000: more_than_sixty_count+=1
            ##print(shortest_path(graph,str(bhq[0]),node))
                ##print mst_link
            # less_than_sixty_count+=1
        else:
            tree_dist.append(0)
    if (flag == 1):
        return tree_dist,more_than_sixty_count
    else:
        #print ("Total distance return")
        #return total_dist_bhq_to_nodes
        return more_than_sixty_count
        
    # #print "no of blocks within 60km are ",less_than_sixty_count,"total blocks",count
    # #print "all links in mst" 
    # #print total_dist_bhq_to_nodes
    # f = open('mstlinks', 'w')
    # for link in all_links_in_mst:
    #     f.write(",".join(link))
    #     f.write("\n")
    #get_leaf_nodes(all_links_in_mst,count)
 

def get_leaf_nodes(all_links_in_mst,count):
    #print "leaf nodes "
    leaf_nodes = []
    for node in range(1,count):
        count = 0
        for link in all_links_in_mst:
            if str(node) in link:
                count+=1
            if count == 2:
                break
            else:
                continue
        if count == 1:
            leaf_nodes.append(str(node))                
    #print leaf_nodes


def prun_leaf_wps(tree_dict): #removes wp's which are leaf nodes

    flag = True
    while flag:
        flag = False
        for x in tree_dict.keys():
            x_type = x.split(',')[0]
            if (x_type == 'wp' and len(tree_dict[x][2])==0): #wp is a leaf node and we need to remove it
                flag = True #Need one more iteration
                x_parent = tree_dict[x][0]
                # print x,x_parent
                tree_dict[x_parent][2] = [y for y in tree_dict[x_parent][2] if y != x] #remove x from the children list of its parent
                del tree_dict[x]
    return tree_dict



def fibre_saved_if_wireless(tree_dict,node): #returns length of fibre saved if the gp is connected wirelessly
    
    node_type = node.split(',')[0]
    node_id = int(node.split(',')[1])

    fibre_saved = 0
    flag = True
    curr_node = node

    if node_type == 'wp':
        print "fibre_saved_if_wireless:::: WP is not a valid input!!",node
        sys.exit()
    elif tree_dict[node][2] != []:
        print "fibre_saved_if_wireless:::: node is not a leaf node!!",node
        sys.exit()
    else:
        while flag:
            fibre_saved += tree_dict[curr_node][1]
            parent = tree_dict[curr_node][0]
            
            if (len(tree_dict[parent][2]) > 1) or (parent.split(',')[0] == 'gp'): #stop if parent has more children or if it is a GP
                flag = False
            else:
                curr_node = parent

    return fibre_saved


                

def handle_no_road_cases(tree_dict,gp_latlng_list,wp_latlng_list,blk_dist_map,state,dist):
    #returns updated tree_dict and satellite recommendations

    flag = True
    satellite_reco_list = list()

    while flag:
        flag = False
        for x in tree_dict.keys():
            if tree_dict[x][3] < 1000000 or len(tree_dict[x][2]) > 0:
                continue
            else:
                flag = True
                x_type = x.split(',')[0]
                x_id = int(x.split(',')[1])
                if x_type == 'gp':
                    x_latlng = gp_latlng_list[blk_dist_map[x_id]]
                else:
                    x_latlng = wp_latlng_list[x_id]

                min_arial_dist = 10000000000000000000
                for y in tree_dict.keys():
                    if x == y or tree_dict[y][3] >= 1000000:
                        continue
                    else:
                        y_type = y.split(',')[0]
                        y_id = int(y.split(',')[1])
                        if y_type == 'gp':
                            y_latlng = gp_latlng_list[blk_dist_map[y_id]]
                        else:
                            y_latlng = wp_latlng_list[y_id]

                        xy_dist = latlongdist(x_latlng,y_latlng)
                        if xy_dist < min_arial_dist:
                            min_arial_dist = xy_dist
                            min_dist_id = y

                y = min_dist_id
                y_type = y.split(',')[0]
                y_id = int(y.split(',')[1])
                
                
                if min_arial_dist <= 5000 and satellite_recommendation(x_latlng,y_latlng,state,dist): #Update tree dictionary
                    x_parent = tree_dict[x][0]
                    if x_parent != y or tree_dict[y][0] == None:
                        tree_dict[x_parent][2] = [z for z in tree_dict[x_parent][2] if z != x] 
                        #remove x from children list of its parent (detach x from its parent)
                        tree_dict[y][2].append(x) #add x to children list of y (attach x to y)
                        tree_dict[x][0] = y # make y x's parent
                        tree_dict[x][1] = min_arial_dist #update x's link length
                        tree_dict[x][2] = [] # x has no children. Not required, put for safety
                        tree_dict[x][3] = tree_dict[y][3]+min_arial_dist # update x's route length from bhq
                    else:
                        print "handle_no_road_cases:::: This can not happen!!!",x,y,tree_dict
                        sys.exit()
                else:
                    satellite_reco_list.append(x) #recomment x for satellite
                    x_parent = tree_dict[x][0] 
                    tree_dict[x_parent][2] = [z for z in tree_dict[x_parent][2] if z != x] # detach x from its parent
                    del tree_dict[x] #remove x from the tree

    return tree_dict,satellite_reco_list



def satellite_recommendation(to_latlng,from_latlng,state,dist):
        # returns True to elevation is good, false otherwise
        elev_threshold = 500
        
        elevation = get_elevation_profile([to_latlng[0],to_latlng[1],from_latlng[0],from_latlng[1]],state,dist)
        
        if (abs(max(elevation) - min(elevation)) <= elev_threshold ):
            return True 

        return False



def get_tree_distance(from_node,to_node,tree_dict):
    #Returns the distance along the tree between nodes from_node and to_node
    #Should not get unconnected nodes
    
    if from_node == to_node:
        return 0

    from_node_ancestors = [from_node]
    to_node_ancestors = [to_node]

    last_from_node_ancestor = from_node
    last_to_node_ancestor = to_node

    #k = 0
    common_ancestor = None

    for k in range(len(tree_dict.keys())):
        
        parent = tree_dict[last_from_node_ancestor][0] #Process from node
        #print "from node parent == ",parent
        if parent != None: #lowest common ancestor found
            if parent in to_node_ancestors:
                common_ancestor = parent
                break
            else:
                last_from_node_ancestor = parent #Update the last ancestor processed
                from_node_ancestors.append(parent) #Update the ancestors' list

        parent = tree_dict[last_to_node_ancestor][0] #Process to node
        #print "to node parent == ",parent
        
        if parent != None: #lowest common ancestor found
            if parent in from_node_ancestors:
                common_ancestor = parent
                break
            else:
                last_to_node_ancestor = parent #Update the last ancestor processed
                to_node_ancestors.append(parent) #Update the ancestors' list

    if common_ancestor == None:
        print "get_tree_distance:::: Common Ancestor can not be None!!!",from_node,to_node
        sys.exit()
    else:
        return tree_dict[from_node][3]+tree_dict[to_node][3]-2*tree_dict[common_ancestor][3] #returns tree distance



def get_te_route_length(tree_dict,te_id):
    #Returns dictionary {node_id:route_length from te_id}

    #print "get_te_route_length:::: te_id = ",te_id
    route_length_dict = dict()

    if tree_dict[te_id][0] == None and len(tree_dict[te_id][2]) > 0: 
    # te_id is the original bhq
        for x in tree_dict.keys():
            route_length_dict.update({x:tree_dict[x][3]})
    else: #some other TE
        for x in tree_dict.keys():
            route_length_dict.update({x:get_tree_distance(te_id,x,tree_dict)})

    #print "get_te_route_length:::: Route Length Dict = ",route_length_dict, len(route_length_dict)

    return route_length_dict



def make_rooted_tree(node,tree_dict,nodes_tobe_connected,olt_tree,process_nodes_list):

    #Node - current node from where links will be made
    #tree_dict - Original tree rooted at bhq
    #nodes_tobe_connected - list of [nodes,distance from current olt] those are closest to the current olt
    #olt_tree - object being built recursievely and will eventually be returned
    #process_node_lists - list of candidate nodes to be considerd
    if node not in olt_tree.keys():
        print "make_rooted_tree:::: Node not in tree!!", node,olt_tree
        sys.exit()

    for x in process_nodes_list:
        temp_list = [y for y in nodes_tobe_connected if y[0] == x]
        if len(temp_list) == 1: #Add node x to the tree
            process_x_list = [y for y in tree_dict[x][2] if y != node]
            
            if x in tree_dict[node][2]:
                olt_tree.update({x:[node,tree_dict[x][1],[],float(temp_list[0][1])]})
            elif node in tree_dict[x][2]:
                olt_tree.update({x:[node,tree_dict[node][1],[],float(temp_list[0][1])]})
                process_x_list.append(tree_dict[x][0])
            else:
                sys.exit()
            olt_tree[node][2].append(x)
            olt_tree = make_rooted_tree(x,tree_dict,nodes_tobe_connected,olt_tree,process_x_list)
            #return olt_tree
        elif len(temp_list) == 0:
            #return olt_tree
            print "Do nothing!!"
        else:
            print "make_rooted_tree:::: Not possible!!!"
            sys.exit()

    return olt_tree


def remove_nodes_from_tree(tree_dict,remove_list):

    flag = True
    tree_nodes = tree_dict.keys()
    while flag:
        flag = False
        for x in remove_list:
            if x not in tree_nodes:
                continue
            if tree_dict[x][0] == None:
                print "ERROR::Can not remove root!!!!!"
                sys.exit()
            elif tree_dict[x][2] == []: #x is a leaf node
                flag = True
                x_parent = tree_dict[x][0]
                tree_dict[x_parent][2] = [u for u in tree_dict[x_parent][2] if u!= x]
                del tree_dict[x]
                remove_list = [u for u in remove_list if u != x]
        tree_dict = prun_leaf_wps(tree_dict)

    return tree_dict
                







