import os
import json


def extrect_formate_data(formate_data):
    url = formate_data["url"]
    format = formate_data["format"]
    ext = formate_data["ext"]

    orignal_formate = ["video"]
    if (formate_data.get("format_note")):
        orignal_formate = formate_data["format_note"]

    filesize = 0
    if (formate_data.get("filesize")):
        filesize = formate_data["filesize"] / 1000000

    return {
        "url": url,
        "ext": ext,
        "orignal_formate": orignal_formate,
        "filesize": filesize,
        "format": format
    }


def extract_video_data_from_url(video_data):
    title = video_data["title"]
    formats = video_data["formats"]
    thumbnails = video_data["thumbnails"][-1]
    all_formats = [extrect_formate_data(
        formate_data) for formate_data in formats]

    return {
        "formats": all_formats,
        "thumbnails": thumbnails,
        "title": title
    }


def formate_ext(mimetype):
    ext = mimetype.split(";", 1)[0]
    if (ext):
        ext = ext.split("/")

    return ext


def add_ext(data):
    newFormats = []
    newAdaptiveFormats = []
    formats = data["formats"]
    adaptiveFormats = data["adaptiveFormats"]

    for y in formats:
        ext1 = formate_ext(y["mimeType"])
        # size = int(y["contentLength"]) / 1000000
        newFormats.append({**y,  "ext": ext1})

    for x in adaptiveFormats:
        ext = formate_ext(x["mimeType"])
        # size = int(x["contentLength"]) / 1000000
        newAdaptiveFormats.append({**x,  "ext": ext})

    return {
        "formats": newFormats,
        "adaptiveFormats": newAdaptiveFormats
    }


def extract_facebook_video_data_from_url(video_data):
    formats = video_data["formats"]
    all_formats = [
        formate_data for formate_data in formats if formate_data.get("format_id") in ["sd", "hd"]]
    # result = [number for number in numbers if number > 5]
    # [function(number) for number in numbers if condition(number)]

    return {
        "formats": all_formats,
    }


def extract_moj_video_data_from_url(formate_data):
    url = formate_data["url"]
    format = formate_data["format"]
    ext = formate_data["ext"]

    orignal_formate = ["video"]
    filesize = 0
    if (formate_data.get("filesize")):
        filesize = formate_data["filesize"] / 1000000

    return {
        "url": url,
        "ext": ext,
        "orignal_formate": orignal_formate,
        "filesize": filesize,
        "format": format
    }


def extract_bandcamp_video_data_from_url(video_data):
    return {
        "id": video_data["id"],
        "uploader": video_data["uploader"],
        "artist": video_data["artist"],
        "url": video_data["url"],
        "album": video_data["album"],
        "fulltitle": video_data["fulltitle"],
        "title": video_data["title"],
        "format": video_data["format"],
        "thumbnail": video_data["thumbnail"],
        "track": video_data["track"],
        "ext": video_data["ext"],
        "timestamp": video_data["timestamp"],
        "duration": video_data["duration"],
    }


def get_arr_of_obj(array):
    iResponse = []

    for data in array:
        if data:
            updatedStr = data+"}"
            output = json.loads(updatedStr)
            # formateObj = extract_bandcamp_video_data_from_url(output) #It is taking too much time that's why I ignore filtering data
            iResponse.append(output)

    return iResponse
