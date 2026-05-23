import pygame,random,json,os,re

fullscreenWidth = 1280
fullscreenHeight = 720

# create pen to be used in any function
global_pen = pygame.font.SysFont('arial',20)

selecting = 1
deleting = -1
placing = -1

scale_factor = 1
current_layer = 0

bg_offset_x = 0
bg_offset_y = 0

leftClick = False
rightClick = False

# check if there is a json file that already exists and we just want to do editiing
# file_exists = input('Is there a json file already? Type "yes" or "no" or "quit": ')

# # stay in while loop till they answer with true or false
# while file_exists not in ['yes','no','quit']:
#     file_exists = input('Is there a json file already? Type "yes" or "no" or "quit": ')

# if a json file exists then open the json file and load it in open('config_tilemap.json','r')
# if file_exists == 'yes':

file_exists = 'no'

with open('config_tilemap.json','r') as tilemap_coors_andsurface_file:
    tilemap_coors_andsurface = json.load(tilemap_coors_andsurface_file)

# if file_exists == 'quit':
#     sys.exit()

#####open jsons
with open("config_windows.json",'r') as window_parameter_files:

    window_parameters = json.load(window_parameter_files)


### Making Windows
# pygame.display.set_mode((0,0),pygame.FULLSCREEN)
win = pygame.display.set_mode((window_parameters['PALETTESCREENWIDTH'],window_parameters['PALETTESCREENHEIGHT']))
empty_surface = pygame.Surface((window_parameters['SCREENWIDTH'],window_parameters['SCREENHEIGHT']))

def convert_save_file(jsondata:dict, key_surface:dict):

        # define list to take all the rects and masks
        # {layer_one:{terrain2444:rect,mask}}
        all_rects_masks_surfaces_scalefactor = {}

        # do something different for colliding with an object in each layer of the tilemap
        for layer in list(jsondata.keys()):

            # add the layer to the dict and let the value be any empty dict that we will fill below in the for looop
            all_rects_masks_surfaces_scalefactor[layer] = {}

            ##its now a dictionary within a dictionary so we need the actual layer name to access the rect names and corrdinates inside of it
            # for key,coors_scalefactor in jsondata[layer].items():
            for pos_as_str,tile_attirbutes in jsondata[layer].items():

                # breakdown each of the attributes
                key, coors, scale_factor = tile_attirbutes

                #remove the unique identifier from the different rects so we can just draw what needs to be drawn
                extracted_key = re.sub(r'_.*$','',key)

                # here we want the actual key because we are trying to get back to what the json actually looks like

                the_rect = pygame.FRect(coors[0], coors[1], key_surface[extracted_key].surface.get_width()*scale_factor,key_surface[extracted_key].surface.get_height()*scale_factor)
                transformed_surface = pygame.transform.scale(key_surface[extracted_key].surface, (key_surface[extracted_key].surface.get_width()*scale_factor, key_surface[extracted_key].surface.get_height()*scale_factor))
                the_mask = pygame.mask.from_surface(transformed_surface)



                # add all this info to a new dictionary.
                # give key and not extracted key to the dictionary because we still want them to have their individual unique ids, we use extracted key just to be able to make the rect and mask
                all_rects_masks_surfaces_scalefactor[layer][key] = [transformed_surface,the_rect,scale_factor]

        return all_rects_masks_surfaces_scalefactor




### function to produce the final json dictionary of data with the rects in all the layers
def produce_json_data(final_layer):

    data_for_json = {}

    ###extract only the rcet coors (x and y) and thje unique id from the surface attributes which is a list of three things. CHECK LINE 550 in player updated class for more info
    ##first go through every key and if the layer information is not empty then extract the data into a json
    # no need to reverse the layer order here because that is already done in Creativemode/draw json data
    for key in final_layer.keys():

        data_for_json[key] = {}

        for rectname,surfaceattributes in final_layer[key].items():

            # acess the layer then create a key value pair for the reect name and its surface attributes
            data_for_json[key][rectname] = [(surfaceattributes[1].x,surfaceattributes[1].y),surfaceattributes[2]]

    return data_for_json


####drawing assets for layer
# layerimgnameimgsurf is a dictionary that holds the layer as a key and its value is another dictionary with the name of the image being used as a key and the surface,rect and scale factor being used as a value
def draw_assets_to_layer(layer_imgname_imgsurf_imgrect_sf, layer_to_draw, screen_boundaries = window_parameters['SCREENWIDTH'],screen_height=window_parameters['SCREENHEIGHT'] ):

    if layer_imgname_imgsurf_imgrect_sf[layer_to_draw] != {}:

        ##the values here has surface ,the rect coors, and the unique id for that surface. so the indices are 0 1 2
        for rectname,surface_coors in layer_imgname_imgsurf_imgrect_sf[layer_to_draw].items():

            ###if the rect itself is within the boundaries we have set for the screen.i.e the 1200,1200 surface we have created within the 1600x1600 surface which is the whole screen
            ##so essentiallyw e only see the rects when they are in frame. so if the rects x AND y coordinates are in frame then we do smth
            if (surface_coors[1].x < screen_boundaries - bg_offset_x and surface_coors[1].y < screen_height - bg_offset_y):
                win.blit(surface_coors[0],(surface_coors[1].x + bg_offset_x,surface_coors[1].y + bg_offset_y))

# example run command, function is unused now because we have foumd a batter way to draw our progress onto the scrteen
# draw_assets_to_layer(layer_imgname_imgsurf_imgrect_sf=layer_imgname_imgsurf_imgrect_sf,layer_to_draw=f'layer_{Creative_Mode.current_layer}')

def draw_info(pen = global_pen, win=win):

    xcoor,ycoor = 900,100

    # Assign text depending on what is being said
    txt2 = pen.render(f'The scale factor is {scale_factor}. Hit 1 to increase and 2 to decrease',1,'red')
    txt1 = pen.render(f'The current layer is {current_layer} Hit UP to increase and DOWN to decrease',1,'red')

    # if selcting palette or placing the tiles is chose n the text is different
    if selecting == 1:
        txt3= pen.render(f'You are selecting your palette. No tiles can be placed. \nHit Space to change',1,'red')

    elif selecting == -1:
        txt3= pen.render(f'You are placing tiles. No pallette can be selected. \nHit Space to change',1,'red')

    if deleting == -1:
        txt4= pen.render(f'You are not deleting tiles. Hit LSHIFT to start deleting',1,'red')

    elif deleting == 1:
        txt4= pen.render(f'You are  deleting tiles. Hit LSHIFT to stop deleting',1,'red')

    txt5 = pen.render('a d to go left right, w s to go up down',1,'red')

    txt7 = pen.render('Escape to exit without saving, P to save',1,'red')

    # put all the text into a list and loop through it so we can change the y coorinfate
    txt_towrite = [txt1,txt2,txt3,txt4,txt5,txt7]

    for text in txt_towrite:

        #change the y coor everytime so the info is on a new line
        ycoor += 50
        win.blit(text,(xcoor,ycoor))




######## HAVE A FLAG CALLED FINAL PICTURE WHIUCH SHOIWS YUOU HOW EVERYTHIONG LOOKS LIKE WHILST YOU ARE STILL EDITING
def main():

    # layer_imgname_imgsurf_imgrect_sf = layer, image name, image surface, image rect,scale factor
    playing = True
    clock = pygame.time.Clock()

    # bgs = Creative_Mode.get_background('Assets_Platformer','Background',tile_size_height=window_parameters['TILE_SIZE'],tile_size_width=window_parameters['TILE_SIZE'],PALETTESCREENWIDTH=window_parameters['PALETTESCREENWIDTH'],
    #                      SCREENWIDTH=window_parameters['SCREENWIDTH'])

    bgs = Creative_Mode.get_sprites(bgpaths=('Sprites','Environment'),tile_size_height=window_parameters['TILE_SIZE'],tile_size_width=window_parameters['TILE_SIZE'],PALETTESCREENWIDTH=window_parameters['PALETTESCREENWIDTH'],
                         SCREENWIDTH=window_parameters['SCREENWIDTH'])

    # this rerturns a dictionary
    bgs2 = Creative_Mode.get_background_2(bgpaths=('Assets_Platformer','Background'),item_trap_paths=('Assets_Platformer','Traps'),tile_size_height=window_parameters['TILE_SIZE'],tile_size_width=window_parameters['TILE_SIZE'],PALETTESCREENWIDTH=window_parameters['PALETTESCREENWIDTH'],
                         SCREENWIDTH=window_parameters['SCREENWIDTH'])

    # create object that is going to place rects
    # artist = Creative_Mode()
    #MIGHT BE SOME REDUNDUNCY HERE
    ###create a layer here... it will acc jsut be in the json but for nwo you can put it here
    ###this creates our whole list of possible rect cooridnates that we can then go on to manipulate since they are in a dictionary
    tileset_rects = Creative_Mode.divide_screen(width=window_parameters['SCREENWIDTH'],height=window_parameters['SCREENHEIGHT'],tile_size=window_parameters['TILE_SIZE'],empty_surface=empty_surface,win=win,extra_space=1)
    layer_rects = {'layer_one':tileset_rects}

    # create dictionary for game lines
    game_lines = {'lines':[]}

    ###changhe name of layer coors image to draw to surface_rect_uniquieid

    # only create an empty screen if the jsoin file tilempa doesnt exist
    if file_exists == 'no':
        layer_imgname_imgsurf_imgrect_sf = {'layer_1':{}}

    elif file_exists == 'yes':
        layer_imgname_imgsurf_imgrect_sf = convert_save_file(jsondata=tilemap_coors_andsurface,key_surface=bgs)


    # zero zero rect
    topleft_rect = pygame.FRect(0,0,window_parameters['TILE_SIZE'],window_parameters['TILE_SIZE'])

    while playing:

        clock.tick(window_parameters['FPS'])
        win.fill(window_parameters['DEFAULT_WINFILL'])





        for event in pygame.event.get():

            # recognises mouse inputs
            # add scoll wheel to allow you to cycle between different rotations of the same sprite
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == pygame.BUTTON_LEFT:

                    leftClick = True

                if event.button == pygame.BUTTON_RIGHT:

                    rightClick = True

            if event.type == pygame.MOUSEBUTTONUP:

                if event.button == pygame.BUTTON_LEFT:

                    # artist.selecting = False
                    leftClick = False

                if event.button == pygame.BUTTON_RIGHT:

                    rightClick = False

                    # artist.placing = False

            if event.type == pygame.QUIT:
                img_surf = pygame.Surface((1600,1600))
                data_for_json = {}
                ###extract only the rcet coors (x and y) and thje unique id from the surface attributes which is a list of three things. CHECK LINE 550 in player updated class for more info
                ##first go through every key and if the layer information is not empty then extract the data into a json
                for key in layer_imgname_imgsurf_imgrect_sf.keys():
                    data_for_json[key] = {}
                    for rectname,surfaceattributes in layer_imgname_imgsurf_imgrect_sf[key].items():
                        data_for_json[key][rectname] = [(surfaceattributes[1].x,surfaceattributes[1].y),surfaceattributes[2]]
                Creative_Mode.draw_jsondata(jsondata=data_for_json,key_surface=bgs,win=img_surf)
                pygame.image.save(surface=img_surf,file='trial_img.png')

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    Creative_Mode.deleting_editing *= -1

                if event.key == pygame.K_TAB: # to start doing the adding lines for FOV
                    Creative_Mode.adding_lines *= -1

                if event.key == pygame.K_3: # to delete the last line you made

                    if game_lines['lines']:

                        del game_lines['lines'][-1]

                if event.key == pygame.K_a:
                    Creative_Mode.bg_offset_x += (window_parameters['TILE_SIZE']*2)
                if event.key == pygame.K_d:
                    Creative_Mode.bg_offset_x -= (window_parameters['TILE_SIZE']*2)

                if event.key == pygame.K_w:
                    Creative_Mode.bg_offset_y += (window_parameters['TILE_SIZE']*2)
                if event.key == pygame.K_s:
                    Creative_Mode.bg_offset_y -= (window_parameters['TILE_SIZE']*2)

                if event.key == pygame.K_SPACE:
                    Creative_Mode.selecting_editing *= -1

                if event.key == pygame.K_1:
                    Creative_Mode.scale_factor +=1
                if event.key == pygame.K_2:
                    Creative_Mode.scale_factor -= 1

                if event.key == pygame.K_UP:
                    Creative_Mode.current_layer += 1

                    # add layers where necessary
                    if f'layer_{Creative_Mode.current_layer}' not in list(layer_imgname_imgsurf_imgrect_sf.keys()):
                        layer_imgname_imgsurf_imgrect_sf[f'layer_{Creative_Mode.current_layer}'] = {}

                if event.key == pygame.K_DOWN:
                    Creative_Mode.current_layer -= 1

                if event.key == pygame.K_RIGHT:
                    Creative_Mode.final_picture *= -1

                if event.key == pygame.K_0:

                    # until we find a new way (when you take a screenshot you need to go to the leftmost topmost corner of the screen so everything fits into the screenshot)
                    # create a new surface
                    img_surf = pygame.Surface((window_parameters['SCREENWIDTH'],window_parameters['SCREENHEIGHT']))
                    data_for_json = {}
                    ###extract only the rcet coors (x and y) and thje unique id from the surface attributes which is a list of three things. CHECK LINE 550 in player updated class for more info
                    ##first go through every key and if the layer information is not empty then extract the data into a json
                    for key in layer_imgname_imgsurf_imgrect_sf.keys():
                        data_for_json[key] = {}
                        for rectname,surfaceattributes in layer_imgname_imgsurf_imgrect_sf[key].items():
                            data_for_json[key][rectname] = [(surfaceattributes[1].x,surfaceattributes[1].y),surfaceattributes[2]]
                    Creative_Mode.draw_jsondata(jsondata=data_for_json,key_surface=bgs,win=img_surf)
                    pygame.image.save(surface=img_surf,file='trial_img_astar.png')

                # saving progress
                if event.key == pygame.K_p:

                    ###crashe sbecause json can only have numbers or strings so we need to enumerate all the surfaces
                    with open('config_tilemap.json','w') as f:
                        data_for_json = {}
                        ###extract only the rcet coors (x and y) and thje unique id from the surface attributes which is a list of three things. CHECK LINE 550 in player updated class for more info
                        ##first go through every key and if the layer information is not empty then extract the data into a json
                        for layer in layer_imgname_imgsurf_imgrect_sf.keys():

                            data_for_json[layer] = {}

                            for rectname,surfaceattributes in layer_imgname_imgsurf_imgrect_sf[layer].items():
                                # print(surfaceattributes)

                                # from rect name, get only the last elements,which is the coors
                                position = f'({surfaceattributes[1].x},{surfaceattributes[1].y})'

                                data_for_json[layer][position] = [rectname,(surfaceattributes[1].x,surfaceattributes[1].y),surfaceattributes[2]]

                        json.dump(data_for_json,f,indent=4)

                        print('Saved json data!')

                    # save copy
                    with open('config_tilemap_COPY.json','w') as f:
                        data_for_json = {}
                        ###extract only the rcet coors (x and y) and thje unique id from the surface attributes which is a list of three things. CHECK LINE 550 in player updated class for more info
                        ##first go through every key and if the layer information is not empty then extract the data into a json
                        for layer in layer_imgname_imgsurf_imgrect_sf.keys():

                            data_for_json[layer] = {}

                            for rectname,surfaceattributes in layer_imgname_imgsurf_imgrect_sf[layer].items():
                                # print(surfaceattributes)

                                # from rect name, get only the last elements,which is the coors
                                position = f'({surfaceattributes[1].x},{surfaceattributes[1].y})'

                                data_for_json[layer][position] = [rectname,(surfaceattributes[1].x,surfaceattributes[1].y),surfaceattributes[2]]

                        json.dump(data_for_json,f,indent=4)

                        print('Saved copy json data!')


                    with open('config_tilemap_wall_lines.json','w') as f:

                        json.dump(game_lines,f,indent=4)

                        print('Saved wall line data!')

                    # this is the file we load back in if we want to do editing
                    # with open('config_tilemap_editing_file.json','w') as f:

                    #     # dump the json as it is
                    #     json.dump(layer_imgname_imgsurf_imgrect_sf,f,indent=4)
                    # pygame.quit()
                    # sys.exit()

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)



        # track mouise pos
        Creative_Mode.tracking_mouse_pos()

        ##draw this onto a surface of the right size and only draw a portion of that onto the screen
        Creative_Mode.divide_screen(width=window_parameters['SCREENWIDTH'],height=window_parameters['SCREENHEIGHT'],
                                    tile_size=window_parameters['TILE_SIZE'],empty_surface=empty_surface,win=win,extra_space=1)


        # draw json layer - check this
        Creative_Mode.update_json_and_draw_layer(win=win,layer_imgname_imgsurf_imgrect_sf=layer_imgname_imgsurf_imgrect_sf,tile_width=window_parameters['TILE_SIZE'],
                                                 tile_height=window_parameters['TILE_SIZE'],editingscreenwidth=window_parameters['SCREENWIDTH'],
                                                 editingscreenheight=window_parameters['SCREENHEIGHT'])
        # deleting tiles
        Creative_Mode.delete_tiles(layer_imgname_imgsurf_imgrect_sf=layer_imgname_imgsurf_imgrect_sf,tile_width=window_parameters['TILE_SIZE'],
                                   tile_height=window_parameters['TILE_SIZE'],editingscreenwidth=window_parameters['SCREENWIDTH'],
                                   editingscreenheight=window_parameters['SCREENHEIGHT'])



        # this allows all the layers to be drawn to the screen
        if Creative_Mode.final_picture == 1:

            # store final json data with layers and positions into a var
            my_json = produce_json_data(final_layer = layer_imgname_imgsurf_imgrect_sf)

            # draw the fuill and final json data with all the layers. key surface tells you which sprites to use depending on the rectname given to the json data
            Creative_Mode.draw_jsondata(jsondata=my_json,key_surface=bgs,win=win)




        ###draw each of the assets onto the screen as a palette on the right hand side
        # this draws palette of assets on the right hand side, and also the actual tiles on the screen
        for asset in bgs.values():
            # asset.draw_assets_and_collisions(win=win,layer_rects=layer_rects,layer_imgname_imgsurf_imgrect_sf=layer_imgname_imgsurf_imgrect_sf,editingscreenwidth=window_parameters['SCREENWIDTH'],editingscreenheight=window_parameters['SCREENHEIGHT'])

            # draw the asset on the right hand side of the screen
            asset.draw_asset(win=win)

            # get the assets being used
            Creative_Mode.update_asset(asset=asset)

        # draw the lines
        Creative_Mode.draw_wall_lines(win=win,game_lines=game_lines,tile_width=window_parameters['TILE_SIZE'],
                                        tile_height=window_parameters['TILE_SIZE'],editingscreenwidth=window_parameters['SCREENWIDTH'],
                                        editingscreenheight=window_parameters['SCREENHEIGHT'])

        print(game_lines)

        # draw the info regarding editing and all that
        draw_info()

        # draw 0,0 rect
        pygame.draw.rect(win,'red',topleft_rect)



        # uncomment to see the whole tilemap dictionary
        # print(layer_imgname_imgsurf_imgrect_sf)

        pygame.display.flip()


##press c to confirm press r and type in a number to scale the image. press tab to be able to see all the possible items and select one

if __name__ == '__main__':
    main()