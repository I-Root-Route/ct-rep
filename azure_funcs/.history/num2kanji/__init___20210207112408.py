import logging

import azure.functions as func

from settings import settings


def split_to_chunks(number):
    chunks = []
    for i in range(0, len(str(number)), 4):
        temp = str(number)[::-1][i:i + 4]
        chunks.append(temp[::-1])

    return chunks[::-1]


def num_to_kanji_helper(chunk):
    kanji_chunk = ''
    for i, num in enumerate(chunk):
        if int(num) == 0:
            continue
        rank = settings.chunk_base[len(chunk) - i - 1]
        kanji_chunk += settings.kanjitable[int(num)] + rank

    return kanji_chunk


def num_to_kanji(num):
    try:
        assert 0 <= num <= 9999999999999999
        out = ""
        chunks = split_to_chunks(num)
        for i, chunk in enumerate(chunks):
            kanji_chunk = num_to_kanji_helper(chunk)
            out += kanji_chunk + settings.split_base[len(chunks)-i - 1]

        return out
    except Exception as e:
        return 204

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    num = req.route_params.get('num')

    
