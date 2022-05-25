import requests
import time
import matplotlib.pyplot as plt

def get_response(url):
    return requests.post(url,json={"msg":"no"})


def generate_requests(request_count):
    requests = ['http://localhost:5000/get_response']*request_count
    for r in requests:
        get_response(r)

def test_response():
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

def test_ner():
    import ner_handler
    names = ['Steven Johnson', 'Eldridge Copeland', 'Earl Rogge', 'Dora Espinoza', 'Michael Wentworth', 'Calvin Dillahunt', 'Leona Acevedo', 'Emma Erlewine', 'Brandon Sample', 'Carl Hoffman', 'Marjorie Vandiver', 'Troy Adam', 'Nickolas Marine', 'Peter Mosley', 'Arlene Dupre', 'Kristopher Dube', 'Robert Emery', 'David Borkowski', 'Kevin Bontrager', 'Serafina Davies', 'Mary Stults', 'Katherine Todd', 'Betty Jewell', 'Anna Harper', 'Larry Black', 'Wanda Reier', 'Thelma Herring', 'Mark Vasquez', 'Gary Hills', 'Chad Parisi', 'Mark Moore', 'Charlie Mckinsey', 'Jeanne Null', 'Sue Escobar', 'Theodore Situ', 'Joan Dickman', 'Andrew Wicker', 'Billy Audet', 'Joyce Parker', 'Christina Haslam', 'James Schlau', 'Kimberly Mullen', 'William Alvarado', 'Nicole Godwin', 'William Black', 'Vivian Wozny', 'Libby Porter', 'Frederick Thomas', 'Otto Natera', 'Diego Owens', 'Carey Medina', 'Michael Lopez', 'Rosanne Luckenbach', 'Myrna Vega', 'Lawrence Weil', 'James Tracy', 'Dennis Trujillo', 'Socorro White', 'Adrian Tobler', 'Crystal Herzog', 'Mario Hamilton', 'Ronnie Watkins', 'Julianne Greenler', 'Tammera Cataldo', 'Lashanda Bowers', 'Barry Garcia', 'Madelaine Dasilva', 'Jeffrey Newman', 'Bennett Hawke', 'David Snyder', 'Peter Mcclary', 'David Lopez', 'Debbie Sheehan', 'Marilyn Fee', 'Betty Durbin', 'George Wall', 'Garrett Rathbun', 'Angelo Cruse', 'James Pless', 'Linda Eikenberry', 'Kali Woolery', 'Carol Rodgers', 'Wendy Guidry', 'Lorinda Stover', 'Gayla Barker', 'Katherine George', 'Kathryn Boyd', 'Megan Strong', 'Jennifer Whiting', 'Miriam Smith', 'Maria Haskell', 'Jennifer Hulburt', 'Mayra Kina', 'Gary Hor', 'Christopher Tolle', 'Alton Goetz', 'Manuel Mcquaig', 'Steven Lancaster', 'Natalie Roderick', 'Doris Tarver']
    counter = 0
    for n in names:
        if len(ner_handler.get_entity(n, "PERSON")) ==1:
            counter+=1
    print(counter/len(names))

test_ner()
test_response()