import requests
import ast
import csv


def access_asterank(inclination_max, eccentricity_max, semi_major_max, profit_min=0, num_objects=1):
    """
    Returns a list of dictionaries for each asteroid object
    :param inclination_max: degrees
    :param eccentricity_max:
    :param semi_major_max: AU
    :param profit_min: dollars
    :param num_objects: integer
    :return:
    """

    data = requests.get(f'http://asterank.com/api/asterank?query={{"e":{{"$lt":{eccentricity_max}}},'
                        f'"i":{{"$lt":{inclination_max}}},"a":{{"$lt":{semi_major_max}}}, '
                        f'"profit":{{"$gt": {profit_min}}}}}&limit={num_objects}')

    content = data._content.decode("utf-8")

    content = ast.literal_eval(content)

    return content


def filter_dictionaries(list_of_dictionaries):
    """
    Just filters out the things we actually want
    :param list_of_dictionaries: self explanatory
    :return:
    """
    temp_list = []
    for dictionary in list_of_dictionaries:
        temp_dict = dict()
        temp_dict['Object Name'] = dictionary['full_name']
        temp_dict['NEO?'] = dictionary['neo']
        temp_dict['Profit ($)'] = dictionary['profit']
        temp_dict['Eccentricity'] = dictionary['e']
        temp_dict['Inclination (degrees)'] = dictionary['i']
        temp_dict['Semi-major Axis (AU)'] = dictionary['a']
        temp_list.append(temp_dict)
    return temp_list


def write_content_dict_to_csv(file_location, content_dictionary):
    """
    All this does is write the content dictionary to a csv
    :param file_location: location of the file
    :param content_dictionary: dictionary that you want to convert to csv
    :return: nothing
    """
    a_file = open(file_location, "w", newline='')
    dict_writer = csv.DictWriter(a_file, content_dictionary[0].keys())
    dict_writer.writeheader()
    dict_writer.writerows(content_dictionary)
    a_file.close()


if __name__ == '__main__':
    content_dict = filter_dictionaries(access_asterank(10, .3, 2, 100000000, 100))
    write_content_dict_to_csv('testing_csv.csv', content_dict)
    print('no errors')
