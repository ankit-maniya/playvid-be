import json
import os
import metadata_parser
from pytube import YouTube

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .helper import add_ext, extract_bandcamp_video_data_from_url, extract_facebook_video_data_from_url, extract_moj_video_data_from_url, extract_video_data_from_url, get_arr_of_obj


class MusicApiView(APIView):
    """
    View to list all youtube in the system.

    * Requires token authentication.
    * Only admin youtube are able to access this view.
    """

    def post(self, request, format=None):
        """
        Return a list of all youtube videos/audio.
        """
        url = request.data.get("url")
        if url:
            yt = YouTube(url)
            iRes = yt.streaming_data
            thumbnail = yt.thumbnail_url
            title = yt.title
            iRes = add_ext(iRes)

            # Doownload Video From Youtube-DL
            # command = f'youtube-dl "{url}" -j'
            # output = os.popen(command).read()
            # video_data = json.loads(output)
            # iRes = extract_video_data_from_url(video_data)

            return Response({"thumbnail": thumbnail, "title": title, **iRes})
        return Response({"msg": "Please Provide Link"})

    @api_view(['post'])
    def get_facebook_videos(request, format=None):
        """
            Return a list of all users.
            Doownload Video From Youtube-DL
        """
        url = request.data.get("url")
        if url:

            # Fetch Metadata For Thumbnail & title
            page = metadata_parser.MetadataParser(
                url=url, search_head_only=True)

            fulltitle = page.get_metadatas(
                'title', strategy=['page', 'og', 'dc', ])
            thumbnail = page.get_metadata_link("image")

            # Run Cli Cmd for Get Facebook data
            command = f'youtube-dl "{url}" -j'
            output = os.popen(command).read()
            video_data = json.loads(output)

            iRes = extract_facebook_video_data_from_url(video_data)
            iRes["thumbnail"] = thumbnail
            iRes["title"] = fulltitle

            return Response(iRes)
        return Response({"msg": "Please Provide Link"})

    @api_view(['post'])
    def get_bandcamp_videos(request, format=None):
        """
            Return a list of all users.
            Doownload Video From Youtube-DL
        """
        url = request.data.get("url")
        if url:
            isTrack = "track" in url

            if isTrack:
                command = f'youtube-dl "{url}" -j'
                output = os.popen(command).read()
                video_data = json.loads(output)
                iRes = extract_bandcamp_video_data_from_url(video_data)

                return Response(iRes)

            isAlbum = "album" in url
            if isAlbum:
                command = f'youtube-dl "{url}" -j'
                output = os.popen(command).read()

                splitStr = output.split("}\n")

                video_data = get_arr_of_obj(splitStr)

                albumData = {
                    "thumbnail": video_data[0]["thumbnail"],
                    "uploader": video_data[0]["uploader"],
                    "artist": video_data[0]["artist"],
                    "playlist_title": video_data[0]["playlist_title"],
                    "album": video_data[0]["album"],
                }

                iRes = {**albumData, "all_videos": video_data}

                return Response(iRes)

            return Response({"msg": "Data Not Found!"})
        return Response({"msg": "Please Provide Link!"})

    @api_view(['post'])
    def get_moj_videos(request, format=None):
        """
            Return a list of all users.
            Doownload Video From Youtube-DL
        """
        url = request.data.get("url")
        if url:

            # Fetch Metadata For Thumbnail & title
            page = metadata_parser.MetadataParser(
                url=url, search_head_only=True)

            fulltitle = page.get_metadatas(
                'title', strategy=['page', 'og', 'dc', ])
            description = page.get_metadatas(
                'description', strategy=['page', 'og', 'dc', ])
            thumbnail = page.get_metadata_link("image")

            # Run Cli Cmd for Get Facebook data
            command = f'youtube-dl "{url}" -j'
            output = os.popen(command).read()
            video_data = json.loads(output)

            iRes = extract_moj_video_data_from_url(video_data)
            iRes["thumbnail"] = thumbnail
            iRes["title"] = fulltitle
            iRes["description"] = description

            return Response(iRes)
        return Response({"msg": "Please Provide Link"})