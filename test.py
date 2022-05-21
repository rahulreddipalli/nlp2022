import requests

data={"msg":"Hello how are you?"}
response = requests.post('http://localhost:5000/get_response',json=data)
print(response.text)