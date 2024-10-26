

def create_json_dict(input_list):
    count = len(input_list)
    json_dict = {str(count): ",".join(map(str, input_list))}
    return json_dict
