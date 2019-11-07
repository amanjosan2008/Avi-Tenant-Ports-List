import re
import json

f = open("avi_config.json","r")
config = json.load(f)
f.close()

listed = {}

for i in config['Tenant']:
    port_list =[]
    for k,v  in i.items():
        if k == 'name':
            #print("Tenant: ", v,'\n')
            for j in range(len(config['VirtualService'])):
                if v == config['VirtualService'][j]['tenant_ref'].split('=')[-1]:
                    try:
                        pool = (config["VirtualService"][j]["pool_ref"].split("name=")[-1]).split('&')[0]
                        for m in range(len(config["Pool"])):
                            if (config["Pool"][m]["name"]) == pool:
                                try:
                                    for n in range(len(config["Pool"][m]["servers"])):
                                        try:
                                            port_list.append(config["Pool"][m]["servers"][n]['port'])
                                        except KeyError:
                                            port_list.append(config["Pool"][m]["default_server_port"])
                                except KeyError:
                                    pass
                    except KeyError:
                        pass
                    try:
                        pool_group = (re.findall(r'name=.+', config["VirtualService"][j]["pool_group_ref"]))[0].strip('name=').split('&')[0]
                        for n in range(len(config["PoolGroup"])):
                            if (config["PoolGroup"][n]["name"]) == pool_group:
                                for p in range(len(config["PoolGroup"][n]["members"])):
                                    for q in range(len(config["Pool"])):
                                        if (config["PoolGroup"][n]["members"][p]["pool_ref"].split('name=')[-1]).split('&')[0] == config["Pool"][q]["name"]:
                                            try:
                                                for o in range(len(config["Pool"][q]["servers"])):
                                                    try:
                                                        port_list.append(config["Pool"][q]["servers"][o]['port'])
                                                    except KeyError:
                                                        port_list.append(config["Pool"][q]["servers"][o]['port'])
                                            except KeyError:
                                                pass
                    except:
                        pass
            plist = set(port_list)
            listed.update({v:plist})

for k,v in listed.items():
    print("Tenant: ", k, "\nNo of Ports: ", len(v), '\n', [i for i in v if len(v) >0], '\n')
