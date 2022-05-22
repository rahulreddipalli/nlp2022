import random as rand
intents = ["greeting","goodbye","view_entry","add_entry"]
responses = {i:[] for i in intents}

responses["greeting"].append("Hi {} how are you?")
responses["greeting"].append("Hola {}")

responses["goodbye"].append("Goodbye {}")
responses["goodbye"].append("See ya later {}")
def get_intent(user_input):
    return intents[3]

def get_response_by_intent(intent):
    return rand.choice(responses[intent])
