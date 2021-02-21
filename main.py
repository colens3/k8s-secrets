import time

def main():
    while True:
        print("Secret Read Started")
        filename = "/etc/secret-volume/username"

        with open(filename, 'r') as filehandle:
            for line in filehandle:
                print(f"Username: {line}")
        time.sleep(5)

if __name__ == "__main__":
    main()
