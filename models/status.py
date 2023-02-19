class Status():
    def __init__(self, classification, download, image, image_total, video):
        self.classification = classification
        self.download = download
        self.image = image
        self.image_total = image_total
        self.video = video

    def to_dict(self):
        return dict({
            "classification": self.classification,
            "download": self.download,
            "image": self.image,
            "image_total": self.image_total,
            "video":  self.video
        })
