import pandas as pd
import librosa
import glob
import numpy as np
from keras.models import model_from_json
from scipy.special import softmax
# from sklearn.preprocessing import LabelEncoder
import warnings

warnings.simplefilter('ignore')


def infer_from_audio(audio):
    # audio should be a string
    # sampel audio format: 'output10.wav'

    # audio_duration should be a real number in seconds

    # loading pre-trained model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("Emotion_Voice_Detection_Model.h5")

    # loading audio input
    X, sample_rate = librosa.load(audio, res_type='kaiser_fast',
                                  duration=librosa.get_duration(
                                      filename=audio),
                                  sr=22050 * 2,
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

    # choosing top 3 values
    agg_livepreds = []
    for i in range(5):
        agg_livepreds.append(livepreds[0][i] + livepreds[0][i + 5])

    idx = np.argsort(agg_livepreds)[-3:]
    idx = np.flip(idx)
    prob = softmax(agg_livepreds)
    prob_list = []
    for i in idx:
        prob_list.append(prob[i] * 100)
    string_prob_list = [round(p, 3) for p in prob_list]

    #     livepreds1=livepreds.argmax(axis=1)
    #     liveabc = livepreds1.astype(int).flatten()

    #     pred = liveabc[0]



    # emotion = emotion_dict.get(pred).split('_')[1]
    # emotion = emotion_dict.get(pred)
    # emotion_list = [emotion_dict.get(i) for i in idx]

    # return 3 value pairs (emotion, probability)
    # possible emotion values: 'angry', 'calm', 'fearful', 'happy', 'sad'
    output = list(zip(idx, string_prob_list))

    return output
