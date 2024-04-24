"""Various lists to support the plandomizer."""

import re

from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Minigames import Minigames
from randomizer.Enums.Plandomizer import ItemToPlandoItemMap, PlandoItems
from randomizer.Enums.Types import Types
from randomizer.Enums.VendorType import VendorType
from randomizer.Lists.CustomLocations import CustomLocations, LocationTypes
from randomizer.Lists.FairyLocations import fairy_locations
from randomizer.Lists.Item import ItemList
from randomizer.Lists.KasplatLocations import KasplatLocationList
from randomizer.Lists.Location import LocationListOriginal as LocationList
from randomizer.Lists.MapsAndExits import RegionMapList
from randomizer.Lists.Minigame import BarrelMetaData, MinigameRequirements
from randomizer.Lists.ShufflableExit import ShufflableExits


def getKongString(kongEnum: Kongs) -> str:
    """Get the string name of the kong from the enum."""
    if kongEnum == Kongs.donkey:
        return "Donkey"
    elif kongEnum == Kongs.diddy:
        return "Diddy"
    elif kongEnum == Kongs.lanky:
        return "Lanky"
    elif kongEnum == Kongs.tiny:
        return "Tiny"
    elif kongEnum == Kongs.chunky:
        return "Chunky"
    else:
        return "All Kongs"


def GetLevelString(levelEnum: Levels) -> str:
    """Get the string name of a level from the enum."""
    if levelEnum == Levels.DKIsles:
        return "D.K. Isles"
    elif levelEnum == Levels.JungleJapes:
        return "Jungle Japes"
    elif levelEnum == Levels.AngryAztec:
        return "Angry Aztec"
    elif levelEnum == Levels.FranticFactory:
        return "Frantic Factory"
    elif levelEnum == Levels.GloomyGalleon:
        return "Gloomy Galleon"
    elif levelEnum == Levels.FungiForest:
        return "Fungi Forest"
    elif levelEnum == Levels.CrystalCaves:
        return "Crystal Caves"
    elif levelEnum == Levels.CreepyCastle:
        return "Creepy Castle"
    elif levelEnum == Levels.HideoutHelm:
        return "Hideout Helm"
    elif levelEnum == Levels.Shops:
        return "Shops"
    else:
        return None


# Some useful lists of locations. These will mostly be used for on-the-fly
# input validation. They will be populated as we build out other data
# structures.

# A list of all locations where items can be placed.
ItemLocationList = []
# A list of all shop locations.
ShopLocationList = []
# A list of all minigame locations.
MinigameLocationList = []
# A list of all hint locations.
HintLocationList = []

# Additional lists we need in order to disable certain locations.
CrownPlandoLocationList = []
DirtPatchPlandoLocationList = []
FairyPlandoLocationList = []
KasplatPlandoLocationList = []
MelonCratePlandoLocationList = []


def createShopLocationKongMapObj() -> dict:
    """Initialize an entry in the ShopLocationKongMap."""
    return {VendorType.Candy.name: {"shared": None, "individual": []}, VendorType.Cranky.name: {"shared": None, "individual": []}, VendorType.Funky.name: {"shared": None, "individual": []}}


# A map of shop locations, grouped by level and broken into shared/individual.
ShopLocationKongMap = {
    "DKIsles": createShopLocationKongMapObj(),
    "JungleJapes": createShopLocationKongMapObj(),
    "AngryAztec": createShopLocationKongMapObj(),
    "FranticFactory": createShopLocationKongMapObj(),
    "GloomyGalleon": createShopLocationKongMapObj(),
    "FungiForest": createShopLocationKongMapObj(),
    "CrystalCaves": createShopLocationKongMapObj(),
    "CreepyCastle": createShopLocationKongMapObj(),
}

##########
# PANELS #
##########


def createPlannableLocationObj() -> dict:
    """Initialize the plannable location object."""
    return {"All Kongs": [], "Donkey": [], "Diddy": [], "Lanky": [], "Tiny": [], "Chunky": [], "Enemies": []}


def isMinigameLocation(locationEnum: Locations) -> bool:
    """Determine if this location is a minigame location."""
    return locationEnum in BarrelMetaData


PlandomizerPanels = {
    "DKIsles": {"name": "D.K. Isles", "locations": createPlannableLocationObj()},
    "JungleJapes": {"name": "Jungle Japes", "locations": createPlannableLocationObj()},
    "AngryAztec": {"name": "Angry Aztec", "locations": createPlannableLocationObj()},
    "FranticFactory": {"name": "Frantic Factory", "locations": createPlannableLocationObj()},
    "GloomyGalleon": {"name": "Gloomy Galleon", "locations": createPlannableLocationObj()},
    "FungiForest": {"name": "Fungi Forest", "locations": createPlannableLocationObj()},
    "CrystalCaves": {"name": "Crystal Caves", "locations": createPlannableLocationObj()},
    "CreepyCastle": {"name": "Creepy Castle", "locations": createPlannableLocationObj()},
    "HideoutHelm": {"name": "Hideout Helm", "locations": {"All Kongs": [], "Medals": [], "Enemies": []}},
    # Shops, minigames and hints are grouped by level, not by Kong.
    "Shops": {
        "name": "Shops",
        "levels": {
            "DKIsles": {"name": "D.K. Isles", "locations": []},
            "JungleJapes": {"name": "Jungle Japes", "locations": []},
            "AngryAztec": {"name": "Angry Aztec", "locations": []},
            "FranticFactory": {"name": "Frantic Factory", "locations": []},
            "GloomyGalleon": {"name": "Gloomy Galleon", "locations": []},
            "FungiForest": {"name": "Fungi Forest", "locations": []},
            "CrystalCaves": {"name": "Crystal Caves", "locations": []},
            "CreepyCastle": {"name": "Creepy Castle", "locations": []},
        },
    },
    # "Blueprints": {
    #    "name": "Blueprints",
    #    "locations": createPlannableLocationObj()
    # },
    "Minigames": {
        "name": "Minigames",
        "levels": {
            "DKIsles": {"name": "D.K. Isles", "locations": []},
            "JungleJapes": {"name": "Jungle Japes", "locations": []},
            "AngryAztec": {"name": "Angry Aztec", "locations": []},
            "FranticFactory": {"name": "Frantic Factory", "locations": []},
            "GloomyGalleon": {"name": "Gloomy Galleon", "locations": []},
            "FungiForest": {"name": "Fungi Forest", "locations": []},
            "CrystalCaves": {"name": "Crystal Caves", "locations": []},
            "CreepyCastle": {"name": "Creepy Castle", "locations": []},
            "HideoutHelm": {"name": "Hideout Helm", "locations": []},
        },
    },
    "Locations": {
        "name": "Custom Locations",
        "categories": {
            "Fairy": {
                "name": "Banana Fairies",
                "singular": "fairy",
                "locations": [],
            },
            "CrownPad": {
                "name": "Battle Crown Arenas",
                "singular": "arena",
                "locations": [],
            },
            "DirtPatch": {
                "name": "Dirt Patches",
                "singular": "patch",
                "locations": [],
            },
            "Kasplat": {
                "name": "Kasplats",
                "singular": "kasplat",
                "locations": [],
            },
            "MelonCrate": {
                "name": "Melon Crates",
                "singular": "crate",
                "locations": [],
            },
        },
    },
    "Hints": {
        "name": "Hints",
        "levels": {
            "JungleJapes": {"name": "Jungle Japes", "locations": []},
            "AngryAztec": {"name": "Angry Aztec", "locations": []},
            "FranticFactory": {"name": "Frantic Factory", "locations": []},
            "GloomyGalleon": {"name": "Gloomy Galleon", "locations": []},
            "FungiForest": {"name": "Fungi Forest", "locations": []},
            "CrystalCaves": {"name": "Crystal Caves", "locations": []},
            "CreepyCastle": {"name": "Creepy Castle", "locations": []},
        },
    },
}
for locationEnum, locationObj in LocationList.items():
    # Do not randomize constant rewards.
    if locationObj.type == Types.Constant:
        continue
    # Do not include training barrels or pre-given move locations. We will fill
    # those automatically based on the user's selected starting moves.
    if locationObj.type in [Types.TrainingBarrel, Types.PreGivenMove]:
        continue
    locationJson = {"name": locationObj.name, "value": locationEnum.name}
    kongString = getKongString(locationObj.kong)
    if locationObj.type == Types.BlueprintBanana:
        # PlandomizerPanels["Blueprints"]["locations"][kongString].append(locationJson)
        continue
    elif locationObj.type == Types.Hint:
        levelName = locationObj.level.name
        PlandomizerPanels["Hints"]["levels"][levelName]["locations"].append(locationJson)
        HintLocationList.append(locationEnum.name)
    elif locationObj.type == Types.Shop:
        levelName = locationObj.level.name
        PlandomizerPanels["Shops"]["levels"][levelName]["locations"].append(locationJson)
        ShopLocationList.append(locationEnum.name)
        # Add this to the ShopLocationKongMap, which will be used for validation.
        vendor = locationObj.vendor.name
        if locationObj.kong == Kongs.any:
            ShopLocationKongMap[levelName][vendor]["shared"] = {"name": locationEnum.name, "value": locationObj}
        else:
            ShopLocationKongMap[levelName][vendor]["individual"].append({"name": locationEnum.name, "value": locationObj})
    elif locationObj.level == Levels.Shops:
        # This is the Rareware coin.
        PlandomizerPanels["Shops"]["levels"]["DKIsles"]["locations"].append(locationJson)
        ShopLocationList.append(locationEnum.name)
    else:
        levelName = locationObj.level.name
        if locationObj.level == Levels.HideoutHelm and locationObj.type == Types.Medal:
            PlandomizerPanels[levelName]["locations"]["Medals"].append(locationJson)
        elif locationObj.type == Types.Enemies:
            PlandomizerPanels[levelName]["locations"]["Enemies"].append(locationJson)
        else:
            PlandomizerPanels[levelName]["locations"][kongString].append(locationJson)
        ItemLocationList.append(locationEnum.name)

        # We need to keep track of locations for dirt patches, fairies, arenas,
        # melon crates, and Kasplats.
        if locationObj.type == Types.Crown:
            CrownPlandoLocationList.append(locationEnum.name)
        elif locationObj.type == Types.RainbowCoin:
            DirtPatchPlandoLocationList.append(locationEnum.name)
        elif locationObj.type == Types.Fairy:
            FairyPlandoLocationList.append(locationEnum.name)
        elif locationObj.type == Types.Blueprint:
            KasplatPlandoLocationList.append(locationEnum.name)
        elif locationObj.type == Types.CrateItem:
            MelonCratePlandoLocationList.append(locationEnum.name)

        # If this is a minigame location, add it to the Minigames list.
        if isMinigameLocation(locationEnum):
            PlandomizerPanels["Minigames"]["levels"][levelName]["locations"].append({"name": locationObj.name, "value": locationEnum.name, "kong": kongString})
            MinigameLocationList.append(locationEnum.name)

# Hideout Helm minigame locations get manually added here, as they're not
# locations where rewards can be placed, so they don't get naturally added.
PlandomizerPanels["Minigames"]["levels"]["HideoutHelm"]["locations"] = [
    {"name": "Helm Donkey 1", "value": "HelmDonkey1", "kong": "Donkey"},
    {"name": "Helm Donkey 2", "value": "HelmDonkey2", "kong": "Donkey"},
    {"name": "Helm Diddy 1", "value": "HelmDiddy1", "kong": "Diddy"},
    {"name": "Helm Diddy 2", "value": "HelmDiddy2", "kong": "Diddy"},
    {"name": "Helm Lanky 1", "value": "HelmLanky1", "kong": "Lanky"},
    {"name": "Helm Lanky 2", "value": "HelmLanky2", "kong": "Lanky"},
    {"name": "Helm Tiny 1", "value": "HelmTiny1", "kong": "Tiny"},
    {"name": "Helm Tiny 2", "value": "HelmTiny2", "kong": "Tiny"},
    {"name": "Helm Chunky 1", "value": "HelmChunky1", "kong": "Chunky"},
    {"name": "Helm Chunky 2", "value": "HelmChunky2", "kong": "Chunky"},
]
MinigameLocationList += ["HelmDonkey1", "HelmDonkey2", "HelmDiddy1", "HelmDiddy2", "HelmLanky1", "HelmLanky2", "HelmTiny1", "HelmTiny2", "HelmChunky1", "HelmChunky2"]

#########
# ITEMS #
#########

# These PlandoItems enums have multiple Items enums that map to each of them,
# and so they should not be automatically added to the list of PlannableItems.
# Handle these manually.
doNotAutoAddPlandoItemSet = {PlandoItems.DonkeyBlueprint, PlandoItems.DiddyBlueprint, PlandoItems.LankyBlueprint, PlandoItems.TinyBlueprint, PlandoItems.ChunkyBlueprint, PlandoItems.JunkItem}
# These items are extras that map to PlandoItems already covered by other
# Items. Do not add these.
doNotAutoAddItemSet = {Items.ProgressiveSlam2, Items.ProgressiveSlam3, Items.ProgressiveAmmoBelt2, Items.ProgressiveInstrumentUpgrade2, Items.ProgressiveInstrumentUpgrade3}

PlannableItems = []  # Used to select rewards for locations.

for itemEnum, itemObj in ItemList.items():
    # Only include items that have a matching item in the plando map.
    if itemEnum not in ItemToPlandoItemMap:
        continue
    # Do not include items in this set.
    if itemEnum in doNotAutoAddItemSet:
        continue

    plandoItemEnum = ItemToPlandoItemMap[itemEnum]
    # Do not add blueprints or junk items. These will be replaced with generic
    # items.
    if plandoItemEnum in doNotAutoAddPlandoItemSet:
        continue
    itemJson = {"name": itemObj.name, "value": plandoItemEnum.name}
    PlannableItems.append(itemJson)

PlannableItems.append({"name": "Blueprint (Donkey)", "value": "DonkeyBlueprint"})
PlannableItems.append({"name": "Blueprint (Diddy)", "value": "DiddyBlueprint"})
PlannableItems.append({"name": "Blueprint (Lanky)", "value": "LankyBlueprint"})
PlannableItems.append({"name": "Blueprint (Tiny)", "value": "TinyBlueprint"})
PlannableItems.append({"name": "Blueprint (Chunky)", "value": "ChunkyBlueprint"})
PlannableItems.append({"name": "Junk Item", "value": "JunkItem"})

# The maximum amount of each item that the user is allowed to place.
# If a plando item is not here, that item has no limit.
PlannableItemLimits = {
    PlandoItems.Donkey: 1,
    PlandoItems.Diddy: 1,
    PlandoItems.Lanky: 1,
    PlandoItems.Tiny: 1,
    PlandoItems.Chunky: 1,
    PlandoItems.Vines: 1,
    PlandoItems.Swim: 1,
    PlandoItems.Oranges: 1,
    PlandoItems.Barrels: 1,
    PlandoItems.ProgressiveSlam: 3,
    PlandoItems.BaboonBlast: 1,
    PlandoItems.StrongKong: 1,
    PlandoItems.GorillaGrab: 1,
    PlandoItems.ChimpyCharge: 1,
    PlandoItems.RocketbarrelBoost: 1,
    PlandoItems.SimianSpring: 1,
    PlandoItems.Orangstand: 1,
    PlandoItems.BaboonBalloon: 1,
    PlandoItems.OrangstandSprint: 1,
    PlandoItems.MiniMonkey: 1,
    PlandoItems.PonyTailTwirl: 1,
    PlandoItems.Monkeyport: 1,
    PlandoItems.HunkyChunky: 1,
    PlandoItems.PrimatePunch: 1,
    PlandoItems.GorillaGone: 1,
    PlandoItems.Coconut: 1,
    PlandoItems.Peanut: 1,
    PlandoItems.Grape: 1,
    PlandoItems.Feather: 1,
    PlandoItems.Pineapple: 1,
    PlandoItems.HomingAmmo: 1,
    PlandoItems.SniperSight: 1,
    PlandoItems.ProgressiveAmmoBelt: 2,
    PlandoItems.Bongos: 1,
    PlandoItems.Guitar: 1,
    PlandoItems.Trombone: 1,
    PlandoItems.Saxophone: 1,
    PlandoItems.Triangle: 1,
    PlandoItems.ProgressiveInstrumentUpgrade: 3,
    PlandoItems.Camera: 1,
    PlandoItems.Shockwave: 1,
    PlandoItems.NintendoCoin: 1,
    PlandoItems.RarewareCoin: 1,
    PlandoItems.JungleJapesKey: 1,
    PlandoItems.AngryAztecKey: 1,
    PlandoItems.FranticFactoryKey: 1,
    PlandoItems.GloomyGalleonKey: 1,
    PlandoItems.FungiForestKey: 1,
    PlandoItems.CrystalCavesKey: 1,
    PlandoItems.CreepyCastleKey: 1,
    PlandoItems.HideoutHelmKey: 1,
    # Forty of these bananas are currently allocated to blueprint rewards.
    PlandoItems.GoldenBanana: 201,
    PlandoItems.BananaFairy: 20,
    PlandoItems.BananaMedal: 40,
    PlandoItems.BattleCrown: 10,
    PlandoItems.Bean: 1,
    PlandoItems.Pearl: 5,
    PlandoItems.FakeItem: 16,
    PlandoItems.JunkItem: 100,
    PlandoItems.RainbowCoin: 16,
    PlandoItems.DonkeyBlueprint: 8,
    PlandoItems.DiddyBlueprint: 8,
    PlandoItems.LankyBlueprint: 8,
    PlandoItems.TinyBlueprint: 8,
    PlandoItems.ChunkyBlueprint: 8,
}

#############
# MINIGAMES #
#############

PlannableMinigames = []
for minigameEnum, minigameObj in MinigameRequirements.items():
    # NoGame is an invalid selection.
    if minigameEnum == Minigames.NoGame:
        continue
    minigameJson = {"name": minigameObj.name, "value": minigameEnum.name}
    PlannableMinigames.append(minigameJson)

###################
# SPAWN LOCATIONS #
###################

PlannableSpawns = []

for transition, exit in ShufflableExits.items():
    if exit.back.regionId in RegionMapList:
        transitionJson = {"name": exit.name, "value": transition.name}
        PlannableSpawns.append(transitionJson)

####################
# CUSTOM LOCATIONS #
####################

PlannableCustomLocations = {}

CrownLocationEnumList = [
    Locations.JapesBattleArena.name,
    Locations.AztecBattleArena.name,
    Locations.FactoryBattleArena.name,
    Locations.GalleonBattleArena.name,
    Locations.ForestBattleArena.name,
    Locations.CavesBattleArena.name,
    Locations.CastleBattleArena.name,
    Locations.IslesBattleArena1.name,
    Locations.IslesBattleArena2.name,
    Locations.HelmBattleArena.name,
]
KasplatLocationEnumList = [
    Locations.JapesDonkeyKasplatRando.name,
    Locations.JapesDiddyKasplatRando.name,
    Locations.JapesLankyKasplatRando.name,
    Locations.JapesTinyKasplatRando.name,
    Locations.JapesChunkyKasplatRando.name,
    Locations.AztecDonkeyKasplatRando.name,
    Locations.AztecDiddyKasplatRando.name,
    Locations.AztecLankyKasplatRando.name,
    Locations.AztecTinyKasplatRando.name,
    Locations.AztecChunkyKasplatRando.name,
    Locations.FactoryDonkeyKasplatRando.name,
    Locations.FactoryDiddyKasplatRando.name,
    Locations.FactoryLankyKasplatRando.name,
    Locations.FactoryTinyKasplatRando.name,
    Locations.FactoryChunkyKasplatRando.name,
    Locations.GalleonDonkeyKasplatRando.name,
    Locations.GalleonDiddyKasplatRando.name,
    Locations.GalleonLankyKasplatRando.name,
    Locations.GalleonTinyKasplatRando.name,
    Locations.GalleonChunkyKasplatRando.name,
    Locations.ForestDonkeyKasplatRando.name,
    Locations.ForestDiddyKasplatRando.name,
    Locations.ForestLankyKasplatRando.name,
    Locations.ForestTinyKasplatRando.name,
    Locations.ForestChunkyKasplatRando.name,
    Locations.CavesDonkeyKasplatRando.name,
    Locations.CavesDiddyKasplatRando.name,
    Locations.CavesLankyKasplatRando.name,
    Locations.CavesTinyKasplatRando.name,
    Locations.CavesChunkyKasplatRando.name,
    Locations.CastleDonkeyKasplatRando.name,
    Locations.CastleDiddyKasplatRando.name,
    Locations.CastleLankyKasplatRando.name,
    Locations.CastleTinyKasplatRando.name,
    Locations.CastleChunkyKasplatRando.name,
    Locations.IslesDonkeyKasplatRando.name,
    Locations.IslesDiddyKasplatRando.name,
    Locations.IslesLankyKasplatRando.name,
    Locations.IslesTinyKasplatRando.name,
    Locations.IslesChunkyKasplatRando.name,
]


def GetCrownVanillaLocation(location: Locations) -> str:
    """Extract the vanilla location for the provided crown location enum."""
    locationString = LocationList[location].name
    return re.search(r"^[^(\)]+?\((.+)\)$", locationString)[1]


# This groups crown locations together by level.
CrownVanillaLocationMap = {
    Levels.JungleJapes: {
        Locations.JapesBattleArena: GetCrownVanillaLocation(Locations.JapesBattleArena),
    },
    Levels.AngryAztec: {
        Locations.AztecBattleArena: GetCrownVanillaLocation(Locations.AztecBattleArena),
    },
    Levels.FranticFactory: {
        # This one location has to be manually adjusted.
        Locations.FactoryBattleArena: f"{GetCrownVanillaLocation(Locations.FactoryBattleArena)} (1)",
    },
    Levels.GloomyGalleon: {
        Locations.GalleonBattleArena: GetCrownVanillaLocation(Locations.GalleonBattleArena),
    },
    Levels.FungiForest: {
        Locations.ForestBattleArena: GetCrownVanillaLocation(Locations.ForestBattleArena),
    },
    Levels.CrystalCaves: {
        Locations.CavesBattleArena: GetCrownVanillaLocation(Locations.CavesBattleArena),
    },
    Levels.CreepyCastle: {
        Locations.CastleBattleArena: GetCrownVanillaLocation(Locations.CastleBattleArena),
    },
    Levels.DKIsles: {
        Locations.IslesBattleArena1: GetCrownVanillaLocation(Locations.IslesBattleArena1),
        Locations.IslesBattleArena2: GetCrownVanillaLocation(Locations.IslesBattleArena2),
    },
    Levels.HideoutHelm: {
        Locations.HelmBattleArena: GetCrownVanillaLocation(Locations.HelmBattleArena),
    },
}

# This map associates Kasplat physical locations (where they appear on the map)
# with the locations associated with their rewards, and groups them by level.
KasplatLocationToRewardMap = {
    Levels.JungleJapes: {
        Locations.JapesDonkeyKasplatRando: Locations.JapesKasplatLeftTunnelNear,
        Locations.JapesDiddyKasplatRando: Locations.JapesKasplatNearPaintingRoom,
        Locations.JapesLankyKasplatRando: Locations.JapesKasplatNearLab,
        Locations.JapesTinyKasplatRando: Locations.JapesKasplatLeftTunnelFar,
        Locations.JapesChunkyKasplatRando: Locations.JapesKasplatUnderground,
    },
    Levels.AngryAztec: {
        Locations.AztecDonkeyKasplatRando: Locations.AztecKasplatSandyBridge,
        Locations.AztecDiddyKasplatRando: Locations.AztecKasplatOnTinyTemple,
        Locations.AztecLankyKasplatRando: Locations.AztecKasplatLlamaTemple,
        Locations.AztecTinyKasplatRando: Locations.AztecKasplatNearLab,
        Locations.AztecChunkyKasplatRando: Locations.AztecKasplatChunky5DT,
    },
    Levels.FranticFactory: {
        Locations.FactoryDonkeyKasplatRando: Locations.FactoryKasplatProductionTop,
        Locations.FactoryDiddyKasplatRando: Locations.FactoryKasplatProductionBottom,
        Locations.FactoryLankyKasplatRando: Locations.FactoryKasplatRandD,
        Locations.FactoryTinyKasplatRando: Locations.FactoryKasplatStorage,
        Locations.FactoryChunkyKasplatRando: Locations.FactoryKasplatBlocks,
    },
    Levels.GloomyGalleon: {
        Locations.GalleonDonkeyKasplatRando: Locations.GalleonKasplatGoldTower,
        Locations.GalleonDiddyKasplatRando: Locations.GalleonKasplatLighthouseArea,
        Locations.GalleonLankyKasplatRando: Locations.GalleonKasplatCannons,
        Locations.GalleonTinyKasplatRando: Locations.GalleonKasplatNearLab,
        Locations.GalleonChunkyKasplatRando: Locations.GalleonKasplatNearSub,
    },
    Levels.FungiForest: {
        Locations.ForestDonkeyKasplatRando: Locations.ForestKasplatNearBarn,
        Locations.ForestDiddyKasplatRando: Locations.ForestKasplatInsideMushroom,
        Locations.ForestLankyKasplatRando: Locations.ForestKasplatOwlTree,
        Locations.ForestTinyKasplatRando: Locations.ForestKasplatLowerMushroomExterior,
        Locations.ForestChunkyKasplatRando: Locations.ForestKasplatUpperMushroomExterior,
    },
    Levels.CrystalCaves: {
        Locations.CavesDonkeyKasplatRando: Locations.CavesKasplatNearLab,
        Locations.CavesDiddyKasplatRando: Locations.CavesKasplatNearFunky,
        Locations.CavesLankyKasplatRando: Locations.CavesKasplatPillar,
        Locations.CavesTinyKasplatRando: Locations.CavesKasplatNearCandy,
        Locations.CavesChunkyKasplatRando: Locations.CavesKasplatOn5DI,
    },
    Levels.CreepyCastle: {
        Locations.CastleDonkeyKasplatRando: Locations.CastleKasplatTree,
        Locations.CastleDiddyKasplatRando: Locations.CastleKasplatCrypt,
        Locations.CastleLankyKasplatRando: Locations.CastleKasplatHalfway,
        Locations.CastleTinyKasplatRando: Locations.CastleKasplatLowerLedge,
        Locations.CastleChunkyKasplatRando: Locations.CastleKasplatNearCandy,
    },
    Levels.DKIsles: {
        Locations.IslesDonkeyKasplatRando: Locations.IslesKasplatHelmLobby,
        Locations.IslesDiddyKasplatRando: Locations.IslesKasplatCastleLobby,
        Locations.IslesLankyKasplatRando: Locations.IslesKasplatCavesLobby,
        Locations.IslesTinyKasplatRando: Locations.IslesKasplatFactoryLobby,
        Locations.IslesChunkyKasplatRando: Locations.IslesKasplatGalleonLobby,
    },
}


# These will be filled in later.
DirtPatchVanillaLocationMap = {}
FairyVanillaLocationMap = {}
MelonCrateVanillaLocationMap = {}

plannableCrates = []
plannableCrownPads = {
    Levels.JungleJapes.name: [],
    Levels.AngryAztec.name: [],
    Levels.FranticFactory.name: [],
    Levels.GloomyGalleon.name: [],
    Levels.FungiForest.name: [],
    Levels.CrystalCaves.name: [],
    Levels.CreepyCastle.name: [],
    Levels.HideoutHelm.name: [],
    Levels.DKIsles.name: [],
}
plannableDirt = []


def getKongFromLocationEnum(location: Locations) -> Kongs:
    """Parse the name of a location and return the associated Kong."""
    for kong in [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]:
        if kong.name.capitalize() in location.name:
            return kong
    raise ValueError(f"Location {location.name} does not have an associated Kong.")


# Populate battle arena locations in the PlandomizerPanels object.
for level, locations in CrownVanillaLocationMap.items():
    for crownLocation, vanillaLocation in locations.items():
        fullName = crownLocation.name.replace("Battle", " Battle ").replace("1", " 1").replace("2", " 2")
        PlandomizerPanels["Locations"]["categories"]["CrownPad"]["locations"].append(
            {
                "name": fullName,
                "level": level.name,
                "vanilla_value": vanillaLocation,
                "location_id": f"plando_{crownLocation.name}_location",
                "reward_id": f"plando_{crownLocation.name}_location_reward",
            }
        )
# Populate Kasplat locations in the PlandomizerPanels object.
for level, locations in KasplatLocationToRewardMap.items():
    for kasplatLocation, rewardLocation in locations.items():
        fullName = kasplatLocation.name.replace("Rando", "")
        for kong in ["Donkey", "Diddy", "Lanky", "Tiny", "Chunky"]:
            if kong in fullName:
                fullName = fullName.replace(kong, f" {kong} ")
        PlandomizerPanels["Locations"]["categories"]["Kasplat"]["locations"].append(
            {
                "name": fullName,
                "level": level.name,
                "kong": getKongFromLocationEnum(kasplatLocation).name,
                "vanilla_value": LocationList[rewardLocation].name,
                "location_id": f"plando_{kasplatLocation.name}_location",
                "reward_id": f"plando_{kasplatLocation.name}_location_reward",
            }
        )
# Populate dirt patch locations in the PlandomizerPanels object.
for i in range(0, 16):
    PlandomizerPanels["Locations"]["categories"]["DirtPatch"]["locations"].append(
        {
            "name": f"Dirt Patch {i+1}",
            "vanilla_value": "",
            "location_id": f"plando_patch_{i}_location",
            "reward_id": f"plando_patch_{i}_location_reward",
        }
    )
# Populate fairy locations in the PlandomizerPanels object.
fairyLevelCounts = {
    Levels.JungleJapes: 2,
    Levels.AngryAztec: 2,
    Levels.FranticFactory: 2,
    Levels.GloomyGalleon: 2,
    Levels.FungiForest: 2,
    Levels.CrystalCaves: 2,
    Levels.CreepyCastle: 2,
    Levels.DKIsles: 4,
    Levels.HideoutHelm: 2,
}
overallFairyCount = 0
for level, fairyLimit in fairyLevelCounts.items():
    for i in range(0, fairyLimit):
        PlandomizerPanels["Locations"]["categories"]["Fairy"]["locations"].append(
            {
                "name": f"{GetLevelString(level)} Fairy {i+1}",
                "level": level.name,
                "vanilla_value": "",
                "location_id": f"plando_fairy_{overallFairyCount}_location",
                "reward_id": f"plando_fairy_{overallFairyCount}_location_reward",
            }
        )
        overallFairyCount += 1
# Populate melon crate locations in the PlandomizerPanels object.
for i in range(0, 13):
    PlandomizerPanels["Locations"]["categories"]["MelonCrate"]["locations"].append(
        {
            "name": f"Melon Crate {i+1}",
            "vanilla_value": "",
            "location_id": f"plando_crate_{i}_location",
            "reward_id": f"plando_crate_{i}_location_reward",
        }
    )

currentVanillaCrateIndex = 0
currentVanillaDirtIndex = 0

for level, locations in CustomLocations.items():
    for customLocation in locations:
        jsonValue = f"{level.name};{customLocation.name}"
        if LocationTypes.CrownPad not in customLocation.banned_types:
            plannableCrownPads[level.name].append({"name": f"{GetLevelString(level)}: {customLocation.name}", "value": customLocation.name})
        if LocationTypes.DirtPatch not in customLocation.banned_types:
            if customLocation.vanilla_patch:
                PlandomizerPanels["Locations"]["categories"]["DirtPatch"]["locations"][currentVanillaDirtIndex]["vanilla_value"] = jsonValue
                DirtPatchVanillaLocationMap[f"patch_{currentVanillaDirtIndex}"] = jsonValue
                currentVanillaDirtIndex += 1
            plannableDirt.append({"name": f"{GetLevelString(level)}: {customLocation.name}", "value": jsonValue})
        if LocationTypes.MelonCrate not in customLocation.banned_types:
            if customLocation.vanilla_crate:
                PlandomizerPanels["Locations"]["categories"]["MelonCrate"]["locations"][currentVanillaCrateIndex]["vanilla_value"] = jsonValue
                MelonCrateVanillaLocationMap[f"crate_{currentVanillaCrateIndex}"] = jsonValue
                currentVanillaCrateIndex += 1
            plannableCrates.append({"name": f"{GetLevelString(level)}: {customLocation.name}", "value": jsonValue})
PlannableCustomLocations[LocationTypes.CrownPad.name] = plannableCrownPads
PlannableCustomLocations[LocationTypes.DirtPatch.name] = plannableDirt
PlannableCustomLocations[LocationTypes.MelonCrate.name] = plannableCrates

plannableFairies = {
    Levels.JungleJapes.name: [],
    Levels.AngryAztec.name: [],
    Levels.FranticFactory.name: [],
    Levels.GloomyGalleon.name: [],
    Levels.FungiForest.name: [],
    Levels.CrystalCaves.name: [],
    Levels.CreepyCastle.name: [],
    Levels.DKIsles.name: [],
    Levels.HideoutHelm.name: [],
}
currentVanillaFairyIndex = 0
for level, locations in fairy_locations.items():
    for customLocation in locations:
        jsonValue = f"{level.name};{customLocation.name}"
        if customLocation.is_vanilla:
            PlandomizerPanels["Locations"]["categories"]["Fairy"]["locations"][currentVanillaFairyIndex]["vanilla_value"] = jsonValue
            FairyVanillaLocationMap[f"fairy_{currentVanillaFairyIndex}"] = jsonValue
            currentVanillaFairyIndex += 1
        plannableFairies[level.name].append({"name": f"{GetLevelString(level)}: {customLocation.name}", "value": jsonValue})
PlannableCustomLocations[Types.Fairy.name] = plannableFairies

plannableKasplats = {
    Levels.JungleJapes.name: {
        Kongs.donkey.name: [],
        Kongs.diddy.name: [],
        Kongs.lanky.name: [],
        Kongs.tiny.name: [],
        Kongs.chunky.name: [],
    },
    Levels.AngryAztec.name: {
        Kongs.donkey.name: [],
        Kongs.diddy.name: [],
        Kongs.lanky.name: [],
        Kongs.tiny.name: [],
        Kongs.chunky.name: [],
    },
    Levels.FranticFactory.name: {
        Kongs.donkey.name: [],
        Kongs.diddy.name: [],
        Kongs.lanky.name: [],
        Kongs.tiny.name: [],
        Kongs.chunky.name: [],
    },
    Levels.GloomyGalleon.name: {
        Kongs.donkey.name: [],
        Kongs.diddy.name: [],
        Kongs.lanky.name: [],
        Kongs.tiny.name: [],
        Kongs.chunky.name: [],
    },
    Levels.FungiForest.name: {
        Kongs.donkey.name: [],
        Kongs.diddy.name: [],
        Kongs.lanky.name: [],
        Kongs.tiny.name: [],
        Kongs.chunky.name: [],
    },
    Levels.CrystalCaves.name: {
        Kongs.donkey.name: [],
        Kongs.diddy.name: [],
        Kongs.lanky.name: [],
        Kongs.tiny.name: [],
        Kongs.chunky.name: [],
    },
    Levels.CreepyCastle.name: {
        Kongs.donkey.name: [],
        Kongs.diddy.name: [],
        Kongs.lanky.name: [],
        Kongs.tiny.name: [],
        Kongs.chunky.name: [],
    },
    Levels.DKIsles.name: {
        Kongs.donkey.name: [],
        Kongs.diddy.name: [],
        Kongs.lanky.name: [],
        Kongs.tiny.name: [],
        Kongs.chunky.name: [],
    },
}
currentVanillaKasplatIndex = 0
for level, locations in KasplatLocationList.items():
    for customLocation in locations:
        for kong in [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]:
            if kong in customLocation.kong_lst:
                plannableKasplats[level.name][kong.name].append({"name": customLocation.name, "value": customLocation.name})
PlannableCustomLocations["Kasplat"] = plannableKasplats
