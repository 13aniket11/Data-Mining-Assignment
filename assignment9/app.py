import streamlit
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout

streamlit.set_option("deprecation.showPyplotGlobalUse", False)


WCE_LOGO_PATH = "./assets/images/wceLogo.png"

streamlit.set_page_config(
    page_title="Data Mining Project",
    page_icon=WCE_LOGO_PATH,
    layout="wide",
    initial_sidebar_state="expanded",
)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
streamlit.markdown(hide_streamlit_style, unsafe_allow_html=True)



streamlit.markdown("<br />", unsafe_allow_html=True)


streamlit.markdown("<h2 style='text-align: center; color: black'>Stock Prediction</h2><hr />", unsafe_allow_html=True)

styles = {
    "container": {
        "margin": "0px !important",
        "padding": "0!important",
        "align-items": "stretch",
        "background-color": "#fafafa",
    },
    "icon": {"color": "black", "font-size": "20px"},
    "nav-link": {
        "font-size": "20px",
        "text-align": "left",
        "margin": "0px",
        "--hover-color": "#eee",
    },
    "nav-link-selected": {
        "background-color": "lightblue",
        "font-size": "20px",
        "font-weight": "normal",
        "color": "black",
    },
}

with streamlit.sidebar:
    streamlit.sidebar.markdown("<hr />", unsafe_allow_html=True)

    main_option = None
    dataframe = None

    main_option = option_menu(
            "",
            [
                "Home",
                "Predict Stock",
                # "Prediction"
            ],
            icons=["clipboard-data", "eyeglasses"],
            default_index=0,
        )

    streamlit.sidebar.markdown("<hr />", unsafe_allow_html=True)

    


if main_option == 'Home':
    streamlit.markdown(
        """<center><h1>Guided by,</h1>
    <h3>Dr. B.F Momin<br /></h3></center>""",
        unsafe_allow_html=True,
    )
    
    streamlit.markdown(
        """<hr />
        <center>
        <h2>Developed by</h2>
        </center>""",
        unsafe_allow_html=True,
    )
    c1,c2 = streamlit.columns(2)
    with c1:
        streamlit.markdown("""<center><h4>Sanket Mote:<br />2019BTECS00113</h4></center>""", unsafe_allow_html=True,)
    with c2:
        streamlit.markdown("""<center><h4>Swapnil Kanade:</br>2019BTECS00114</h4></center>""",unsafe_allow_html=True,)
    

def create_dataset(df):
    x = []
    y = []
    for i in range(50, df.shape[0]):
        x.append(df[i-50:i, 0])
        y.append(df[i, 0])
    x = np.array(x)
    y = np.array(y)
    return x,y 

if main_option == "Predict Stock":
    file = st.file_uploader("Upload Data Set to Train and Predict")
    if(file):
        df = pd.read_csv(file)
        st.dataframe(df)
        df = df['Open'].values
        df = df.reshape(-1, 1)

        # df.dropna()

        print(df)


        dataset_train = np.array(df[:int(df.shape[0]*0.8)])

        dataset_test = np.array(df[int(df.shape[0]*0.8):])

        print(dataset_train.shape)

        print(dataset_test.shape)

        # scaling data
        scaler = MinMaxScaler(feature_range=(0,1))
        dataset_train = scaler.fit_transform(dataset_train)

        print(dataset_train[:5])

        dataset_test = scaler.transform(dataset_test)

        print(dataset_test[:5])

        

        x_train, y_train = create_dataset(dataset_train)

        x_test, y_test = create_dataset(dataset_test)

        model = Sequential()
        
        with st.spinner('Wait for it...'):
            
            model.add(LSTM(units=96, return_sequences=True, input_shape=(x_train.shape[1], 1)))
            model.add(Dropout(0.2))
            model.add(LSTM(units=96, return_sequences=True))
            model.add(Dropout(0.2))
            model.add(LSTM(units=96, return_sequences=True))
            model.add(Dropout(0.2))
            model.add(LSTM(units=96))
            model.add(Dropout(0.2))
            model.add(Dense(units=1))

            x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
            x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

            model.compile(loss='mean_squared_error', optimizer='adam')
            history = model.fit(x_train, y_train, epochs=50, batch_size=32)  
            loss = history.history['loss']
            epoch_count = range(1, len(loss) + 1)
            plt.figure(figsize=(12,8))
            plt.plot(epoch_count, loss, 'r--')
            plt.legend(['Training Loss'])
            plt.xlabel('Epoch')
            plt.ylabel('Loss')
            # plt.show()
            st.pyplot(plt) 
             
        st.success('Done!')
        st.write("Model Summary")
        model.summary(print_fn=st.write)
        predictions = model.predict(x_test)
        predictions = scaler.inverse_transform(predictions)
        y_test_scaled = scaler.inverse_transform(y_test.reshape(-1, 1))
        print('predictions',predictions,y_test_scaled)
        fig, ax = plt.subplots(figsize=(16,8))
        plt.xlabel('Time', fontsize=15)
        plt.ylabel('Stock Price',fontsize=15)
        plt.plot(y_test_scaled, color='red', label='Original price')
        plt.plot(predictions, color='cyan', label='Predicted price')
        plt.legend()
        plt.show()
        st.pyplot(plt)

        


elif main_option == "Prediction":
    file = st.file_uploader("Upload Data Set to Train and Predict")
    if(file):
        df = pd.read_csv(file)
        stockprices = df.sort_values('Date')

        test_ratio = 0.2
        training_ratio = 1 - test_ratio

        train_size = int(training_ratio * len(stockprices))
        test_size = int(test_ratio * len(stockprices))

        print("train_size: " + str(train_size))
        print("test_size: " + str(test_size))

        train = stockprices[:train_size][['Date', 'Open']]
        test = stockprices[train_size:][['Date', 'Open']]

        st.dataframe(df)

        
        # df = df['Open'].values
        # df = df.reshape(-1, 1)
        stockprices = stockprices.set_index('Date')


        # # df.dropna()

        # print(df)


        # dataset_train = np.array(df[:int(df.shape[0]*0.8)])

        # dataset_test = np.array(df[int(df.shape[0]*0.8):])

        # print(dataset_train.shape)

        # print(dataset_test.shape)

        # # scaling data
        scaler = MinMaxScaler(feature_range=(0,1))  
        # scaler = StandardScaler()
        scaled_data = scaler.fit_transform(stockprices[['Open']])
        scaled_data_train = scaled_data[:train.shape[0]]


        # print(dataset_train[:5])

        dataset_test = scaler.transform(stockprices[['Open']])

        # print(dataset_test[:5])

        

        x_train, y_train = create_dataset(scaled_data_train)
        print(x_train,y_train)
        x_test, y_test = create_dataset(dataset_test)

        model = Sequential()
        
        with st.spinner('Wait for it...'):
            
            model.add(LSTM(units=96, return_sequences=True, input_shape=(x_train.shape[1], 1)))
            model.add(Dropout(0.2))
            model.add(LSTM(units=96, return_sequences=True))
            model.add(Dropout(0.2))
            model.add(LSTM(units=96, return_sequences=True))
            model.add(Dropout(0.2))
            model.add(LSTM(units=96))
            model.add(Dropout(0.2))
            model.add(Dense(units=1))

            x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
            x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

            model.compile(loss='mean_squared_error', optimizer='adam')
            history = model.fit(x_train, y_train, epochs=50, batch_size=32)  
            loss = history.history['loss']
            epoch_count = range(1, len(loss) + 1)
            plt.figure(figsize=(12,8))
            plt.plot(epoch_count, loss, 'r--')
            plt.legend(['Training Loss'])
            plt.xlabel('Epoch')
            plt.ylabel('Loss')
            # plt.show()
            st.pyplot(plt) 
             
        st.success('Done!')
        st.write("Model Summary")
        model.summary(print_fn=st.write)

        def preprocess_testdat(data=stockprices, scaler=scaler, window_size=50, test=test):    
            raw = data['Close'][len(data) - len(test) - window_size:].values
            raw = raw.reshape(-1,1)
            raw = scaler.transform(raw)
            
            X_test = []
            for i in range(window_size, raw.shape[0]):
                X_test.append(raw[i-window_size:i, 0])
                
            X_test = np.array(X_test)
            
            X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
            return X_test
        
        x_test = preprocess_testdat()

        predictions = model.predict(x_test)
        predictions = scaler.inverse_transform(predictions)

        test['Predictions_lstm'] = predictions

        y_test_scaled = scaler.inverse_transform(y_test.reshape(-1, 1))
        print('predictions',predictions,y_test_scaled)

        fig, ax = plt.subplots(figsize=(16,8))
        plt.xlabel('Time', fontsize=15)
        plt.ylabel('Stock Price',fontsize=15)
        plt.plot(y_test_scaled, color='red', label='Original price')
        plt.plot(predictions, color='cyan', label='Predicted price')
        plt.legend()
        plt.show()
        st.pyplot(plt)

        # fig = plt.figure(figsize = (20,10))
        # # plt.plot(train['Date'], train['Open'], label = 'Train Closing Price')
        # plt.plot(test['Date'], test['Open'], label = 'Test Closing Price')
        # plt.plot(test['Date'], test['Predictions_lstm'], label = 'Predicted Closing Price')
        # plt.title('LSTM Model')
        # plt.xlabel('Date')
        # plt.ylabel('Stock Price ($)')
        # plt.legend(loc="upper left")
        # st.pyplot(plt)
        # plt.show()