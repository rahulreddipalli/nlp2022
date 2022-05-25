from concurrent.futures import ThreadPoolExecutor
import requests
import time
import matplotlib.pyplot as plt

def get_response(url):
    return requests.post(url,json={"msg":"no"})


def generate_requests(request_count):
    requests = ['http://localhost:5000/get_response']*request_count
    for r in requests:
        get_response(r)

requests.post('http://localhost:5000/start_greeting',json={})
requests.post('http://localhost:5000/get_response',json={"msg":"yes"})
requests.post('http://localhost:5000/get_response',json={"msg":"Harry Potter"})
request_count = [1,5,10,20]
end_l = []
for x in request_count:
    start = time.perf_counter()
    generate_requests(x)
    end = time.perf_counter()-start
    end_l.append(end)

plt.plot(request_count, end_l)
plt.xlabel('Number of requests')
plt.ylabel('Time (secs)')
plt.title('Testing Speed of request and response')
plt.show()

