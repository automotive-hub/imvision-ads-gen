import json
from multiprocessing.pool import ThreadPool
import os
import platform
import subprocess
from subprocess import Popen
from models.vehicleInfo import VehicleInfo


class EditlyRunner:
    desktopRatio = {
        "width": 1920,
        "height": 1080,
        "name": "desktop_ratio"
    }
    mobileRatio = {
        "width": 640,
        "height": 640,
        "name": "mobile_ratio"
    }

    aspectRatio = [
        desktopRatio,
        mobileRatio,
    ]

    mediaFiles = []
    # make ads aspectRatio
    tempFolderLocation = os.getenv("TEMP_FOLDER_LOCATION")
    generatedFolder = os.getenv("GENERATED_FOLDER_LOCATION")

    # dataFile = build({})
    # with open('data.json', 'w') as f:
    #     f.write(json.dumps(dataFile))

    # with open('data.json', 'r+') as f:
    #     data = json.load(f)
    #     for ratio in aspectRatio:
    #         data["width"] = ratio["width"]
    #         data["height"] = ratio["height"]

    #         newFileName = '''{folder}/media_X_{name}.json'''.format(
    #             name=ratio["name"], folder=generatedFolder)
    #         os.makedirs(os.path.dirname(newFileName), exist_ok=True)
    #         with open(newFileName, 'w+') as newFile:
    #             mediaFiles.append(newFile.name)
    #             data["outPath"] = newFileName + ".mp4"
    #             json.dump(data, newFile)

    def createAdaptiveRatioDataFile(self, dataFile, info: VehicleInfo):
        data = dataFile
        for ratio in self.aspectRatio:
            data["width"] = ratio["width"]
            data["height"] = ratio["height"]
            newFolder = os.path.join(self.generatedFolder, info.vin)
            newFileName = '''{folder}/media_{name}.json'''.format(
                name=ratio["name"], folder=newFolder)
            os.makedirs(os.path.dirname(newFileName), exist_ok=True)
            with open(newFileName, 'w+') as newFile:
                self.mediaFiles.append(newFile.name)
                data["outPath"] = newFileName + ".mp4"
                json.dump(data, newFile)

    def render(self):
        headless_gl = ""
        if platform.system() == "Linux":
            headless_gl = '''xvfb-run -s "-ac -screen 0 1280x1024x24 "'''
        # copy paste form stackoverflow
        commands = ['''{headless_gl}editly {file}'''.format(
            file=name, headless_gl=headless_gl) for name in self.mediaFiles]
        n = 2  # the number of parallel processes you want
        for j in range(max(int(len(commands)/n), 1)):
            procs = [subprocess.Popen(i, shell=True)
                     for i in commands[j*n: min((j+1)*n, len(commands))]]
            for p in procs:
                p.wait()
            print("HelloRunPALLL")
        print("Hello")

    def task(self, file):
        os.system('''editly {file}'''.format(file=file))

    # for file in mediaFiles:
    #     os.system('''editly {file}'''.format(file=file))
