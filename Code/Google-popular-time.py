import populartimes
token = "AIzaSyALhAZt_ytM7tkOl-XKN_KXlIajgEXttNk"

# print(populartimes.get_id(token, "ChIJ01CaE2PfnUcRUpb8Ylg-UXo"))
stuff = populartimes.get(token, ["restaurant"], (-33.860, 151.210), (-33.790, 151.270))
print(stuff) # get coordinates and place type
# https://developers.google.com/places/supported_types
