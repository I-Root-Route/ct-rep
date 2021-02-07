import logging
import json
from typing import List

import azure.functions as func

from settings import settings


class N2K(object):
    @staticmethod
    def split_to_chunks(number: int) -> List[str]:
        # 上から4つづつの塊に分ける
        chunks = []
        for i in range(0, len(str(number)), 4):
            temp = str(number)[::-1][i:i + 4]
            chunks.append(temp[::-1])

        return chunks[::-1]

    @staticmethod
    def num_to_kanji_helper(chunk: str) -> str:
        kanji_chunk = ''
        for i, num in enumerate(chunk):
            if int(num) == 0:
                continue
            rank = settings.chunk_base[len(chunk) - i - 1]
            kanji_chunk += settings.kanjitable[int(num)] + rank

        return kanji_chunk

    def num_to_kanji(self, num: int) -> str:
        assert 0 <= num <= 9999999999999999
        if 0 <= num <= 10:
            return settings.kanjitable[num]
        out = ""
        chunks = self.split_to_chunks(num)
        for i, chunk in enumerate(chunks):
            kanji_chunk = self.num_to_kanji_helper(chunk)
            out += kanji_chunk + settings.split_base[len(chunks) - i - 1] if kanji_chunk else ''

        return out


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    code = 200
    message = None

    try:
        n2k = N2K()
        num = int(req.route_params.get('num'))
        kanji_num = n2k.num_to_kanji(num)
        message = kanji_num
    except ValueError:
        code = 204
    except Exception:
        code = 204
    finally:
        if message:
            return func.HttpResponse(json.dumps(message), status_code=code)
        else:
            return func.HttpResponse(status_code=code)
