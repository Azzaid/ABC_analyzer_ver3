import pandas
import analyze_ABC
import Name_checker

# configure analysis
values_for_abc = {'Доход': {'column_name': 'Доход', 'function': 'sum', 'abc_groups': [0, 80, 95, 110]},
                  'Товарооборот': {'column_name': 'Товарооборот', 'function': 'sum', 'abc_groups': [0, 80, 95, 110]},
                  'Количество': {'column_name': 'Количество', 'function': 'count', 'abc_groups': [0, 80, 95, 110]}}

levels_for_abc = [['Группа', 'Подгруппа', 'Товар'], ['Группа', 'Подгруппа'], ['Группа']]

periods_for_abc = [['06-2015', '10-2015'], ['11-2015', '05-2016'], ['06-2016', '10-2016'], ['11-2016', '05-2017']]
# how many columns of group sugroup an so on are in excell file counting from 1
grouping_depth = 2

# choose output excel files
results_output_file = pandas.ExcelWriter(r"D:\PyToExel\Results\ABC_ver2.xlsx")
debug_output_file = pandas.ExcelWriter(r"D:\PyToExel\Results\ABC_test.xlsx")

# chose input excel files
data_to_analyse = pandas.read_excel(r"D:\PyToExel\Results\AllSales.xlsx", index_col='Дата')
Goods_table = pandas.read_excel(r"D:\PyToExel\Klassif\Klassif_ready.xlsx", index_col='Код')

#index groupp and goods names for bad names search
indexed_sales = data_to_analyse.set_index(['Группа', 'Подгруппа', 'Товар'], drop=True, inplace=False, append=True)
indexed_goods = Goods_table.set_index(['Группа', 'Подгруппа', 'Товар'], drop=True, inplace=False, append=True)

# check whether the names of goods in data_to_analyse are the same as in the Goods_table an get the list of possible name changes
bad_names_list = Name_checker.check(check_table=indexed_sales, master_table=indexed_goods, recursion_depth=1, grouping_depth=grouping_depth)
print(bad_names_list)

# list all months in sales table
data_to_analyse = data_to_analyse.sort_index()
begin_date = data_to_analyse.head(1).index[0]                                                                                #
end_date = data_to_analyse.tail(1).index[0]
months_to_analyse = pandas.date_range(begin_date, end_date, freq='M', closed='right').strftime('%Y-%m')

list_of_all_times = periods_for_abc.append(months_to_analyse)

all_tables_list = {}

# abc analysis
for time_shard in list_of_all_times:
    all_tables_list[time_shard] = analyze_ABC.deep_analyze()

# constructing output table
