import json
import re
import html

def to_json(obj):
    return json.dumps(obj, separators=(',', ':'), ensure_ascii=True)


def response_to_json_or_text(response):
    text = response.text
    try:
        if response.headers['content-type'].startswith('application/json'):
            return json.loads(text)
    except KeyError:
        # $ Thanks Cloudflare
        pass
    return text


_HTML_TAGS_ = re.compile("<[^<]*>")
def HTML_parse(text, replace=""):
    text = text.replace("\n", "")
    text = html.unescape(text)
    text = re.sub(_HTML_TAGS_, replace, text)
    return text