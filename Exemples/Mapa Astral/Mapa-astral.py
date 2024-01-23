
# Import the main class for creating a kerykeion instance:
from kerykeion import KrInstance, MakeSvgInstance

# Create a kerykeion instance:
# Args: Name, year, month, day, hour, minuts, city, nation(optional)
kanye = KrInstance("Kanye", 1977, 6, 8, 8, 45, "Atlanta")

# Get the information about the sun in the chart:
# (The position of the planets always starts at 0)
kanye.sun

#> {'name': 'Sun', 'quality': 'Mutable', 'element': 'Air', 'sign': 'Gem', 'sign_num': 2, 'pos': 17.598992059774275, 'abs_pos': 77.59899205977428, 'emoji': '♊️', 'house': '12th House', 'retrograde': False}

# Get informations about the first house:
kanye.first_house

#> {'name': 'First House', 'quality': 'Cardinal', 'element': 'Water', 'sign': 'Can', 'sign_num': 3, 'pos': 17.995779673209114, 'abs_pos': 107.99577967320911, 'emoji': '♋️'}

# Get element of the moon sigSn:
kanye.moon.get("element")

#> 'Water'

kanye = KrInstance(
    "Kanye", 1977, 6, 8, 8, 45,
    lng=50, lat=50, tz_str="Europe/Rome"
    )

first = KrInstance("Jack", 1990, 6, 15, 15, 15, "Roma")
second = KrInstance("Jane", 1991, 10, 25, 21, 00, "Roma")

# Set the type, it can be Natal, Composite or Transit

name = MakeSvgInstance(first, chart_type="Composite", second_obj=second)
name.makeSVG()
print(len(name.aspects_list))

#> Generating kerykeion object for Jack...
#> Generating kerykeion object for Jane...
#> Jack birth location: Roma, 41.89193, 12.51133
#> SVG Generated Correctly
#> 38
