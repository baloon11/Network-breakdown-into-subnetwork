# coding: utf-8
from random import randint
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
result_dir=os.path.join(BASE_DIR, 'result')

def create_matrix(curr_network_list):
    network_matrix=[]
    line_in_matrix=[]

    mask_and_max_ip=[[32,0],[31,1],
                     [30,3],[29,7],
                     [28,15],[27,31],
                     [26,63],[25,127],[24,255] ]

    def zero_check(network_list): # проверка, если все подсети из передаваемого списка  использованы, то return False
        counter_zero=0
        for net_index in xrange(len(network_list)):
            if network_list[net_index][0]==0:
                counter_zero+=1
            if counter_zero==len(network_list):
                return False
        return True

    def belong_range(network,range24,exist_27): # проверка, есть ли возможность добавить в этот диапазон данную сеть ( диапазон с каждой добавленной сетью уменьшается)
    # будем возвращать кортеж range24 и True/False
        for m in mask_and_max_ip:
            if network[1]==m[0]:# если мы определили маску подсети 

                if network[1]==27 and exist_27==False:
                    if range24-(m[1]+1)>=0 : #если еще в диапазоне хватает места для этой сети , то
                        range24=range24-(m[1]+1)
                        exist_27=True
                        return range24, True,True

                if network[1]!=27 and exist_27==False:
                    if range24-(m[1]+1)>=0 : 
                        range24=range24-(m[1]+1)
                        exist_27=False
                        return range24, True,False

                if network[1]!=27 and exist_27==True:
                    if range24-(m[1]+1)>=0 :
                        range24=range24-(m[1]+1)
                        exist_27=True
                        return range24, True,True

                if network[1]==27 and exist_27==True:
                    exist_27=True #если  пришедшая сеть 27 и она уже есть --   просто возвращаем кортеж
                    return range24, False,True

        return range24, False,exist_27

    def add_in_network_matrix(network,line_in_matrix):
        #провеяем, есть ли упоминание о сети, которую мы получили, в строке из матрицы -- line_in_matrix
        if len(line_in_matrix)>0:
            is_cell_exist=False
            for cell in line_in_matrix:
                if cell[1]==network[1]:
                    cell[0]=cell[0]+1 # если есть упоминание добавлем единицу,
                    is_cell_exist=True #выставляем флаг, что есть
            if is_cell_exist==False: # если после цикла не была найдена ячейка, то строка в матрице не пустая, но в нее нужно добавить эту ячейку
                line_in_matrix.append( [1,network[1]] )

        else:#если список пустой, создаем список и добавляем единицу
            line_in_matrix.append( [1,network[1]] )
        return line_in_matrix

    range24=256
    exist_27=False
    while True:
        if zero_check(curr_network_list) == False:
            break
        rand_network=curr_network_list[randint(0,len(curr_network_list)-1)]#любой индекс из существующих для списка curr_network_list
        if rand_network[0]==0:
            continue
        else:
            range24,can_include_in_range,exist_27=belong_range(rand_network,range24,exist_27)
            #exist_27 -флаг -проверка на подсеть,если уже есть 27 подсеть, то новая не запишется в 24 диапазон)
            if can_include_in_range:
                line_in_matrix=add_in_network_matrix(rand_network,line_in_matrix)
                rand_network[0]=rand_network[0]-1

                if range24==0:# если диапазон полностью исчерпан
                    range24=256 # то используем новый диапазон
                    network_matrix.append(line_in_matrix)#и добавляем строку в мартицу
                    line_in_matrix=[]# потом эту строку обнуляем,чтобы создать новую
                    exist_27=False # выставляем флаг в False

    for i in xrange(1000):
        first_index=randint(0,len(network_matrix)-1)
        first_elem=network_matrix[first_index]
        second_index=randint(0,len(network_matrix)-1)
        second_elem=network_matrix[second_index]
        network_matrix[first_index]=second_elem
        network_matrix[second_index]=first_elem

    network_matrix_file_path=os.path.join(result_dir, 'network_matrix')
    if os.path.exists(network_matrix_file_path):
        os.remove(network_matrix_file_path)
    n_m=open (network_matrix_file_path,'a')
    n_m.write(str(network_matrix))

    return network_matrix