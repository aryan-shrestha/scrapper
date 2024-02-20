def list_to_dict(input_list):
    result_dict = {}
    current_key = None

    for item in input_list:
        if ':' in item:
            current_key = item.replace(':', '')
            result_dict[current_key] = None
        elif current_key is not None:
            result_dict[current_key] = item

    return result_dict
