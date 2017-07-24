import pandas
import analyze_ABC
import Name_checker

# configure analysis
values_for_abc = {'Доход': {'column_name': 'Доход', 'function': 'sum', 'abc_groups': [0, 80, 95, 110]},
                  'Товарооборот': {'column_name': 'Товарооборот', 'function': 'sum', 'abc_groups': [0, 80, 95, 110]},
                  'Количество': {'column_name': 'Количество', 'function': 'count', 'abc_groups': [0, 80, 95, 110]}}

levels_for_abc = [['Группа', 'Подгруппа', 'Товар'], ['Группа', 'Подгруппа'], ['Группа']]

periods_for_abc = {'Сезон_1': ['06-2015', '10-2015'], 'Не_сезон_1': ['11-2015', '05-2016'],
                   'Сезон_2': ['06-2016', '10-2016'], 'Не_сезон_2': ['11-2016', '05-2017']}
#how many columns of group sugroup an so on are in excell file including column goods name and counting from 1
grouping_depth = 3

# choose output excel files
results_output_file = pandas.ExcelWriter(r"D:\PyToExel\Results\ABC_ver2.xlsx")
debug_output_file = pandas.ExcelWriter(r"D:\PyToExel\Results\ABC_test.xlsx")

# chose input excel files
data_to_analyse = pandas.read_excel(r"D:\PyToExel\Results\AllSales.xlsx", index_col='Дата')
Goods_table = pandas.read_excel(r"D:\PyToExel\Klassif\Klassif_ready.xlsx", index_col='Код')

#turn groups and goods names into index cos panda cant read russsian str into index when reading from excell
data_to_analyse.set_index(['Группа', 'Подгруппа', 'Товар'], drop=True, inplace=True)
Goods_table.set_index(['Группа', 'Подгруппа', 'Товар'], drop=True, inplace=True)

# check whether the names of goods in data_to_analyse are the same as in the Goods_table an get the list of possible name changes
bad_names_list = Name_checker.check(check_table=data_to_analyse, master_table=Goods_table, recursion_depth=1, grouping_depth=grouping_depth)
print(bad_names_list)
