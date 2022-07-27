import streamlit as st
from trainingModel import trainModel
from training_validation_insertion import train_validation

st.header('Train Model')
path=st.text_input('Enter File absolute Path')

def trainmodel(path):
    try:
        if path is not None:

            train_val = train_validation(path) #object Initialization
            train_val.train_validation() #calling the training_validation function

            train_model = trainModel() #object initialization
            train_model.trainingModel() #training the model for the files in the table


    except ValueError:

       st.write("Error Occurred! %s" % ValueError)

    except KeyError:

        st.write("Error Occurred! %s" % KeyError)

    except Exception as e:

        st.write("Error Occurred! %s" % e)
    st.write("Training successfull!!")

if st.button('Train'):
    trainmodel(path)

