def json_operations():
    import json
    data = {"key" + str(i): i for i in range(5000)}
    json_str = json.dumps(data)
    return json.loads(json_str)

json_operations()
