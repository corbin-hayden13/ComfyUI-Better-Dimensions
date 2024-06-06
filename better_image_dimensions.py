from copy import copy
from math import ceil


pxl_base = 64
ratios = ["Custom", "1:1", "2:3", "4:5", "4:7", "5:12", "7:9", "9:16", "9:21", "13:19"]
ratios = {
    "Custom": None,
    "1:1": {"SD 1.5": 1024 / 2, "SDXL": 1024},
    "2:3": {"SD 1.5": 418 / 2, "SDXL": 418},
    "4:5": {"SD 1.5": 228.75 / 2, "SDXL": 228.75},
    "4:7": {"SD 1.5": 192 / 2, "SDXL": 192},
    "5:12": {"SD 1.5": 128 / 2, "SDXL": 128},
    "7:9": {"SD 1.5": 128 / 2, "SDXL": 128},
    "9:16": {"SD 1.5": 60, "SDXL": 90},
    "9:21": {"SD 1.5": (670 / 9) / 2, "SDXL": 670 / 9},
    "13:19": {"SD 1.5": 32, "SDXL": 64},
}
str_ratios = list(ratios.keys())
sdxl_dimensions = [
    "1024 x 1024",
    "896 x 1152",  # 7:9
    "832 x 1216",  # 13:19
    "768 x 1344",  # 4:7
    "640 x 1536",  # 5:12
    # Common dimensions but not SDXL compatible
    # "1144 x 915", "915 x 1144",  # 4:5
    # "1182 x 886", "886 x 1182",  # 3:4
    # "1254 x 836", "836 x 1254",  # 2:3
    # "1440 x 810", "810 x 1440",  # 9:16
    # "1564 x 670", "670 x 1564",  # 9:21
]


def apply_ratio(width, height, ratio, enforce_width: bool=True, swapped: bool=False):
    """
    Parameters
    ----------
    width: pixel width of the image
    height: pixel height of the image
    ratio: tuple as (width: int, height: int)
    enforce_width: bool to maintain original width or height (False) pixel values when returning ratioed width and height
    swapped: bool to flag whether the width and height should be swapped or not

    Returns
    -------

    """

    r_width, r_height = ratio

    print(f"better_dims > apply_ratio: r_w={r_width}, r_h={r_height}")
    if enforce_width:
        factor = width // r_width
        ret_tuple = (width, (factor * r_height)) if not swapped else ((factor * r_height), width)
        print(f"better_dims > apply_ratio: swapped={swapped} ret_tuple={ret_tuple}")
        return ret_tuple

    else:
        factor = height // r_height
        ret_tuple = ((factor * r_width), height) if not swapped else (height, (factor * r_width))
        print(f"better_dims > apply_ratio: swapped={swapped} ret_tuple={ret_tuple}")
        return ret_tuple


def apply_pure_ratio(ratio, ratio_scale: float=1.0, swapped: bool=False):
    global pxl_base

    r_width, r_height = ratio

    ratioed_width = int(r_width * pxl_base * ratio_scale)
    ratioed_height = int(r_height * pxl_base * ratio_scale)

    print(f"better_dims > apply_pure_ratio: ratioed_width={ratioed_width} ratioed_height={ratioed_height}")

    if swapped: return ratioed_height, ratioed_width
    else: return ratioed_width, ratioed_height


class SDXLDimensions:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "dimensions": (sdxl_dimensions,),
                "order": (["default (width,height)", "swapped (height,width)"],),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")

    FUNCTION = "better_dimensions"
    CATEGORY = "BetterDimensions"

    def better_dimensions(self, dimension: str="", order: str=""):
        return tuple([int(dim) for dim in dimension.split(" x ")[::-1 if order == "swapped (height,width)" else 1]])


class PureRatio:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "ratio": (str_ratios[1:],),
                "adjust_scale": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.01,
                    "round": 0.001,
                    "display": "number",
                }),
                "model": (["SDXL", "SD 1.5"],),
                "order": (["default (width,height)", "swapped (height,width)"],),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")

    FUNCTION = "better_dimensions"
    CATEGORY = "BetterDimensions"

    def better_dimensions(self, ratio: str="", adjust_scale: float=1.0, model: str="", order: str=""):
        swapped = order == "swapped (height,width)"
        builtin_scale = ratios[ratio][model]
        width, height = tuple([ceil(int(dim) * builtin_scale * adjust_scale) for dim in ratio.split(":")])

        return (width, height) if not swapped else (height, width)


class BetterDimensions:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {
                    "default": 1024,
                    "min": 64,
                    "max": 2 ** 20,
                    "step": 2,
                    "display": "number",
                }),
                "height": ("INT", {
                    "default": 1024,
                    "min": 64,
                    "max": 2 ** 20,
                    "step": 2,
                    "display": "number",
                }),
                "ratio": (str_ratios,),
                "enforce_dimension": (["width", "height"],),
                "order": (["default (width,height)", "swapped (height,width)"],),
            },
        }

    RETURN_TYPES = ("INT","INT")
    RETURN_NAMES = ("width","height")

    FUNCTION = "better_dimensions"
    CATEGORY = "BetterDimensions"

    def better_dimensions(self, width: int=0, height: int=0, ratio: str="None", enforce_dimension: str="width",
                          order: str="default (width,height)"):
        """ Parameters are given as keywords arguments so they have to match the key of the input types return dict """
        swapped = order == "swapped (height,width)"
        w = copy(width) if width > 0 else 64
        h = copy(height) if height > 0 else 64
        if ratio == str_ratios[0]:
            if swapped: return h, w
            else: return w, h

        tuple_ratio = tuple([int(r) for r in ratio.split(":")])
        enforce_width = enforce_dimension == "width"

        return apply_ratio(w, h, tuple_ratio, enforce_width=enforce_width, swapped=swapped)


NODE_CLASS_MAPPINGS = {
    "BetterImageDimensions": BetterDimensions,
    "SDXLDimensions": SDXLDimensions,
    "PureRatio": PureRatio,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "BetterImageDimensions": "Better Image Dimensions",
    "SDXLDimensions": "Standard SDXL Dimensions",
    "PureRatio": "Dimensions by Ratio",
}
