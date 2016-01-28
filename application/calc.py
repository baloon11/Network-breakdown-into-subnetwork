# coding: utf-8
from random import randint
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
result_dir=os.path.join(BASE_DIR, 'result')

def create_table(main_ips,network_matrix):

    all_file_path=os.path.join(result_dir, 'all')
    if os.path.exists(all_file_path):
        os.remove(all_file_path) #удаляем предыдущий файл all если, он есть, чтобы не дописывалось в конец

    mask_and_max_ip=[[32,0],[31,1],
                     [30,3],[29,7],
                     [28,15],[27,31],
                     [26,63],[25,127],[24,255] ]

    def zero_check(network_list):
        counter_zero=0
        for net_index in xrange(len(network_list)):
            if network_list[net_index][0]==0:
                counter_zero+=1
            if counter_zero==len(network_list):
                return False
        return True

    def belong_range(network,range27): # проверка, есть ли возможность добавить в этот диапазон данную сеть ( диапазон с каждой добавленной сетью уменьшается)
    # будем возвращать кортеж range27 и True/False
        for m in mask_and_max_ip:
            if network[1]==m[0]:# если мы определили маску подсети 
                if range27-(m[1]+1)>=0: #если еще в диапазоне хватает места для этой сети, то
                    range27=range27-(m[1]+1)
                    return range27, True
        return range27, False

    def group_masks(info_range_27):
        unik_info_range_27=sorted(list(set(info_range_27)))#находим, какие именно подсети входят в диапазон /27(сортированные по возрастанию)
        min_mask=unik_info_range_27[0] # мин маска (с самым большим количеством ip)
        dict_of_num_and_unik_mask={} 

        for unik_mask in unik_info_range_27:# создадим словарь [маска]=количество (изначально[маска]=0)
            dict_of_num_and_unik_mask[unik_mask]=0
        for info in info_range_27:#тут собираем словарь
            if dict_of_num_and_unik_mask.get(info,None)!=None:#если есть в словаре такая маска
                dict_of_num_and_unik_mask[info]+=1
        list_of_num_and_unik_mask=dict_of_num_and_unik_mask.items() # тут его переводим с список кортежей

        out_unsort_list=[]
        out_unsort_list_consist_only_nums=[]
        for l in list_of_num_and_unik_mask:
            if min_mask!=l[0]:#если это не мин маска
                num_group=l[1]/2# сколько целых групп по 2 шт  можно получить  с одной маски
                remainder_division_group=l[1]%2 #есть ли одиночная подсеть с этой маской ( остаток от деления будет или 0 или 1)

                for gr in xrange(num_group): #создаем  группы
                    out_unsort_list.append([l[0],l[0]]) #тут в выходной список добавляем списки(по 2) данной маски

                if remainder_division_group:
                    out_unsort_list.append(l[0])#тут в выходной список добавляем  единичную подсеть с данной маской
            else: #если это мин маска просто добавляем единичные маски подсетей в список
                for min_mask_unit in xrange(l[1]):
                    out_unsort_list.append(l[0])#тут в выходной список добавляем  единичную подсеть с мин маской

        for i in xrange(1000):
            first_index=randint(0,len(out_unsort_list)-1)
            first_elem=out_unsort_list[first_index]
            second_index=randint(0,len(out_unsort_list)-1)
            second_elem=out_unsort_list[second_index]
            out_unsort_list[first_index]=second_elem
            out_unsort_list[second_index]=first_elem

        for unit in out_unsort_list:# тут полностью перегоняем список в список из чисел (каждый эдемент -маска подсети)
            if str(type(unit))=="<type 'list'>":
                out_unsort_list_consist_only_nums.append(unit[0])
                out_unsort_list_consist_only_nums.append(unit[1])
            if str(type(unit))=="<type 'int'>":
                out_unsort_list_consist_only_nums.append(unit)
        return out_unsort_list_consist_only_nums

    for index, network_list in enumerate(network_matrix):
        curr_ip= [int(bite) for bite in main_ips[index].split(".")]

        out_file_path=os.path.join(result_dir, 'out'+str(index))
        out=open(out_file_path,'a')
        range27=32 # количество ip в сетис маской 27
        # тут берем список списков network_list (строку из матрицы network_matrix) и вызываем любой из элементов
        info_range_27=[]
        sort_list_for_create_networks=[]
        while True: 
            if zero_check(network_list) == False:
                break
            rand_network=network_list[randint(0,len(network_list)-1)]#любой индекс из существующих для списка network_list
            if rand_network[0]==0:
                continue
            else:
                range27,can_include_in_range=belong_range(rand_network,range27)
                if can_include_in_range:
                    info_range_27.append(rand_network[1])#записываем маску подети для сети подпадяющей в диапазон /27 и начальный адрес
                    rand_network[0]=rand_network[0]-1

                    if range27==0:# если диапазон полностью исчерпан
                        sort_list_for_create_networks.extend(group_masks(info_range_27))
                        info_range_27=[]#обнуляем список
                        range27=32 # и  используем новый диапазон

    # потом  берем диапазон 24 и список и  просто прогоняем значения по списку
        for n_mask in sort_list_for_create_networks:
            if curr_ip[-1]>255:
                break
            else:
                out.write(".".join([str(bite) for bite in curr_ip])+" Network "+str(n_mask)+"\n")

                for mm in mask_and_max_ip: #вот тут находим максимальное значение 2 байта для данного диапазона
                    if mm[0]==n_mask:
                        max_ip=curr_ip[-1]+mm[1]
                        break

                for num_new_ip,l_bit in enumerate(xrange (curr_ip[-1]+1,max_ip+1)):#новые ip будут начинаться со следующего от текущего ip до макс в этой сети 
                    if num_new_ip == 0:
                        curr_ip[-1]=l_bit
                        out.write(".".join([str(bite) for bite in curr_ip])+" Gateway"+"\n")
                        curr_ip[-1]+=1 # это для формирования нового ip
                        continue
                    if l_bit==max_ip:
                        curr_ip[-1]=l_bit
                        out.write(".".join([str(bite) for bite in curr_ip])+" Broadcast"+"\n")
                        curr_ip[-1]+=1
                        continue
                    curr_ip[-1]=l_bit
                    out.write(".".join([str(bite) for bite in curr_ip])+"\n")
                    curr_ip[-1]+=1
                    continue
        out.close()

    out_list=[]
    all_parts=open(all_file_path,'a')

    for f in xrange(len(main_ips)):
        out_list.append(open(os.path.join(result_dir, 'out'+str(f)),'r'))

    for curr_out in out_list:
        for line in curr_out:
            all_parts.write(line)
    all_parts.close()

    for del_index in xrange(len(main_ips)):
        os.remove(os.path.join(result_dir, 'out'+str(del_index)))