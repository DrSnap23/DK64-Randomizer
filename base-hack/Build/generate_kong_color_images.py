"""Convert RGB colors into a kong color palette."""

color_palettes = [
    {
        "kong": "dk",
        "zones": [
            {
                "zone": "base",
                "image": 3724,
                "colors": ["#363430"],
                "fill_type": "radial"
            }
        ]
    },
    {
        "kong": "diddy",
        "zones": [
            {
                "zone": "cap_shirt",
                "image": 3686,
                "colors": ["#363430"],
                "fill_type": "radial"
            }
        ]
    },
    {
        "kong": "lanky",
        "zones": [
            {
                "zone": "overalls",
                "image": 3689,
                "colors": ["#363430"],
                "fill_type": "radial",
            }
        ]
    },
    {
        "kong": "tiny",
        "zones": [
            {
                "zone": "overalls",
                "image": 3689,
                "colors": ["#363430"],
                "fill_type": "radial",
            }
        ]
    },
    {
        "kong": "chunky",
        "zones": [
            {
                "zone": "shirt_back",
                "image": 3769,
                "colors": ["#FFFFFF","#000000"],
                "fill_type": "checkered"
            },
            {
                "zone": "shirt_front",
                "image": 3687,
                "colors": ["#363430"],
                "fill_type": "radial"
            }
        ]
    }
]

def convertRGBAToBytearray(rgba_lst):
    """Convert RGBA list with 4 items (r,g,b,a) to a two-byte array in RGBA5551 format."""
    twobyte = (rgba_lst[0] << 11) | (rgba_lst[1] << 6) | (rgba_lst[2] << 1) | rgba_lst[3]
    lower = twobyte % 256
    upper = int(twobyte / 256)
    return [upper,lower]

def convertColors():
    """Convert color into RGBA5551 format"""
    for palette in color_palettes:
        for zone in palette["zones"]:
            rgba_list = []
            if zone["fill_type"] == "checkered" or zone["fill_type"] == "radial":
                lim = 2 
            else:
                lim = 1
            for x in range(lim):
                rgba = [0,0,0,1]
                for i in range(3):
                    if zone["fill_type"] == "radial":
                        val = int(int(f"0x{zone['colors'][0][(2*i)+1:(2*i)+3]}",16) * (1/8))
                        if x == 1:
                            val = int(val * 2)
                    else:
                        val = int(int(f"0x{zone['colors'][x][(2*i)+1:(2*i)+3]}",16) * (1/8))
                    if val < 0:
                        val = 0
                    elif val > 31:
                        val = 31
                    rgba[i] = val
                rgba_list.append(rgba)
            bytes_array = []
            if zone["fill_type"] == "block":
                ext = convertRGBAToBytearray(rgba_list[0])
                for x in range(32*32):
                    bytes_array.extend(ext)
            elif zone["fill_type"] == "radial":
                cen_x = 15.5
                cen_y = 15.5
                max_dist = (cen_x * cen_x) + (cen_y * cen_y)
                channel_diffs = [0,0,0]
                for i in range(3):
                    channel_diffs[i] = rgba_list[1][i] - rgba_list[0][i]
                for y in range(32):
                    for x in range(32):
                        dx = cen_x - x
                        dy = cen_y - y
                        dst = (dx * dx) + (dy * dy)
                        proportion = 1 - (dst / max_dist)
                        prop = [0,0,0,1]
                        for i in range(3):
                            val = int((channel_diffs[i] * proportion) + rgba_list[0][i])
                            if val < 0:
                                val = 0
                            elif val > 31:
                                val = 31
                            prop[i] = val
                        ext = convertRGBAToBytearray(prop)
                        bytes_array.extend(ext)
            elif zone["fill_type"] == "checkered":
                for y in range(32):
                    for x in range(32):
                        color_polarity_x = int(x / 4) % 2
                        color_polarity_y = int(y / 4) % 2
                        color_polarity = (color_polarity_x + color_polarity_y) % 2
                        ext = convertRGBAToBytearray(rgba_list[color_polarity])
                        bytes_array.extend(ext)

            with open(f"{palette['kong']}_{zone['zone']}.bin","wb") as fh:
                fh.write(bytearray(bytes_array))

convertColors()