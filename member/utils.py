# -*- coding: utf-8 -*-
from django.utils import simplejson as json
from django.http import HttpResponse


def iframe_jsonify(*args, **kwargs):
    if len(args) == 1:
        content = json.dumps(args[0])
    else:
        content = json.dumps(dict(*args, **kwargs))

    response = HttpResponse(content=content, mimetype="text/html")
    response['Cache-Control'] = 'no-cache'

    return response


def errors_to_json(errors):
    return dict(
        (k, map(unicode, v))
        for (k, v) in errors.iteritems()
    )


