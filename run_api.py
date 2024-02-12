import os


def run():
    try:
        os.system('uvicorn api.main:app --reload --port=8080')
    except Exception as e:
        print(f"Failed to run API: {e}")


if __name__ == "__main__":
    run()
