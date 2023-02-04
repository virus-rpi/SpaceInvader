import os

reserved = [10, 127]

for i in range(1, 240):
    if not i in reserved:
    	os.system(f'java -Dfile.encoding=UTF-8 -jar qubo.jar -th 500 -ti 1000 -fulloutput -range {i}.* -ports 25565')