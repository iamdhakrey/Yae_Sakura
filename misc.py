import json

def return_data(id,file_path):
    """
        return guild_id data
    """ 
    with open(file_path,'r') as f:
        data = json.load(f)
    try:
        # print(data)
        return dict(data[id])
    except Exception as e:
        print(e)
        return None

def write_data(wdata,file_path):
    """
    write data in json file
    """
    with open(file_path,"r") as f:
        data = json.load(f)
    
    data.update(wdata)
    # print(data)
    with open(file_path,'w') as f:
        json.dump(data,f,indent=4)

def check_exist(id,file_path):
    """
    Check owner exist or not
    """
    with open(file_path,'r') as f:
        data = json.load(f)
    try:
        # print(data[id])
        if data[id]:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def check_role():
    print("ados")