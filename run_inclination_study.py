#### Very small file to produce plots for inclination choices relevant to us

import math
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb

def get_string_labels_from_list(list1, number_of_labels):
    '''
    '''
    label_list = []
    list_length = len(list1)
    iter_good = int(list_length / number_of_labels)
    for iter1, val in enumerate(list1):
        if not iter1 % iter_good:
            label_list.append(str(val))
        else:
            label_list.append('')
    return label_list

def get_inc_change_dv(v1, v2, inclination):
    '''
    inclination change dv, 
    v1 in m/s
    v2 in m/s
    inclination in radians
    '''
    return math.sqrt(v1 ** 2 + v2 ** 2 - 2 * v1 * v2 * math.cos(math.radians(inclination)))

def get_inc_change_dv_with_cos(v1, v2, cos_inclination):
    '''
    inclination change dv, 
    v1 in m/s
    v2 in m/s
    inclination in radians
    '''
    v1 = int(v1)
    v2 = int(v2)
    
    return math.sqrt(v1 ** 2 + v2 ** 2 - 2 * v1 * v2 * cos_inclination)


def create_plot(v1_range, v2_range, inclination):
    '''
    create plots for v1 steps and v2 range at a given inclinattion
    v1 and v2 range is [int, int]
    inclination is float    
    '''
    inclination_radians = math.cos(math.radians(inclination))
    data_array_2D = np.zeros(shape=(len(np.arange(v1_range[0], v1_range[1], 100)),len(np.arange(v2_range[0], v2_range[1], 100))))

    v1_for_iterations = list(np.arange(v1_range[0], v1_range[1],100))
    v1_for_iterations = list(reversed(v1_for_iterations))

    v2_for_iterations = list(np.arange(v2_range[0], v2_range[1],100))
    #v2_for_iterations = list(reversed(v2_for_iterations))
    for iter1, v1 in enumerate(v1_for_iterations):
        for iter2, v2 in enumerate(v2_for_iterations):
            data_array_2D[iter1][iter2] = get_inc_change_dv_with_cos(v1, v2, inclination_radians)

    v1_for_iterations.reverse()
    v2_for_iterations.reverse()
    v1_list = get_string_labels_from_list(v1_for_iterations, 10)
    v2_list = get_string_labels_from_list(v2_for_iterations, 10)
    heatm = sb.heatmap(data = data_array_2D, xticklabels=v1_list, yticklabels=v2_list)
    plt.xlabel('Velocity After Burn (m/s)')
    plt.ylabel('Velocity Before Burn (m/s)')
    plt.title('DeltaV Req. For Combined Burn With An Inc. Change | inc. change = 4.81 deg')
    plt.plot(26000,34000,'*','g')
    plt.show()



v1_range = [25000, 35001]

v2_range = [25000, 35001]

inclination = 4.81

print(get_inc_change_dv(28140, 29784, 4.81))
print(get_inc_change_dv(36630, 34910, 4.81))


#create_plot(v1_range, v2_range, inclination)