import requests
import json

HASHSTAX_STORAGE_URL = "https://hackathon.dltstax.net/projects/DiamondsChain/contexts/DiamondsChain/storage"
GET_REQUEST_SUCCESS_CODE = 200
POST_REQUEST_SUCCESS_CODE = 201

def get_storage(passphrase):
	request_result = requests.get(HASHSTAX_STORAGE_URL, 
		headers = { 
			"Originator-Ref": passphrase,
			"accept": "application/json"
		}
	)
	handle_request_error(request_result, GET_REQUEST_SUCCESS_CODE)
	return request_result.content

def post_storage(passphrase, storage_data):
	request_result = requests.post(HASHSTAX_STORAGE_URL, headers = 
		{ 
			"Originator-Ref": passphrase,
			"Content-Type": "application/json"
		},
		data=json.dumps(storage_data)
	)
	handle_request_error(request_result, POST_REQUEST_SUCCESS_CODE)

	return request_result.content

def handle_request_error(failed_request, success_code):
	if (int(failed_request.status_code) != success_code):
		raise Exception('Request FAILED, Status: {}\nContent:\n{}'
			.format(failed_request.status_code, failed_request.reason))

'''
# Tests
if __name__ == '__main__':
	print(post_storage('test_storage_object', {
			'user_id': 'test_user_id',
			'start_location': '56\'',
			'stop_location': '12\'',
			'status': 'COMPLETED',
			'request_timestamp': '2017-01-01 12:00:00'
		}))
	print(get_storage('test_storage_object'))
'''