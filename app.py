import streamlit as st
import pickle
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import base64
import os


vector_form = pickle.load(open('vector.pkl', 'rb'))
load_model = pickle.load(open('model.pkl', 'rb'))


port_stem = PorterStemmer()


def stemming(content):
    con = re.sub('[^a-zA-Z]', ' ', content)
    con = con.lower()
    con = con.split()
    con = [port_stem.stem(word) for word in con if not word in stopwords.words('english')]
    con = ' '.join(con)
    return con


def fake_news(news):
    news = stemming(news)
    input_data = [news]
    vector_form1 = vector_form.transform(input_data)
    prediction = load_model.predict(vector_form1)
    return prediction


def main():

   def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
   add_bg_from_local('111.jpg')
  
   app_directory = os.path.dirname(__file__)
   image_path = os.path.join(app_directory, "logoimage.jpeg")
   st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 100px 
        }
    </style>
    """,
    unsafe_allow_html=True,
)
   st.sidebar.image(image_path, width=150 )
   st.sidebar.header("Natural Language Process")
   st.sidebar.subheader("Fake News Predictor using NLP is a Python tool that employs Natural Language Processing techniques to analyze and classify news articles as either authentic or fake, helping users identify unreliable information with high accuracy.")

   

   st.title('Fake News Classification app')
   st.markdown('<style>h1{color: white;}</style>', unsafe_allow_html=True)
   st.subheader("Input the News content below")
   st.markdown('<style>h3{color: white;}</style>', unsafe_allow_html=True)

   sentence = st.text_area("Enter your news content here", "", height=200)
    

   predict_btt = st.button("Predict")
    
   if predict_btt:

        if sentence.strip() == "":
            st.warning("Please enter some news content.")
        else:
            prediction_class = fake_news(sentence)
            if prediction_class == [0]:
                st.success('Authentic news')
            elif prediction_class == [1]:
                st.warning('Fake news')

if __name__ == '__main__':
    main()

