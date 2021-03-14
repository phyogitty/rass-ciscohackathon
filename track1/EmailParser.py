import os
import re
import time
import base64
import codecs
import unicodedata
from bs4 import BeautifulSoup


# Code Referenced from https://www.thepythoncode.com/article/use-gmail-api-in-python
class EmailParser:
    def __init__(self):
        print()

    # Email parsing
    # message = service.users().messages().get(userId='me', id=NONE, format='full').execute()
    def read_message(self, message):
        payload = message["payload"]
        headers = payload.get("headers")
        parts = payload.get("parts")
        folder = "html"

        buffer = {"labelIds": [], "date": 0, "from": 0, "to": 0, "subject": 0, "body": 0}
        buffer["labelIds"] += message.get("labelIds")
        if headers:
            for header in headers:
                if header.get("name") == 'From':
                    buffer['from'] = header.get("value")
                elif header.get("name") == 'To':
                    buffer['to'] = header.get("value")
                elif header.get("name") == 'Subject':
                    buffer['subject'] = header.get("value")
                elif header.get("name") == 'Date':
                    buffer['date'] = header.get("value")
        buffer['body'] = self.parse_parts(parts, folder)
        return buffer

    def parse_parts(self, parts, folder):
        output = []
        filled = False
        if parts:
            for part in parts:
                mimetype = part.get("mimeType")
                data = part.get("body").get("data")
                filename = part.get("filename") + str(int(time.time()))
                plain = ""
                parsed = ""
                unreadable = 0

                """
                if part.get("parts"):
                    output.append(self.parse_parts(part.get("parts"), folder))
                """
                if mimetype == "text/plain" and data is not None:
                    plain = base64.urlsafe_b64decode(data + "===").decode()
                elif mimetype == "text/html":
                    if not filename:
                        filename = "index" + str(int(time.time())) + ".html"
                    filepath = os.path.join(folder, filename)
                    # Download the html for parsing
                    with open(filepath, "wb") as f:
                        f.write(base64.urlsafe_b64decode(data + "==="))
                    with codecs.open(filepath, 'r', encoding="utf-8", errors="ignore") as f:
                        raw_html = f.read()
                    os.remove(filepath)
                    html = BeautifulSoup(raw_html, 'html.parser')
                    for tag in html.findAll('a', href=True):
                        tag.extract()
                    parsed = unicodedata.normalize("NFKD", html.get_text())
                    parsed = re.sub(r'\n+', '\n', parsed)
                    parsed = re.sub(r'\t+', '\t', parsed)
                    parsed = re.sub(r'\r+', '\r', parsed)
                else:
                    unreadable += 1

            # Prioritize parsed html, parsing gives more control
            if parsed:
                output.append(parsed)
            if plain and not parsed:
                output.append(plain)
            for i in range(unreadable):
                output.append("UNRECOGNIZED")
        return ",".join(output)

    # Utility Functions
    def get_size_format(self, bytes, factor=1024, suffix="B"):
        """
        Scale bytes to proper format (Ex: 1253656 => 1.20MB)
        :param bytes:
        :param factor:
        :param suffix:
        :return:
        """
        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor
        return f"{bytes:.2f}Y{suffix}"

    def clean(self, text):
        return "".join(c if c.isalnum() else "_" for c in text)
