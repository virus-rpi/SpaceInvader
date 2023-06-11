import os
from custom_modules import importer
from custom_modules import loadEnv

importer = importer.importer()

reserved = [127]
env = loadEnv.load()
scanning_method = env["scanning_method"]
masscan_rate = 1000


for i in range(1, 240):
    if i not in reserved:
        if scanning_method == "qubo":
            os.system(f'java -Dfile.encoding=UTF-8 -jar custom_modules/qubo.jar -th 500 -ti 1000 -fulloutput -range {i}.* -ports 25565')
        elif scanning_method == "masscan":
            os.system(f'masscan -p25565 {i}.0.0.0-{i}.255.255.255 --rate={masscan_rate} --output-filename outputs/{i}.0.0.0-{i}.255.255.255.txt')
        try:
            importer.importData(f"outputs/{i}.0.0.0-{i}.255.255.255.txt")
        except FileNotFoundError:
            pass
