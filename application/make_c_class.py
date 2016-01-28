# coding: utf-8
from random import randint
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
result_dir=os.path.join(BASE_DIR, 'result')

def create_c_classes(curr_ip,mask):
    mask_and_c_class=[[24,1],[23,2],[22,4],
                      [21,8],[20,16],[19,32],
                      [18,64],[17,128],[16,256]]

    for m in mask_and_c_class:
        if mask==m[0]:
            delta=m[1]-1# количество подсетей- 1 (изначальная), которую прибавляем отдельно

    list_c_path=os.path.join(result_dir, 'list_c')
    if os.path.exists(list_c_path):
        os.remove(list_c_path) #удаляем предыдущий файл list_c, если он есть, чтобы не дописывалось в конец 
    list_c=open(list_c_path,'a')
    range_ips=[]#  этот список заполняется,начальными адресами в  каждом новом диапазоне

    if curr_ip[2]+delta>255: #если маска подсети и текущий ip адрес выбраны такими, что необхожимо перебросить часть 
                             #адресов на 3 справа байт
        for end in xrange(curr_ip[2],256):# сначала добавляем ip подсетей чтоб полностью заполнить второй байт
            range_ips.append([curr_ip[0],curr_ip[1],end,0]) 
            list_c.write(str([curr_ip[0],curr_ip[1],end,0])+'\n')

        # потом идет работа с уже измененным третим байтом
        delta_3_bite=(delta+1)-len(xrange(curr_ip[2],256))#  количество  ip адресов с измененным 3 байтом
        if curr_ip[1]<255:# вариант когда в третий байт возможно добавить единицу
            for d_3 in xrange(delta_3_bite):#добавляем в общий список новые адреса подсетей (отсчет будет вестись с 0 -так что все правильно)
                curr_ip_new_3_bite=[curr_ip[0],curr_ip[1]+1,d_3,0]
                range_ips.append(curr_ip_new_3_bite)
                list_c.write(str(curr_ip_new_3_bite)+'\n')
        else:# вариант когда добавляем единицу в 4 байт, а третий обнуляем( тк третий байт =255 и его нельзя дальше заполнять)
            for d_3 in xrange(delta_3_bite):
                curr_ip_new_3_bite=[curr_ip[0]+1,0,d_3,0]
                range_ips.append(curr_ip_new_3_bite)
                list_c.write(str(curr_ip_new_3_bite)+'\n')
    else:
        for i in xrange(delta+1):
            range_ips.append([curr_ip[0],curr_ip[1],curr_ip[2]+i,0])
            list_c.write(str([curr_ip[0],curr_ip[1],curr_ip[2]+i,0])+'\n')

    list_range_ips=[ ".".join([str(bite) for bite in ip_list]) for ip_list in range_ips ]
    return list_range_ips