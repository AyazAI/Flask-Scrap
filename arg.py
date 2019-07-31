"""
Example Explaining Argument Parsing

Included in App as a function
"""

import argparse as arg

def get_data():
    print("Getting data")

def getSinglePlayerDetail():
    print("getSingle")


FUNCTION_MAP = {'get_data' : get_data, 
                'getSinglePlayerDetail': getSinglePlayerDetail
                }

parser = arg.ArgumentParser(description="Showing Addition")
parser.add_argument('-f','--first',type=int, metavar='' ,help="First Parameter")
parser.add_argument('-s','--second',type=int, metavar='' ,help="Second Param")
parser.add_argument('-st','--str',type=str, metavar='' ,help="Str Param")
parser.add_argument('command', choices=FUNCTION_MAP.keys(), help="If you specify scrap then only list of names under alphabet a and detail for first player will be displayed")
parser.add_argument("-p", "--port", action="store", default="8000")


args = parser.parse_args()
func = FUNCTION_MAP[args.command]
func()


