from flask import Blueprint, jsonify, request

accounts_bp = Blueprint("accounts", __name__)

accounts = {}
next_id = 1


@accounts_bp.route("/accounts", methods=["POST"])
def create_account():
    global next_id
    data = request.get_json(silent=True) or {}

    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "name and email are required"}), 400

    account = {
        "id": next_id,
        "name": data["name"],
        "email": data["email"],
        "address": data.get("address", ""),
        "phone_number": data.get("phone_number", ""),
    }
    accounts[next_id] = account
    next_id += 1
    return jsonify(account), 201


@accounts_bp.route("/accounts", methods=["GET"])
def list_accounts():
    return jsonify(list(accounts.values())), 200


@accounts_bp.route("/accounts/<int:account_id>", methods=["GET"])
def read_account(account_id):
    account = accounts.get(account_id)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    return jsonify(account), 200


@accounts_bp.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    account = accounts.get(account_id)
    if account is None:
        return jsonify({"error": "Account not found"}), 404

    data = request.get_json(silent=True) or {}
    for field in ("name", "email", "address", "phone_number"):
        if field in data:
            account[field] = data[field]

    return jsonify(account), 200


@accounts_bp.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    if account_id not in accounts:
        return jsonify({"error": "Account not found"}), 404

    del accounts[account_id]
    return "", 204
