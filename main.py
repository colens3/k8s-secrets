import time

def main():
    filename = "/etc/secret-volume/username"
    secret_value = ""
    while True:
        with open(filename, 'r') as filehandle:
            for line in filehandle:
                if line != secret_value:
                    secret_value = line
                    print(f"Secret Value: {secret_value}")
        time.sleep(1)

if __name__ == "__main__":
    main()
