def get_response(topic: str, lang: str):
    # Dummy responses example
    predefined = {
        "hello": "Hi there!",
        "python": "Python is a programming language"
    }
    return predefined.get(topic.lower())
