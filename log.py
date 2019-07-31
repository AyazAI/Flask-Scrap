import logging

def write_to(a):
    if a == 'X':
        logging.basicConfig(filename='X.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
        logging.warning('This will get logged to a file second')


write_to('X')