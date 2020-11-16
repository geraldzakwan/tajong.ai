from flask import jsonify

def reply_success(data):
    response = jsonify({
        "data": data
    })
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

def reply_error(code, message):
    response = jsonify({
        "error": {
            "code": code,
            "message": message
        }
    })
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
