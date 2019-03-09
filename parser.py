from classes import Photo

def parse_file(file_name: str) -> list:
    photos = []
    with open(file_name) as file:
        lines = [line.replace('\n', '') for line in file]
        lines.pop(0)
        photos = [line.split(" ") for line in lines]
        photos = [{ 
                    "index": idx,
                    "orientation": 0 if photo[0] == "H" else 1, 
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

def print_output(slide_show: list, output_name:str):
    with open(output_name, "+w") as file:
        file.write("{}\n".format(len(slide_show)))
        for slide in slide_show:
            photos_idx = [photo.index for photo in slide.photos]
            photos_idx = " ".join(photos_idx)
            file.write("{}\n".format(photos_idx))

class Slide:
    
    def __init__(self, photos:list):
        self.photos = photos

if __name__ == "__main__":
    file_name = "a_example.txt"
    photos = parse_file(file_name)
    for photo in photos:
        print("Foto numero {}, en {}, con {} tags: \n {}".format(photo["index"],photo["orientation"] ,photo["number_of_tags"] ," ".join(photo["tags"]) ))



    @staticmethod
    def commonTags(elem1, elem2):
        result = 0
        for tag in elem1.tags:
            if tag in elem2.tags:
                result+=1
        return result


    def puntuation(self, photo2: Photo):
        common = Slide.commonTags(self, photo2)
        return min(common, len(self.tags) - common, len(photo2.tags) - common)

    def pointsSlides(self, slide: Slide):

        common = Slide.commonTags(self, slide)
        