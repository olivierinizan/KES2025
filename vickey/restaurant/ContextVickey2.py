from itertools import product

FILTERED_PROPERTIES = []

def load_triples(filename):
    triples = []
    with open (filename) as input_file:
        lines = input_file.readlines()
        for line in lines:
            line_strip = line.strip().split('\t')
            triples.append((line_strip[0],line_strip[1],line_strip[2]))
    return triples

def load_films(triples):
    dict_of_film = {}
    for s,p,o in triples:
        if s not in dict_of_film:
            dict_of_film[s] = []
        dict_of_film[s].append((s,p,o))
    return dict_of_film

def load_triples_to_dict(filename):
    dict_of_ids = {}
    with open (filename) as input_file:
        lines = input_file.readlines()
        for line in lines:
            line_strip = line.strip().split('\t')
            triple = (line_strip[0],line_strip[1],line_strip[2])
            if triple[0] not in dict_of_ids:
                dict_of_ids[triple[0]] = []
            dict_of_ids[triple[0]].append(triple)    
    return dict_of_ids

def load_gold(filename):
    gold_ids = []
    with open (filename) as input_file:
        lines = input_file.readlines()
        for line in lines:
            line_strip = line.strip().split('\t')
            if line_strip[0] != line_strip[1]:
                raise Exception("Gold std ids are different")
            gold_ids.append(line_strip[0])
    return gold_ids

def extract_gold_from_dict():
    pass

def get_properties(instance):
    properties = set()
    for s,p,o in instance:
        if p not in properties:
            properties.add(p)
    return properties

def get_property_values(prop,instance):
    values = []
    for s,p,o in instance:
        if p == prop:
            values.append(o)
    return values

def compute_shared_unshared_properties(pair):
    i1_properties = get_properties(pair[0])
    i2_properties = get_properties(pair[1])
    
    shared_properties = i1_properties & i2_properties
    unshared_properties = i1_properties ^ i2_properties

    return shared_properties, unshared_properties

def compute_pair_of_instances(ids_DB,ids_YAGO):
    return product(ids_DB,ids_YAGO)

def compute_epsilon_delta_omega():
    triples_DB = load_triples("DB_Film")        
    triples_YAGO = load_triples("YAGO_Film")        

    dict_of_DB_film = load_films(triples_DB)
    dict_of_YAGO_film = load_films(triples_YAGO)
    
    ids_DB = dict_of_DB_film.keys()
    ids_YAGO = dict_of_YAGO_film.keys()

    ids_DB_sorted = sorted(ids_DB)
    ids_YAGO_sorted = sorted(ids_YAGO)

    # sort ids and keep 100 first
    # warn: the 100 first film are not necessary the same between the 2 lists 

    #pair_of_ids = compute_pair_of_instances(ids_DB_sorted[:10000],ids_YAGO_sorted[:10000])
    #pair_of_ids = compute_pair_of_instances(ids_DB_sorted[:5000],ids_YAGO_sorted[:5000])
    pair_of_ids = compute_pair_of_instances(ids_DB_sorted[:1000],ids_YAGO_sorted[:1000])
    #pair_of_ids = compute_pair_of_instances(ids_DB_sorted[:100],ids_YAGO_sorted[:100])

    all_contexts = []

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
        all_contexts.append([(pair_ids[0],pair_ids[1]),cwa_context])

    return all_contexts

def index_context(all_context):
    context_indexed = {}
    for item in all_context:
        pair = item[0]
        context = str(item[1])
        if context not in context_indexed:
            context_indexed[context] = []
        context_indexed[context].append(pair)
    return context_indexed

# TODO: we not need a list of list anymore
def index_subcontext(context_indexed,is_epslion_beta_omega):
    subcontext_indexed = {}
    for context_str in context_indexed:
        context = eval(context_str)
        subcontext = context[is_epslion_beta_omega]
        subcontext_str = str(subcontext)
        if subcontext_str not in subcontext_indexed:
            subcontext_indexed[subcontext_str] = [[],[]]
        subcontext_indexed[subcontext_str][0] = subcontext_indexed[subcontext_str][0] + context_indexed[context_str]
    return subcontext_indexed

def _index_subcontext(context_indexed,is_epslion_beta_omega):
    subcontext_indexed = {}
    for context_str in context_indexed:
        context = eval(context_str)
        subcontext = context[is_epslion_beta_omega]
        subcontext_str = str(subcontext)
        if subcontext_str not in subcontext_indexed:
            subcontext_indexed[subcontext_str] = [[],[]]
        subcontext_indexed[subcontext_str][0] = subcontext_indexed[subcontext_str][0] + context_indexed[context_str]
        subcontext_indexed[subcontext_str][1].append(context_str)  
    return subcontext_indexed


# we do a plus, usefull when id contexts > 10
def plus(level_times_10,index_subc):
    if index_subc >= 10:
        return int(str(int(level_times_10/10)) + str(index_subc))
    else:
        return level_times_10 + index_subc

def level_subcontext(subcontext_indexed):
    levels = {}
    max_level = 0
    for subcontext_str in subcontext_indexed:
        subcontext = eval(subcontext_str)
        level = len(subcontext)

        if level == 0: continue
        if level > max_level: max_level = level
        
        if level not in levels:
            levels[level] = []
        levels[level].append(subcontext)

    for i in range(max_level+1)[1:]:
        if i not in levels:
            levels[i] = []

    return levels


# return the number of instances for each subcontext
def count_pair_for_levelled_subcontexts(subcontext_indexed,subcontext_levelled):
    pair_count = {}
    pair_index = {}
    for level in subcontext_levelled:
        if len (subcontext_levelled[level]) != 0:
            for subcontext in subcontext_levelled[level]:
                subcontext_id = str(level * 10 + subcontext_levelled[level].index(subcontext))
                pair_list = subcontext_indexed[str(subcontext)][0]
                count = len(pair_list)
                pair_count[subcontext_id] = count
                pair_index[subcontext_id] = pair_list
    return pair_count, pair_index

def count_pair_for_levelled_subcontexts_100(subcontext_indexed,subcontext_levelled):
    pair_count = {}
    pair_index = {}
    for level in subcontext_levelled:
        if len (subcontext_levelled[level]) != 0:
            for subcontext in subcontext_levelled[level]:
                subcontext_id = str(plus(level * 10,subcontext_levelled[level].index(subcontext)))
                pair_list = subcontext_indexed[str(subcontext)][0]
                count = len(pair_list)
                pair_count[subcontext_id] = count
                pair_index[subcontext_id] = pair_list
    return pair_count, pair_index


def partition_all_context(all_context):
    context_partionned = {}
    for p in ("P1","P2","P3","P4","P5","P6","P7","P8"):
        context_partionned[p] = []
    for l in all_context:
        pair = l[0]
        context = l[1]
        if is_P1(context):
            context_partionned["P1"].append(l)
        elif is_P2(context):
            context_partionned["P2"].append(l)
        elif is_P3(context):
            context_partionned["P3"].append(l)
        elif is_P4(context):
            context_partionned["P4"].append(l)
        elif is_P5(context):
            context_partionned["P5"].append(l)
        elif is_P6(context):
            context_partionned["P6"].append(l)
        elif is_P7(context):
            context_partionned["P7"].append(l)
        elif is_P8(context):
            context_partionned["P8"].append(l)
    return context_partionned


def partition_context_indexed(context_indexed):
    context_partionned = {}
    for p in ("P1","P2","P3","P4","P5","P6","P7","P8"):
        context_partionned[p] = {}

    for context_str in context_indexed:
        context = eval(context_str)
        if is_P1(context):
            if context_str not in context_partionned["P1"]:
                context_partionned["P1"][context_str] = []
            context_partionned["P1"][context_str] = context_partionned["P1"][context_str] + context_indexed[context_str]
        elif is_P2(context):
            if context_str not in context_partionned["P2"]:
                context_partionned["P2"][context_str] = []
            context_partionned["P2"][context_str] = context_partionned["P2"][context_str] + context_indexed[context_str]
        elif is_P3(context):
            if context_str not in context_partionned["P3"]:
                context_partionned["P3"][context_str] = []
            context_partionned["P3"][context_str] = context_partionned["P3"][context_str] + context_indexed[context_str]
        elif is_P4(context):
            if context_str not in context_partionned["P4"]:
                context_partionned["P4"][context_str] = []
            context_partionned["P4"][context_str] = context_partionned["P4"][context_str] + context_indexed[context_str]
        elif is_P5(context):
            if context_str not in context_partionned["P5"]:
                context_partionned["P5"][context_str] = []
            context_partionned["P5"][context_str] = context_partionned["P5"][context_str] + context_indexed[context_str]
        elif is_P6(context):
            if context_str not in context_partionned["P6"]:
                context_partionned["P6"][context_str] = []
            context_partionned["P6"][context_str] = context_partionned["P6"][context_str] + context_indexed[context_str]
        elif is_P7(context):
            if context_str not in context_partionned["P7"]:
                context_partionned["P7"][context_str] = []
            context_partionned["P7"][context_str] = context_partionned["P7"][context_str] + context_indexed[context_str]
        elif is_P8(context):
            if context_str not in context_partionned["P8"]:
                context_partionned["P8"][context_str] = []
            context_partionned["P8"][context_str] = context_partionned["P8"][context_str] + context_indexed[context_str]
    return context_partionned

def is_epsilon_empty(context):
    return len(context[0]) == 0

def is_delta_empty(context):
    return len(context[1]) == 0

def is_omega_empty(context):
    return len(context[2]) == 0

def is_P1(context):
    return is_epsilon_empty(context) and is_delta_empty(context) and is_omega_empty(context)

def is_P2(context):
    return is_epsilon_empty(context) and is_delta_empty(context) and not is_omega_empty(context)

def is_P3(context):
    return is_epsilon_empty(context) and not is_delta_empty(context) and is_omega_empty(context)

def is_P4(context):
    return is_epsilon_empty(context) and not is_delta_empty(context) and not is_omega_empty(context)

def is_P5(context):
    return not is_epsilon_empty(context) and is_delta_empty(context) and is_omega_empty(context)

def is_P6(context):
    return not is_epsilon_empty(context) and is_delta_empty(context) and not is_omega_empty(context)

def is_P7(context):
    return not is_epsilon_empty(context) and not is_delta_empty(context) and is_omega_empty(context)

def is_P8(context):
    return not is_epsilon_empty(context) and not is_delta_empty(context) and not is_omega_empty(context)

def try_connect(current_subc,subc_visited,level_visited,current_subc_id,in_connected):
    link_done = False
    for subc in subc_visited:
        id_subc = str(level_visited) + str(subc_visited.index(subc))
        if set(subc).issubset(set(current_subc)):
            if id_subc not in in_connected:
                in_connected[id_subc] = []
            in_connected[id_subc].append(current_subc_id)
            link_done = True

    return link_done

def try_connect_100(current_subc,subc_visited,level_visited,current_subc_id,in_connected):
    link_done = False
    for subc in subc_visited:
        id_subc = str(level_visited) + str(subc_visited.index(subc))
        if set(subc).issubset(set(current_subc)):
            if id_subc not in in_connected:
                in_connected[id_subc] = []
            in_connected[id_subc].append(current_subc_id)
            link_done = True

    return link_done


def connect(current_level,all_levels,in_connected):
    current_subcs = all_levels[current_level]
    levels_visited = list(range(current_level))[1:]
    levels_visited.reverse()

    for current_subc in current_subcs:
        current_subc_id = str(current_level) + str(current_subcs.index(current_subc))
    # we try to connect the top levels to the current one
        for level_visited in levels_visited:
            subcs_visited = all_levels[level_visited]
            if try_connect(current_subc,subcs_visited,level_visited,current_subc_id,in_connected):
                break

def connect_100(current_level,all_levels,in_connected):
    current_subcs = all_levels[current_level]
    levels_visited = list(range(current_level))[1:]
    levels_visited.reverse()

    for current_subc in current_subcs:
        current_subc_id = str(current_level) + str(current_subcs.index(current_subc))
    # we try to connect the top levels to the current one
        for level_visited in levels_visited:
            subcs_visited = all_levels[level_visited]
            if try_connect(current_subc,subcs_visited,level_visited,current_subc_id,in_connected):
                break

# we do not use this init anymore ...
def init_count_connected(connected_subcontexts,pair_count_levelled):
    count_connected_init = {}
    for subc in pair_count_levelled:
        nb_connected = 0
        nb_specific = pair_count_levelled[subc]
        if subc in connected_subcontexts:
            nb_connected = len(connected_subcontexts[subc])
        count_connected_init[subc] = [nb_connected,nb_specific,nb_specific]
    return count_connected_init    

def nb_levels_minus_1(connected_subcontexts):
    nb = max(connected_subcontexts)
    return nb[0]

def extract_levels(connected_subcontexts,level):
    levels = []
    for key in connected_subcontexts:
        if key.startswith(level) and key not in levels:
            levels.append(key)
    return levels

def extract_nodes_and_edges(connected_subcontexts):
    nodes = []
    edges = []
    for subc1 in connected_subcontexts:
        if subc1 not in nodes:
            nodes.append(subc1)
        
        for subc2 in connected_subcontexts[subc1]:
            if subc2 not in nodes:
                nodes.append(subc2)
            edges.append((subc1,subc2))
    nodes.sort()
    return nodes, edges

def replace_nodes_and_edges(nodes,edges,pair_levelled_count,prefix=""):
    replacer = pair_levelled_count.get
    new_nodes = [prefix + n+"/"+ str(replacer(n)) for n in nodes]
    new_edges = [ ( prefix + t[0] + "/" + str(replacer(t[0])), prefix + t[1] + "/" + str(replacer(t[1])) ) for t in edges]
    return new_nodes,new_edges

def replace_subc_ids(pair_index,pair_levelled_count,prefix=""):
    pair_index_replaced = {}
    for subc_id in pair_index:
        new_subc_id = prefix + subc_id + "/" + str(pair_levelled_count[subc_id])
        pair_index_replaced[new_subc_id] = pair_index[subc_id]
    return pair_index_replaced

def count_pair_for_2_connected_subcontext(levels,connected_subcontexts,count_connected):
    for subc in levels:
        nb_pair_connected = 0
        for connected_subc in connected_subcontexts[subc]:
            nb_pair_connected = nb_pair_connected + count_connected[connected_subc][2]

        nb_pair_connected = nb_pair_connected + count_connected[subc][2]
        count_connected[subc][2] = nb_pair_connected

def link_2_graph(nodes_graph1,index1,nodes_graph2,index2):
    edges_to_add = []
    for node1 in nodes_graph1:
        for node2 in nodes_graph2:
            set_item1 = set(index1[node1])
            set_item2 = set(index2[node2])
            if len(set_item1 & set_item2) != 0:
                edges_to_add.append((node1,node2,len(set_item1 & set_item2)))
    return edges_to_add

# it seems that we do not need to count connetced
def count_pair_for_connected_subcontexts(connected_subcontexts,count_connected):
    # obtain the list of levels
    nb_level_int = int(nb_levels_minus_1(connected_subcontexts))
    l_nb_level_str= []
    for nb in range(nb_level_int):
        l_nb_level_str.append(str(nb+1))

    for level_number in reversed(l_nb_level_str):
        current_levels = extract_levels(connected_subcontexts,level_number)
        count_pair_for_2_connected_subcontext(current_levels,connected_subcontexts,count_connected)

def inverse_connected(connected_subcontexts):
    inverse_connected = {}
    for subc1 in connected_subcontexts:
        for subc2 in connected_subcontexts[subc1]:
            if subc2 not in inverse_connected:
                inverse_connected[subc2] = []
            inverse_connected[subc2].append(subc1)    
    return inverse_connected 

def get_x_y_z_for_scatter_plot(all_context):
    pairs = []
    x = []
    y = []
    z = []
    for l in all_context:
        pair = l[0]
        context = l[1]
        pairs.append(pair)
        # len epsilon
        x.append(len(context[0]))
        # len delta
        y.append(len(context[1]))
        # len omega
        z.append(len(context[2]))
    return pairs,x,y,z

def compute_s_for_scatter_plot(serie1,serie2):
    count = {}
    s = [0] * len(serie1)
    for i in range(len(serie1)):
        key = str(serie1[i]) + "|" +str(serie2[i])
        if key not in count:
            count[key] = 0
        count[key] = count[key] + 1
    
    for i in range(len(serie1)):
        key = str(serie1[i]) + "|" + str(serie2[i])
        s[i] = count[key] 
    
    return s

def compute_s3_for_scatter_plot(serie1,serie2,serie3):
    count = {}
    s = [0] * len(serie1)
    for i in range(len(serie1)):
        key = str(serie1[i]) + "|" + str(serie2[i]) + "|" + str(serie3[i])
        if key not in count:
            count[key] = 0
        count[key] = count[key] + 1
    
    for i in range(len(serie1)):
        key = str(serie1[i]) + "|" + str(serie2[i]) + "|" + str(serie3[i])
        s[i] = count[key] 
    
    return s



def count_pair_in_partition(partition):
        count = 0
        for context in partition:
            count = count + len(partition[context])
        return count

def reindex_subcontext_with_filter(subc_indexed,len_filter,index_on_epsilon_delta_omega):
    out_subc_index = {}
    for str_subc in subc_indexed:
        current_subc = eval(str_subc)
        if len(current_subc) != len_filter:
            continue
        
        current_pairs = subc_indexed[str_subc][0]
        current_contexts = subc_indexed[str_subc][1]
   
        if len(current_pairs) != len(current_contexts):
            print()
            print(len(current_pairs))
            print(len(current_contexts))
            print(current_subc)


        assert(len(current_pairs) == len(current_contexts))

        for i in range(len(current_contexts)):
            current_pair = current_pairs[i]
            current_context = current_contexts[i]
            new_subc_key = str(eval(current_context)[index_on_epsilon_delta_omega])

            if new_subc_key not in out_subc_index:
                out_subc_index[new_subc_key] = [[],[]]
            
            out_subc_index[new_subc_key][0].append(current_pair)
            out_subc_index[new_subc_key][1].append(current_context)

    return out_subc_index
