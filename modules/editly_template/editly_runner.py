import json
from multiprocessing.pool import ThreadPool
import os
import platform
import subprocess
from subprocess import Popen
from models.vehicleInfo import AdsMedia, MediaRatio, VehicleInfo


class EditlyRunner:
    desktopRatio = MediaRatio(
        width=1920,
        height=1080,
        name="desktop_ratio",
        type="desktop_video_ref",
        file_extension=".mp4"
    )
    mobileRatio = MediaRatio(
        width=640,
        height=640,
        name="mobile_ratio",
        type="mobile_video_ref",
        file_extension=".mp4"
    )
    # bannerRatio = {
    #     "width": 728,
    #     "height": 90,
    #     "name": "banner_ratio",
    #     "file_extension": ".png"
    # }
    gifRatio = MediaRatio(
        width=300,
        height=60,
        name="gif_ratio",
        type="gif_ref",
        file_extension=".gif")

    aspectRatio = [
        desktopRatio,
        mobileRatio,
        # bannerRatio
    ]

    def __init__(self):
        self.mediaFiles = []
        self.adsMedia: AdsMedia = AdsMedia()
        self.tempFolderLocation = os.getenv("TEMP_FOLDER_LOCATION")
        self.generatedFolder = os.getenv("GENERATED_FOLDER_LOCATION")

    # make ads aspectRatio

    def createAdaptiveRatioDataFile(self, dataFile, info: VehicleInfo):
        data = dataFile
        for ratio in self.aspectRatio:
            data["width"] = ratio.width
            data["height"] = ratio.height
            newFolder = os.path.join(self.generatedFolder, info.id)
            newFileName = '''{folder}/media_{name}.json'''.format(
                name=ratio.name, folder=newFolder)
            os.makedirs(os.path.dirname(newFileName), exist_ok=True)
            with open(newFileName, 'w+') as newFile:
                self.mediaFiles.append(newFile.name)
                data["outPath"] = newFileName + ratio.file_extension
                json.dump(data, newFile)
                file = os.path.basename(data["outPath"])
                self.adsMedia.addMediaRef(
                    ratio=ratio, vin=info.id,  fileName=file)

    def render(self):
        headless_gl = ""
        # TODO require in-dept on xvfb-run -a -s "-ac -screen 0 1280x1024x24
        # currently i don't understand what the shit that was
        if platform.system() == "Linux":
            headless_gl = '''xvfb-run -a -s "-ac -screen 0 1280x1024x24" '''
        # copy paste form stackoverflow
        commands = ['''{headless_gl}editly {file}'''.format(
            file=name, headless_gl=headless_gl) for name in self.mediaFiles]
        print(commands)

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
