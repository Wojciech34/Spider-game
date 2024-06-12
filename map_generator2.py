import numpy as np
np.random.seed(133)

points = []
lines = []
for j in range(90):
    flag = True
    tries = 0
    while flag:
        tries += 1
        if tries > 10000:
            break
        x = np.random.uniform(low=150, high=800)
        y = np.random.uniform(low=120, high=900)
        ok = True
        for point in points:
            if not (abs(point[0] - x) > 10 and abs(point[1] - y) > 10):
                ok = False
                break
        if ok:
            lines.append(f'{x} {y}\n')
            points.append((x, y))
            flag = False
    


with open('data/positions4', 'w') as f:
    f.writelines(lines)

n = len(lines)
conns = []
for j in range(n):
    to_check = [j]
    tries = 0
    flag = True
    for _ in range(2):
        x = np.random.randint(n)
        while x in to_check or abs(points[x][0]-points[j][0]) > 100 or abs(
            points[x][1]-points[j][1]) > 100: # we want neighbours to be close to each other
            x = np.random.randint(n)
            tries += 1
            if tries > 1000:
                flag = False
                break
        if flag:    
            conns.append(f'{j} {x}\n')
            to_check.append(x)
       

with open('data/connections4', 'w') as f:
    f.writelines(conns)        