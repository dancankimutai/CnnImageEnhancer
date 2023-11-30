# from tensorflow import keras
#
# model_path = "./model/enhancemod.h5"
# try:
#     model = keras.models.load_model(model_path)
#     print("Model loaded successfully.")
# except Exception as e:
#     print(f"Error loading the model: {e}")
from tensorflow import keras

def load_and_return_model(model_path="enhancemod.h5"):
    try:
        model = keras.models.load_model(model_path)
        print("Model loaded successfully.", model)
        return model
    except Exception as e:
        print(f"Error loading the model: {e}")
        return None


