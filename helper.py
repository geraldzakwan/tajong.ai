from flask import jsonify

def reply_success(data):
    return jsonify({
        "data": data
    })

def reply_error(code, message):
    return jsonify({
        "error": {
            "code": code,
            "message": message
        }
    })
