"""Update wrinkly hints compressed file."""
import random
from io import BytesIO

import js
from randomizer.Lists.WrinklyHints import HintLocation, hints
from randomizer.Patching.Patcher import ROM
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Translations import Translations
from randomizer.Lists.Translations import TranslationDB, TranslationInfo


def writeWrinklyHints(file_start_offset, text):
    """Write the text to ROM."""
    ROM().seek(file_start_offset)
    ROM().writeMultipleBytes(len(text), 1)
    position = 0
    offset = 1
    for textbox in text:
        ROM().seek(file_start_offset + offset)
        ROM().writeMultipleBytes(1, 1)
        ROM().seek(file_start_offset + offset + 1)
        ROM().writeMultipleBytes(1, 1)
        ROM().seek(file_start_offset + offset + 2)
        ROM().writeMultipleBytes(len(textbox), 1)
        offset += 3
        for string in textbox:
            ROM().seek(file_start_offset + offset)
            ROM().writeMultipleBytes(position, 4)
            ROM().seek(file_start_offset + offset + 4)
            ROM().writeMultipleBytes(len(string), 2)
            ROM().seek(file_start_offset + offset + 6)
            ROM().writeMultipleBytes(0, 2)
            offset += 8
            position += len(string)
        ROM().seek(file_start_offset + offset)
        ROM().writeMultipleBytes(0, 4)
        offset += 4
    ROM().seek(file_start_offset + offset)
    ROM().writeMultipleBytes(position, 2)
    offset += 2
    for textbox in text:
        for string in textbox:
            for x in range(len(string)):
                ROM().seek(file_start_offset + offset + x)
                ROM().writeMultipleBytes(int.from_bytes(string[x].encode("ascii"), "big"), 1)
            offset += len(string)


def UpdateHint(WrinklyHint: HintLocation, message: str):
    """Update the wrinkly hint with the new string.

    Args:
        WrinklyHint (Hint): Wrinkly hint object.
        message (str): Hint message to write.
    """
    # Seek to the wrinkly data
    if len(message) <= 914:
        # We're safely below the character limit
        WrinklyHint.hint = message
        return True
    else:
        raise Exception("Hint message is longer than allowed.")
    return False


def updateRandomHint(message: str, kongs_req=[], keywords=[], levels=[]):
    """Update a random hint with the string specifed.

    Args:
        message (str): Hint message to write.
    """
    hint_pool = []
    for x in range(len(hints)):
        if hints[x].hint == "" and hints[x].kong in kongs_req and hints[x].level in levels:
            is_banned = False
            for banned in hints[x].banned_keywords:
                if banned in keywords:
                    is_banned = True
            if not is_banned:
                hint_pool.append(x)
    if len(hint_pool) > 0:
        selected = random.choice(hint_pool)
        return UpdateHint(hints[selected], message)
    return False


def PushHints():
    """Update the ROM with all hints."""
    hint_arr = []
    for wrinkly_hint in hints:
        replacement_hint = wrinkly_hint.hint
        if replacement_hint == "":
            replacement_hint = "PLACEHOLDER HINT"
        hint_arr.append([replacement_hint.upper()])
    writeWrinklyHints(js.pointer_addresses[12]["entries"][41]["pointing_to"], hint_arr)


def wipeHints():
    """Wipe the hint block."""
    for x in range(len(hints)):
        if hints[x].kong != Kongs.any:
            hints[x].hint = ""


def ConvertHint(translation_entry: Translations, params: list) -> str:
    """Convert a text entry based on a translation with optional parameters."""
    param_index = 0
    language = TranslationInfo["language_name"]
    text_entry = TranslationDB[translation_entry][language]
    if len(text_entry) == 1:
        return text_entry[0]
    elif len(text_entry) > 1:
        text = ""
        for subtext in text_entry:
            if subtext == "~":  # Param character
                text += str(params[param_index])
                param_index += 1
            else:
                text += str(subtext)
        return text
    return ""
