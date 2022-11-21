
import json





def iterate_dict(dict_to_iterate):
    data = []
    for key, value in dict_to_iterate.items():
        if type(value) == dict:
          
            iterate_dict(value)
            to_append = {key:value}
            data.append(to_append)
        else:
            print(key + "::" + str(value))
            to_append = {key:value}
            data.append(to_append)

    return data