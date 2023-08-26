import pygame, random, math, time
from rich import print as rprint

WEAPSTATS = {
    "rifle": {
        "recoil": 3,
        "damage.min": 9,
        "damage.max": 20,
        "reloadtime.min": 7,
        "reloadtime.max": 13,
        "range.min": 7,
        "range.max": 10,
        "weight.min": 20,
        "weight.max": 50,
        "delay.min": 1,
        "delay.max": 3,
        "bullets.min": 25,
        "bullets.max": 60 
    },
    "blank": {
        "recoil": 0,
        "damage.min": 0,
        "damage.max": 0,
        "reloadtime.min": 0,
        "reloadtime.max": 0,
        "range.min": 0,
        "range.max": 0,
        "weight.min": 0,
        "weight.max": 0,
        "delay.min": 0,
        "delay.max": 0,
        "bullets.min": 0,
        "bullets.max": 0   
    }
}

class Weapon:
    def __init__(self, image : pygame.Surface, classtype : str = None):
        self.image = pygame.Surface((256,256))
        self.image.fill((1,1,1)); self.image.set_colorkey((1,1,1))
        self.image.blit(image,(128-image.get_size()[0],128-image.get_size()[1]))
        self.classtype = classtype
        try:
            self.stats = WEAPSTATS[self.classtype]
        except:
            self.stats = WEAPSTATS["blank"]
        self.recoil = self.stats["recoil"]
        self.damage = random.randint(self.stats["damage.min"],self.stats["damage.max"])
        self.reloadtime = random.randint(self.stats["reloadtime.min"],self.stats["reloadtime.max"])
        self.range = random.randint(self.stats["range.min"],self.stats["range.max"])
        self.weight = random.randint(self.stats["weight.min"],self.stats["weight.max"])
        self.delay = random.randint(self.stats["delay.min"],self.stats["delay.max"])
        self.bullets = random.randint(self.stats["bullets.min"],self.stats["bullets.max"])

        self.rarity = 100
    
    def getrarity(self):
        weight = (self.stats["weight.min"]+self.stats["weight.max"]) - self.weight
        delay = (self.stats["delay.min"]+self.stats["delay.max"]) - self.delay
        reloadtime = (self.stats["reloadtime.min"]+self.stats["reloadtime.max"]) - self.reloadtime
        bullets = (self.stats["bullets.min"]+self.stats["bullets.max"]) - self.delay
        try:
            self.rarity = sum([100 * (self.stats["damage.max"] - self.damage) / (self.stats["damage.max"] - self.stats["damage.min"]),
                           100 * (self.stats["reloadtime.max"] - reloadtime) / (self.stats["reloadtime.max"] - self.stats["reloadtime.min"]),
                           100 * (self.stats["range.max"] - self.range) / (self.stats["range.max"] - self.stats["range.min"]),
                           100 * (self.stats["weight.max"] - weight) / (self.stats["weight.max"] - self.stats["weight.min"]),
                           100 * (self.stats["delay.max"] - delay) / (self.stats["delay.max"] - self.stats["delay.min"]),
                           100 * (self.stats["bullets.max"] - bullets) / (self.stats["bullets.max"] - self.stats["bullets.min"])
                        ]) / 6
        except Exception as e:
            print(e)

        if self.rarity >= 50: rating = " common "
        elif self.rarity >= 25: rating = " [blue]rare[/blue] "
        elif self.rarity >= 10: rating = " [purple]epic[/purple] "
        elif self.rarity >= 5: rating = "[orange_red1]legendary[/orange_red1]"
        elif self.rarity >= 1.5: rating = " [bright_yellow]mythical[/bright_yellow] "
        elif self.rarity >= -11: rating = " [red]unreal[/red] "
        else: rating = " [bright_cyan]godly[/bright_cyan] "

        self.rating = rating

        # if not rating in [" common "," [blue]rare[/blue] "," [purple]epic[/purple] ","[orange_red1]legendary[/orange_red1]"," [bright_yellow]mythical[/bright_yellow] "," [red]unreal[/red] "]: rprint(f"{self.damage} dmg | {self.reloadtime / 10} reload (s) | {self.range} range | {self.weight} weight | {self.delay / 10} delay (s) | {self.bullets} mag. size || rarity: {self.rarity} | rating: {rating}")
        rprint(f"{self.damage} dmg | {self.reloadtime / 10} reload (s) | {self.range} range | {self.weight} weight | {self.delay / 10} delay (s) | {self.bullets} mag. size || rarity: {self.rarity} | rating: {rating}")
        return [self.damage,self.reloadtime,self.range,self.weight,self.delay,self.bullets]

temp = Weapon(pygame.Surface((256,256)),"rifle")
i = 0
while True:
    temp = Weapon(pygame.Surface((256,256)),"rifle")
    temp.getrarity()
    i += 1
    if not temp.rating in [" [bright_cyan]godly[/bright_cyan] "]: 
        if not temp.rating in [" common "," [blue]rare[/blue] "]: rprint("[red]nope[/red]") #[" [red]unreal[/red] "," [bright_yellow]mythical[/bright_yellow] "," [bright_cyan]godly[/bright_cyan] "]: rprint("[red]nope[/red]")
    else:
        rprint("[green]yay[/green] attempts: [yellow]"+str(i)+"[/yellow]")
        time.sleep(3)
        i = 0

