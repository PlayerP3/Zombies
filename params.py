import os,json

# load files in
with open(os.path.join(os.path.dirname(__file__),'configs/config_gun.json'),'r') as gun_attributes_file:

    gun_parameters = json.load(gun_attributes_file)