"""Functions used to support music selection."""
import itertools
import js
import json
import re

from randomizer.Enums.Songs import Songs
from randomizer.Lists.Songs import SongLocationList
from ui.bindings import bind
from ui.download import download_json_file

CUSTOM_PACK_NAME = "custom"


def is_custom_music_loaded() -> bool:
    """Return true if a custom music pack has been loaded."""
    return js.cosmetic_names is not None


def get_custom_song_map() -> dict:
    """Return a map between song categories and their relevant lists."""
    return {
        "bgm": zip(js.cosmetic_names.bgm, js.cosmetic_truncated_names.bgm),
        "majoritems": zip(js.cosmetic_names.majoritems, js.cosmetic_truncated_names.majoritems),
        "minoritems": zip(js.cosmetic_names.minoritems, js.cosmetic_truncated_names.minoritems),
        "events": zip(js.cosmetic_names.events, js.cosmetic_truncated_names.events),
    }


def update_custom_path_name(pathName: str, baseName: str) -> str:
    """Replace the first part of a custom path name with a new base name.
    
    E.g. update_custom_path_name("foo/bgm/song", "bar") -> "bar/bgm/song"
    """
    return f'{baseName}/{"/".join(pathName.split("/")[1:])}'


def serialize_music_selections(form: dict, for_file: bool = False) -> dict:
    """Serialize music selections into an enum-focused JSON object.

    Args:
        form (dict) - The form data of the page, in dictionary form.
        for_file (bool) - True if this data should be written out to a file.
            This will write out some values as strings instead of enums.
    Returns:
        dict: Dictionary of form settings.
    """
    def get_value(enum_val):
        """Return either the value of a given enum or the display name."""
        return enum_val.name if for_file else enum_val
    
    def is_music_select_input(inputName: str) -> bool:
        """Determine if an input is a song selection input."""
        return inputName is not None and inputName.startswith("music_select_")

    songs_map = {}
    for obj in form:
        if not is_music_select_input(obj.name):
            continue
        # Extract the location name.
        location_name = re.search("^music_select_(.+)$", obj.name)[1]
        location = get_value(Songs[location_name])
        if obj.value != "":
            # If this is an in-game song, use the enum value.
            try:
                songs_map[location] = get_value(Songs[obj.value])
            except KeyError:
                # If this is a custom song, find and use the full string path.
                bgm_map = zip(js.cosmetic_truncated_names.bgm, js.cosmetic_names.bgm)
                major_map = zip(js.cosmetic_truncated_names.majoritems, js.cosmetic_names.majoritems)
                minor_map = zip(js.cosmetic_truncated_names.minoritems, js.cosmetic_names.minoritems)
                event_map = zip(js.cosmetic_truncated_names.events, js.cosmetic_names.events)
                music_map = itertools.chain(bgm_map, major_map, minor_map, event_map)
                for truncated_name, path_name in music_map:
                    if obj.value == truncated_name:
                        final_path_name = path_name
                        if for_file:
                            final_path_name = update_custom_path_name(path_name, CUSTOM_PACK_NAME)
                        songs_map[location] = final_path_name
                        break
    return songs_map


def get_current_pack_name() -> str:
    """Gets the name of the currently loaded music pack, if there is one.
    
    This will either return the first time one of our lists is non-empty, or it
    will return None at the very end. It's a silly way to write a function, but
    jsProxy objects are hard to work with.
    """
    for song in js.cosmetic_names.bgm:
        return song.split("/")[0]
    for song in js.cosmetic_names.majoritems:
        return song.split("/")[0]
    for song in js.cosmetic_names.minoritems:
        return song.split("/")[0]
    for song in js.cosmetic_names.events:
        return song.split("/")[0]
    # No custom music has been loaded.
    return None


def update_custom_song_names(fileContents: dict) -> dict:
    """Update custom music with the name of the newest music zip file.
    
    This is to prevent an issue where the user uploads one music file, saves
    their selections to file, uploads a music pack with a new name, then tries
    to import the same file. So long as the songs are in the right place, with
    the right names, the name of the pack should be irrelevant.
    """
    currentPackName = get_current_pack_name()
    if not currentPackName:
        return fileContents
    musicData = {}
    for location, song in fileContents.items():
        pathName = song
        if song.startswith(CUSTOM_PACK_NAME):
            pathName = update_custom_path_name(song, currentPackName)
        musicData[location] = pathName
    return musicData


def raise_music_validation_error(errString: str) -> None:
    """Raise an error and display a message about an invalid music file."""
    musicErrorsElement = js.document.getElementById("music_import_errors")
    musicErrorsElement.innerText = errString
    musicErrorsElement.style = ""
    raise ValueError(errString)


def validate_music_location(locationName: str) -> None:
    """Ensure that a given location is a valid song location."""
    try:
        _ = Songs[locationName]
    except KeyError:
        errString = f'The music selection file is invalid: "{locationName}" is not a valid song location.'
        raise_music_validation_error(errString)


def validate_custom_song(songPath: str) -> None:
    """Ensure that a given song represents a currently loaded custom song."""
    # Check to see if the path is correctly formed.
    splitPath = songPath.split("/")
    if len(splitPath) != 3:
        errString = f'The music selection file is invalid: song name "{songPath}" is malformed.'
        raise_music_validation_error(errString)
    _, category, songName = splitPath
    # Check to see if the path has a valid category.
    if category not in ["bgm", "majoritems", "minoritems", "events"]:
        errString = f'The music selection file is invalid: song name "{songPath}" has an invalid category "{category}".'
        raise_music_validation_error(errString)
    # Check to see if any custom music has been loaded.
    if not is_custom_music_loaded():
        errString = f'The music selection file contains custom songs, but no custom songs have been loaded.'
        raise_music_validation_error(errString)
    
    # Search for the song in the currently loaded songs.
    customSongList = get_custom_song_map()[category]
    songFound = False
    for loadedSong, _ in customSongList:
        _, _, loadedSongName = loadedSong.split("/")
        if songName == loadedSongName:
            songFound = True
            break
    if not songFound:
        errString = f'The custom song "{songName}" is not in the currently loaded pack.'
        raise_music_validation_error(errString)


def validate_vanilla_song(songName: str) -> None:
    """Ensure that a given song represents a valid song from the base game."""
    try:
        _ = Songs[songName]
    except KeyError:
        errString = f'The music selection file is invalid: "{songName}" is not a valid song name.'
        raise_music_validation_error(errString)


def validate_music_file(fileContents: dict) -> None:
    """Ensure that the provided music file is valid and not malformed."""
    # Hide the div for import errors.
    musicErrorsElement = js.document.getElementById("music_import_errors")
    musicErrorsElement.style.display = "none"

    for location, song in fileContents.items():
        # Validate the location.
        validate_music_location(location)
        if "/" in song:
            validate_custom_song(song)
        else:
            validate_vanilla_song(song)


@bind("click", "import_music_selections")
def music_filebox(evt):
    """Open a file upload prompt and begin importing music selections."""
    input = js.document.createElement("input")
    input.type = "file"
    input.accept = ".json"

    input.onchange = lambda e: import_music_selections(e.target.files.item(0))

    input.click()


async def import_music_selections(file) -> None:
    """Imports music selections from a JSON file."""
    fileText = await file.text()
    fileContents = json.loads(fileText)

    # Inform the user their current settings will be erased.
    if not js.window.confirm("This will replace your current music selections. Continue?"):
        return

    # Ensure this is an actual valid music selections file.
    validate_music_file(fileContents)

    # Update the names of all custom songs to match the currently loaded pack.
    musicData = update_custom_song_names(fileContents)

    # Reset all of the music selections to their defaults.
    reset_music_selections_no_prompt()

    # Set all of the options specified in the music file.
    for location, songName in musicData.items():
        locationElem = js.document.getElementById(f"music_select_{location}")
        # If this is a custom song, find the matching select value.
        if "/" in songName:
            _, category, _ = songName.split("/")
            customSongList = get_custom_song_map()[category]
            for customSongName, customTruncatedName in customSongList:
                if songName == customSongName:
                    locationElem.value = customTruncatedName
                    break
        else:
            locationElem.value = songName

    js.savesettings()


@bind("click", "export_music_selections")
def export_music_selections(evt):
    """Save the current music selections to a JSON file."""
    form = js.jquery("#form").serializeArray()
    musicSelectData = serialize_music_selections(form, True)
    download_json_file(musicSelectData, "music_selections.json")


@bind("click", "reset_music_selections")
def reset_music_selections(evt):
    """Resets all music selection options to their default settings.

    Issues a prompt first, warning the user.
    """
    if js.window.confirm("Are you sure you want to reset all music selections?"):
        reset_music_selections_no_prompt()
        js.savesettings()


def reset_music_selections_no_prompt():
    """Resets all music selection options to their default settings."""
    for songLocation in SongLocationList:
        songElement = js.document.getElementById(f"music_select_{songLocation}")
        songElement.value = ""
