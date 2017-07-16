def analyze(table, pivot_by, value, function, abc_groups, **kwargs):

    import pandas

    Grouped_table = table.pivot_table(index=pivot_by, values=value, aggfunc=function)

    Summ = Grouped_table.sum(axis=0)

    Grouped_table['Процент ' + value] = Grouped_table[value]/Summ[value]*100

    Grouped_table['Нарастающий процент ' + value] = Grouped_table.sort_values('Процент ' + value, ascending=False)['Процент ' + value].cumsum(0)

    Grouped_table['Группа по ' + value] = pandas.cut(Grouped_table['Нарастающий процент ' + value], abc_groups, right=True, labels = ['A', 'B', 'C'])

    return Grouped_table
