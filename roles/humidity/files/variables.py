#!/usr/bin/python3

import yaml
filename = 'main.yml'

def get_var(requested):
    with open(filename) as f:
        try:
            vars_dict = yaml.safe_load(f)
            for key, value in vars_dict.items():
                answer = vars_dict[requested]
                return(answer)
        except yaml.YAMLError as exc:
            print(exc)