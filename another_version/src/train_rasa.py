import subprocess

def train_rasa_model():
    try:
        subprocess.run(["rasa", "train"], check=True)
        print("Rasa model trained successfully.")
    except subprocess.CalledProcessError as e:
        print("Error training Rasa model:", e)

if __name__ == "__main__":
    train_rasa_model()
