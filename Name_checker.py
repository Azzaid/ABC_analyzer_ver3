def check(check_table, master_table, recursion_depth, grouping_depth, **kwargs):
    posible_changes = {}

    names_to_check_list = check_table.index.get_level_values(recursion_depth).drop_duplicates(keep='first')
    right_names_list = master_table.index.get_level_values(recursion_depth).drop_duplicates(keep='first')

#check names on this level
    for name_to_check in names_to_check_list:
        if name_to_check not in right_names_list:
            posible_changes[name_to_check] = []
            for right_name in right_names_list:
                match_worlds = 0
                right_name_lenght = len(right_name.split(" "))
                for word_to_check in name_to_check.split(" "):
                    if word_to_check in right_name: match_worlds += 1
                if (right_name_lenght - match_worlds) <= 1 and match_worlds > 0: posible_changes[name_to_check].append(right_name)

#go one grouping level down
    if recursion_depth < grouping_depth:
        for group in names_to_check_list:
            posible_changes.update(check(check_table=check_table.xs(group, axis=0, level=recursion_depth), master_table=master_table.xs(group, axis=0, level=recursion_depth), recursion_depth=recursion_depth + 1, grouping_depth=grouping_depth))

    return (posible_changes)
