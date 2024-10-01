import backend

backend_int = backend.BackendInterface()


print("Welcome to GPbeT Type 'quit' to exit.")
first_query = True
while True:
    user_input = input("User: ")
    if user_input.lower() == "quit":
        break

    if first_query:
        response = backend_int.get_result_single(user_input)
        first_query = False
    else:
        response = backend_int.get_followup_response(user_input)
    print("Bot:", response)

