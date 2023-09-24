import pygame
card_back_sprite_sheet=pygame.image.load("Assets\\Sprites\\Card Backs.xcf")
sprite={
    "Card Back":{
        "Default":card_back_sprite_sheet.subsurface((0,0,140,180))
    },
    "Card Effect":{
        "Default":{
            "Sprite":pygame.Surface((1,1)),
            "Alpha":0
        },
        "Effect 1":{
            "Sprite":pygame.image.load("Assets\\Sprites\\Idle Card Effects\\Effect 1.xcf"),
            "Alpha":54
        },
        "Effect 2":{
            "Sprite":pygame.image.load("Assets\\Sprites\\Idle Card Effects\\Effect 2.xcf"),
            "Alpha":63
        },
        "Effect 3":{
            "Sprite":pygame.image.load("Assets\\Sprites\\Idle Card Effects\\Effect 3.xcf"),
            "Alpha":63
        },
        
    }
}
for i in sprite:
    if i in ["Card Back"]:
        for i1 in sprite[i]:
            sprite[i][i1].set_colorkey((0,0,1))
qualities=[
    {
        "Name":"Useless",
        "Effect":"Default",
        "Alpha":0
    },
    {
        "Name":"Copper Scorched",
        "Effect":"Effect 1",
        "Alpha":54
    },
    {
        "Name":"Cobalt Melted",
        "Effect":"Effect 2",
        "Alpha":63
    },
    {
        "Name":"Ocularized",
        "Effect":"Effect 3",
        "Alpha":72
    },
]