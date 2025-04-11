from ContextVickey2Gold import *
from ContextVickey2 import *
from rdflib import *
from itertools import product

# R1 Types
R1_ADDRESS = "http://www.okkam.org/ontology_restaurant1.owl#Address"
R1_RESTAURANT = "http://www.okkam.org/ontology_restaurant1.owl#Restaurant"
R1_CITY = "http://www.okkam.org/ontology_restaurant1.owl#City"

# R2 Types
R2_ADDRESS = "http://www.okkam.org/ontology_restaurant2.owl#Address"
R2_CATEGORY ="http://www.okkam.org/ontology_restaurant2.owl#Category"
R2_RESTAURANT = "http://www.okkam.org/ontology_restaurant2.owl#Restaurant"

# to find all:sameAs 
#FILTERED_PROPERTIES = ['type','has_address','category','name']
# otherwise ...
FILTERED_PROPERTIES = ['type']

def load_restaurant1_type():
    dict_of_address = {}
    dict_of_city = {}
    dict_of_restaurant = {}
    g = Graph()
    g.parse("restaurant1.rdf")
    for stmt in g:
        triple = (stmt[0],stmt[1],stmt[2])
        # create entry for each type
        if triple[1].endswith("#type"):
            if str(triple[2]) == R1_ADDRESS:
                if triple[0] not in dict_of_address:
                    dict_of_address[triple[0]] = []
            elif str(triple[2]) == R1_CITY:
                if triple[0] not in dict_of_city:
                    dict_of_city[triple[0]] = []
            elif str(triple[2]) == R1_RESTAURANT:
                if triple[0] not in dict_of_restaurant:
                    dict_of_restaurant[triple[0]] = []
            else:
                raise Exception("Load R1 type, unknonw type: " + triple[2])
    return dict_of_restaurant,dict_of_address,dict_of_city               
            
def load_restaurant1_instance(dict_of_restaurant,dict_of_address,dict_of_city):
    g = Graph()
    g.parse("restaurant1.rdf")
    for stmt in g:
        triple = (stmt[0],stmt[1],stmt[2])
        triple = replace_value_phone_number(triple)
        if triple[0] in dict_of_address:
            dict_of_address[triple[0]].append(triple)
        elif triple[0]  in dict_of_city:
            dict_of_city[triple[0]].append(triple)
        elif triple[0]  in dict_of_restaurant:
            dict_of_restaurant[triple[0]].append(triple)
        else:
            raise Exception("Load R1 instance, can not affect " + str(triple[0]) + \
                    " to an Adress, City or Restaurant")
 
def load_restaurant2_type():
    dict_of_address = {}
    dict_of_category = {}
    dict_of_restaurant = {}
    g = Graph()
    g.parse("restaurant2.rdf")
    for stmt in g:
        triple = (stmt[0],stmt[1],stmt[2])
        
        if triple[1].endswith("#type"):
            if str(triple[2]) == R2_ADDRESS:
                dict_of_address[triple[0]] = []
            elif str(triple[2]) == R2_CATEGORY:
                dict_of_category[triple[0]] = []
            elif str(triple[2]) == R2_RESTAURANT:
                dict_of_restaurant[triple[0]] = []
            else: 
                raise Exception("Load R2 type, unknonw type: " + triple[2])

    return dict_of_restaurant,dict_of_address,dict_of_category

def load_restaurant2_instance(dict_of_restaurant,dict_of_address,dict_of_category):
    g = Graph()
    g.parse("restaurant2.rdf")
    for stmt in g:
        triple = (stmt[0],stmt[1],stmt[2])
  
        # replace 'has_category' with 'category'
        triple = replace_property_has_category(triple) 
        # replace phone number
        triple = replace_value_phone_number(triple)
        if triple[0] in dict_of_address:
            dict_of_address[triple[0]].append(triple)
        elif triple[0]  in dict_of_category:
            dict_of_category[triple[0]].append(triple)
        elif triple[0]  in dict_of_restaurant:
            dict_of_restaurant[triple[0]].append(triple)
        else:
            raise Exception("Load R2 instance, can not affect " + str(triple[0]) + \
                    " to an Adress, Category or Restaurant")

def replace_property_has_category(triple):
    p = triple[1]
    if p == URIRef('http://www.okkam.org/ontology_restaurant2.owl#has_category'):
        p = URIRef('http://www.okkam.org/ontology_restaurant2.owl#category')
    return (triple[0],p,triple[2])

def replace_value_phone_number(triple):
    p = triple[1]
    o = triple[2]
    if p.endswith("#phone_number"):
        if "/ " in o:
            nb = o.replace("/ ","-")
            o = Literal(nb)
        elif "/" in triple[2]:
            nb = o.replace("/","-")
            o = Literal(nb)
    return (triple[0],p,o) 


def get_properties(instance):
    properties = set()
    for s,p,o in instance:
        if p not in properties:
            if "#" in p:
                p_hashtag = p.split("#")
                properties.add(p_hashtag[1])
            else:
                properties.add(p)
    return properties

def test_address_multivalued(d_restaurant):
    for r in d_restaurant:
        nb_p_has_address = 0
        for s,p,o in d_restaurant[r]:
            if p.endswith("#has_address"):
                nb_p_has_address = nb_p_has_address + 1
        if nb_p_has_address != 1:
            raise Exception("has_address property is multivalued")

def compute_edo_for_a_pair(i1,i2,id_i1,id_i2,d_category_r2,d_address_r1,d_address_r2,d_city_r1,all_contexts):
        # epsilon: the set of properties with the same values
        # delta: the set of properties with different values
        # omega: the set of unshared properties
        epsilon, delta, omega = [],[],[]
        shared,unshared = compute_shared_unshared_properties((i1,i2))

        # only suffix not full name
        i1_properties = get_properties(i1)
        i2_properties = get_properties(i2)

        # shared and unsahred properties must cover all properties
        assert(set(list(i1_properties) + list(i2_properties)) == set(list(shared) + list(unshared))) 

        # for each property in shared
        for p in shared:

            # filter properties
            if p in FILTERED_PROPERTIES:
                continue
            # object properties
            if p == "category":
                if is_same_category(i1,i2,d_category_r2):
                    epsilon.append(p)
                else:
                    delta.append(p)
            elif p == "has_address":
                if is_same_address(i1,i2,d_address_r1,d_address_r2,d_city_r1):
                    epsilon.append(p)
                else:
                    delta.append(p)
            else: 
                # value property
                # list of values for instances x and y     
                # we need full property, not only prefix
                p1 = URIRef("http://www.okkam.org/ontology_restaurant1.owl#" + p)
                p2 = URIRef("http://www.okkam.org/ontology_restaurant2.owl#" + p)
                i1_list_of_values = get_property_values(p1,i1)
                i2_list_of_values = get_property_values(p2,i2)
                 
                # we consider all properties as data properties
                i1_set_of_values = set(i1_list_of_values)
                i2_set_of_values = set(i2_list_of_values)

                i1_and_i2 = i1_set_of_values & i2_set_of_values
                i1_xor_i2 = i1_set_of_values ^ i2_set_of_values
 
                if len(i1_and_i2) != 0:
                    epsilon.append(p)
                if len(i1_xor_i2) != 0:
                    delta.append(p)
 
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

def compute_edo(d_restaurant_r1,d_restaurant_r2,d_category_r2,d_address_r1,d_address_r2,d_city_r1):

    ids1 = list(d_restaurant_r1.keys())
    ids2 = list(d_restaurant_r2.keys())

    ids1_sorted = sorted(ids1)    
    ids2_sorted = sorted(ids2)    
 
    # cartesian product
    cartesian_product = product(ids1_sorted,ids2_sorted)

    # all contexts
    all_contexts = []

    for id1,id2 in cartesian_product:
        i1 = d_restaurant_r1[id1]
        i2 = d_restaurant_r2[id2]
        compute_edo_for_a_pair(i1,i2,id1,id2,d_category_r2,d_address_r1,d_address_r2,d_city_r1,all_contexts)
    
    return all_contexts

def compute_edo_gd(d_restaurant_r1,d_restaurant_r2,d_category_r2,d_address_r1,d_address_r2,d_city_r1):
    all_contexts = []
    prefix_r1 = "http://www.okkam.org/oaie/restaurant1-Restaurant"
    prefix_r2 = "http://www.okkam.org/oaie/restaurant2-Restaurant"
    for r in range(112):
        current_r1 = URIRef(prefix_r1 + str(r))
        current_r2 = URIRef(prefix_r2 + str(r))
        # missing restaurant only in r2
        if current_r2 not in d_restaurant_r2:
            print()
            print(str(current_r2))
            print("Not Found")
            continue
        r1 = d_restaurant_r1[current_r1]
        r2 = d_restaurant_r2[current_r2]
        compute_edo_for_a_pair(r1,r2,current_r1,current_r2,d_category_r2,d_address_r1,d_address_r2,d_city_r1,all_contexts) 
    return all_contexts

def compute_shared_unshared_properties(pair):
    i1_properties = get_properties(pair[0])
    i2_properties = get_properties(pair[1])
    
    shared_properties = i1_properties & i2_properties
    unshared_properties = i1_properties ^ i2_properties

    return shared_properties, unshared_properties

def get_properties(instance):
    properties = set()
    for s,p,o in instance:
        if p not in properties:
            p = p.split('#')[1]
            properties.add(p)
    return properties



def is_same_category(r1,r2,d_category_r2):
    # category in R1 is literal
    c_r1 = None
    for s,p,o in r1:
        if p == URIRef('http://www.okkam.org/ontology_restaurant1.owl#category'):
            c_r1 = o
    # category in R2 is object
    c_r2 = None
    for s,p,o in r2:
        if p == URIRef('http://www.okkam.org/ontology_restaurant2.owl#category'):
            c_r2 = o
    for s,p,o in d_category_r2[c_r2]:
        if p == URIRef('http://www.okkam.org/ontology_restaurant2.owl#name'):
            name_r2 = o
            break
    return c_r1 == name_r2    

def is_same_address(r1,r2,d_address_r1,d_address_r2,d_city_r1):
    d_r1 = None
    city_r1 = None
    street_r1 = None
    for s,p,o in r1:
        if p == URIRef('http://www.okkam.org/ontology_restaurant1.owl#has_address'):
            d_r1 = o
    c_r1 = None
    #for t in d_address_r1[d_r1]:
    #    print(t)
    for s,p,o in d_address_r1[d_r1]:
        if p == URIRef('http://www.okkam.org/ontology_restaurant1.owl#is_in_city'):
            c_r1 = o
            for s_c,p_c,o_c in  d_city_r1[c_r1]:
                if p_c == URIRef('http://www.okkam.org/ontology_restaurant1.owl#name'):
                    city_r1 = o_c
        elif p == URIRef('http://www.okkam.org/ontology_restaurant1.owl#street'):
            street_r1 = o
     
    d_r2 = None
    city_r2 = None
    street_r2 = None
    for s,p,o in r2:
        if p == URIRef('http://www.okkam.org/ontology_restaurant2.owl#has_address'):
            d_r2 = o
    for s,p,o in d_address_r2[d_r2]:
        if p == URIRef('http://www.okkam.org/ontology_restaurant2.owl#city'):
            city_r2 = o
        elif p == URIRef('http://www.okkam.org/ontology_restaurant2.owl#street'):
            street_r2 = o

    return city_r1 == city_r2 and street_r1 == street_r2

def is_same_phone_number(r1,r2):
    p_r1 = None
    for s,p,o in r1:
        if p == URIRef('http://www.okkam.org/ontology_restaurant1.owl#phone_number'):
            p_r1 = o
            break
    p_r2 = None
    for s,p,o in r2:
        if p == URIRef('http://www.okkam.org/ontology_restaurant2.owl#phone_number'):
            p_r2 = o
            break
    return p_r1 == p_r2

def is_same_name(r1,r2):
    n_r1 = None
    for s,p,o in r1:
        if p == URIRef('http://www.okkam.org/ontology_restaurant1.owl#name'):
            n_r1 = o
            break
    n_r2 = None
    for s,p,o in r2:
        if p == URIRef('http://www.okkam.org/ontology_restaurant2.owl#name'):
            n_r2 = o
            break
    print()
    print(str(n_r1) + " " + str(n_r2))
    return n_r1 == n_r2


# more out | grep "Not Found" | wc -l
# more out | grep "False" | wc -l
# more out | grep "True" | wc -l
def compare_gd_category(d_restaurant1,d_restaurant2,d_category_r2):
    prefix_r1 = "http://www.okkam.org/oaie/restaurant1-Restaurant"
    prefix_r2 = "http://www.okkam.org/oaie/restaurant2-Restaurant"
    for r in range(112):
        current_r1 = URIRef(prefix_r1 + str(r))
        current_r2 = URIRef(prefix_r2 + str(r))
        # missing restaurant only in r2
        if current_r2 not in d_restaurant2:
            print()
            print(str(current_r2))
            print("Not Found")
            continue
        r1 = d_restaurant_r1[current_r1]
        r2 = d_restaurant_r2[current_r2]
        print()
        print(str(current_r1) + " " + str(current_r2))
        print(is_same_category(r1,r2,d_category_r2))

# more out | grep False | wc -l
# more out | grep True | wc -l
# more out | grep "Not Found" | wc -l
def compare_gd_address(d_restaurant1,d_restaurant2,d_address_r1,d_address_r2,d_city_r1):
    prefix_r1 = "http://www.okkam.org/oaie/restaurant1-Restaurant"
    prefix_r2 = "http://www.okkam.org/oaie/restaurant2-Restaurant"
    for r in range(112):
        current_r1 = URIRef(prefix_r1 + str(r))
        current_r2 = URIRef(prefix_r2 + str(r))
        # missing restaurant only in r2
        if current_r2 not in d_restaurant2:
            print()
            print(str(current_r2))
            print("Not Found")
            continue
        r1 = d_restaurant_r1[current_r1]
        r2 = d_restaurant_r2[current_r2]
        print()
        print(str(current_r1) + " " + str(current_r2))
        print(is_same_address(r1,r2,d_address_r1,d_address_r2,d_city_r1))
 
def compare_gd_phone_numer(d_restaurant1,d_restaurant2):
    prefix_r1 = "http://www.okkam.org/oaie/restaurant1-Restaurant"
    prefix_r2 = "http://www.okkam.org/oaie/restaurant2-Restaurant"
    for r in range(112):
        current_r1 = URIRef(prefix_r1 + str(r))
        current_r2 = URIRef(prefix_r2 + str(r))
        # missing restaurant only in r2
        if current_r2 not in d_restaurant2:
            print()
            print(str(current_r2))
            print("Not Found")
            continue
        r1 = d_restaurant_r1[current_r1]
        r2 = d_restaurant_r2[current_r2]
        print()
        print(str(current_r1) + " " + str(current_r2))
        print(is_same_phone_number(r1,r2))
 
def compare_gd_name(d_restaurant1,d_restaurant2):
    prefix_r1 = "http://www.okkam.org/oaie/restaurant1-Restaurant"
    prefix_r2 = "http://www.okkam.org/oaie/restaurant2-Restaurant"
    for r in range(112):
        current_r1 = URIRef(prefix_r1 + str(r))
        current_r2 = URIRef(prefix_r2 + str(r))
        # missing restaurant only in r2
        if current_r2 not in d_restaurant2:
            print()
            print(str(current_r2))
            print("Not Found")
            continue
        r1 = d_restaurant_r1[current_r1]
        r2 = d_restaurant_r2[current_r2]
        print()
        print(str(current_r1) + " " + str(current_r2))
        print(is_same_name(r1,r2))


if __name__ == "__main__":
    d_restaurant_r1,d_address_r1,d_city_r1 = load_restaurant1_type()
    load_restaurant1_instance(d_restaurant_r1,d_address_r1,d_city_r1)
    
    d_restaurant_r2,d_address_r2,d_category_r2 = load_restaurant2_type()
    load_restaurant2_instance(d_restaurant_r2,d_address_r2,d_category_r2)
 
    # count nb restaurant
    print ()
    print (len(d_restaurant_r2))



    # is has_address multivalued ?
    test_address_multivalued(d_restaurant_r1)
    test_address_multivalued(d_restaurant_r2)

    # TODO: is category multi valued

    id_r10 = "http://www.okkam.org/oaie/restaurant1-Restaurant0"
    id_r20 = "http://www.okkam.org/oaie/restaurant2-Restaurant0"
    r10 = d_restaurant_r1[URIRef(id_r10)]
    r20 = d_restaurant_r2[URIRef(id_r20)]


    # same categories between gd ?
    #compare_gd_category(d_restaurant_r1,d_restaurant_r2,d_category_r2)

    # same addresses between gd ?
    #compare_gd_address(d_restaurant_r1,d_restaurant_r2,d_address_r1,d_address_r2,d_city_r1)
    
    # same phone number between gd ?
    #compare_gd_phone_numer(d_restaurant_r1,d_restaurant_r2)

    # same name between gd ?
    #compare_gd_name(d_restaurant_r1,d_restaurant_r2)

    #all_contexts = compute_edo_gd(d_restaurant_r1,d_restaurant_r2,d_category_r2,d_address_r1,d_address_r2,d_city_r1)
    #all_partitions = partition_all_context(all_contexts)
    #for p_name in all_partitions:
    #    print()
    #    print(p_name + " " + str(len(all_partitions[p_name])))
 
    #print()
    #for t in r10:
    #    print(t)

    #print()
    #for t in r20:
    #   print(t)
    #is_same_category(r10,r20,d_category_r2)

    #r1_keys = d_restaurant_r1.keys()
    #r2_keys = d_restaurant_r2.keys()

    #cartesian_product = product(r1_keys,r2_keys)
    #for r1,r2 in cartesian_product:
    #    pass


    #dict_of_DB = load_triples_to_dict("../gold/Book/DB_Book")
