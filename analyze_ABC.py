import pandas

def analyze(table, pivot_by, value, function, abc_groups, **kwargs):

    Grouped_table = table.pivot_table(index=pivot_by, values=value, aggfunc=function)

    Summ = Grouped_table.sum(axis=0)

    Grouped_table['Процент ' + value] = Grouped_table[value]/Summ[value]*100

    Grouped_table['Нарастающий процент ' + value] = Grouped_table.sort_values('Процент ' + value, ascending=False)['Процент ' + value].cumsum(0)

    Grouped_table['Группа по ' + value] = pandas.cut(Grouped_table['Нарастающий процент ' + value], abc_groups, right=True, labels = ['A', 'B', 'C'])

    return Grouped_table


def deep_analyze(table, time, upgroup, levels_for_ABC, values_for_ABC, grouping_depth, debug_file, recursion_depth, upgroup_list,  **kwargs):

    print('глубина реурсии', recursion_depth, 'анализирую уровень ', levels_for_ABC[recursion_depth], 'внутри ', upgroup)

    #pre-made short table to fill it with info from different values analysis
    if type(table[levels_for_ABC[recursion_depth]]) == str:
        #short_table = pandas.DataFrame({levels_for_ABC[recursion_depth]: table[levels_for_ABC[recursion_depth]], (time, '% дохода'):100, (time, 'группы'):'AAA'})
        short_table = pandas.DataFrame.from_dict({(time, '% дохода'):{table[levels_for_ABC[recursion_depth]]:100}, (time, 'группы'):{table[levels_for_ABC[recursion_depth]]:'AAA'}})
        print(short_table)
        return(short_table)
    else:
        short_table = pandas.DataFrame(
            index=table[levels_for_ABC[recursion_depth]].drop_duplicates(keep='first'),
            columns=[[time], ['% дохода']])
        short_table.loc[:, (time, 'группы')] = ''

    #calculate income percent and fill it into short table
    income_table = table.pivot_table(index=levels_for_ABC[recursion_depth],
                                     values=['Сумма', 'Доход', 'Дней в месяце', 'Дней в наличии'],
                                     aggfunc='sum')
    short_table.loc[:, (time, '% дохода')] = income_table['Доход'] / income_table['Сумма'] * 100
    short_table.loc[:, (time, '% времени')] = income_table['Дней в наличии'] / income_table['Дней в месяце'] * 100

    #analyse abc for every value listed in main programm block
    for value in values_for_ABC:
        debug_table = analyze(
            table = table,
            pivot_by = levels_for_ABC[recursion_depth],
            value = values_for_ABC[value]['column_name'],
            function = values_for_ABC[value]['function'],
            abc_groups = values_for_ABC[value]['abc_groups'])

        #fill info about abc group into short table
        short_table.loc[:, (time, 'группы')] += \
            debug_table['Группа по ' + value].astype(str)

        debug_table.to_excel(debug_file, str(time)+str(upgroup)[:8]+str(value))

    #Construct multiindex for proper sorting
    for i in range(0,grouping_depth+1):
        if i < recursion_depth:
            short_table[levels_for_ABC[i]] = str(upgroup_list[i])
        elif i == recursion_depth:
            short_table.reset_index(inplace=True, col_level=0)
        elif i > recursion_depth:
            short_table[levels_for_ABC[i]] = ''
    short_table.set_index(levels_for_ABC, inplace=True)

    #if there are subgrupps
    if recursion_depth < grouping_depth:

        # analyse subgroups in every group
        for GroupToDive in short_table.index.get_level_values(recursion_depth).drop_duplicates():
            print('провожу анализ подгрупп в группе ', GroupToDive)
            passing_list = upgroup_list[:]
            passing_list.append(str(GroupToDive))
            short_table_part = deep_analyze(
                table=table[table[levels_for_ABC[recursion_depth]] == GroupToDive],
                upgroup=GroupToDive,
                time=time,
                levels_for_ABC=levels_for_ABC,
                values_for_ABC=values_for_ABC,
                grouping_depth=grouping_depth,
                recursion_depth=recursion_depth+1,
                debug_file=debug_file,
                upgroup_list=passing_list)
            short_table = pandas.concat((short_table, short_table_part), axis=0, join='outer')

    return(short_table)
