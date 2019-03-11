from database.hash_code import HashCodeDB
from classes import Slide, Photo
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from core.utils import utils
from core.logger import PersonalLogger

import time
print = PersonalLogger.progress_msg

def commonTags(elem1, elem2):
    return len(list(set(elem1["tags"]).intersection(set(elem2["tags"]))))

# def puntuation(photo1: Photo, photo2: Photo):
#     common = Slide.commonTags(photo1, photo2)
#     return min(common, len(photo1.tags) - common, len(photo2.tags) - common)


def get_points(stored_slide, stored_slide2):
    common = commonTags(stored_slide, stored_slide2)
    points = min(common, len(
        stored_slide["tags"]) - common, len(stored_slide2["tags"]) - common)
    return points


def get_points_of_show(show):
    points = 0
    copy_of_show = [slide for slide in show]
    current_slide = copy_of_show[0]
    while copy_of_show:
        points += get_points(current_slide, copy_of_show[0])
        current_slide = copy_of_show.pop(0)
    return points


def get_partners(stored_slide, other_stored_slides):
    partners = [{
                "points": get_points(stored_slide, other_slide),
                "_id": other_slide["_id"],
                "number_of_tags": other_slide["number_of_tags"]
                } for other_slide in other_stored_slides]
    partners = [elem for elem in partners if elem["points"] > 0]

    return partners


def update_partner_points(stored_slide, db, collection_name):
    try:
        query = {"tags": {"$in": stored_slide["tags"]}}
        # print("Buscando con mismos tags")
        matches = db.search(
            collection=collection_name,
            mongo_query=query,
            fields={"_id": 1, "tags": 1, "number_of_tags": 1})
        matches = [match for match in matches
                   if (match["_id"] != stored_slide["_id"])]
        # print("Obteniendo puntos")
        partners = get_partners(stored_slide, matches)

        stored_slide["partners"] = partners
        points = [partner["points"] for partner in partners]
        points.extend([0, 0])
        points = sorted(points)[::-1]
        stored_slide["best_points"] = points[0]
        stored_slide["best_points_2"] = points[1]
        # print(points)
        return stored_slide
    except Exception as error:
        utils.print_exception()
        raise error

def get_indexes(slides: list):
    index = 0
    for slide in slides:
        slide.index = index
        index += 1


def update_chunk(chunk):
    with ThreadPoolExecutor(max_workers=10) as executor, HashCodeDB() as database:
        try:
            tasks = [executor.submit(
                     update_partner_points, stored_slide,
                     database, collection_name) for stored_slide in chunk]
            updated_slides = list()
            aux = 0
            for task in tasks:
                if aux%1 == 0:
                    pass
                    # print("{} done of {}".format(aux, len(tasks)))
                updated_slides.append(task.result())
                aux+=1
        except Exception as e:
            utils.print_exception()
    return updated_slides


if __name__ == "__main__":
    print("Parsing file")
    start = time.time()
    attempt = "inputs/b_lovely_landscapes.txt"
    collection_name = 'b_lovely_landscapes'
    data = Slide.parse_file(attempt)
    end = time.time()
    print(
        "File parsed. Execution time: {}".format(end - start))
    print("Creating slides of horizontal photos")
    start = time.time()
    dataV = [photo for photo in data if photo.orientation]
    dataH = [photo for photo in data if not photo.orientation]
    pairs_of_vertical_photos = utils.chunks(dataV, 2)
    vertical_slides = [Slide(pair)
                       for pair in pairs_of_vertical_photos if len(pair) == 2]
    end = time.time()
    slides = [Slide([photo]) for photo in dataH]
    slides.extend(vertical_slides)

    print("Clasifying by number of tags")
    start=time.time()
    slides_by_num_of_tags={}
    for slide in slides:
        if len(slide.tags) in slides_by_num_of_tags:
            slides_by_num_of_tags[len(slide.tags)]["count"] += 1
            slides_by_num_of_tags[len(slide.tags)]["slides"].append(slide)
        else:
            slides_by_num_of_tags[len(slide.tags)]={
                "count" :1,
                "slides" : [slide]
            }

    end=time.time()

    print("Done in {} secs. Show count by ammount of tags? (y/n) {}  total keys".format(end-start, len(slides_by_num_of_tags.keys())))
    tags_ammounts=sorted(slides_by_num_of_tags.keys())
    if input() == "y":
        for key in tags_ammounts:
                print("{:2}: {} {}".format(key,"="*(int(slides_by_num_of_tags[key]["count"]/100)) ,slides_by_num_of_tags[key]["count"]))

    print("DONE")
    tags = {}
    for slide in slides:
        for tag in slide.tags:
            if tag in tags:
                tags[tag] += 1
            else:
                tags[tag] = 0
    print("{} tags diferentes. Imprimir? (y/n)".format(len(tags.keys())))
    if input() == "y":

        for tag, count in tags.items():
            print("{}: {} {}".format(tag, "="*int(count/200), count))
     # slides = slides[0:20000]
    print("Obteniendo indices de las slides")
    get_indexes(slides)
    print("Convirtiendo a diccionarios")
    mongo_slides = [{
        "index": slide.index,
        "tags": slide.tags,
        "partners": 0,
        "best_points": 0,
        "best_points_2": 0,
        "number_of_tags": slide.number_of_tags,
        "photos" : [photo.index for photo in slide.photos]
    } for slide in slides]
    print("Conectando con base de datos")
    with HashCodeDB() as database:
        print("Eliminando previamente la base de datos")
        database.drop_collection(collection_name)
        print("Insertando elementos")
        database.insert_many(collection=collection_name,
                             new_elements=mongo_slides)
        print("Creando indice en tags")
        database.create_index(collection=collection_name, field="tags")
        print("Obtienendolos de la base de datos")
        stored_slides = database.search(
            collection=collection_name, mongo_query={})
        print("Lanzando 25 hilos")
        updated_slides = list()
        # for stored_slide in stored_slides:
        #     updated_slides.append(
        #         update_partner_points(stored_slide, database))
        start = time.time()
        stored_slides = [slide for slide in stored_slides]
    chunks = utils.chunks(stored_slides, 10000)
    updated_slides = list()
    with ProcessPoolExecutor(max_workers=4) as process_executor:
        tasks = [process_executor.submit(update_chunk, chunk)
                 for chunk in chunks]
        count = 0
        for task in tasks:
            print("{} slides actualizadas".format(count))
            updated_slides.extend(task.result())
            count += 10000

        # with ThreadPoolExecutor(max_workers=50) as executor:
        #     tasks = [executor.submit(
        #         update_partner_points, stored_slide, database)
        #         for stored_slide in stored_slides]
        #     aux = 0
        #     for task in tasks:
        #         if aux % 2000 == 0:
        #             print(
        #                 "Actualizados {} slides".format(aux))
        #         updated_slides.append(task.result())
        #         aux += 1

    with HashCodeDB() as database:
        print("Eliminando base de datos y actualizando")
        database.drop_collection(collection_name)
        print("Insertando")
        end = time.time()
        print(
            "Tiempo de ejecucion {} segundos".format(end - start))
        print(
            "Insertando {} elementos".format(len(updated_slides)))
        database.insert_many(collection=collection_name,
                             new_elements=updated_slides)
        print("Creando indice en tags")
        database.create_index(collection=collection_name, field="tags")
        print("Creando indice en partners._id")
        database.create_index(collection=collection_name, field="partners._id")
        print("Creando indice en best_points_2")
        database.create_index(collection=collection_name,
                              field="best_points_2")
        print("Creando indice en _id")
        database.create_index(collection=collection_name, field="_id")

    with ProcessPoolExecutor(max_workers=4) as process_executor:
        pass
    with HashCodeDB() as database:
        # COMIENZA ALGORITMO
        print("COMIENZA EL ALGORITMO")
        show = list()
        current_slide = database.search(
            collection=collection_name, mongo_query={},
            sort=[("best_partner_2", 1), ("number_of_tags", 1)],
            limit=1)[0]
        mongo_query = {"_id": current_slide["_id"]}
        database.remove(collection=collection_name, mongo_query=mongo_query)
        pull_statement = {
            "partners": {"_id": current_slide["_id"]}
        }
        database.pull(collection=collection_name, mongo_query={},
                      pull_statement=pull_statement, multi=True)
        show.append(current_slide)
        start = time.time()
        while database.count(collection=collection_name):

            if len(show) % 5000 == 0:
                print(
                    "{}. Tiempo de ejecucion de los ultimos 5000: {} segundos".format(
                    len(show), time.time() - start))
                start = time.time()
            # if current_slide["partners"]:
            next_slide = {}
            while current_slide["partners"]:
                points = [partner["points"]
                          for partner in current_slide["partners"]]
                max_points = max(points)
                number_of_tags = [partner["number_of_tags"]
                                  for partner in current_slide["partners"]
                                  if partner["points"] == max_points]
                min_tags = min(number_of_tags)
                best_partner = [partner for partner in current_slide["partners"]
                                if partner["points"] == max_points and partner["number_of_tags"] == min_tags][0]
                next_slide = database.find_one_and_delete(
                    collection=collection_name, mongo_query={"_id": best_partner["_id"]})
                if not next_slide:
                    current_slide["partners"] = [
                        partner for partner in current_slide["partners"] if partner["_id"] != best_partner["_id"]]
                else:
                    current_slide = next_slide
                    break
            if not next_slide:
                current_slide = database.find_one_and_delete(collection=collection_name, mongo_query={
                }, sort=[("best_partner_2", 1), ("number_of_tags", 1)])
            # else:
            #     import pdb
            #     pdb.set_trace()
            #     current_slide = database.find_one_and_delete(collection = collection_name, mongo_query = {},sort = [("best_partner_2",1), ("number_of_tags",1)], limit= 1)
            # pull_statement = {
            #     "partners" : {"_id": current_slide["_id"]}
            # }
            # database.pull(collection = collection_name, mongo_query = {}, pull_statement = pull_statement, multi = True)
            show.append(current_slide)
    total_points = get_points_of_show(show)
    # show_copy = [slide for slide in show]
    # next_slide = show_copy.pop(0)
    # current_slide = Slide(photos = [Photo(index = index) for index in first_slide.photos])
    # while show_copy:
    #     next_slide = show.pop(0)
    #     new_slide = Slide(photos = [Photo(index = index) for index in first_slide.photos])
    #     current_slide.next = new_slide
    #     new_slide.prev  = current_slide
    #     current_slide = new_slide
    slide_show = [Slide(photos = [Photo(index= index) for index in slide.photos]) for slide in show]
    output = "/outputs/b_lovely_landscapes.txt"
    Slide.parse_output(show, output)
    data = 0
