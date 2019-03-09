class Photo:
    
    def __init__(self, orientation: bool, numTags: int, tags: list, index: int):
        self.index = index
        self.orientation = orientation
        self.numTags = numTags
        self.tags = tags

    def __repr__(self):
        result = "Photo: " + str(self.index) + "Orientation: " + str(self.orientation) +"tags " + str(self.tags)
        return result

class Slide:
    def __init__(self, photos:list, index: int = 0, prev = None, next = None):
        self.index = index
        self.photos = photos

        self.tags = []
        for photo in self.photos:
            self.tags.extend(photo.tags)
        self.tags = list(set(self.tags))
        self.number_of_tags = len(self.tags)
        self.prev = prev
        self.next = next
        self.best_partner_points = -1
        self.best_partner_index = -1
        self.has_coincidence = False


    def commonTags(self, elem2):
        return len(list(set(self.tags).intersection(set(elem2.tags))))

    # def puntuation(photo1: Photo, photo2: Photo):
    #     common = Slide.commonTags(photo1, photo2)
    #     return min(common, len(photo1.tags) - common, len(photo2.tags) - common)
    
    def points(self, slide):
        common = self.commonTags(slide)
        points = min(common, len(self.tags) - common, len(slide.tags) - common)
        return points

    def parse_file(file_name: str) -> list:
        photos = []
        with open(file_name) as file:
            lines = [line.replace('\n', '') for line in file]
            lines.pop(0)
            photos = [line.split(" ") for line in lines]
            photos = [{ 
                        "index": idx,
                        "orientation": (photo[0] != "H"), 
                        "number_of_tags": int(photo[1]),
                        "tags": photo[2::]
                    } for idx, photo in enumerate(photos)]
            photos = [  Photo(
                            index = photo["index"],
                            orientation = photo["orientation"],
                            numTags = photo["number_of_tags"],
                            tags = photo["tags"]) 
                        for photo in photos]
        return photos

    def parse_output(slide_show: list, output_name:str):
        with open(output_name, "w+") as file:
            file.write("{}\n".format(len(slide_show)))
            for slide in slide_show:
                photos_idx = [str(photo.index) for photo in slide.photos]
                photos_idx = " ".join(photos_idx)
                file.write("{}\n".format(photos_idx))