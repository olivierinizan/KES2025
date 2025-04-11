import unittest
from ContextVickey2Gold import *
import matplotlib.pyplot as plt
import networkx as nx

class BookPatternIde(unittest.TestCase):
    
    def test_1_g_ide(self):
        all_contexts = compute_epsilon_delta_omega_book()
        p_all_context = partition_all_context(all_contexts)
        p = p_all_context["P5"]

        max_epsilon_size,max_delta_size,max_omega_size = compute_subc_max_size(p)
        print (max_epsilon_size)
        k=3
        assert(k < max_epsilon_size)

        filter_ide = compute_filter_identity(max_epsilon_size,k)
        ide = compute_identity(p)

        genuine_ide = []
        artificial_ide = []
        for l in ide:
            if l[2] > filter_ide:
                genuine_ide.append(l)
            else:
                artificial_ide.append(l)
        
        self.assertEqual((len(genuine_ide)+len(artificial_ide)),len(ide))
        # pattern for genuine identity 
        # work on genuine ide
        # get genuine identites individuals in the partition
        filtered_context = filter_context_for_genuine_or_artificial_individual(genuine_ide,p)
        assert(len(filtered_context) == len(genuine_ide))    
 
        # plot distribution
        context_indexed = index_context(filtered_context)
        subc_indexed = index_subcontext(context_indexed,0)
        subc_levels = level_subcontext(subc_indexed)
        pair_subc_level_count, pair_subc_indexed = count_pair_for_levelled_subcontexts_100(subc_indexed,subc_levels)
        x,y = plot_distribution(pair_subc_level_count,"./Book/graph/distribution_g_identities")

        # heavy nodes
        heavy_nodes = compute_heavy_nodes(x,y,7,1)
        heavy_nodes_ratio = compute_heavy_nodes_ratio(heavy_nodes,pair_subc_level_count)
        # build epsilon  lattice for genuine ide      
        in_subc_connected = {}
        connect(1,subc_levels,in_subc_connected)
        connect(2,subc_levels,in_subc_connected)
        connect(3,subc_levels,in_subc_connected)
        connect(4,subc_levels,in_subc_connected)
        connect(5,subc_levels,in_subc_connected)
        connect(6,subc_levels,in_subc_connected)
        
        subc_index = index_subc_id(subc_levels)
        ############################ 
        # compute Genuine Ide 100
        ############################ 
        heavy_connected = extract_heavy_nodes_from_lattice(heavy_nodes,in_subc_connected)
        nodes_hn,edges_hn = extract_nodes_and_edges(heavy_connected)
        nodes_hn_replaced,edges_hn_replaced = replace_nodes_and_edges(nodes_hn,edges_hn,pair_subc_level_count,"e")
        
        G = nx.Graph() 
        G.add_nodes_from(nodes_hn_replaced) 
        G.add_edges_from(edges_hn_replaced)
        ccs = nx.connected_components(G)
 
        print()
        print("Genuine Identities 100")
        print(heavy_nodes_ratio)
        print("n100: "  + str(len(heavy_nodes)))
        for cc in ccs:
            print("cc")
            index = index_cc(cc,subc_index)
            index_sorted = sort_index_cc(index)
            for item in index_sorted:
                print(item)

        nx.write_graphml(G,"./Book/graph/lattice_g_identities.graphml")

    def test_2_w_ide(self):
        all_contexts = compute_epsilon_delta_omega_book()
        p_all_context = partition_all_context(all_contexts)
        p = p_all_context["P5"]

        max_epsilon_size,max_delta_size,max_omega_size = compute_subc_max_size(p)

        k=3
        assert(k < max_epsilon_size)

        filter_ide = compute_filter_identity(max_epsilon_size,k)
        ide = compute_identity(p)

        genuine_ide = []
        artificial_ide = []
        for l in ide:
            if l[2] > filter_ide:
                genuine_ide.append(l)
            else:
                artificial_ide.append(l)
        
        self.assertEqual((len(genuine_ide)+len(artificial_ide)),len(ide))
        # pattern for artificial identity 
        filtered_context = filter_context_for_genuine_or_artificial_individual(artificial_ide,p)
        assert(len(filtered_context) == len(artificial_ide))    
 
        # plot distribution
        context_indexed = index_context(filtered_context)
        subc_indexed = index_subcontext(context_indexed,0)
        subc_levels = level_subcontext(subc_indexed)
        pair_subc_level_count, pair_subc_indexed = count_pair_for_levelled_subcontexts_100(subc_indexed,subc_levels)
        x,y = plot_distribution(pair_subc_level_count,"./Book/graph/distribution_a_identities")

        # heavy nodes
        heavy_nodes = compute_heavy_nodes(x,y,68,1)
        heavy_nodes_ratio = compute_heavy_nodes_ratio(heavy_nodes,pair_subc_level_count)
        # build epsilon  lattice for aritifcial ide      
        in_subc_connected = {}
        connect(1,subc_levels,in_subc_connected)
        connect(2,subc_levels,in_subc_connected)
        connect(3,subc_levels,in_subc_connected)
        connect(4,subc_levels,in_subc_connected)
        
        subc_index = index_subc_id(subc_levels)
        ############################ 
        # compute Weak Ide 100
        ############################ 
        heavy_connected = extract_heavy_nodes_from_lattice(heavy_nodes,in_subc_connected)
        nodes_hn,edges_hn = extract_nodes_and_edges(heavy_connected)
        nodes_hn_replaced,edges_hn_replaced = replace_nodes_and_edges(nodes_hn,edges_hn,pair_subc_level_count,"e")
        
        G = nx.Graph() 
        G.add_nodes_from(nodes_hn_replaced) 
        G.add_edges_from(edges_hn_replaced)
        ccs = nx.connected_components(G)
 
        print()
        print("Weak Identities 100")
        print(heavy_nodes_ratio)
        print("n100: "  + str(len(heavy_nodes)))
        for cc in ccs:
            print("cc")
            index = index_cc(cc,subc_index)
            index_sorted = sort_index_cc(index)
            for item in index_sorted:
                print(item)

        nx.write_graphml(G,"./Book/graph/lattice_w_identities.graphml")
if __name__ == "__main__":
    unittest.main()
