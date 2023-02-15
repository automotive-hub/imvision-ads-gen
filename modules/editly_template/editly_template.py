class EditlyTemplate:
    def makeDealershipSense(self, dealerShipIMGPath, senseDuration=3, voicePath=""):
        print("makeDealershipLayer")

        layers = [
            {
                "type": "image",
                "path": dealerShipIMGPath
            },
            {
                "type": "title",
                "text": "WE GOT YOU COVERED"
            }]
        if len(voicePath) != 0:
            layers.insert(0, {"type": 'detached-audio', "path": voicePath})

        sense = {
            "duration": senseDuration,
            "layers": layers
        }
        return sense

    def makeIntroGreeting(self, text, fontPath):
        layers = [
            {
                "type": "rainbow-colors"
            },
            {
                "type": "title",
                        "fontPath": fontPath,
                        "text": text
            }
        ]
        sense = {
            "duration": 1,
            "layers": layers
        }
        return sense

    def makeVehicleMainEntrySense(self, vehicleMainIMG, vehicleName):
        layers = [
            {
                "type": "image",
                "path": vehicleMainIMG
            },
            {
                "type": "title",
                "text": vehicleName,
                "position": "center"
            }
        ]
        sense = {
            "duration": 2,
            "layers": layers
        }
        return sense

    def makeVehicleIMGSense(self, dealerShipIMGPath, senseDuration=0.3, voicePath=""):
        print("makeVehicleSense")

        layers = [
            {
                "type": "image",
                "path": dealerShipIMGPath,
                "resizeMode": "cover"
            }
        ]
        sense = {
            "layers": layers
        }
        return sense

    def makeVehicleCallToAction(self, callToActionIMGPath, senseDuration=0.3, voicePath=""):
        layers = [
            {
                "type": "image",
                "path": callToActionIMGPath,
                "resizeMode": "cover"
            }
        ]
        sense = {
            "duration": 3,

            "transition": {
                "name": "colorphase",
                "duration": 0.5
            },
            "layers": layers
        }
        return sense

    def buildDataFrame(self, outPath, fontPath, audioPath, senses=[]):
        return {
            "outPath": outPath,
            "defaults": {
                "layer": {
                    "fontPath": fontPath
                },
            },
            "clips": senses,
            "audioFilePath": audioPath,
        }
