from Assets.Scripts.Global import *
from Assets.Scripts.DEF import *
card_gradient=7
card_data={}
for root, dirs, files in os.walk(r"Assets\\JSON\\Cards"):
    for file in files:
        if file.endswith(".json"):
            print(file)
            card_data.update(json.loads(open(os.path.join(root,file),"r").read()))
card_pools={}
for i in card_data:
    if not card_data[i]["Tribe"] in card_pools:
        card_pools[card_data[i]["Tribe"]]=[]
    card_pools[card_data[i]["Tribe"]].append(i)
card_tribe_colors={
    "Neutral":(255,255,255),
    "Warrior":(155,13,13),
}
base_q_exponent=1.58
class Card:
    def __init__(self,name,quality=10):
        self.name=name
        self.quality=min(len(qualities)-1,croll(quality))
        self.data=card_data[self.name].copy()
        self.color=card_tribe_colors[self.data["Tribe"]]

        self.energy_cost=self.data["Energy Cost"]
        self.effects=self.data["Effects"].copy()
        self.Q_total_power=base_q_exponent**self.quality
        power_sum=[]
        for effect in self.effects:
            this_power=base_q_exponent**(random()*self.quality)
            power_sum.append(this_power)
            self.effects[effect]=int(self.effects[effect]*this_power)
        self.draw_sprite()
        
        if not "Custom Card Back" in self.data:
            self.card_back="Default"
        else:
            self.card_back=self.data["Custom Card Back"]
        self.card_back_sprite=sprite["Card Back"][self.card_back].copy()
        self.display_sprite=self.sprite.copy()
        self.aframe=0
        self.animation="None"
        self.display_sprite.set_colorkey((0,0,1))
        self.card_back_sprite.set_colorkey((0,0,1))
        self.flipped=False
        self.affected_sprite=pygame.Surface((140,180))
        if self.quality>0:
            self.card_effect=pygame.transform.scale(sprite["Card Effect"][qualities[self.quality]["Effect"]]["Sprite"],(1500,1500))
            
            self.card_effect.set_alpha(int(150*sum(power_sum)/len(power_sum)/self.Q_total_power))
            self.card_effect_destination=[0,0]
            self.card_effect_timer=0
    def draw_sprite(self):
        self.sprite=pygame.Surface((140,180))
        self.sprite.fill((0,0,1))
        for i in range(card_gradient):
            gradient_color=[i1/card_gradient*(card_gradient-i)/2 for i1 in self.color]
            pygame.draw.rect(self.sprite,gradient_color,(i*1,i*1,140-i*2,180-i*2),100,8)
        center(produce(self.energy_cost,15),self.sprite,125,15)
        center(produce(self.data["Name"],min(15,140/len(self.name))),self.sprite,70,25)
        for i,effect in enumerate(self.effects):
            if effect=="Deal Damage":
                text="Deal "+str(self.effects[effect])+" Damage"
            center(produce(text,min(15,130/len(text)*2)),self.sprite,70,40+i*15)
    def flip(self,speed=50):
        self.max_aframe=speed
        self.aframe=self.max_aframe
        self.animation="Being Flipped Horizontally"
    def instaflip(self):
        self.flipped=not self.flipped
        self.display_sprite.blit([self.sprite,self.card_back_sprite][self.flipped],(0,0))
    def animate(self):
        ############## EFFECT THINGY
        self.affected_sprite.blit(self.sprite,(0,0))
        if self.quality>0:
            if self.card_effect_timer==0:
                self.max_card_effect_timer=randint(50,200)
                self.card_effect_timer=self.max_card_effect_timer
                self.card_effect_pos=self.card_effect_destination
                self.card_effect_destination=[randint(0,self.card_effect.get_width()-140),randint(0,self.card_effect.get_height()-180)]
            self.card_effect_timer-=1
            self.card_q=self.card_effect_timer/self.max_card_effect_timer
            self.affected_sprite.blit(self.card_effect.subsurface((self.card_effect_pos[0]*self.card_q+self.card_effect_destination[0]*(1-self.card_q)),(self.card_effect_pos[1]*self.card_q+self.card_effect_destination[1]*(1-self.card_q)),140,180),(0,0))

        ################ Animations
        if self.aframe>0:
            self.aframe-=1
            if self.animation=="Being Flipped Horizontally":
                self.display_sprite.fill((0,0,1))
                if self.aframe>=self.max_aframe/2:
                    flipsprite=pygame.transform.scale([self.affected_sprite,self.card_back_sprite][self.flipped],(int((self.aframe-self.max_aframe/2)/self.max_aframe*2*140),180))
                else:
                    flipsprite=pygame.transform.scale([self.card_back_sprite,self.affected_sprite][self.flipped],(int((self.max_aframe/2-self.aframe)/self.max_aframe*2*140),180))
                flipsprite.set_colorkey((0,0,1))
                self.display_sprite.blit(flipsprite,(70-flipsprite.get_width()/2,0))
                if self.aframe==0:
                    self.flipped=not self.flipped
                    self.display_sprite.blit([self.affected_sprite,self.card_back_sprite][self.flipped],(0,0))
        else:
            self.animation="None"
            self.display_sprite.blit([self.affected_sprite,self.card_back_sprite][self.flipped],(0,0))

