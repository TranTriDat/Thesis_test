from keras.layers import Activation
from keras.utils.generic_utils import get_custom_objects
from keras.models import load_model
from keras import backend as K
from keras.backend import sigmoid

def f1_score(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    recall = true_positives / (possible_positives + K.epsilon())
    f1_val = 2*(precision * recall)/(precision + recall + K.epsilon())
    return f1_val

def swish(x, beta = 1):
    return (x * K.sigmoid(beta * x))

get_custom_objects().update({'swish': swish})

# model = load_model('G:\Atom\Thesis\Implementation\age_detection_EB7.h5',custom_objects={"activation":Activation(swish)})
def age_model():
    # model1 = load_model('age_detection3_resnet50v2_new.h5',custom_objects={"activation":Activation(swish),
    #                                                                         'f1_score':f1_score})
    model1 = load_model('age_detection2_from_other_file_new.h5',custom_objects={"activation":Activation(swish)})
    return model1

def gender_model():
    model2 = load_model('gender_detection_from_other_file_new.h5',custom_objects={"activation":Activation(swish)})
    return model2

def emotion_model():
    model3 = load_model('emotion_detection1_resnet50v2.h5',custom_objects={"activation":Activation(swish)})
    return model3
