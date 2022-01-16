
def replace_template_params(line, params) -> str:
    while True:
        bri = line.find('|}')
        if bri < 0:
            return line
        bli = line.find('{|', 0, bri)
        if bli < 0:
            return line

        name = line[bli + 2:bri]
        if name in params:
            line = line.replace('{|' + name + '|}', params[name])
            continue

        
line='asdzxczxc{|var1|}czxcasdasd{|var2|}asdasd'
parm={'var1':'1111111111111111', 'var2':'2222222222222222'}

print(replace_template_params(line, parm))


