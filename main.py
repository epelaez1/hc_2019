from classes import Slide, Photo
import time
def get_indexes(slides:list):
    index=0
    for slide in slides:
        slide.index=index
        index += 1

def get_best_partner(slide: Slide, slides:list, max_points_posible: int) -> set:
    points=-1
    best_partner=None
    for other_slide in slides:
        if other_slide.index == slide.index:
            continue

        if points < slide.points(other_slide):
            points=slide.points(other_slide)
            best_partner=other_slide
        if points == max_points_posible:
            break

    if best_partner is None:
        raise Exception("best_partner is None")
    return best_partner, points
# n² complexity
def get_best_partners(slides:list):
    index=0
    for slide in slides:
        if index%100 == 0:
            print("Obteniendo best_partner_of: {}".format(index), end="\r")
        for other_slide in slides:
            if slide.index == other_slide.index:
                continue
            points=slide.points(other_slide)
            if slide.best_partner_points < points:
                slide.best_partner_points=points
                slide.best_partner_index=other_slide.index
        index += 1

def get_coincidences(slides:list):
    for slide in slides:
        if slide.has_coincidence:
            continue
        other_slide=get_slide(slides=slides, index= slide.best_partner_index)
        if slide.best_partner_index == other_slide.best_partner_index:
            slide.has_coincidence=True
            other_slide.has_coincidence=True

def get_slide(slides:list, index: int)-> Slide:
    for slide in slides:
        if slide.index == index:
            return slide
    raise Exception("Slide not found")

def get_max_points_with_next_and_prev_group(index, tags_ammounts):

    if index == 0:
        max_prev_points=0
    else:
        max_prev_points=min([tags_ammounts[index], tags_ammounts[index-1]])//2
    if index == len(tags_ammounts) -1:
        max_next_points=0
    else:
        max_next_points=min([tags_ammounts[index], tags_ammounts[index+1]])//2

    return max_prev_points, max_next_points


def get_best_sort(slides:list):
    print("Obteniendo indices de las slides")
    get_indexes(slides)
    print("Obteniendo mejores compañeros")
    get_best_partners(slides)
    print("Obteniendo coincidencias")
    get_coincidences(slides)
    best_sort_aprox=list()
    best_sort_aprox.append(slides[0])
    slides.pop(0)
    last=best_sort_aprox[0]
    print("Ordenando")
    while len(slides):
        if len(slides)%100 == 0:
            print("Quedan {}.0000 slides por ordenar".format(len(slides)))
        if last.has_coincidence:
                
            next_slide=get_slide(slides=slides, index=last.best_partner_index)
            remove_index=0
            for index, slide in enumerate(slides):
                if slide.index == next_slide.index:
                    remove_index=index
                    break
            best_sort_aprox.append(next_slide)
            last=next_slide
            slides.pop(remove_index)
        else:
            next_slide=get_lover(slides=slides, slide=last)
            best_sort_aprox.append(next_slide)
            last=next_slide
            remove_index=0
            for index, slide in enumerate(slides):
                if slide.index == next_slide.index:
                    remove_index=index
                    break
            slides.pop(remove_index)
    return best_sort_aprox
def remove_slide(slides, slide):
    aux = 0
    found = False
    for elem in slides:
        if elem.index == slide.index:
            found = True
            break
        else:
            aux += 1
    if not found:
        raise Exception("Slide not in list")
    slides.pop(aux)
def get_best_partner_in_other_groups(
        slide: Slide, groups_of_slides: list,
        max_points: list, points_reached:int,
        best_partner: Slide, best_partner_group: list):

    if not max_points:
        return best_partner, best_partner_group
    
    index_of_best_group=max_points.index(max(max_points))
    max_points_posible=max(max_points)
    if max_points_posible <= points_reached:
        return best_partner, best_partner_group

    selected_group=groups_of_slides[index_of_best_group]
    new_best_partner, points=get_best_partner(
        slide=slide, slides=selected_group,
        max_points_posible=max_prev_points)


    if points > points_reached:
        best_partner = new_best_partner
        points_reached = points
        best_partner_group = selected_group
    # Best group checked, discard
    max_points.pop(index_of_best_group)
    groups_of_slides.pop(index_of_best_group)
    
    if not max_points or points >= max(max_points):
        return best_partner, best_partner_group
    else:
        return get_best_partner_in_other_groups(slide, groups_of_slides, max_points, points_reached, best_partner, best_partner_group)
def get_total_points(first_slide:Slide)->int:
    points = 0
    current_slide = first_slide
    while current_slide.next is not None:
        points += current_slide.points(current_slide.next)
        current_slide = current_slide.next
    return points

if __name__ == "__main__":
    print("Parsing file")
    start=time.time()
    attempt="inputs/b_lovely_landscapes.txt"

    data=Slide.parse_file(attempt)
    end=time.time()
    print("File parsed. Execution time: {}".format(end-start))
    print("Creating slides of horizontal photos")
    start=time.time()
    # dataV=[photo for photo in data if photo.orientation]
    dataH=[photo for photo in data if not photo.orientation]

    end=time.time()
    slides=[Slide([photo]) for photo in dataH]
    print("Obteniendo indices de las slides")
    # slides=slides[0:10000]
    get_indexes(slides)
    print("Done. Execution time: {}".format(end-start))
    #slides.extend(dataV) #TODO
    # print("Organazing tags")
    # start=time.time()
    # tags={}

    # for slide in slides:
    #   for tag in slide.tags:
    #       if tag in tags:
    #           tags[tag] +=1
    #       else:
    #           tags[tag]=1
    # end=time.time()
    # print("Done. Execution time: {}.".format(end-start))
    # print("Number of different tags: {}. Show count? (y/n)".format(len(tags.keys())))
    # if input() == "y":
    #   for key, element in tags.items():
    #       if element>3:
    #           print("{}: {}".format(key, element))
    # slides_solution=get_best_sort(slides)

    # Slide.parse_output(slides_solution,solution)
    print("DONE")

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
    
    # POSIBLE IDEA: ASOCIAR UN NUMERO A LAS TAGS EN FUNCION DE NUMERO DE APARICIONES: ORDENAR LAS LISTAS DE SLIDES POR SUMA DE LOS VALORES DE SUS TAGS
    # ES POSIBLE QUE SI LA SLIDE TIENE LAS TAGS COMUNES ENCUENTRE LA MEJOR PUNTUACION PRONTO
    # PARA ORDENARLAS LAS PONES EN UN DICT DE CLAVE SU PUNTUACION Y SU VALOR UN ARRAY CON LAS SLIDES CON ESOS PUNTOS
    # ORDENAS LAS CLAVES Y RECORRES EL DICT EN ESE ORDEN
    
    # Algorithm:
    # Organice the slides by groups depending of the number of tags. 
    # Start the slide show with the slide with lowest number of tags, the left side of the first slide is empty so you lose less points
    # Then continue with the slides with the same number of tags.. Stop when the half of the slides of that group are used.
    # Then use the next group. At the last group of slides use them all. Then go back to the previus group and use them all.
    # Repeat this till the end
    # .
    # .
    # .
    # To get the best slide you try with all the slides in the same group. Save the points. 
    # [[MARK]]
    # If you get the best points posible int(number_of_tags/2), use that slide.
    # If you dont get the best points compare the best points you can get in that group with the previus group and the next group.
    # If you can get higher points move to the best group. GOTO MARK
    # .
    # If you moved your group go back to the group you were at. 
    # If at any time a group is empty go forward and delete the group

    print("Iniciando algoritmo")
    total_groups_of_tags=len(tags_ammounts)

    usless_slides=1 in tags_ammounts
    index=0 if not usless_slides else 1
    
    origin_number_of_slides_in_current_ammount=len(slides_by_num_of_tags[tags_ammounts[index]]["slides"])

    first_slide=slides_by_num_of_tags[tags_ammounts[index]]["slides"].pop(0)
    current_slide=first_slide
    current_group=slides_by_num_of_tags[tags_ammounts[index]]["slides"]
    best_points_at_this_index=int(tags_ammounts[index]/2)
    max_prev_points, max_next_points=get_max_points_with_next_and_prev_group(index=index, tags_ammounts=tags_ammounts)
    # Frist part of the sort: from bottom to top
    direction = 1
    check_half_done = True
    aux = 0
    start = time.time()
    start_aux = time.time()
    while slides_by_num_of_tags.keys():
        if aux%1000 == 0:
            print("Se han procesado {:5} slides. Tiempo transcurrido: {:5.1f} segundos.\nLas 1000 ultimas han tardado {:5.1f} segundos".format(aux, time.time()- start, time.time() - start_aux))
            start_aux = time.time()
        # Stop condition and move forward condition
        number_of_slides_in_current_ammount=len(slides_by_num_of_tags[tags_ammounts[index]]["slides"])
        if check_half_done and (number_of_slides_in_current_ammount <= origin_number_of_slides_in_current_ammount/2):
            print("El grupo tenia {} slides, ahora tiene {}".format(origin_number_of_slides_in_current_ammount, number_of_slides_in_current_ammount))
            print("Ya ha acabado la mitad de este grupo ({}), movemos al siguiente".format(tags_ammounts[index]))
            if index == len(tags_ammounts) - 1:
                # Top reached, time to go to the bottom
                print("hemos llegado al grupo con mas tags, cambiamos direccion y continuamos")
                direction = -1
                check_half_done = False
                continue
            index += direction
            origin_number_of_slides_in_current_ammount=len(slides_by_num_of_tags[tags_ammounts[index]]["slides"])
            best_points_at_this_index=int(tags_ammounts[index]/2)
            max_prev_points, max_next_points=get_max_points_with_next_and_prev_group(index=index, tags_ammounts=tags_ammounts)
            current_group=slides_by_num_of_tags[tags_ammounts[index]]["slides"]

        
        best_partner, points=get_best_partner(slide= current_slide, slides= current_group, max_points_posible=best_points_at_this_index)

        if not (points == best_points_at_this_index or (points < max_next_points and points < max_prev_points)):
            other_groups = list()
            max_points = list()
            if max_prev_points:
                other_groups.append(slides_by_num_of_tags[tags_ammounts[index-1]]["slides"])
                max_points.append(max_prev_points)
            if max_next_points:
                other_groups.append(slides_by_num_of_tags[tags_ammounts[index+1]]["slides"])
                max_points.append(max_next_points)

            best_partner, best_partner_group = get_best_partner_in_other_groups(slide= current_slide, groups_of_slides=other_groups,
                max_points= max_points, points_reached= points,
                best_partner= best_partner, best_partner_group=current_group)
        else:
            best_partner_group = current_group
        current_slide.next=best_partner
        best_partner.prev=current_slide
        current_slide=best_partner
        try:
            # best_partner_group.remove(slide)
            remove_slide(slide= current_slide, slides= best_partner_group)
        except Exception as error:
            data = error
            import pdb
            pdb.set_trace()
            data = 0
        if not best_partner_group:
            print("Grupo vacio, se elimina del diccionario y de la lista ordenada con las claves")
            slides_by_num_of_tags.pop(current_slide.number_of_tags)
            tags_ammounts.remove(current_slide.number_of_tags)
        
        if not current_group:
            print("El grupo en el que estabamos se ha vaciado")
            if index < 0:
                print("Index menor que cero, todo hecho")
                continue
            if index >= len(tags_ammounts):
                print("El grupo era el ultimo grupo. Cambiamos direccion y actualizamos index")
                direction = -1
                check_half_done = False
                index = len(tags_ammounts) - 1
                if index == -1:
                    print("Era el ultimo continuamos")
                    continue
            origin_number_of_slides_in_current_ammount=len(slides_by_num_of_tags[tags_ammounts[index]]["slides"])
            best_points_at_this_index=int(tags_ammounts[index]/2)
            max_prev_points, max_next_points=get_max_points_with_next_and_prev_group(index=index, tags_ammounts=tags_ammounts)
            current_group=slides_by_num_of_tags[tags_ammounts[index]]["slides"]
        aux+=1
    # while True:
    #     input()
    end=time.time()
    tiempo=end-start
    print("Tiempo de ejecucion {} segundos".format(tiempo))
    print("Convertir a lista el show")
    show = list()
    current_slide = first_slide
    show.append(current_slide)
    while current_slide.next:
        current_slide = current_slide.next
        show.append(current_slide)
    output = "outputs/prueba_b_1.txt"
    total_points = get_total_points(first_slide = first_slide)
    Slide.parse_output(show,output)


    import pdb
    pdb.set_trace()