import requests
from typing import List, Dict


#########################[ start run_test ]##############################################
def run_test(payloads: List[Dict[str, str]]):
    """
    An example function that takes a list of payloads and returns a list of results.
    This function should append a "response" key to the payloads with the LLM's response.
    """
    # Example testing Gandalf
    session = requests.Session()
    base_url = "https://gandalf.lakera.ai"

    # Initial GET request to establish session and cookies
    session.get(base_url)
    results = []
    count = 0
    for payload in payloads:
        # Define the form data
        data = {"defender": "baseline", "prompt": payload["prompt"]}

        # Send the POST request with form data
        response = session.post(f"{base_url}/api/send-message", data=data)
        response_json = response.json()

        payload["response"] = response_json["answer"]
        results.append(payload)
        count += 1
        if count == 3:
            break


    return results


#########################[ end run_test ]################################################
