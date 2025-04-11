from ContextVickey2 import *
import numpy as np
import matplotlib.pyplot as plt

def compute_edo_for_a_pair(i1,i2,id_i1,id_i2,all_contexts):
        # epsilon: the set of properties with the same values
        # delta: the set of properties with different values
        # omega: the set of unshared properties
        epsilon, delta, omega = [],[],[]
        shared,unshared = compute_shared_unshared_properties((i1,i2))

        i1_properties = get_properties(i1)
        i2_properties = get_properties(i2)

        # shared and unsahred properties must cover all properties
        assert(set(list(i1_properties) + list(i2_properties)) == set(list(shared) + list(unshared))) 

        # for each property in shared
        for p in shared:
            # filter properties
            if p in FILTERED_PROPERTIES:
                continue

            # list of values for instances x and y     
            i1_list_of_values = get_property_values(p,i1)
            i2_list_of_values = get_property_values(p,i2)
            
            # we consider all properties as data properties
            i1_set_of_values = set(i1_list_of_values)
            i2_set_of_values = set(i2_list_of_values)

            i1_and_i2 = i1_set_of_values & i2_set_of_values
            i1_xor_i2 = i1_set_of_values ^ i2_set_of_values
 
            if len(i1_and_i2) != 0:
                epsilon.append(p)
            if len(i1_xor_i2) != 0:
                delta.append(p)
            # we can not have both sets empty 
            if len(i1_and_i2) == 0 and len(i1_xor_i2) ==0:
                raise exception("values/properties exception")

        for p in unshared:
            # filter properties
            if p in FILTERED_PROPERTIES:
                continue
            omega.append(p)

        # sort epsilon, delta omega in oder to use them as dict keys
        epsilon.sort()
        delta.sort()
        omega.sort()

        cwa_context = (epsilon,delta,omega)
        # all properties must be present in the context
        flat_context = epsilon + delta + omega + FILTERED_PROPERTIES
        assert(set(list(i1_properties) + list(i2_properties)) == set(flat_context))
        all_contexts.append([(id_i1,id_i2),cwa_context])

def compute_edo(db_file,yago_file,gold_file):
    dict_of_DB = load_triples_to_dict(db_file)
    dict_of_YAGO = load_triples_to_dict(yago_file)

    gold_ids = load_gold(gold_file)

    all_contexts = []

    for gold_id in gold_ids:
        i1 = dict_of_DB[gold_id]
        i2 = dict_of_YAGO[gold_id]
        compute_edo_for_a_pair(i1,i2,gold_id,gold_id,all_contexts)
    return all_contexts
    

def compute_epsilon_delta_omega_book():
    return compute_edo("./Book/DB_Book","./Book/YAGO_book","./Book/Book.Goldstandard.txt.oi")

def compute_epsilon_delta_omega_actor():
    return compute_edo("./Actor/DB_Actor","./Actor/YAGO_actor","./Actor/Actor.Goldstandard.txt")

def compute_epsilon_delta_omega_university():
    return compute_edo("./University/DB_University","./University/YAGO_university","./University/University.Goldstandard.txt")

def compute_epsilon_delta_omega_mountain():
    return compute_edo("./Mountain/DB_Mountain","./Mountain/YAGO_mountain","./Mountain/Mountain.Goldstandard.txt")

def compute_epsilon_delta_omega_city():
    return compute_edo("./City/DB_City","./City/YAGO_city","./City/City.Goldstandard.txt")


def compute_and_partition_epsilon_delta_omega_file():
    triples_DB = load_triples("DB_Film")        
    triples_YAGO = load_triples("YAGO_Film")        

    dict_of_DB_film = load_films(triples_DB)
    dict_of_YAGO_film = load_films(triples_YAGO)
    
    ids_DB = dict_of_DB_film.keys()
    ids_YAGO = dict_of_YAGO_film.keys()

    ids_DB_sorted = sorted(ids_DB)
    ids_YAGO_sorted = sorted(ids_YAGO)

    print ()
    print (len(ids_DB_sorted))
    print (len(ids_YAGO_sorted))

    # sort ids and keep 100 first
    # warn: the 100 first film are not necessary the same between the 2 lists 

    #pair_of_ids = compute_pair_of_instances(ids_DB_sorted[:10000],ids_YAGO_sorted[:10000])
    #pair_of_ids = compute_pair_of_instances(ids_DB_sorted[:5000],ids_YAGO_sorted[:5000])
    #pair_of_ids = compute_pair_of_instances(ids_DB_sorted[:1000],ids_YAGO_sorted[:1000])
    pair_of_ids = compute_pair_of_instances(ids_DB_sorted[:100],ids_YAGO_sorted[:100])


    writer_P1 = open("./partitions/P1","w")
    writer_P2 = open("./partitions/P2","w")
    writer_P3 = open("./partitions/P3","w")
    writer_P4 = open("./partitions/P4","w")
    writer_P5 = open("./partitions/P5","w")
    writer_P6 = open("./partitions/P6","w")
    writer_P7 = open("./partitions/P7","w")
    writer_P8 = open("./partitions/P8","w")
 
    for pair_ids in pair_of_ids:
        i1 = dict_of_DB_film[pair_ids[0]]
        i2 = dict_of_YAGO_film[pair_ids[1]]
        # epsilon: the set of properties with the same values
        # delta: the set of properties with different values
        # omega: the set of unshared properties
        epsilon, delta, omega = [],[],[]
        shared,unshared = compute_shared_unshared_properties((i1,i2))


        i1_properties = get_properties(i1)
        i2_properties = get_properties(i2)
        
        # shared and unsahred properties must cover all properties
        assert(set(list(i1_properties) + list(i2_properties)) == set(list(shared) + list(unshared))) 

        # for each property in shared
        for p in shared:
            # filter properties
            if p in FILTERED_PROPERTIES:
                continue

            # list of values for instances x and y     
            i1_list_of_values = get_property_values(p,i1)
            i2_list_of_values = get_property_values(p,i2)
            
            # we consider all properties as data properties
            i1_set_of_values = set(i1_list_of_values)
            i2_set_of_values = set(i2_list_of_values)

            i1_and_i2 = i1_set_of_values & i2_set_of_values
            i1_xor_i2 = i1_set_of_values ^ i2_set_of_values
 
            if len(i1_and_i2) != 0:
                epsilon.append(p)
            if len(i1_xor_i2) != 0:
                delta.append(p)
            # we can not have both sets empty 
            if len(i1_and_i2) == 0 and len(i1_xor_i2) ==0:
                raise Exception("Values/Properties Exception")

        for p in unshared:
            # filter properties
            if p in FILTERED_PROPERTIES:
                continue
            omega.append(p)

        # sort epsilon, delta omega in oder to use them as dict keys
        epsilon.sort()
        delta.sort()
        omega.sort()

        cwa_context = (epsilon,delta,omega)
        # all properties must be present in the context
        flat_context = epsilon + delta + omega + FILTERED_PROPERTIES
        assert(set(list(i1_properties) + list(i2_properties)) == set(flat_context))

       
        if is_P1(cwa_context):
            writer_P1.write(str([(pair_ids[0],pair_ids[1]),cwa_context])+"\n")

        elif is_P2(cwa_context):
            writer_P2.write(str([(pair_ids[0],pair_ids[1]),cwa_context])+"\n")

        elif is_P3(cwa_context):
            writer_P3.write(str([(pair_ids[0],pair_ids[1]),cwa_context])+"\n")
            
        elif is_P4(cwa_context):
            writer_P4.write(str([(pair_ids[0],pair_ids[1]),cwa_context])+"\n")
            
        elif is_P5(cwa_context):
            writer_P5.write(str([(pair_ids[0],pair_ids[1]),cwa_context])+"\n")
            
        elif is_P6(cwa_context):
            writer_P6.write(str([(pair_ids[0],pair_ids[1]),cwa_context])+"\n")
            
        elif is_P7(cwa_context):
            writer_P7.write(str([(pair_ids[0],pair_ids[1]),cwa_context])+"\n")
            
        elif is_P8(cwa_context):
            writer_P8.write(str([(pair_ids[0],pair_ids[1]),cwa_context])+"\n")
            
        else:
            raise Exception("Partition Exception")

    writer_P1.close()
    writer_P2.close()
    writer_P3.close()
    writer_P4.close()
    writer_P5.close()
    writer_P6.close()
    writer_P7.close()
    writer_P8.close()

# the partition is from all_context and NOT from context indexed
def compute_subc_max_size(partition_from_all_context):
    max_epsilon = 0
    max_delta = 0
    max_omega = 0

    for l in partition_from_all_context:
        pair = l[0]
        context = l[1]
        
        epsilon_size = len(context[0])
        delta_size = len(context[1])
        omega_size = len(context[2])

        max_epsilon = max(epsilon_size,max_epsilon)
        max_delta = max(delta_size,max_delta)
        max_omega = max(omega_size,max_omega)

    return max_epsilon,max_delta,max_omega

# compute in
def compute_incompleteness(partition_from_all_context,max_omega_size=0):
    if max_omega_size == 0:
        max_epsilon_size,max_delta,max_omega_size = compute_subc_max_size(partition_from_all_context)
    ic = []
    for l in partition_from_all_context:
        omega_size = len(l[1][2])
        incompletness = _compute_incompletness(omega_size,max_omega_size)
        ic.append([l[0],len(l[1][2]),incompletness])
    return ic

def _compute_incompletness(len_omega,max_omega_size):
    #return len_omega/max_omega_size
    return len_omega

def compute_difference(partition_from_all_context):
    max_epsilon_size,max_delta_size,max_omega_size = compute_subc_max_size(partition_from_all_context)
    di = []
    for l in partition_from_all_context:
        delta_size = len(l[1][1])
        difference = _compute_difference(delta_size,max_delta_size)
        di.append([l[0],len(l[1][1]),difference])
    return di

def compute_identity(partition_from_all_context):
    max_epsilon_size,max_delta_size,max_omega_size = compute_subc_max_size(partition_from_all_context)
    ide = []
    for l in partition_from_all_context:
        epsilon_size = len(l[1][0])
        identity = _compute_identity(epsilon_size,max_epsilon_size)
        ide.append([l[0],len(l[1][0]),identity])
    return ide

def _compute_difference(len_delta,max_delta_size):
    return len_delta

def _compute_identity(len_epsilon,max_epsilon_size):
    return len_epsilon

# we temporarilly not use the filter in the 'with' functions
# we prefer apply the filters one by one 
def compute_difference_with_incompletness(partition_from_all_context,max_delta_size=0,max_omega_size=0):
    # TODO clean
    if max_omega_size == 0 and max_omega_size == 0:
        max_epsilon_size,max_delta_size,max_omega_size = compute_subc_max_size(partition_from_all_context)
    di_in = []
    for l in partition_from_all_context:
        pair = l[0]
        delta_size = len(l[1][1])
        omega_size = len(l[1][2])
        
        difference = _compute_difference(delta_size,max_delta_size)
        incompletness = _compute_incompletness(omega_size,max_omega_size)
        di_in.append([pair,delta_size,omega_size,difference,incompletness])

    return di_in 

def compute_identity_with_incompletness(partition_from_all_context,max_epsilon_size=0,max_omega_size=0):
    if max_epsilon_size == 0 and max_omega_size ==0:
        max_epsilon_size,max_delta_size,max_omega_size = compute_subc_max_size(partition_from_all_context)
    id_in = []
    for l in partition_from_all_context:
        pair = l[0]
        epsilon_size = len(l[1][0])
        omega_size = len(l[1][2])
        
        identity = _compute_identity(epsilon_size,max_epsilon_size)
        incompletness= _compute_incompletness(omega_size,max_omega_size)

        id_in.append([pair,epsilon_size,omega_size,identity,incompletness])
    return id_in

def compute_indescisivness_with_incompletness(partition_from_all_context,max_omega_size=0):
    if max_omega_size == 0:
        max_epsilon_size,max_delta_size,max_omega_size = compute_subc_max_size(partition_from_all_context)
    list_ind_inc = []
    for l in partition_from_all_context:
        pair = l[0]
        context = l[1]
        len_epsilon = len(context[0])
        len_delta = len(context[1])
        len_omega = len(context[2])

        current_ind = _compute_indesciviness(len_epsilon,len_delta)
        current_inc = _compute_incompletness(len_omega,max_omega_size) 
        
        list_ind_inc.append([pair,len_epsilon,len_delta,len_omega,current_ind,current_inc])

    return list_ind_inc


def keep_pair_filter1_filter2(metric1,metric2,filter_identity,filter_incompletness):
    if not (filter_identity[0] <= metric1 <= filter_identity[1]):
        return False
    elif not(filter_incompletness[0] <= metric2 <= filter_incompletness[1]):
        return False
    return True

def compute_indecisiveness(partition_from_all_context):
    list_in = []
    for l in partition_from_all_context:
        pair = l[0]
        context = l[1]
        len_epsilon = len(context[0])
        len_delta = len(context[1])
        current_in = _compute_indesciviness(len_epsilon,len_delta)
        list_in.append([pair,len_epsilon,len_delta,current_in])
    return list_in

def _compute_indesciviness(len_epsilon,len_delta):
    return (len_epsilon - len_delta) / (len_epsilon + len_delta)

def compute_filter_indicisvness():
    # 0.333 epsilon is x2 delta
    b = 1/3
    return (-b,b)
    # 0.5: epsilon is x3 delta
    #return (-0.5,0.5)
    # 0.6: epsilon is x4 delta
    i#return (-0.6,0.6)
    #return (-1,-0.6) (0.6,1)
    # 0.7: epsilon is x5.666666 delta
    #return (-0.7,0.7)
    # O.8: epsilon is x9 delta 
    #return (-0.8,0.8)

def compute_filter_identity(max_epsilon,k=3):
    return max_epsilon - (max_epsilon/k)

def compute_filter_difference(max_delta,k=3):
    return max_delta - (max_delta/k)

def compute_filter_incompletness(max_omega_size,k=3):
    return max_omega_size/k

# compute heavy nodes
# x: list of nodes ids
# y: lisy of weight
# return: list of nodes heavy nodes whose weight >= 80% total weight 
def compute_heavy_nodes(x,y,nb_all_pair,cutoff=0.8):
    pcent_80_of_all_pairs = round(nb_all_pair * cutoff)
    weight_80 = 0
    heavy_nodes = []
    for i in range(len(y)):
        weight_80 = weight_80 + y[i]
        heavy_nodes.append(x[i])
        if weight_80 >= pcent_80_of_all_pairs:
            break
    return heavy_nodes

def compute_heavy_nodes_ratio(heavy_nodes,pair_level_count):
    return len(heavy_nodes)/len(pair_level_count)

# compute connected component height and width
def compute_heavy_connected_size(in_cc):
    l_cc = list(in_cc)
    l_cc.sort()
    levels = {}
    max_width = 0
    for node in l_cc:
        level = node.split("/")[0][1]
        if level not in levels:
            levels[level] = []
        levels[level].append(node)

    for l in levels:
        max_width = max(max_width,len(levels[l]))

    return (len(levels),max_width)

# extract heavy nodes from lattice
def extract_heavy_nodes_from_lattice(heavy_nodes,in_connected):
    heavy_connected = {}
    assert_heavy = []
    # keys nodes
    for k_node in in_connected:
        if k_node in heavy_nodes:
            heavy_connected[k_node] = []
            assert_heavy.append(k_node)
            # values nodes
            for v_node in heavy_nodes:
                if v_node in in_connected[k_node]:
                    heavy_connected[k_node].append(v_node)
                    assert_heavy.append(v_node)
    # assert all heavy nodes are visited
    assert(len(assert_heavy) >= len(heavy_connected))
    
    return heavy_connected

def filter_context_for_genuine_or_artificial_individual(genuine_or_artificial_computed,partition):
    individuals = []
    contexts = []
    for l  in genuine_or_artificial_computed:
        individuals.append(l[0])
    for l in partition:
        if l[0] in individuals:
            contexts.append(l)
    return contexts

def plot_distribution(pair_level_count,path_to_plot):
    sorted_pair_level_count = dict(sorted(pair_level_count.items(), key=lambda item: item[1]))
    x = []
    y = []
    for key in sorted_pair_level_count:
        x.append(key)
        y.append(sorted_pair_level_count[key])
    fig, ax = plt.subplots()
    # plot omega distribution
    x.reverse()
    y.reverse()
    ax.bar(x,y)
    ax.set_ylabel('pair count')
    ax.set_title('nodes')
    ax.legend(title='nodes distribution')
    plt.savefig(path_to_plot)
    plt.close()
    return x,y

def index_subc_id(subc_levels):
    index = {} 
    for level in subc_levels:
        for subc in subc_levels[level]:
            key = str(level) + str(subc_levels[level].index(subc))
            index[key] = subc
    return index

def index_cc(cc,subc_id_indexed):
    index = {}
    for node_id in cc:
        subc_id = node_id.split("/")[0][1:]
        index[node_id] = subc_id_indexed[subc_id]
    return index

# index a partion with the pair
def index_partition(p):
    index = {}
    for l in p:
        key = str(l[0])
        index[key] = l
    return index

def sort_index_cc(index_cc):
    l_index_cc = []
    for key in index_cc:
        item1 = key.split("/")[0]
        item2 = key.split("/")[1]
        item3 = index_cc[key]

        l_index_cc.append([item1,int(item2),item3])

    l_index_cc.sort(key = lambda row: row[1])
    l_index_cc.reverse()
    return l_index_cc
