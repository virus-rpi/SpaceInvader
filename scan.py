import os
from custom_modules import importer
from custom_modules import loadEnv

importer = importer.importer()

reserved = [127]
env = loadEnv.load()
scanning_method = env["scanning_method"]
masscan_rate = env["masscan_rate"]

for i in range(1, 240):
    if i not in reserved:
        if scanning_method == "qubo":
            command = f'java -Dfile.encoding=UTF-8 -jar custom_modules/qubo.jar -th 500 -ti 1000 -fulloutput -range {i}.* -ports 25565'
            os.system(command)
        elif scanning_method == "masscan":
            print("Scann for ip range: " + f"{i}.255.255.0-{i}.255.255.255")
            output_file = f"outputs/{i}.255.255.0-{i}.255.255.255.txt"
            command = f'masscan -p25565 {i}.0.0.0-{i}.255.255.255 --rate={masscan_rate} -v'
            result = os.popen(command).read()
            with open(output_file, "w") as f:
                f.write(result)
            print(result)
            try:
                print(f"Importing data from: {output_file}")
                importer.importData(output_file)
            except FileNotFoundError:
                print("File not found: {output_file}")
                pass
