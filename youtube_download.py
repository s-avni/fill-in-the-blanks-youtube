import urllib

import youtube_dl


class YDLWrapper:
    def __init__(self, yt_link):
        ydl_opts = {"skip_download": True,
                    "writesubtitles": True,
                    "writeautomaticsub": True,
                    }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(yt_link, download=False)
        self.info = info
        self.yt_link = yt_link

    def get_link(self):
        return self.yt_link

    def get_title(self):
        return self.info['title']

    def list_available_captions(self):
        return list(self.info["subtitles"].keys())

    def list_automatic_captions(self):
        return list(self.info["automatic_captions"].keys())

    def download_captions(self, lang_initials):
        print("lang initials")
        print(lang_initials)

        #manually created subtitles
        if lang_initials in self.info["subtitles"]:
            desired_subtitles_link = self.info["subtitles"][lang_initials][1]['url']
            print(desired_subtitles_link)
        #automatically generated subtitles
        elif lang_initials in self.info["automatic_captions"]:
            desired_subtitles_link = self.info["automatic_captions"][lang_initials][0]['url']
            print(desired_subtitles_link)
        else:
            raise ValueError("no matching subittiles")

        opener = urllib.request.FancyURLopener({})
        with opener.open(desired_subtitles_link) as f:
            content = f.read().decode('utf-8')
        content = content.splitlines()
        return content

# if __name__ == "__main__":
#     download_captions("")

# def youtube_download_subs(yt_link, lang_initials):
#     '''
#     @summary: returns original caption file and video title
#     '''
#
#     ydl_opts = {"skip_download": True,
#                 "writesubtitles": True}
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(yt_link, download=False)
#         title = info['title']
#         subtitle_dict = info["subtitles"]
#         # get the plain link of subtitles
#         desired_subtitles_link = subtitle_dict[lang_initials][1]['url']
#         print(desired_subtitles_link)
#
#         opener = urllib.request.FancyURLopener({})
#         with opener.open(desired_subtitles_link) as f:
#             content = f.read().decode('utf-8')
#         content = content.splitlines()
#
#     return title, content
