import logging
import json
from typing import List, Tuple

import azure.functions as func

from settings import settings


class K2N(object):
    @staticmethod
    def check_kanji(kanji_num: str) -> bool:
        # 大字表記のはじめは必ずsettings.baseにあるべき。
        # 例) 拾は認めず、壱拾は認める
        if kanji_num[0] not in settings.base:
            return False

        temp = None
        for i, kanji in enumerate(kanji_num):
            if temp is None:
                temp = kanji
                continue
            # 壱参などの形は認めない
            if temp[-1] in settings.base and kanji in settings.base:
                return False
            else:
                temp += kanji
        return True

    def split_to_chunks(self, kanji_num: str, temp='', overall=None, max_exp=None) -> List[Tuple[str]]:
        # [("四百参拾弐", "兆"), ("四千参百弐拾七", "億").....]
        # のような四つ区切りで出てくる位(万、億、兆)とそれ以外で分ける。
        if overall is None:
            overall = []

        if max_exp is None:
            max_exp = float('inf')

        if not kanji_num:
            return overall

        for i, kanji in enumerate(kanji_num):
            if kanji not in settings.exp_base:
                temp += kanji
                if i == len(kanji_num) - 1:
                    overall.append((temp if temp else None, None))
                    return overall
            else:
                assert max_exp > settings.num_table[kanji]  # 壱兆参千「万」七「兆」のような形を受け付けない
                overall.append((temp if temp else None, kanji))
                return self.split_to_chunks(kanji_num[i + 1:], temp='', overall=overall,
                                            max_exp=settings.num_table[kanji])

    @staticmethod
    def kanji_to_num_helper(base: str) -> int:
        # チャンクごとに漢数字をアラビア数字に変換する
        base_num = 0
        temp = 0
        max_chunk_base = 0
        for i, kanji in enumerate(base):
            if kanji not in settings.exp:
                temp += settings.num_table[kanji]
                if i == len(base) - 1:
                    base_num += temp
                    return base_num
            else:
                char_num = settings.num_table[kanji]
                if char_num in settings.chunk_base:
                    temp_max = max_chunk_base
                    max_chunk_base = max(max_chunk_base, char_num)
                temp *= char_num
                base_num += temp
                temp = 0

        return base_num

    def kanji_to_num(self, kanji_num: str) -> int:
        if not self.check_kanji(kanji_num):
            raise ValueError

        num = 0
        chunks = self.split_to_chunks(kanji_num)
        for chunk in chunks:
            base = chunk[0]
            exp_base_num = settings.num_table[chunk[1]] if chunk[1] is not None else 1
            base_num = self.kanji_to_num_helper(base)
            num += base_num * exp_base_num

        return num


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    code = 200
    message = None

    try:
        k2n = K2N()
        kanji = req.route_params.get('kanji')
        num = k2n.kanji_to_num(kanji)
        message = str(num)
    except ValueError:
        code = 204
    except Exception:
        code = 204
    finally:
        if message:
            return func.HttpResponse(json.dumps(int(message)), status_code=code)
        else:
            return func.HttpResponse(status_code=code)
