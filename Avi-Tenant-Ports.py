import re
import json

f = open("avi_config.json","r")
config = json.load(f)
f.close()

for i in config['Tenant']:
    for k,v  in i.items():
        if k == 'name':
            print("Tenant: ", v,'\n')
            for j in range(len(config['VirtualService'])):
                if v == config['VirtualService'][j]['tenant_ref'].split('=')[-1]:
                    print("VS: ", config['VirtualService'][j]['name'])
                    try:
                        pool = (config["VirtualService"][j]["pool_ref"].split("name=")[-1]).split('&')[0]
                        print(" - Pool: ", pool)
                        for m in range(len(config["Pool"])):
                            if (config["Pool"][m]["name"]) == pool:
                                try:
                                    for n in range(len(config["Pool"][m]["servers"])):
                                        try:
                                            print("   - ", config["Pool"][m]["servers"][n]['port'])
                                        except KeyError:
                                            print("   - ", config["Pool"][m]["default_server_port"])
                                except KeyError:
                                    print('   - No Servers')
                    except KeyError:
                        pass
                    try:
                        pool_group = (re.findall(r'name=.+', config["VirtualService"][j]["pool_group_ref"]))[0].strip('name=').split('&')[0]
                        print(" - Pool Group: ", pool_group)
                        for n in range(len(config["PoolGroup"])):
                            if (config["PoolGroup"][n]["name"]) == pool_group:
                                for p in range(len(config["PoolGroup"][n]["members"])):
                                    for q in range(len(config["Pool"])):
                                        if (config["PoolGroup"][n]["members"][p]["pool_ref"].split('name=')[-1]).split('&')[0] == config["Pool"][q]["name"]:
                                            try:
                                                for o in range(len(config["Pool"][q]["servers"])):
                                                    try:
                                                        print("   - ", config["Pool"][q]["servers"][o]['port'])
                                                    except KeyError:
                                                        print("   - ", config["Pool"][q]["default_server_port"])
                                            except KeyError:
                                                print('   - No Servers')
                    except:
                        #print("   - No Pool Group")
                        pass
            print("\n")
