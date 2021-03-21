import pandas as pd
import librosa
import glob
import numpy as np
from keras.models import model_from_json
# from sklearn.preprocessing import LabelEncoder
import warnings

warnings.simplefilter('ignore')


def infer_from_audio(audio, audio_duration):
    # audio should be a string
    # sample audio format: 'output10.wav'

    # audio_duration should be a real number

    # loading pre-trained model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("Emotion_Voice_Detection_Model.h5")

    # loading audio input
    X, sample_rate = librosa.load(audio, res_type='kaiser_fast',
                                  duration=audio_duration, sr=22050 * 2,
                                  offset=0.5)

    # changing data shape
    sample_rate = np.array(sample_rate)
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=13),
                    axis=0)
    featurelive = mfccs
    livedf2 = featurelive

    livedf2 = pd.DataFrame(data=livedf2)
    livedf2 = livedf2.stack().to_frame().T

    twodim = np.expand_dims(livedf2, axis=2)

    # inference
    livepreds = loaded_model.predict(twodim,
                                     batch_size=32,
                                     verbose=1)
    livepreds1 = livepreds.argmax(axis=1)
    liveabc = livepreds1.astype(int).flatten()

    pred = liveabc[0]

    emotion_dict = {

        0: 'female_angry',
        1: 'female_calm',
        2: 'female_fearful',
        3: 'female_happy',
        4: 'female_sad',
        5: 'male_angry',
        6: 'male_calm',
        7: 'male_fearful',
        8: 'male_happy',
        9: 'male_sad'
    }

    emotion = emotion_dict.get(pred).split('_')[1]

    # return a string
    # possible output values: 'angry', 'calm', 'fearful', 'happy', 'sad'

    return emotion
