import pygame,random,json,os
from Player import *
from Drawing_TileMaps import Creative_Mode
from Game_Clock import Timer
from A_star_search_algorithm import *
from Enemy import *
import numpy as np
import sys

# list events
player_interaction = pygame.USEREVENT + 1

class Event_Handler():

    # list events
    player_interaction = pygame.USEREVENT + 1

    # this function will handle all player events, optionally in the future it could be an array of players
    def player_events(self,all_events,player:Player,item_bench_manager):

        # constanly reset player velocity
        # player.velocity = min_velocity

        for event in all_events:

            # if the event is the player death
            if event.type == player.is_dead:

                # sys.exit()
                pass

            # if the event is a collision detection, prevent movement in the direction of the collision
            # if event.type == player.collided_north:

            #     player.can_move_north = 0
            #     print(f'COLIIDIDEE\n\n\n\n')

            # if event.type == player.collided_south:

            #     player.can_move_south = 0

            # if event.type == player.collided_west:

            #     player.can_move_west = 0

            # if event.type == player.collided_east:

            #     player.can_move_east = 0

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_m:

                    player.add_items_to_player(item_type='orbital',item_name="MERRY-GOES-ROUND",player=player)
                    player.update_player_attributes(item_name="QUICK-STEP")

                if event.key == pygame.K_n:

                    player.add_items_to_player(item_type='orbital',item_name="YOUR_WORLD",player=player)
                    player.player_speed = 1000


                    # sys.exit()

                if event.key == pygame.K_l:
                    # sys.exit()
                    player.update_weapon_attributes(item = "WHISKY DICK")
                    # print(player.left_hand_weapon.of)


                if event.key == pygame.K_u:
                    player.update_weapon_attributes(item = 'TACTICAL TURKEY')

                if event.key == pygame.K_8:
                    player.update_weapon_attributes(item = "MUM'S SLIPPER")


                if event.key == pygame.K_r:

                    if player.left_hand_weapon:

                        # if not dual wield or alternating click and dual wield
                        if not player.left_hand_weapon.is_dual_wield or (player.left_hand_weapon.is_dual_wield and not player.left_hand_weapon.alternating_clicks):

                            if (player.left_hand_weapon.bullets_remaining_in_mag < player.left_hand_weapon.magazine_size) and player.left_hand_weapon.total_ammo_stock > 0:
                                player.left_hand_weapon.is_reloading = True



                        # if dual click and dual wield
                        if (player.left_hand_weapon.is_dual_wield and player.left_hand_weapon.alternating_clicks):
                            if (player.left_hand_weapon.bullets_remaining_in_mag < player.left_hand_weapon.magazine_size) and player.left_hand_weapon.total_ammo_stock > 0:
                                player.left_hand_weapon.is_reloading = True



                    # check if there is a second wepaon
                    if player.right_hand_weapon:

                        # if not dual wield or alternating click and dual wield
                        if not player.right_hand_weapon.is_dual_wield or (player.right_hand_weapon.is_dual_wield and not player.right_hand_weapon.alternating_clicks):

                            if (player.right_hand_weapon.bullets_remaining_in_mag < player.right_hand_weapon.magazine_size) and player.right_hand_weapon.total_ammo_stock > 0:
                                player.right_hand_weapon.is_reloading = True

                if event.key == pygame.K_a:

                    player.movementx[0] = -1

                    # if sum(player.movementx) != 0 or sum(player.movementy) != 0:
                    acceleration = player.movement_vectors['movement']['acceleration']
                    player.update_movement_vectors(unique_id='movement',direction_vectorX=sum(player.movementx),direction_vectorY=sum(player.movementy),acceleration=acceleration,
                                            Xcceleration_rate=12,Xcceleration_rate_change='positive',max_value=1,
                                        reduce_on_wall_collision=False,reset_on_max_value=False)
                    # player.update_movement_vectors(unique_id='movementX0',direction_vectorX=-1,direction_vectorY=0,acceleration=0,
                    #                      Xcceleration_rate=12,Xcceleration_rate_change='positive',max_value=1,
                    #                      reduce_on_wall_collision=False,reset_on_max_value=False)
                    # player.movementx[1] = 0
                    # player.acceleration = 1
                    # player.raX0 = False
                    # player.accelerationX0 = -1
                    # self.direction = re.sub('_.*','_left',self.direction)

                if event.key == pygame.K_d:
                    player.movementx[1] = 1
                    # if sum(player.movementx) != 0 or sum(player.movementy) != 0:
                    acceleration = player.movement_vectors['movement']['acceleration']
                    player.update_movement_vectors(unique_id='movement',direction_vectorX=sum(player.movementx),direction_vectorY=sum(player.movementy),acceleration=acceleration,
                                            Xcceleration_rate=12,Xcceleration_rate_change='positive',max_value=1,
                                            reduce_on_wall_collision=False,reset_on_max_value=False)
                    

                if event.key == pygame.K_w:
                    player.movementy[0] = -1
                    # if sum(player.movementx) != 0 or sum(player.movementy) != 0:
                    acceleration = player.movement_vectors['movement']['acceleration']
                    player.update_movement_vectors(unique_id='movement',direction_vectorX=sum(player.movementx),direction_vectorY=sum(player.movementy),acceleration=acceleration,
                                            Xcceleration_rate=12,Xcceleration_rate_change='positive',max_value=1,
                                            reduce_on_wall_collision=False,reset_on_max_value=False)
                    

                if event.key == pygame.K_s:
                    player.movementy[1] = 1

                    # if sum(player.movementx) != 0 or sum(player.movementy) != 0:
                    acceleration = player.movement_vectors['movement']['acceleration']
                    player.update_movement_vectors(unique_id='movement',direction_vectorX=sum(player.movementx),direction_vectorY=sum(player.movementy),acceleration=acceleration,
                                            Xcceleration_rate=12,Xcceleration_rate_change='positive',max_value=1,
                                            reduce_on_wall_collision=False,reset_on_max_value=False)
                   

                # if we dont have the same thj
                if event.key == pygame.K_LSHIFT:

                    # player.velocity = max_velocity
                    player.acceleration = player.max_acceleration
                    # player.player_speed = 200
                    # set player sprinting to true
                    player.is_sprinting = True

                if event.key == pygame.K_SPACE:

                    # if the player has not just rolled
                    # if not player.has_just_rolled:
                    if player.performed_rolls < player.allowed_rolls:

                        # player.velocity = max_velocity
                        player.is_rolling = True # set the player to be currently rolling
                        player.acceleration = player.roll_acceleration # adjust how fast the player is going

                        # get the keys currently being pressed
                        keys_being_pressed = {'north':player.movementy[0],
                                              'west':player.movementx[0],
                                              'south':player.movementy[1],
                                              'east':player.movementx[1]}

                        player.keys_used_for_roll = keys_being_pressed

                        # print(keys_being_pressed)
                        # sys.exit()

                # reset ammo back to maximum
                if event.key == pygame.K_TAB:

                    player.left_hand_weapon.total_ammo_stock = player.left_hand_weapon.total_ammo_stock_reset


                    if player.right_hand_weapon:
                        player.right_hand_weapon.total_ammo_stock = player.right_hand_weapon.total_ammo_stock_reset




                    #     if bullet.already_fired:
                    #         # bullet.is_inactive = True # so this is triggered when the entity hits a target or it has hit a wlal
                    #         bullet.reset()

                    # for bullet in player_bullet_manager.inactive_pool:


                    #     if bullet.already_fired:
                    #         # bullet.is_inactive = True # so this is triggered when the entity hits a target or it has hit a wlal
                    #         bullet.reset()

                # doing gun swaps
                if event.key == pygame.K_1:

                    # check if player weapon 1 is a free slot
                    if player.left_hand_weapon_slots['weapon_1']:

                        if player.weapon_choice != 'weapon_1':
                            # set shooting to false on the gun
                            player.left_hand_weapon.is_shooting = False

                        # update the weapon slot
                        player.weapon_choice = 'weapon_1'

                        # set the current weapon to be the first weapon
                        player.left_hand_weapon = player.left_hand_weapon_slots[player.weapon_choice]
                        player.right_hand_weapon = player.right_hand_weapon_slots[player.weapon_choice]

                if event.key == pygame.K_2:

                    # check if player weapon 1 is a free slot
                    if player.left_hand_weapon_slots['weapon_2']:

                        if player.weapon_choice != 'weapon_2':
                            # set shooting to false on the gun
                            player.left_hand_weapon.is_shooting = False

                        # update the weapon slot
                        player.weapon_choice = 'weapon_2'

                        # set the current weapon to be the first weapon
                        player.left_hand_weapon = player.left_hand_weapon_slots[player.weapon_choice]
                        player.right_hand_weapon = player.right_hand_weapon_slots[player.weapon_choice]

                # handle interactions with e
                if event.key == pygame.K_e:

                    # send message for open
                    pygame.event.post(pygame.event.Event(player_interaction))

                    # handles all buying and weapon swapping/ inventory adjustments from purchasing
                    player.is_interacting = True
                    # player.buying_items(item_bench = item_bench_manager)
                    player.left_hand_weapon = player.left_hand_weapon_slots[player.weapon_choice]




            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.movementx[0] = 0
                    player.movement_vectors['movement']["direction_vectorX"]=sum(player.movementx)


                if event.key == pygame.K_d:
                    player.movementx[1] = 0
                    player.movement_vectors['movement']["direction_vectorX"]=sum(player.movementx)


                if event.key == pygame.K_w:
                    player.movementy[0] = 0
                    player.movement_vectors['movement']["direction_vectorY"]=sum(player.movementy)


                if event.key == pygame.K_s:
                    player.movementy[1] = 0
                    player.movement_vectors['movement']["direction_vectorY"]=sum(player.movementy)

                if event.key == pygame.K_LSHIFT:

                    player.acceleration = player.acceleration_reset

                    if 'movement' in player.movement_vectors:
                        player.movement_vectors['movement']['acceleration'] = player.acceleration
                    # player.player_speed = 120

                    player.is_sprinting = False

                # handle interactions with e
                if event.key == pygame.K_e:

                    player.is_interacting = False

            # handling mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == pygame.BUTTON_LEFT:

                    # handle left clicks differently for semi auto and full aout weapons
                    if player.left_hand_weapon.select_fire == 'FULLAUTO' or player.left_hand_weapon.select_fire == 'CHARGEABLE':

                    # only allow shoointg if there are ammo reserrves or ammo in the current magazine
                        if (player.left_hand_weapon.total_ammo_stock > 0 or player.left_hand_weapon.bullets_remaining_in_mag > 0) :#and not player_bullet_manager.is_reloading, this prevents shooting if theyre using auto weapons and try to hold shoot whilskt reloading

                            # if the gun is not a dual wiled weapon set the regular shooting to true
                            if not player.left_hand_weapon.is_dual_wield or (player.left_hand_weapon.is_dual_wield and not player.left_hand_weapon.alternating_clicks):

                                # set shooting to be true
                                player.left_hand_weapon.is_shooting = True

                                # if it is secondary auto shoot then fire the secondary weapon here
                                if player.left_hand_weapon.secondary_weapon_auto_shoot:
                                    player.right_hand_weapon.is_shooting = True

                            # if its a dual wield weapon set the elft shot to true
                            elif player.left_hand_weapon.is_dual_wield and player.left_hand_weapon.alternating_clicks:


                                # set left to shooting
                                player.left_hand_weapon.is_shooting = True
                                # player.right_hand_weapon.is_shooting = True
                                # player_bullet_manager.is_shooting = True



                    elif player.left_hand_weapon.select_fire == 'SEMIAUTO':

                        # only allow shoointg if there are ammo reserrves or ammo in the current magazine
                        if not player.left_hand_weapon.is_burst:
                            if (player.left_hand_weapon.total_ammo_stock > 0 or player.left_hand_weapon.bullets_remaining_in_mag > 0) and (player.left_hand_weapon.time_between_shots == player.left_hand_weapon.reset_time_between_shots) : # and not player_bullet_manager.is_reloading


                                # if the gun is not a dual wiled weapon set the regular shooting to true
                                if not player.left_hand_weapon.is_dual_wield or (player.left_hand_weapon.is_dual_wield and not player.left_hand_weapon.alternating_clicks):

                                    # set shooting to be true
                                    player.left_hand_weapon.is_shooting = True

                                    # if it is secondary auto shoot then fire the secondary weapon here
                                    if player.left_hand_weapon.secondary_weapon_auto_shoot:
                                        player.right_hand_weapon.is_shooting = True

                                # if its a dual wield weapon set the elft shot to true
                                elif player.left_hand_weapon.is_dual_wield and player.left_hand_weapon.alternating_clicks:

                                    # set left to shooting
                                    player.left_hand_weapon.is_shooting = True

                        # only allow shoointg if there are ammo reserrves or ammo in the current magazine
                        elif player.left_hand_weapon.is_burst:
                            if (player.left_hand_weapon.total_ammo_stock > 0 or player.left_hand_weapon.bullets_remaining_in_mag > 0) and not player.left_hand_weapon.burst_countdown_active:#and not player_bullet_manager.is_reloading


                                # if the gun is not a dual wiled weapon set the regular shooting to true
                                if not player.left_hand_weapon.is_dual_wield or (player.left_hand_weapon.is_dual_wield and not player.left_hand_weapon.alternating_clicks):

                                    # set shooting to be true
                                    player.left_hand_weapon.is_shooting = True

                                # if its a dual wield weapon set the elft shot to true
                                elif player.left_hand_weapon.is_dual_wield and player.left_hand_weapon.alternating_clicks:

                                    # set left to shooting
                                    player.left_hand_weapon.is_shooting_left_gun = True


                if event.button == pygame.BUTTON_RIGHT and player.right_hand_weapon:

                    # handle left clicks differently for semi auto and full aout weapons
                    if player.right_hand_weapon.select_fire == 'FULLAUTO':

                    # only allow shoointg if there are ammo reserrves or ammo in the current magazine
                        if (player.right_hand_weapon.total_ammo_stock > 0 or player.right_hand_weapon.bullets_remaining_in_mag > 0) :#and not player_bullet_manager.is_reloading, this prevents shooting if theyre using auto weapons and try to hold shoot whilskt reloading

                            # if the gun is not a dual wiled weapon set the regular shooting to true
                            if not player.right_hand_weapon.is_dual_wield or (player.right_hand_weapon.is_dual_wield and not player.right_hand_weapon.alternating_clicks and not player.left_hand_weapon.secondary_weapon_auto_shoot):

                                # set shooting to be true
                                player.right_hand_weapon.is_shooting = True

                            # if its a dual wield weapon set the elft shot to true
                            elif player.right_hand_weapon.is_dual_wield and player.right_hand_weapon.alternating_clicks:

                                # set left to shooting
                                player.right_hand_weapon.is_shooting_left_gun = True
                                # player_bullet_manager.is_shooting = True

                    elif player.right_hand_weapon.select_fire == 'SEMIAUTO':

                        # only allow shoointg if there are ammo reserrves or ammo in the current magazine
                        if not player.right_hand_weapon.is_burst:
                            if (player.right_hand_weapon.total_ammo_stock > 0 or player.right_hand_weapon.bullets_remaining_in_mag > 0) and (player.right_hand_weapon.time_between_shots == player.right_hand_weapon.reset_time_between_shots) : # and not player_bullet_manager.is_reloading


                                # if the gun is not a dual wiled weapon set the regular shooting to true
                                if not player.right_hand_weapon.is_dual_wield or (player.right_hand_weapon.is_dual_wield and not player.right_hand_weapon.alternating_clicks):

                                    # set shooting to be true
                                    player.right_hand_weapon.is_shooting = True

                                # if its a dual wield weapon set the elft shot to true
                                elif player.right_hand_weapon.is_dual_wield and player.right_hand_weapon.alternating_clicks:

                                    # set left to shooting
                                    player.right_hand_weapon.is_shooting_left_gun = True

                        # only allow shoointg if there are ammo reserrves or ammo in the current magazine
                        elif player.right_hand_weapon.is_burst:
                            if (player.right_hand_weapon.total_ammo_stock > 0 or player.right_hand_weapon.bullets_remaining_in_mag > 0) and not player.right_hand_weapon.burst_countdown_active:#and not player_bullet_manager.is_reloading


                                # if the gun is not a dual wiled weapon set the regular shooting to true
                                if not player.right_hand_weapon.is_dual_wield or (player.right_hand_weapon.is_dual_wield and not player.right_hand_weapon.alternating_clicks):

                                    # set shooting to be true
                                    player.right_hand_weapon.is_shooting = True

                                # if its a dual wield weapon set the elft shot to true
                                elif player.right_hand_weapon.is_dual_wield and player.right_hand_weapon.alternating_clicks:

                                    # set left to shooting
                                    player.right_hand_weapon.is_shooting_left_gun = True




            # MOUSE BUTTON UP EVENTS
            if event.type == pygame.MOUSEBUTTONUP:

                if event.button == pygame.BUTTON_LEFT:

                    # if mouse is taken off the trigger then let shooting be False and reset the player bullet manager variables that need to be reset
                    # if the gun is not a dual wiled weapon set the regular shooting to true
                    if not player.left_hand_weapon.is_dual_wield or (player.left_hand_weapon.is_dual_wield and not player.left_hand_weapon.alternating_clicks):

                        # set shooting to be true
                        player.left_hand_weapon.is_shooting = False
                        player.left_hand_weapon.release_charge_shot = True
                        # player.left_hand_weapon.time_between_shots = 0

                        # reset charge
                        if player.left_hand_weapon.select_fire != 'CHARGEABLE':
                            player.left_hand_weapon.reset_charge(player.left_hand_weapon.charge_information)

                        # if it is secondary auto shoot then fire the secondary weapon here
                        if player.left_hand_weapon.secondary_weapon_auto_shoot:
                            player.right_hand_weapon.is_shooting = False
                            # reset charge
                            player.right_hand_weapon.reset_charge(player.right_hand_weapon.charge_information)

                    # if its a dual wield weapon set the elft shot to true
                    elif player.left_hand_weapon.is_dual_wield and player.left_hand_weapon.alternating_clicks:

                        # set left to shooting
                        player.left_hand_weapon.is_shooting = False
                        player.alternating_shot_ID = 1
                        player.left_hand_weapon.reset_charge(player.left_hand_weapon.charge_information)
                        # player.right_hand_weapon.is_shooting = False
                        # player.alternating_shot_delay = 0
                        # player.alternating_shot_ID = 1 # so back to the left gun

                if event.button == pygame.BUTTON_RIGHT and player.right_hand_weapon:

                    # if mouse is taken off the trigger then let shooting be False and reset the player bullet manager variables that need to be reset
                    # if the gun is not a dual wiled weapon set the regular shooting to true
                    # if not player_bullet_manager.is_dual_wield:

                    #     # set shooting to be true
                    #     player_bullet_manager.is_shooting = False

                     # if mouse is taken off the trigger then let shooting be False and reset the player bullet manager variables that need to be reset
                    # if the gun is not a dual wiled weapon set the regular shooting to true
                    if not player.right_hand_weapon.is_dual_wield or (player.right_hand_weapon.is_dual_wield and not player.right_hand_weapon.alternating_clicks and not player.right_hand_weapon.secondary_weapon_auto_shoot):

                        # set shooting to be true
                        player.right_hand_weapon.is_shooting = False

                    # if its a dual wield weapon set the elft shot to true
                    elif player.right_hand_weapon.is_dual_wield and player.right_hand_weapon.alternating_clicks:

                        # set left to shooting
                        player.right_hand_weapon.is_shooting_left_gun = False

        if sum(player.movementx) != 0 or sum(player.movementy) != 0:
            player.previous_movement = (sum(player.movementx),sum(player.movementy))
            acceleration = player.movement_vectors['movement']["acceleration"]
            player.movement_vectors['movement']["Xcceleration_rate_change"] = 'positive'
            player.movement_vectors['movement']["max_value"] = 1
            player.movement_vectors['movement']["Xcceleration_rate"] = 6

        elif sum(player.movementx) == 0 and sum(player.movementy) == 0:
            player.movement_vectors['movement']['direction_vectorX'] = player.previous_movement[0]
            player.movement_vectors['movement']['direction_vectorY'] = player.previous_movement[1]
            player.movement_vectors['movement']["Xcceleration_rate_change"] = 'negative'
            player.movement_vectors['movement']["max_value"] = 0
            player.movement_vectors['movement']["Xcceleration_rate"] = 5

        # if sum(player.movementx) == 0 and sum(player.movementy) == 0:
        #     player.movement_vectors['movement']["Xcceleration_rate_change"] = 'negative'
        #     player.movement_vectors['movement']["max_value"] = 0
        #     player.movement_vectors['movement']["Xcceleration_rate"] = 2

    def entity_events(self,all_events,enemy_manager,player):

        for event in all_events:

            if event.type == pygame.KEYDOWN:

                # if event.key == pygame.K_SPACE:

                #     enemy_manager.are_there_available_entities()

            # adjust the end point for the entities when this is selected
                if event.key == pygame.K_p:

                    possible_coors = [(500, 600), (550, 600), (550, 550), (200, 400), (600, 550), (150, 500), (650, 500), (600, 450),(0,100),(0,50)]

                    # enemy_manager.target_destination = (math.floor(player.rect.x),math.floor(player.rect.y))

                    # print(f'Pathinfinding to point {(math.floor(player.rect.x),math.floor(player.rect.y))}')
                    enemy_manager.target_destination = random.choice(possible_coors)



    def game_events(self,all_events,boss_controller,player):

        for event in all_events:

            # if the actual X is clicked to close the tab
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)

                if event.key == pygame.K_p:

                    # boss_controller.spawn_boss(boss_name = "DUMMY",point=(320,320))
                    boss_controller.spawn_boss(boss_name = "SUN-SEEKER",point=(320,320))
                    # boss_controller.spawn_boss(boss_name = "TEDDY MAG-DYLAN",point=(320,320))

                # if event.key == pygame.K_7:
                #     dum.spawn_dummy(player=player)

                # if event.key == pygame.K_z:
                #     Creative_Mode.bg_offset_x -= 100
                # if event.key == pygame.K_x:
                #     ##if im goign right then start subtracting the offset of x to move things to the left
                #     Creative_Mode.bg_offset_x += 100

                # if event.key == pygame.K_n:
                #     Creative_Mode.bg_offset_y += 100
                # if event.key == pygame.K_m:
                #     ##if im goign right then start subtracting the offset of x to move things to the left
                #     Creative_Mode.bg_offset_y-= 100

                # if event.key == pygame.K_f:

                #     if not is_fullscreen:
                #         win = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
                #         # need to know hwo big full screen paprrameter is, so i canm center th eplayerr withiun it
                #         # win = pygame.display.set_mode((window_parameters['SCREENWIDTH'],window_parameters['SCREENHEIGHT']))

                #         # get exact width and height of the screen once it has been made full screen, this is needed for centering the player
                #         Creative_Mode.fullscreen_width = pygame.display.Info().current_w
                #         Creative_Mode.fullscreen_height = pygame.display.Info().current_h

    def interactable_events(self,all_events:list,interactables:list):

        if interactables:
            for event in all_events:

                for interactable in interactables:
                    if event.type == player_interaction:

                        pass
                        pass






