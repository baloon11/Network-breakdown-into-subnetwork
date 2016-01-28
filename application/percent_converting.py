# coding: utf-8
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
result_dir=os.path.join(BASE_DIR, 'result')

def prs_conv(config,mask):
    mask_and_c_class=[[24,1],[23,2],[22,4],
                      [21,8],[20,16],[19,32],
                      [18,64],[17,128],[16,256]]
    mask_and_num_ip={32:1,  31:2,
                     30:4,  29:8,
                     28:16, 27:32,
                     26:64, 25:128,
                     24:256 }
    out_dict={}
    for m in mask_and_c_class:
        if m[0]==mask:
            num_unit=m[1]*256# находим полное поличество ip для данной маски
            curr_num_unit=m[1]*256 #копия для счетчика

    percents_file_path=os.path.join(result_dir, 'percents')
    if os.path.exists(percents_file_path):
        os.remove(percents_file_path) #удаляем предыдущий файл percents если, он есть, чтобы не дописывалось в конец старого файла
    percents=open (percents_file_path,'a')
    percents.write("общее количество ip для /"+str(mask)+" маски = "+str(num_unit)+"\n\n")
    percents.write("маска|"+"число подсетей|"+"процент от общего в долях единицы"+"\n")
    percents.write("----------------------------------"+"\n")

    def mask27_29(curr_num_unit):
        for l in [27,28,29]: #пройдем в цикле эти маски, а из того кол-ва ip, которое останется-найдем количество 30 подсетей
            if config['percent_'+str(l)]!=0 and config['unit_'+str(l)]==0:
                num_ip=(num_unit*config['percent_'+str(l)]/100)/mask_and_num_ip[l]
                curr_num_unit=curr_num_unit-num_ip*mask_and_num_ip[l]
                if curr_num_unit<=0:
                    return False,curr_num_unit,"ошибка в начальных данных curr_num_unit<=0 маска"+str(l)
                else:
                    out_dict[l]=num_ip
                    prs=float(num_ip*mask_and_num_ip[l])/float(num_unit)
                    percents.write("/"+ str(l)+"  | "+str(out_dict[l])+" | "+str(prs)+"\n")
                    percents.write("----------------------------------"+"\n")

            if config['percent_'+str(l)]==0 and config['unit_'+str(l)]!=0:
                curr_num_unit=curr_num_unit-config['unit_'+str(l)]*mask_and_num_ip[l]
                if curr_num_unit<=0:
                    return False,curr_num_unit,"ошибка в начальных данных curr_num_unit<=0 маска"+str(l)
                else:
                    out_dict[l]=config['unit_'+str(l)]
                    prs=float(out_dict[l]*mask_and_num_ip[l])/ float(num_unit)
                    percents.write("/"+ str(l)+"  | "+str(out_dict[l])+" | "+str(prs)+"\n")
                    percents.write("----------------------------------"+"\n")

        return True,curr_num_unit, "ошибок на этом участке нет"

    is_correct,curr_num_unit,info=mask27_29(curr_num_unit)
    if is_correct:
        out_dict[30]=float(curr_num_unit)/float(mask_and_num_ip[30])
        if out_dict[30].is_integer(): #если мы в результате получаем число с десятичным куском, значит нач. данные заданы неверно
            out_dict[30]=int(out_dict[30])
            prs=float(out_dict[30]*mask_and_num_ip[30])/ float(num_unit)
            percents.write("/30"+"  | "+str(int(out_dict[30]))+" | "+str(prs)+"\n")
            out=[[s_index,f_index] for f_index,s_index in out_dict.items()]#создаем из словаря список списков, меняя порядок значений в каждом подсписке
            return out,'Преобразование из процентов прошло корректно'
        else:
            return None,'ошибка в начальных данных, на уровне значений /30  подсети'
    else:
        return None,info
