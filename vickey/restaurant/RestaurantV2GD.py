import unittest
from ContextRestaurant2 import *

class RestaurantV2GD(unittest.TestCase):
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
        d_restaurant_r1,d_address_r1,d_city_r1 = load_restaurant1_type()
        load_restaurant1_instance(d_restaurant_r1,d_address_r1,d_city_r1)
    
        d_restaurant_r2,d_address_r2,d_category_r2 = load_restaurant2_type()
        load_restaurant2_instance(d_restaurant_r2,d_address_r2,d_category_r2)
 
        all_contexts = compute_edo_gd(d_restaurant_r1,d_restaurant_r2,d_category_r2,d_address_r1,d_address_r2,d_city_r1)
        p_all_context = partition_all_context(all_contexts)
        return p_all_context
 
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
            if l[2] >= filter_ide:
                genuine_ide.append(l)
            else:
                weak_ide.append(l)
        print("")
        print("P Epsilon")
        print("Genuine Ide: " + str(len(genuine_ide)))
        print("Weak Ide: " + str(len(weak_ide)))
        
        self.G_IDE.append(len(genuine_ide))
        self.W_IDE.append(len(weak_ide))

    def test_p_delta(self):
        p_all_context = self.make_partitions()
        p = p_all_context["P3"]

        max_epsilon_size,max_delta_size,max_omega_size = compute_subc_max_size(p)
        k=3
        assert(k < max_delta_size)

        filter_dif = compute_filter_difference(max_delta_size,k)

        dif = compute_difference(p)

        genuine_diff = []
        weak_diff = []

        for l in dif:
            if l[2] >= filter_dif:
                genuine_diff.append(l)
            else:
                weak_diff.append(l)

        print()
        print("P Delta")
        print("Genuine Dif: " + str(len(genuine_diff)))
        print("Weak Dif: " + str(len(weak_diff)))
 
        self.G_DIF.append(len(genuine_diff))
        self.W_DIF.append(len(weak_diff))
    
    def test_p_epsilon_delta(self):
        p_all_context = self.make_partitions()
        p = p_all_context["P7"]
        max_epsilon_size,max_delta_size,max_omega_size = compute_subc_max_size(p)
        filter_und = compute_filter_indicisvness()
        und = compute_indecisiveness(p)
        print()
        print(filter_und)
        genuine_und = []
        weak_und = []
        for l in und:
            if filter_und[0] <= l[3] <= filter_und[1]:
                genuine_und.append(l)
            else:
                weak_und.append(l)
    
        print()
        print("P Epsilon Delta")
        print("Genuine Und: " + str(len(genuine_und)))
        print("Weak Und: " + str(len(weak_und)))

        self.TYPE_2_G.append(len(genuine_und))
        self.TYPE_2_W.append(len(weak_und))



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

