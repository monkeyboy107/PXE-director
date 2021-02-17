import common_tools
import os

settings = common_tools.yaml_to_dict(common_tools.correct_path('settings/host_management.yaml'))

# testing mac address is FF:FF:FF:FF:FF:FF


# This will validate the mac address
# Mac addresses are hex based
# Mac addresses are 18 characters
# Example of a valid mac is the following 12:34:56:78:9A:BC
def is_valid_mac(mac):
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
    default_settings = common_tools.yaml_to_dict(common_tools.correct_path(settings['default_settings']))
    default_settings['mac'] = mac
    filename = common_tools.correct_path(settings['hosts'] + '/' + mac.replace(':', '') + '.yaml')
    common_tools.dict_to_yaml(filename, default_settings)
    return (filename, default_settings)


# This will check if the mac address is already registered
def is_registered(mac):
    # This will go through every single mac address that is registered as the variable mac_in_list
    for mac_in_list in get_info('mac'):
        # This will check if the mac that is being checked is the the mac in the list mac_in_list from the for loop
        if mac == mac_in_list:
            # If the mac is already registered it will return a True
            return True
    # If the mac is not registered it will return a False
    return False


# This will update the mac address of a specific host
def update_description(mac, description):
    # This will define the host as its dictionary
    host = get_info('host', mac=mac)
    # This will change the description to the desired description
    host['description'] = description
    # This will set the save path
    host_path = settings['hosts'] + '/' + host['mac'].replace(':', '') + '.yaml'
    # This will make sure it is set correctly so it works in windows
    host_path = common_tools.correct_path(host_path)
    # This will write the dictionary to its yaml file
    common_tools.dict_to_yaml(host_path, host)
    # This will return the host as a dictionary
    return host


# This will remove a host
def remove_host(mac):
    # This will set the host as a variable
    file_to_be_deleted = common_tools.correct_path(settings['hosts'] + '/' + mac.replace(':', '') + '.yaml')
    # This will delete the host
    os.remove(file_to_be_deleted)
    # This will return that it is deleted
    return file_to_be_deleted + ' has been removed.'


# This will return useful data that im looking for
def get_info(desired_info, mac=None):
    # This defines the list of all the hosts path
    hosts = os.listdir(settings['hosts'])
    # This defines the list of all the hosts
    for host_in_list in range(len(hosts)):
        hosts[host_in_list] = common_tools.correct_path(settings['hosts'] + '/' + hosts[host_in_list])
    # This will set the data as a list
    information = []
    # This goes through all the data
    for host in hosts:
        # This checks if the data desired is the host list
        if desired_info == 'host':
            # This fills the information list with all the host information
            information.append(common_tools.yaml_to_dict(host))
        else:
            try:
                information.append(common_tools.yaml_to_dict(host)[desired_info])
            except KeyError:
                raise KeyError('Expected: host, mac, description, or ipxe-script as a ' + str(type('string')) +
                               '. Did not except ' + desired_info + ' as a ' + str(type(desired_info)))
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
    print(is_valid_mac(testing_mac))
    print(register_host(testing_mac))
    print(is_registered(testing_mac))
    print(update_description(testing_mac, testing_description))
    print(remove_host(testing_mac))
    for desired_info in ['host', 'mac', 'description', 'ipxe-script']:
        print(get_info(desired_info))
