import models
import datetime
from flask import Blueprint, jsonify, request
from flask_login import current_user
from playhouse.shortcuts import model_to_dict

medicine = Blueprint('medicines', 'medicine')

@medicine.route('/<user_id>', methods=['GET'])
def list_medicines(user_id):
    try:
        print('current user: {}'.format(user_id))
        query = models.Medicine.select().where(models.Medicine.user_id == user_id)
        print('query: {}'.format(query))
        # print('pull all: {}'.format([model_to_dict(d) for d in models.Medicine.select()]))
        medicines = [model_to_dict(d) for d in query]
        print('medicines 1: {}'.format(medicines))
        for medicine in medicines:
            medicine['user_id'] = current_user.id
        print('medicines 2: {}'.format(medicines))
        return jsonify(data=medicines, status={'code': 200, 'message': 'Success'})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 400, 'message': 'Error getting resource'})


@medicine.route('/save', methods=['POST'])
def save():
    payload = request.get_json()
    print('Payload recieved: {}'.format(payload))
    payload['user_id'] = current_user.id
    print("Edited payload: {}".format(payload))
    new_medicine = models.Medicine.create(**payload)

    new_medicine_dict = model_to_dict(new_medicine)
    print(new_medicine_dict)
    return jsonify(data=new_medicine_dict, status={'code': 201, 'message': 'Successfully saved'})
    # return 'saved'

# Delete saved medicine
@medicine.route('/<id>/', methods=['DELETE'])
def delete_medicine(id):
	query = models.Medicine.delete().where(models.Medicine.id==id)
	query.execute()
	return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})

# update time medicine was taken
@medicine.route('/update_time/<medicine_id>', methods=['PUT'])
def update_datetime(medicine_id):
    now = datetime.datetime.now()
    query = models.Medicine.update(
        last_taken=now
    ).where(models.Medicine.id == medicine_id).execute()
    updated_time_dict = model_to_dict(models.Medicine.get(id = medicine_id)) 
    print(updated_time_dict)
    return jsonify(data=updated_time_dict, status={'code': 200, 'message': 'successfully updated'})

# update saved medicine
@medicine.route('/update/<medicine_id>', methods=['PUT'])
def update_saved_medicine(medicine_id):
    payload = request.get_json()
    # print("payload: {}".format(payload))
    updated_medicine = models.Medicine.update(payload).where(models.Medicine.id == medicine_id).execute()
    # print('updated medicine: {}'.format(updated_medicine))
    updated_medicine_dict = model_to_dict(models.Medicine.get(id = medicine_id)) 
    # print('dict: {}'.format(updated_medicine_dict))
    # print('updated medicine dict: {}'.format(updated_medicine_dict))
    return jsonify(data=updated_medicine_dict, status={'code': 200, 'message': 'Update successful'})
    # return 'test'