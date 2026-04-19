from register8 import Register8
from procgen_seed48 import Seed48
from procgen_name import ProcgenName
from procgen_person import PgPerson
import copy



class PgSystem:
    """

    A system that generates its properties from the name provided.


    """

    # OMG just yolo the types... I didn't want to go all Rust for a simple test of this algo but really Python!?! WTF!!111eleven
    name = None
    seed = None
    tech_level = None

    colours_1 = ["White", "Cyan", "Purple", "Yellow"]
    colours_2 = ["White", "Red", "Green", "Blue"]
    colour_1 = None
    colour_2 = None

    sun_types = ["Red Dwarf (M-type)", "Yellow Dwarf (G-type)", "Blue Star (O-type)", "Red Giant", 
                    "Binary", "White Dwarf", "Neturon Star", "Brown Dwarf"]
    sun_type = None


    planet_types = ["Terrestial", "Super-Earth", "Ice Giant", "Gas Giant", 
                    "Ocean", "Lava", "Rogue", "Dessert"]
    planets_types = None
    planets_names = None

    station_services = ["Delivery", "Science", "Diplomacy", "Travel"]
    station_services_available = None
    station_manager = None

    security_levels = ["At war with the Culture", "Hostile to the Culture", "Neutrlal to the Culture", "Unknown to the Culture", 
                       "Friendly to the Culture", "Peace treaty with the Culture", "Trade agreements with the Culture", "Member of the Culture"]
    security_level = None


    def __init__(self, name: str):
        self.name = name
        self.generate()

    def generate(self):
        self.seed = Seed48().set_from_name(self.name)
        self.tech_level = self.seed.w0_lo._val & 0b00001111   # 0-15
        self.colour_1 = self.colours_1[(self.seed.w0_lo._val >> 4) & 0b00000011]
        self.colour_2 = self.colours_2[(self.seed.w0_lo._val >> 6) & 0b00000011]
        self.security_level = self.security_levels[self.seed.w0_hi._val & 0b00000111]
        num_planets = (self.seed.w0_hi._val >> 3) & 0b00000011   # 1-4

        self.sun_type = self.sun_types[self.seed.w1_lo._val & 0b00000111]

        planet_seed = copy.copy(self.seed)
        self.planets_types = []
        self.planets_names = []

        for i in range(0, num_planets+1):
            planet_seed.next_seed()
            self.planets_names.append(ProcgenName().multi_from_seed(planet_seed))
            self.planets_types.append(self.planet_types[planet_seed.w0_lo._val & 0b00000111])

        self.station_services_available = ""
        if self.seed.w1_lo.bit(0):
            self.station_services_available += f"{self.station_services[0]}\t"
        if self.seed.w1_lo.bit(1):
            self.station_services_available += f"{self.station_services[1]}\t"
        if self.seed.w1_lo.bit(2):
            self.station_services_available += f"{self.station_services[2]}\t"
        if self.seed.w1_lo.bit(3):
            self.station_services_available += f"{self.station_services[3]}\t"

        self.seed.next_seed()
        self.station_manager = PgPerson(ProcgenName().multi_from_seed(self.seed).name)


        return self
        

    def __repr__(self) -> str:
        planets = ""
        for i in range(0, self.planets_names.__len__()):
            planets = planets + f"\t\t\t{self.planets_names[i]}\t({self.planets_types[i]})\n"

        return (
            f"Name: {self.name}\n"
            f"\tSeed:\t\t{self.seed}\n"
            f"\tSun type:\t{self.sun_type}\n"
            f"\tTech level:\t{self.tech_level}\n"
            f"\t1st colour:\t{self.colour_1}\t"
            f"\t2nd colour:\t{self.colour_2}\n"
            f"\tSecurity:\t{self.security_level}\n"
            f"\tPlanets:\n{planets}"
            f"\tStation services:\n\t\t\t{self.station_services_available}\n"
            f"\tStation manager:\n{self.station_manager}\n"
        )



if __name__ == "__main__":
    system = PgSystem("LAVE")
    print(system)
    system = PgSystem("MOOP")
    print(system)
    system = PgSystem("Jjangmyeon")
    print(system)
    system = PgSystem("Home")
    print(system)

