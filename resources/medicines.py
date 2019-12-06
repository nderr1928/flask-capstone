import models
from flask import Blueprint, jsonify, request
from flask_login import current_user
from playhouse.shortcuts import model_to_dict

medicine = Blueprint('medicines', 'medicine')

@medicine.route('/save', methods=['POST'])
def save():
    payload = request.get_json()
    print(payload)
    new_medicine = models.Medicine.create(**payload)

    new_medicine_dict = models_to_dict(new_medicine)
    print(new_medicine_dict)
    return jsoify(new_medicine_dict)