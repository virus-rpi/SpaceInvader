import os
from custom_modules import importer

i = importer.importer()

reserved = [127]


for i in range(1, 240):
    if i not in reserved:
        os.system(f'java -Dfile.encoding=UTF-8 -jar custom_modules/qubo.jar -th 500 -ti 1000 -fulloutput -range {i}.* -ports 25565')
    i.importData(f"{i}.0.0.0-{i}.255.255.255.txt")
