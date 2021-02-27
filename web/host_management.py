import utils
import os

settings = utils.yaml_to_dict(utils.correct_path('settings/host_management.yaml'))

# testing mac address is FF:FF:FF:FF:FF:FF


def is_valid_mac(mac):
    '''
    This will validate the mac address
    Mac addresses are hex based
    Mac addresses are 18 characters
    Example of a valid mac is the following 12:34:56:78:9A:BC
    :param mac: This asks for a mac address
    :return: This will return True if the mac address is a valid mac and False if it is not a valid mac
    '''
    # This is how I determine if it is correct to validate or not quickly
    valid = False
    # This checks if it is the default mac and will just return that as True
    if mac == settings['default_fake_mac']:
        return True
    # This is every single hex number
    all_hex_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F']
    # 17 is the length of a mac address with the separators
    if len(mac) == 17:
        # This is for keeping track of how many times a hex character has been found.
        correct = 0
        # This will go through every single mac address character. Ignoring the seperator
        for character in mac.replace(':', ''):
            # This will go through ever single hex character
            for hex_number in all_hex_numbers:
                # This will compare if the hex number is the number in question (treating everything as a string)
                if character.upper() == str(hex_number):
                    # This will help with validating later
                    correct = correct + 1
                # This cares about the number of hex numbers it will ignore the semicolones
                if correct == 11:
                    valid = True
    return valid


def register_host(mac):
    '''
    This registers the new host
    :param mac: A mac address to be added
    :return: Returns the file it writes to and settings being passed for troubleshooting
    '''
    # This loads the default settings from the default_settings file fake host as a template
    default_settings = utils.yaml_to_dict(utils.correct_path(settings['default_settings']))
    # This sets the default mac
    default_settings['mac'] = mac
    # This sets the default file
    # filename = utils.correct_path(settings['hosts'] + '/' + mac.replace(':', '') + '.yaml')
    filename = utils.correct_path(f"{settings['hosts']}/{mac.replace(':', '')}.yaml")
    # This writes the new file
    utils.dict_to_yaml(filename, default_settings)
    # This returns what was written and where for troubleshooting
    return (filename, default_settings)


def is_registered(mac):
    '''
    This will check if the mac address is already registered
    :param mac: Asks for the mac being queried about
    :return: True if it registered and False if it is not registered
    '''
    # This will go through every single mac address that is registered as the variable mac_in_list
    for mac_in_list in get_info('mac'):
        # This will check if the mac that is being checked is the the mac in the list mac_in_list from the for loop
        if mac == mac_in_list:
            # If the mac is already registered it will return a True
            return True
    # If the mac is not registered it will return a False
    return False


def update_host(mac, value, key):
    '''
    This will update the mac address of a specific host
    :param mac: The hosts mac address
    :param value: The new value you want updated
    :param key: The key. E.G. description, pxe-script, mac
    :return: Returns the updated host dictionary
    '''
    # This checks if the value being looked for is mac
    if value == 'mac':
        # This checks if the mac is valid
        if is_valid_mac(value) is False:
            return False
    # This will define the host as its dictionary
    host = get_info('host', mac=mac)
    # This will change the desired value
    host[key] = value
    # This will set the save path
    # host_path = settings['hosts'] + '/' + host['mac'].replace(':', '') + '.yaml'
    host_path = f"{settings['hosts']}/{host['mac'].replace(':', '')}.yaml"
    # This will make sure it is set correctly so it works in windows
    host_path = utils.correct_path(host_path)
    # This will write the dictionary to its yaml file
    utils.dict_to_yaml(host_path, host)
    # This will return the host as a dictionary
    return host


def remove_host(mac):
    '''
    This will remove a host
    :param mac: The host you want removed's mac
    :return: A string of the name of the file that was deleted
    '''
    # This will set the host as a variable
    # file_to_be_deleted = utils.correct_path(settings['hosts'] + '/' + mac.replace(':', '') + '.yaml')
    file_to_be_deleted = utils.correct_path(f"{settings['hosts']}/{mac.replace(':', '')}.yaml")
    # This will delete the host
    if os.file.path(file_to_be_deleted):
        os.remove(file_to_be_deleted)
    else:
        raise FileNotFoundError(f"The file {file_to_be_deleted} does not seem to exist. Please retry later")
    # This will return that it is deleted
    return f"{file_to_be_deleted} has been removed."


def get_info(desired_info, mac=None):
    '''
    This will return useful data that im looking for
    :param desired_info: Expects host, mac, description, or ipxe-script as a string
    :param mac: If you want a specific host you can enter it here
    :return: The desired information
    '''
    # This defines the list of all the hosts path
    hosts = os.listdir(settings['hosts'])
    # This defines the list of all the hosts
    for host_in_list in range(len(hosts)):
        # hosts[host_in_list] = utils.correct_path(settings['hosts'] + '/' + hosts[host_in_list])
        hosts[host_in_list] = utils.correct_path(f"{settings['hosts']}/{hosts[host_in_list]}")
    # This will set the data as a list
    information = []
    # This goes through all the data
    for host in hosts:
        # This checks if the data desired is the host list
        if desired_info == 'host':
            # This fills the information list with all the host information
            information.append(utils.yaml_to_dict(host))
        else:
            try:
                information.append(utils.yaml_to_dict(host)[desired_info])
            except KeyError:
                raise KeyError(f"Expected: host, mac, description, or ipxe-script as a {str(type('string'))}." 
                               f"Did not except {desired_info} as a {str(type(desired_info))}")
        # This checks to see if the mac variable has been changed
        if mac is not None:
            # This will just return the list that is requested
            for desired_mac in get_info('host'):
                if mac == desired_mac['mac']:
                    if desired_info == 'host':
                        return desired_mac
                    else:
                        return desired_mac[desired_info]
        # This will raise an error if the desired_info was set wrong and hopefully explain the correct info
    return information


if __name__ == '__main__':
    testing_mac = 'FF:FF:FF:FF:FF:FF'
    testing_description = 'This is a test will remove later'
    # print(is_valid_mac(testing_mac))
    # print(register_host(testing_mac))
    # print(is_registered(testing_mac))
    for key in ['host', 'mac', 'description', 'ipxe-script']:
        print(update_host(testing_mac, testing_description, key))
    # print(remove_host(testing_mac))
    # for desired_info in ['host', 'mac', 'description', 'ipxe-script']:
    #     print(get_info(desired_info))
