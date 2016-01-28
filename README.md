Network breakdown into subnetworks
---------------------

Django-приложение, 
реализуещее разбивку сети на меньшие подсети.

Результат представляет собой текстовый файл с разбивкой
(см. `results/all` )

Директория `results` содержит  информацию по  произведенной разбивке:

`results/percents` --  таблица, содержащая информацию: 

			по общему количеству меньших подсетей в разбивке,
			процент от общего роличества ip в долях единицы.

`results/network_matrix` -- информация по распределению подсетей относительно набора /24 подсетей (в формате вложенного списка )

##### Пример

[[[64, 30]], [[28, 30], [18, 29]], [[17, 29], [10, 30], [5, 28]], [[10, 29], [12, 30], [1, 27], [6, 28]]]

4 подсети  с маской /24

	[[64, 30]]
	[[28, 30], [18, 29]]  -- 28 подсетей  с маской /30 + 18 подсетей с маской /29
	[[17, 29], [10, 30], [5, 28]]
	[[10, 29], [12, 30], [1, 27], [6, 28]]

первое значимое число -- количество подсетей

второе число  -- маска подсети

(Первоначально,заданная сеть разбивается на подсети с маской /24 )


`results/all` -- основной результирующий файл

`results/list_c` --показывает, как заданная сеть была разбита на подсети с маской /24
(для дальнейшей обработки) 

------------------------

Пример разбивки ip адреса `10.11.12.0/22`
на подсети

	/27 --1	шт
	/28 --11 шт
	/29 --45 шт
	/30 --114 шт

вы можете найти в директории `results`

------------------------


#### Usage

	python manage.py runserver

(приложение не требует создания superuser и БД)

затем в браузере `http://127.0.0.1:8000/`

#### Requirements

    pip install django==1.6

(Python 2.7)


