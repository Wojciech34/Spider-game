lines = []
for j in range(7):
    for i in range(9):
        lines.append(f'{150+j*100} {120+i*100}\n')
    if j != 6:    
        for i in range(8):
            lines.append(f'{200+j*100} {170+i*100}\n')


with open('positions2', 'w') as f:
    f.writelines(lines)

conns = []
for j in range(6):
    for i in range(8):
        conns.append(f'{j*17 + i} {j*17 + i + 9}\n')
for j in range(6):
    for i in range(1, 9):
        conns.append(f'{j*17 + i} {j*17 + i + 8}\n')
for j in range(6):
    for i in range(9, 17):
        conns.append(f'{j*17 + i} {j*17 + i + 9}\n')            
for j in range(6):
    for i in range(9, 17):
        conns.append(f'{j*17 + i} {j*17 + i + 8}\n')                  

with open('connections2', 'w') as f:
    f.writelines(conns)        