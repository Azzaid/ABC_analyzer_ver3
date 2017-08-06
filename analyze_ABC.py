import pandas

def analyze(table, pivot_by, value, function, abc_groups, **kwargs):

    Grouped_table = table.pivot_table(index=pivot_by, values=value, aggfunc=function)

    Summ = Grouped_table.sum(axis=0)

    Grouped_table['Процент ' + value] = Grouped_table[value]/Summ[value]*100

    Grouped_table['Нарастающий процент ' + value] = Grouped_table.sort_values('Процент ' + value, ascending=False)['Процент ' + value].cumsum(0)

    Grouped_table['Группа по ' + value] = pandas.cut(Grouped_table['Нарастающий процент ' + value], abc_groups, right=True, labels = ['A', 'B', 'C'])

    return Grouped_table


def deep_analyze(table, time, upgroup, levels_for_ABC, values_for_ABC, grouping_depth, recursion_depth, **kwargs):

    print('глубина реурсии', recursion_depth, 'анализирую', levels_for_ABC[recursion_depth], 'внутри', upgroup)

    #create dict levels and keys to store analysis results
    debug_table_list = {levels_for_ABC[recursion_depth]:{upgroup:{}}}
    short_table_list = {levels_for_ABC[recursion_depth]:{upgroup:{}}}

    #pre-made short table to fill it with info from different values analysis
    print('анализирую строки', table[levels_for_ABC[recursion_depth]], '    ', len(table[levels_for_ABC[recursion_depth]]))
    if type(table[levels_for_ABC[recursion_depth]]) != str:
        short_table_list[levels_for_ABC[recursion_depth]] = pandas.DataFrame(index=table[levels_for_ABC[recursion_depth]].drop_duplicates(keep='first'),
                                                                         columns=[[time], ['% дохода']])
    else:
        short_table_list[levels_for_ABC[recursion_depth]] = pandas.DataFrame(index=table[levels_for_ABC[recursion_depth]],
                                                                         columns=[[time], ['% дохода']])
    short_table_list[levels_for_ABC[recursion_depth]].loc[:, (time, 'группы')] = ''

    #calculate income percent and fill it into short table
    income_table = table.pivot_table(index=levels_for_ABC[recursion_depth],
                                     values=['Себестоимость', 'Доход'],
                                     aggfunc='sum')
    short_table_list[levels_for_ABC[recursion_depth]].loc[:, (time, '% дохода')] = income_table['Доход'] / income_table['Себестоимость'] * 100

    #analyse abc for every value listed in main programm block
    for value in values_for_ABC:
        debug_table_list[levels_for_ABC[recursion_depth]][value] = analyze(table = table,
                                                                                 pivot_by = levels_for_ABC[recursion_depth],
                                                                                 value = values_for_ABC[value]['column_name'] ,
                                                                                 function = values_for_ABC[value]['function'],
                                                                                 abc_groups = values_for_ABC[value]['abc_groups'])

        #fill info about abc group and income percent into short table
        short_table_list[levels_for_ABC[recursion_depth]].loc[:, (time, 'группы')] += debug_table_list[levels_for_ABC[recursion_depth]][value]['Группа по ' + value].astype(str)

    #analyse subgrupp if there are subgrupp
    if recursion_depth < grouping_depth:

        #turn group name into index to chose rows for in-group analysis
        table.set_index([levels_for_ABC[recursion_depth]], drop=True, inplace=True, append=False)

        # analyse subgroups in every group
        print('провести анализ в группах', table.index.drop_duplicates(keep='first'))
        for GroupToDive in table.index.drop_duplicates(keep='first'):
            print('провожу анализ подгрупп в группе', GroupToDive)
            deeper_debug_table_list, deeper_short_table_list = deep_analyze(table=table.xs(GroupToDive, axis=0),
                                                                            upgroup=GroupToDive,
                                                                            time=time,
                                                                            levels_for_ABC=levels_for_ABC,
                                                                            values_for_ABC=values_for_ABC,
                                                                            grouping_depth=grouping_depth,
                                                                            recursion_depth=recursion_depth+1)
            #add results to a listst
            debug_table_list.update(deeper_debug_table_list)
            short_table_list.update(deeper_short_table_list)

    return(debug_table_list, short_table_list)

