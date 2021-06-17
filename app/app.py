try:    
    from flask import Flask, json, make_response           
    from mts import MTS
    from key import _app_debug
except ModuleNotFoundError as e:
    print("Missing required library:- "+str(e))

# app
app = Flask(__name__)

# Json Dump
def jd(obj):
    return json.dumps(obj)

# Response
def response(data={}, code=200):
    resp = {
        "code": code,
        "data": data
    }
    response = make_response(jd(resp))
    response.headers['Status-Code'] = resp['code']
    response.headers['Content-Type'] = "application/json"
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

""" APP APIs
    text: imput text
    lang: Tragat language
    inter_lang: intermdeiate langugae for translation
Returns:
    Json response
"""
@app.route('/<text>', methods=['GET', 'POST'])
@app.route('/<text>/<lang>', methods=['GET', 'POST'])
@app.route('/<text>/<lang>/<inter_lang>', methods=['GET', 'POST'])
def scatterchart(text, lang='en', inter_lang='hi'):
    _mts = MTS()
    output_text = _mts.translate(text, lang, inter_lang)
    return response({"text":text, "output": output_text, "lang": lang, "intermediate_lang": inter_lang})

# Error handing
@app.errorhandler(404)
def page_not_found(error):
    return response({}, 404)

# Driver Method
if __name__ == '__main__':
    app.run(port=5000, debug=_app_debug)