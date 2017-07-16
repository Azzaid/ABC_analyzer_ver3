import pandas
import analyze_ABC
#import Name_checker

# define excel files
results_output_file = pandas.ExcelWriter(r"D:\PyToExel\Results\ABC_ver2.xlsx")
debug_output_file = pandas.ExcelWriter(r"D:\PyToExel\Results\ABC_test.xlsx")

# read input data
data_to_analyse = pandas.read_excel(r"D:\PyToExel\Results\AllSales.xlsx", index_col='Дата')
Goods_table = pandas.read_excel(r"D:\PyToExel\Klassif\Klassif_ready.xlsx", index_col='Код')

#turn groups and goods names into index cos panda cant read russsian str into index when reading from excell
data_to_analyse.set_index(['Группа', 'Подгруппа', 'Товар'], drop=True, inplace=True)
Goods_table.set_index(['Группа', 'Подгруппа', 'Товар'], drop=True, inplace=True)

# configure analysis
values_for_abc = {'Доход': {'column_name': 'Доход', 'function': 'sum', 'abc_groups': [0, 80, 95, 110]},
                  'Товарооборот': {'column_name': 'Товарооборот', 'function': 'sum', 'abc_groups': [0, 80, 95, 110]},
                  'Количество': {'column_name': 'Количество', 'function': 'count', 'abc_groups': [0, 80, 95, 110]}}

levels_for_abc = [['Группа', 'Подгруппа', 'Товар'], ['Группа', 'Подгруппа'], ['Группа']]

periods_for_abc = {'Сезон_1': ['06-2015', '10-2015'], 'Не_сезон_1': ['11-2015', '05-2016'],
                   'Сезон_2': ['06-2016', '10-2016'], 'Не_сезон_2': ['11-2016', '05-2017']}

# check whether the names of goods in data_to_analyse are the same as in the Goods_table an get the list of possible name changes
bad_names_list = Name_checker.check(check_table=list(data_to_analyse.index.get_level_values(2).drop_duplicates(keep='first')),
                                    master_table=list(Goods_table.index.get_level_values(2).drop_duplicates(keep='first')))
print(bad_names_list)






data_to_analyse.set_index(['Группа', 'Товар'], drop=True, append=True, inplace=True)
for pisun in data_to_analyse.xs('01. Кровельные и гидроизоляционные материалы', axis=0, level=1)['Подгруппа']:
    print(pisun)


#Goods_table.set_index(['Группа', 'Подгруппа', 'Товар'], drop=True, inplace=True)

#print(Main_table.xs('01. Кровельные и гидроизоляционные материалы', axis=0, level=0).index)
#print(Goods_table.index)
#print(data_to_analyse.index.difference(Goods_table.index))
#sale_month = pandas.DataFrame(index=data_to_analyse.pivot_table(index=level, values=['Доход'], aggfunc='sum').index)
