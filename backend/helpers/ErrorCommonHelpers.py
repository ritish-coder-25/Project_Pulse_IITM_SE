from flask import jsonify

def createError(errorCode: str, message: str, errorStatus: int) -> dict:
    return jsonify({"errorCode": errorCode, "message": message}), errorStatus

def createFatalError(errorCode: str, message: str, error: str) -> dict:
    return jsonify({"errorCode": errorCode, "message": message, "error": error}), 500
