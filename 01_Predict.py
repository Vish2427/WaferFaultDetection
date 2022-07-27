import streamlit as st

from prediction_Validation_Insertion import pred_validation
from predictFromModel import prediction

st.title('Wafer Fault Detection')

def predictRouteClient(path):
    try:

        if path is not None:

            pred_val = pred_validation(path) #object initialization

            pred_val.prediction_validation() #calling the prediction_validation function

            pred = prediction(path) #object initialization

            # predicting for dataset present in database
            path,json_predictions = pred.predictionFromModel()
            st.write("Result is ready to download")
            return True

        else:
            print('Nothing Matched')
    except ValueError:
        st.write("Error Occurred! %s" %ValueError)
        return False
    except KeyError:
        st.write("Error Occurred! %s" %KeyError)
        return False
    except Exception as e:
        st.write("Error Occurred! %s" %e)
        return False


def result(report):

    with open('Prediction_Output_File\Predictions.csv') as file:
        st.download_button(label='Download Result', data=file, file_name='Wafer result.csv', mime='csv')

def start():
    path = st.text_input('Enter path')

    if st.button('Predict'):
        report = predictRouteClient(path)
        if report == True:
            result(report)

    st.subheader('OR')

    if st.button('Default Predict '):
        report = predictRouteClient('Prediction_batch_files')
        if report == True:
            result(report)



if __name__ == '__main__':
    start()



