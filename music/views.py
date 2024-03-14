import metadata_parser
import ssl
from pytube import YouTube

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .helper import add_ext, extract_bandcamp_video_data_from_url, extract_facebook_video_data_from_url, extract_all_type_video_data, extract_video_data_from_url, fetch_platform_data, get_arr_of_obj


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
        ssl._create_default_https_context = ssl._create_stdlib_context
        url = request.data.get("url")
        if url:
            yt = YouTube(url)
            iRes = yt.streaming_data
            thumbnail = yt.thumbnail_url
            title = yt.title
            iRes = add_ext(iRes)

            # Doownload Video From Youtube-DL #in this lib we can not get all list
            # video_data = fetch_platform_data(url, load_json=True)

            return Response({"thumbnail": thumbnail, "title": title, **iRes})
        return Response({"msg": "Please Provide Link"})

    def get(self, request, format=None):
        """
        Return a test message.
        """
        return Response({"Test": "Api Working Fine!"})

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

            # Make Api Call
            video_data = fetch_platform_data(url, load_json=True)

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
                # Make Api Call
                video_data = fetch_platform_data(url, load_json=True)
                iRes = extract_bandcamp_video_data_from_url(video_data)

                return Response(iRes)

            isAlbum = "album" in url
            if isAlbum:
                # Make Api Call
                output = fetch_platform_data(url, load_json=False)

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
    def get_all_type_videos(request, format=None):
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

            # Make Api Call
            video_data = fetch_platform_data(url, load_json=True)

            iRes = extract_all_type_video_data(video_data)
            iRes["thumbnail"] = thumbnail
            iRes["title"] = fulltitle
            iRes["description"] = description

            return Response(iRes)
        return Response({"msg": "Please Provide Link"})
