from random import *
from math import *
from Assets.Scripts.Cards import *
import pygame
pygame.init()
win=pygame.display.set_mode((0,0))
winsize=win.get_size()
S=pygame.Surface((1200,600))
S2=pygame.Surface((1200,600))
semi_transparent_black_screen=pygame.Surface((1200,600))
run=True

mouse_offset=[1200/winsize[0],600/winsize[1]]
ctimer=[0,0,0]
click=[False for i in range(3)]
def eventall():
    global run,mouse_pos,mouse_down,keys,click,ctimer
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    keys=pygame.key.get_pressed()
    mouse_pos=pygame.mouse.get_pos()
    mouse_pos=[mouse_pos[i]*mouse_offset[i] for i in range(2)]
    mouse_down=pygame.mouse.get_pressed()
    for i in range(3):
        if mouse_down[i]: ctimer[i]+=1
        else: ctimer[i]=0
        click[i]=(ctimer[i]==1)

def discover(card_count,pool="Neutral"):
    global run
    discovering=True
    semi_transparent_black_screen.set_alpha(100)
    S2.set_colorkey((0,0,1))
    discoverable_cards=[Card(choice(card_pools[pool])) for i in range(card_count)]
    for card in discoverable_cards:
        card.instaflip()
    animation="Cards Entering"
    aframe=0
    fliptime=ceil(min(20,200/card_count))
    S.blit(pygame.transform.scale(semi_transparent_black_screen,winsize),(0,0))
    while run and discovering:
        eventall()
        
        S2.fill((0,0,1))
        if animation=="Cards Entering":
            aframe+=1
            for i in range(card_count):
                center(pygame.transform.rotate(discoverable_cards[i].display_sprite,90-i/card_count*360),S2,cos(i/card_count*2*pi)*700*(100-aframe)/100+600,sin(i/card_count*2*pi)*700*(100-aframe)/100+300)
            if aframe==60:
                animation="Cards Flipping"
                aframe=0
        elif animation=="Cards Flipping":
            aframe+=1
            for i in range(card_count):
                center(pygame.transform.rotate(discoverable_cards[i].display_sprite,90-i/card_count*360),S2,cos(i/card_count*2*pi)*700*0.4+600,sin(i/card_count*2*pi)*700*0.4+300)
                if aframe==int(i*fliptime/3)+10:
                    discoverable_cards[i].flip(fliptime)
            if aframe==int(card_count*fliptime/3)+10:
                aframe=0
                animation="Selecting A Card"
        elif animation=="Selecting A Card":
            mouse_closest=-1
            dist=99999
            for i in range(card_count):
                d2=sqrt((cos(i/card_count*2*pi)*700*0.4+600-mouse_pos[0])**2+(sin(i/card_count*2*pi)*700*0.4+300-mouse_pos[1])**2)
                if d2<dist:
                    mouse_closest=i
                    dist=d2
            for i in range(card_count):
                if i==mouse_closest:
                    center(pygame.transform.rotate(discoverable_cards[i].display_sprite,90-i/card_count*360),S2,cos(i/card_count*2*pi)*700*0.39+600,sin(i/card_count*2*pi)*700*0.39+300)
                    if click[0]:
                        animation="Bringing The Card"
                        card_index=i
                        aframe=20
                        afspeed=-1
                else:
                    center(pygame.transform.rotate(discoverable_cards[i].display_sprite,90-i/card_count*360),S2,cos(i/card_count*2*pi)*700*0.4+600,sin(i/card_count*2*pi)*700*0.4+300)
        elif animation=="Bringing The Card":
            aframe=max(min(20,aframe+afspeed),0)
            for i in range(card_count):
                if i==card_index:
                    bring_q=aframe/20
                    center(pygame.transform.rotate(discoverable_cards[i].display_sprite,(90-i/card_count*360)*bring_q),S2,cos(i/card_count*2*pi)*700*0.4*bring_q+600,sin(i/card_count*2*pi)*700*0.4*bring_q+300)
                    if aframe==0 and click[0]:
                        afspeed=1
                    elif aframe==0 and click[2]:
                        aframe=-20
                        animation="Ending The Discovery"
                        for i in discoverable_cards:
                            i.flip(20)
                else:
                    center(pygame.transform.rotate(discoverable_cards[i].display_sprite,90-i/card_count*360),S2,cos(i/card_count*2*pi)*700*0.4+600,sin(i/card_count*2*pi)*700*0.4+300)
            if aframe==20:
                animation="Selecting A Card"
                aframe=0
        elif animation=="Ending The Discovery":
            aframe+=1
            for i in range(card_count):
                if i==card_index:
                    center(discoverable_cards[i].display_sprite,S2,600,300-max(0,aframe)*20)
                else:
                    center(pygame.transform.rotate(discoverable_cards[i].display_sprite,90-i/card_count*360),S2,cos(i/card_count*2*pi)*700*(40+max(0,aframe))/100+600,sin(i/card_count*2*pi)*700*(40+max(0,aframe))/100+300)
            if aframe>60:
                discovering=False
        if keys[27]:
            run=False
            break
        for i,card in enumerate(discoverable_cards):
            card.animate()
        win.blit(pygame.transform.scale(S,winsize),(0,0))
        
        S2_trans=pygame.transform.scale(S2,winsize)
        S2_trans.set_colorkey((0,0,1))
        win.blit(S2_trans,(0,0))
        pygame.display.update()

def materialize(card_count,pool="Neutral"):
    global run
    discovering=True
    semi_transparent_black_screen.set_alpha(100)
    S2.set_colorkey((0,0,1))
    discoverable_cards=[Card(choice(card_pools[pool])) for i in range(card_count)]
    for card in discoverable_cards:
        card.instaflip()
    output=[]
    animation="Cards Entering"
    aframe=0
    fliptime=ceil(min(20,60/card_count))
    S.blit(pygame.transform.scale(semi_transparent_black_screen,winsize),(0,0))
    while run and discovering:
        eventall()
        
        S2.fill((0,0,1))
        if animation=="Cards Entering":
            aframe+=1
            for i in range(card_count):
                center(pygame.transform.rotate(discoverable_cards[i].display_sprite,90-i/card_count*360),S2,cos(i/card_count*2*pi-aframe/10)*700*(100-aframe)/100+600,sin(i/card_count*2*pi-aframe/10)*700*(100-aframe)/100+300)
            if aframe==60:
                animation="Cards Flipping"
                aframe=0
        elif animation=="Cards Flipping":
            aframe+=1
            for i in range(card_count):
                center(pygame.transform.rotate(discoverable_cards[i].display_sprite,90-i/card_count*360),S2,cos(i/card_count*2*pi)*700*0.4+600,sin(i/card_count*2*pi)*700*0.4+300)
                if aframe==i*fliptime+10:
                    discoverable_cards[i].flip(fliptime)
            if aframe==card_count*fliptime+10:
                aframe=0
                animation="Selecting A Card"
        elif animation=="Selecting A Card":
            mouse_closest=-1
            dist=99999
            for i in range(card_count):
                d2=sqrt((cos(i/card_count*2*pi)*700*0.4+600-mouse_pos[0])**2+(sin(i/card_count*2*pi)*700*0.4+300-mouse_pos[1])**2)
                if d2<dist:
                    mouse_closest=i
                    dist=d2
            for i in range(card_count):
                if i==mouse_closest:
                    center(pygame.transform.rotate(discoverable_cards[i].display_sprite,90-i/card_count*360),S2,cos(i/card_count*2*pi)*700*0.39+600,sin(i/card_count*2*pi)*700*0.39+300)
                    if click[0]:
                        animation="Bringing The Card"
                        card_index=i
                        aframe=20
                        afspeed=-1
                else:
                    center(pygame.transform.rotate(discoverable_cards[i].display_sprite,90-i/card_count*360),S2,cos(i/card_count*2*pi)*700*0.4+600,sin(i/card_count*2*pi)*700*0.4+300)
            if click[2]:
                aframe=-40
                animation="Ending The Discovery"
                for i in discoverable_cards:
                    i.flip()
        elif animation=="Bringing The Card":
            aframe=max(min(20,aframe+afspeed),0)
            for i in range(card_count):
                if i==card_index:
                    bring_q=aframe/20
                    center(pygame.transform.rotate(discoverable_cards[i].display_sprite,(90-i/card_count*360)*bring_q),S2,cos(i/card_count*2*pi)*700*0.4*bring_q+600,sin(i/card_count*2*pi)*700*0.4*bring_q+300)
                    if aframe==0 and click[0]:
                        afspeed=1
                    elif aframe==0 and click[2]:
                        animation="Adding to the deck"
                        aframe=0
                else:
                    center(pygame.transform.rotate(discoverable_cards[i].display_sprite,90-i/card_count*360),S2,cos(i/card_count*2*pi)*700*0.4+600,sin(i/card_count*2*pi)*700*0.4+300)
            if aframe==20:
                animation="Selecting A Card"
                aframe=0
        elif animation=="Adding to the deck":
            aframe+=1
            for i in range(card_count):
                if i==card_index:
                    center(discoverable_cards[i].display_sprite,S2,600,300+aframe*15)
                else:
                    time_q=aframe/20
                    angle=(90-i/card_count*360)*(1-time_q)+time_q*((90-(i-1)/(card_count-1)*360)*(card_index<i)+(90-(i)/(card_count-1)*360)*(card_index>i))
                    pos=(i/card_count*2*pi)*(1-time_q)+time_q*((card_index<i)*((i-1)/(card_count-1)*2*pi)+(i/(card_count-1)*2*pi)*(card_index>i))
                    center(pygame.transform.rotate(discoverable_cards[i].display_sprite,angle),S2,cos(pos)*700*0.4+600,sin(pos)*700*0.4+300)
            if aframe==20:
                output.append(discoverable_cards[card_index])
                discoverable_cards.pop(card_index)
                card_count-=1
                animation="Selecting A Card"
                aframe=0
        elif animation=="Ending The Discovery":
            aframe+=1
            for i in range(card_count):
                center(pygame.transform.rotate(discoverable_cards[i].display_sprite,90-i/card_count*360),S2,cos(i/card_count*2*pi)*700*(40+aframe)/100+600,sin(i/card_count*2*pi)*700*(40+aframe)/100+300)
            if aframe>60:
                discovering=False
        if keys[27]:
            run=False
            break
        for i,card in enumerate(discoverable_cards):
            card.animate()
        win.blit(pygame.transform.scale(S,winsize),(0,0))
        S2_trans=pygame.transform.scale(S2,winsize)
        S2_trans.set_colorkey((0,0,1))
        win.blit(S2_trans,(0,0))
        pygame.display.update()
    return output
def combat():
    global run
    player_deck=[]
    for i in range(50):
        player_deck.append(discover(i+1,"Warrior"))
    for i in range(5):
        player_deck.append(discover(40))
    turn="Player"
    while run:
        S.fill((0,0,0))
        eventall()
        if keys[27]:
            run=False
            break
            S.blit(card.display_sprite,(i*140,0))
        win.blit(pygame.transform.scale(S,winsize),(0,0))
        pygame.display.update()
combat()
pygame.quit()