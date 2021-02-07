import logging

import azure.functions as func

from settings import settings


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    kanji = req.route_params.get('kanji')
    code = 200
    res = {}
    if not kanji:
        res["message"] = "漢数字を指定してください"
        return func.HttpResponse(res)

    return func.HttpResponse(kanji)
    
    
