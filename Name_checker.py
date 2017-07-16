def check(check_table, master_table, recursion_depth, grouping_depth, **kwargs):

    posible_changes = {}


    if recursion_depth < grouping_depth:
        for group in check_table:
            posible_changes.update(check(check_table=check_table(), master_table, recursion_depth, grouping_depth + 1))
        for name_to_check in check_table:
            if name_to_check not in master_table:
                posible_changes[name_to_check] = []
                for right_name in master_table:
                    match_worlds = 0
                    right_name_lenght = len(right_name.split(" "))
                    for word_to_check in name_to_check.split(" "):
                        if word_to_check in right_name: match_worlds += 1
                    if (match_worlds - right_name_lenght) <= 1 and match_worlds > 0 : posible_changes[name_to_check].append(right_name)
    return (posible_changes)
