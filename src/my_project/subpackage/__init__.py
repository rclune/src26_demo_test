"""A subpackage"""

def common_function(my_param:str):
    """This function is used a lot
    
    :param my_param: This paramater is a string, defaults to None
    :type my_param: string
    :return: Returns an appended string.
    :rtype: string
    """

    my_return = my_param + " appended to the string!"
    
    return my_return

def obscure_function():
    """This function isn't used as often"""
    pass
