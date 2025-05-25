from rest_framework.parsers import BaseParser


class TextParser(BaseParser):
    media_type = 'text/plain; charset=utf-8'

    def parse(self, stream, media_type=None, parser_context=None):
        return stream.read()


class JSONUTF8Parser(BaseParser):
    media_type = 'application/json; charset=utf-8'

    def parse(self, stream, media_type=None, parser_context=None):
        return stream.read()
