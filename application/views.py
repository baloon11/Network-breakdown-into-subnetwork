# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from application.forms import InputForm
from make_c_class import create_c_classes
from percent_converting import prs_conv
from make_network_matrix import create_matrix
from calc import create_table


def home(request):
    info = ''
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            fcd = form.cleaned_data
            mask=int(fcd['mask'])
            config=dict([('percent_'+str(m),0) for m in xrange(27,31)]+[('unit_'+str(m),0) for m in xrange(27,31)]) #словарь с нулевыми ключами

            for index,num in enumerate(xrange(27,31)):
                net=int(fcd['net_'+str(num)])

                if fcd['prs_or_unit_'+str(num)]=='%':
                    config['percent_'+str(num)]=net
                if fcd['prs_or_unit_'+str(num)]=='unit':
                    config['unit_'+str(num)]=net

            unit_ip_list,info=prs_conv(config,mask)
            if unit_ip_list:#если список не None
                network_matrix=create_matrix(unit_ip_list)
                curr_ip=[int(fcd[bite]) for bite in ['first_bite','second_bite','third_bite','fourth_bite']]
                main_ips=create_c_classes(curr_ip,mask)
                create_table(main_ips,network_matrix) #получаем окончательный файл
                info='Файл успешно сгенерирован'
    else:
        form = InputForm()
    return render_to_response('index.html',{'form': form,'info': info},
                              context_instance=RequestContext(request))