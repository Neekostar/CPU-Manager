import psutil
import time


def main():
    try:
        while True:
            cpu_percent = psutil.cpu_percent(interval=1, percpu=False)
            print(f"CPU Usage: {cpu_percent}%")
    except KeyboardInterrupt:
        print("\nExiting...")


if __name__ == "__main__":
    main()
