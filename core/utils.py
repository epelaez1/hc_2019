#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import linecache
import re
import hashlib
from unicodedata import normalize
from core.logger import PersonalLogger


class utils(object):
    def __init__(self):
        pass

    @staticmethod
    def get_embedded_urls(text):
        url_pattern = re.compile("(?P<url>https?://[^\s]+)")
        embedded_urls = url_pattern.findall(text)
        return embedded_urls

    @staticmethod
    def print_exception() -> dict:
        """Function 'print_exception'.
            Get the error message, line and file
        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:

        Returns:
            dict successful, None otherwise.

        """
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        ret = {
            'type': "exception",
            'file_name': filename,
            'line': lineno,
            'expresion': line.strip(),
            'error': exc_obj
        }
        PersonalLogger.error(msg=ret)
        return ret

    @staticmethod
    def chunks(list, chunk_size):
        PersonalLogger.debug(
            msg="Splitting a list of {0} elements lists of {1} elements".format(
                len(list),
                chunk_size
            ))
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(list), chunk_size):
            yield list[i:i + chunk_size]

    @staticmethod
    def make_readable(text: str) -> str:
        no_composed_letters = {
            "Æ": "ae",
            "Ð": "d",
            "Ø": "o",
            "Þ": "b",
            "ß": "b",
            "æ": "ae",
            "ð": "d",
            "ø": "o",
            "þ": "b",
            "Œ": "oe",
            "œ": "oe",
            "ƒ": "f"
        }
        for special_letter, ascii_letter in no_composed_letters.items():
            text = text.replace(special_letter, ascii_letter)
        text = normalize("NFKC", text).encode(
            "utf-8", "ignore").decode("utf-8")
        text = normalize("NFD", text).encode("ascii", "ignore").decode("utf-8")
        text = re.sub('[^a-zA-Z0-9ñÑáÁéÉíÍóÓúÚçã\n ]', '', text)
        text = text.replace("\n"," ")
        text = re.sub(' +', ' ', text)
        text = text.lower()
        text = text.lstrip()
        text = text.rstrip()

        return text

    @staticmethod
    def calculate_hash(url):
        aux = hashlib.sha224()
        aux.update(url.encode('utf-8'))
        return aux.hexdigest()
