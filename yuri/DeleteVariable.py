def deleteVariable(name:str):
    if name in globals():
        print(name, 'deleted')
        del globals()[name]
