import unittest
from ContextVickey2Gold import *
import matplotlib.pyplot as plt

class City(unittest.TestCase):
    # P Epsilon G Ide
    G_IDE = []

    # P Epsilon W Ide 
    W_IDE = []

    # P Delta G Dif
    G_DIF = []

    # P Delta W Dif
    W_DIF = []

    # P Epsilon Omega G Inc + P Delta Omega G Inc + P Epsilon Delta Omega G Inc Weak Und + P Omega G Inc
    TYPE_1_G = []

    # P Epsilon Omega W Inc + P Delta Omega W Inc + P Omega W Inc 
    TYPE_1_W = []

    # P Epsilon Delta G Und + P Epsilon Delta Omega W Inc Gen Und
    TYPE_2_G = []

    # P Epsilon Delta W Und 
    TYPE_2_W = []

    # P Epsilon Omega Gen Inc Gen Und
    TYPE_1_TYPE_2_G = []

    # P Epsilon Delta Omega W Inc W Und 
    TYPE_1_TYPE_2_W = []



    def make_partitions(self):
        all_contexts = compute_epsilon_delta_omega_city()
        p_all_context = partition_all_context(all_contexts)
        return p_all_context
    
    def _compute_difference(self,len_delta,max_delta_size):
        return len_delta

    def _compute_identity(self,len_epsilon,max_epsilon_size):
        return len_epsilon
   
    def test_p_epsilon(self):
        p_all_context = self.make_partitions()
        p = p_all_context["P5"]

        max_epsilon_size,max_delta_size,max_omega_size = compute_subc_max_size(p)

        k=3
        assert(k < max_epsilon_size)

        filter_ide = compute_filter_identity(max_epsilon_size,k)
        ide = compute_identity(p)

        genuine_ide = []
        weak_ide = []
        for l in ide:
            if l[2] > filter_ide:
                genuine_ide.append(l)
            else:
                weak_ide.append(l)
        print("")
        print("P Epsilon")
        print("Genuine Ide: " + str(len(genuine_ide)))
        print("Weak Ide: " + str(len(weak_ide)))
        
        self.G_IDE.append(len(genuine_ide))
        self.W_IDE.append(len(weak_ide))



    def test_p_dela(self):
        p_all_context = self.make_partitions()
        p = p_all_context["P3"]

        print()
        print("P Delta is empty")
        
        self.G_DIF.append(0)
        self.W_DIF.append(0)
 
    def test_p_epsilon_omega(self):
        p_all_context = self.make_partitions()
        p = p_all_context["P6"]
        max_epsilon_size,max_delta_size,max_omega_size = compute_subc_max_size(p)

        # compute filter incompleteness
        filter_inc = compute_filter_incompletness(max_omega_size)
        k = 3
        self.assertTrue(k < max_epsilon_size)
 
        ident_and_inc = compute_identity_with_incompletness(p)
        
        genuine_inc = []
        weak_inc = []
        
        # compute filter identity k=3
        k = 3
        self.assertTrue(k < max_epsilon_size)
        filter_ide = compute_filter_identity(max_epsilon_size,k)
        genuine_ide = []
        weak_ide = []

        for l in ident_and_inc:
            if l[4] > filter_inc:
                genuine_inc.append(l)
            else:
                weak_inc.append(l)
                if l[3] > filter_ide:
                    genuine_ide.append(l)
                else:
                    weak_ide.append(l)

       
        print("")
        print("P Epsilon Omega")
        print("Genuine Inc: " + str(len(genuine_inc)))
        print("Weak Inc: " + str(len(weak_inc)))
        print("Genuine Ide: "+ str(len(genuine_ide)))
        print("Weak Ide: "+ str(len(weak_ide)))
 
        self.TYPE_1_G.append(len(genuine_inc))
        self.TYPE_1_W.append(len(weak_inc))
        self.G_IDE.append(len(genuine_ide))
        self.W_IDE.append(len(weak_ide))

    def test_p_delta_omega(self):
        p_all_context = self.make_partitions()

        p = p_all_context["P4"]
        max_epsilon_size,max_delta_size,max_omega_size = compute_subc_max_size(p)
      
        # compute incompletness
        filter_inc = compute_filter_incompletness(max_omega_size)
        diff_and_inc = compute_difference_with_incompletness(p) 

        genuine_incompletness = []
        weak_incompletness = []

        # compute difference: k > max_delta_size, all diff are weak
        k = 3

        for l in diff_and_inc:
            if l[4] > filter_inc:
                genuine_incompletness.append(l)
            else:
                weak_incompletness.append(l)
        
        print("")
        print("P Delta Omega")
        print("Genuine Inc: " + str(len(genuine_incompletness)))
        print("Weak Inc: " + str(len(weak_incompletness)))
        print("Genuine Diff: 0")
        print("Weak Diff: " + str(len(weak_incompletness)))

        self.TYPE_1_G.append(len(genuine_incompletness))
        self.TYPE_1_W.append(len(weak_incompletness))
        self.G_DIF.append(0)
        self.W_DIF.append(len(weak_incompletness))

    def test_p_omega(self):
        p_all_context = self.make_partitions()
        p = p_all_context["P2"]

        max_epsilon_size,max_delta_size,max_omega_size = compute_subc_max_size(p)
        filter_inc = compute_filter_incompletness(max_omega_size)
        inc = compute_incompleteness(p)

        genuine_inc = []
        weak_inc = []

        for l in inc:
            if l[2] > filter_inc:
                genuine_inc.append(l)
            else:
                weak_inc.append(l)
        print()
        print("P Omega")
        print("Genuine Inc: " + str(len(genuine_inc)))
        print("Weak Inc: " + str(len(weak_inc)))
        
        self.TYPE_1_W.append(len(weak_inc))
        self.TYPE_1_G.append(len(genuine_inc))
 
    def test_p_epsilon_delta(self):
        p_all_context = self.make_partitions()
        p = p_all_context["P7"]
        # index partition 
        p_indexed = index_partition(p)

        max_epsilon_size,max_delta_size,max_omega_size = compute_subc_max_size(p)
        
        # compute filter ide
        filter_ide = compute_filter_identity(max_epsilon_size,3)
        genuine_ide = []
        weak_ide = []
        # compute_difference
        filter_dif = compute_filter_difference(max_delta_size,3)
        genuine_dif = []
        weak_dif = []

        # compute und
        filter_und = compute_filter_indicisvness()
        und = compute_indecisiveness(p)

        genuine_und = []
        weak_und = []
        for l in und:
            if filter_und[0] <= l[3] <= filter_und[1]:
                genuine_und.append(l)
            else:
                weak_und.append(l)
                # re-affect to weak/genuine identities/incompletness
                key = str(l[0])
                contexts = p_indexed[key]
                if l[3] > 0:
                    epsilon = contexts[1][0]
                    ide = self._compute_identity(len(epsilon),max_epsilon_size) 
                    if ide > filter_ide:
                        genuine_ide.append(l)
                    else:
                        weak_ide.append(l)
                elif l[3] < 0:
                    delta = contexts[1][1]
                    dif = self._compute_difference(len(delta),max_delta_size)
                    if dif > filter_dif:
                        genuine_dif.append(l)
                    else:
                        weak_dif.append(l)
                else:
                    raise Exception("The conlict can not be equal to zero")


        print()
        print("P Epsilon Delta")
        print("Genuine Und: " + str(len(genuine_und)))
        print("Weak Und: " + str(len(weak_und)))
        print("Genuine Ide: " + str(len(genuine_ide)))
        print("Weak Ide: " + str(len(weak_ide)))
        print("Genuine Dif: " + str(len(genuine_dif)))
        print("Weak Dif: " + str(len(weak_dif)))

        self.TYPE_2_G.append(len(genuine_und))
        self.TYPE_2_W.append(len(weak_und))
        self.G_IDE.append(len(genuine_ide))
        self.W_IDE.append(len(weak_ide))
        self.G_DIF.append(len(genuine_dif))
        self.W_DIF.append(len(weak_dif))



    def test_p_epsilon_delta_omega(self):
        p_all_context = self.make_partitions()
        p = p_all_context["P8"]
        # index partition 
        p_indexed = index_partition(p)
        
        max_epsilon_size,max_delta_size,max_omega_size = compute_subc_max_size(p)
        
        # compute filter incompletness
        filter_inc = compute_filter_incompletness(max_omega_size)
   
        # compute filtrer conflicts
        filter_und = compute_filter_indicisvness()
        und_and_inc = compute_indescisivness_with_incompletness(p)

        # compute ide
        filter_ide = compute_filter_identity(max_epsilon_size,3)
        genuine_ide = []
        weak_ide = []
        # compute difference
        filter_dif = compute_filter_difference(max_delta_size,3)
        genuine_dif = []
        weak_dif = []


        # first filter on incompletness
        genuine_inc = []
        weak_inc = []
        for l in und_and_inc:
            if l[5] > filter_inc:
                genuine_inc.append(l)
            else:
                weak_inc.append(l)

        # genuine inc X genuine und
        # and genuine inc X weak und
        genuine_inc_genuine_und = []
        genuine_inc_weak_und = []
        for l in genuine_inc:
            if filter_und[0] <= l[4] <= filter_und[1]:
                genuine_inc_genuine_und.append(l)
            else:
                genuine_inc_weak_und.append(l)

        # weak inc x genuine und
        # and weak inc x weak und
        weak_inc_genuine_und = []
        weak_inc_weak_und = []
        for l in weak_inc:
            if filter_und[0] <= l[4] <= filter_und[1]:
                weak_inc_genuine_und.append(l)
            else:
                weak_inc_weak_und.append(l)
                # re-affect to weak/genuine identities/incompletness
                key = str(l[0])
                contexts = p_indexed[key]
                if l[4] > 0:
                    epsilon = contexts[1][0]
                    ide = self._compute_identity(len(epsilon),max_epsilon_size) 
                    if ide > filter_ide:
                        genuine_ide.append(l)
                    else:
                        weak_ide.append(l)
                elif l[4] < 0:
                    delta = contexts[1][1]
                    dif = self._compute_difference(len(delta),max_delta_size)
                    if dif > filter_dif:
                        genuine_dif.append(l)
                    else:
                        weak_dif.append(l)
                else:
                    raise Exception("The conlict can not be equal to zero")



        print()
        print("P Epsilon Delta Omega")
        print("Genuine Inc Genuine Und: " + str(len(genuine_inc_genuine_und)))
        print("Genuine Inc Weak Und: " + str(len(genuine_inc_weak_und)))
        print("Weak Inc Genuine Und: " + str(len(weak_inc_genuine_und)))
        print("Weak Inc Weak Und: " + str(len(weak_inc_weak_und)))
        print("Genuine Ide: " + str(len(genuine_ide)))
        print("Weak Ide: " + str(len(weak_ide)))
        print("Genuine Dif: " + str(len(genuine_dif)))
        print("Weak Dif: " + str(len(weak_dif)))


        self.TYPE_1_G.append(len(genuine_inc_weak_und))
        self.TYPE_2_G.append(len(weak_inc_genuine_und))
        self.TYPE_1_TYPE_2_G.append(len(genuine_inc_genuine_und))
        self.TYPE_1_TYPE_2_W.append(len(weak_inc_weak_und))
        
        self.G_IDE.append(len(genuine_ide))
        self.W_IDE.append(len(weak_ide))
        self.G_DIF.append(len(genuine_dif))
        self.W_DIF.append(len(weak_dif))


    def test_z_compute(self):
        print("Genuine Identities")
        print(self.G_IDE)
        print("Weak Identities")
        print(self.W_IDE)
        print("Genuine Differences")
        print(self.G_DIF)
        print("Weak Differences")
        print(self.W_DIF)
        print("Undecidability Type 1 Genuine")
        print(self.TYPE_1_G)
        print("Undecidability Type 1 Weak")
        print(self.TYPE_1_W)
        print("Undecidability Type 2 Genuine")
        print(self.TYPE_2_G)
        print("Undecidability Type 2 Weak")
        print(self.TYPE_2_W)
        print("Undecidability Type 1 & 2 Genuine")
        print(self.TYPE_1_TYPE_2_G)
        print("Undecidability Type 1 & 2 Weak")
        print(self.TYPE_1_TYPE_2_W)



if __name__ == "__main__":
    unittest.main()
