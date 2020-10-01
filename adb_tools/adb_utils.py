def print_logcat(connection):
    while True:
        data = connection.read(1024)
        if not data:
            break
        # print(data.decode('utf-8'))

    connection.close()
