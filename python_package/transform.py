import re
import json


class Transform(object):

    def __init__(self):
        pass

    def get_regex_from_html(self, regex, html):

        matches = re.findall(regex, html)
        matches = list(set(matches))

        return matches

    def convert_to_channel_link(self, list_of_channels):

        links_to_channels = []

        for link in list_of_channels:
            links_to_channels.append("www.youtube.com/c/" + link)

        return links_to_channels

    def list_of_dict_to_json(self, data, file_path):
        with open(file_path, "w") as file:
            for d in data:
                json.dump(d, file)
                file.write('\n')
