import logging

import azure.functions as func

from settings import settings

def check_kanji(kanji_num):
    temp = None
    for kanji in kanji_num:
        if temp is None:
            temp = kanji
            continue
        if temp[-1] in settings.base and kanji in settings.base:
            return False
        else:
            temp += kanji
    return True


def split_to_chunks(kanji_num: str, temp='', overall=None):
    if overall is None:
        overall = []

    if not kanji_num:
        return overall

    for i, kanji in enumerate(kanji_num):
        if kanji not in settings.exp_base:
            temp += kanji
            if i == len(kanji_num) - 1:
                overall.append((temp if temp else None, None))
                return overall
        else:
            overall.append((temp if temp else None, kanji))
            return split_to_chunks(kanji_num[i + 1:], temp='', overall=overall)


def kanji_to_num_helper(base):
    base_num = 0
    temp = 0
    for i, kanji in enumerate(base):
        if kanji not in settings.exp:
            temp += settings.num_table[kanji]
            if i == len(base) - 1:
                base_num += temp
                return base_num
        else:
            temp *= settings.num_table[kanji]
            base_num += temp
            temp = 0

    return base_num


def kanji_to_num(kanji_num):
    if not check_kanji(kanji_num):
        return 204

    try:
        num = 0
        chunks = split_to_chunks(kanji_num)
        for chunk in chunks:
            base = chunk[0]
            exp_base_num = settings.num_table[chunk[1]] if chunk[1] is not None else 1
            base_num = kanji_to_num_helper(base)
            num += base_num * exp_base_num

        return num
    except Exception as e:
        return 204


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    kanji = req.route_params.get('kanji')
    code = 200
    res = {}
    if not kanji:
        res["message"] = "漢数字を指定してください"
        return func.HttpResponse(res)

    return func.HttpResponse("YO")
    
    
