# Libraries ------------------------------------------------------------
import streamlit as st
import requests
import json
import os


# Title ------------------------------------------------------------
st.set_page_config(
    page_title="Speech-to-Text Transcription App", layout="wide"
)


# App layout width -------------------------------------------------
def _max_width_():
    max_width_str = f"max-width: 1200px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )

_max_width_()


# Header -------------------------------------------------
st.header("Speech-to-Text Transcription App")

st.text("")
st.markdown(
    f"""
        The speech to text recognition is completed via the [OpenAI's whisper medium model](https://huggingface.co/openai/whisper-medium) from Hugging Face.
        """
)
st.text("")


# region Main ------------------------------------------------
def main():
    demo()

# endregion main ---------------------------------------------


# Transcription -------------------------------------------------
def demo():

    c1, c2, c3 = st.columns([1, 4, 1])
    with c2:

        with st.form(key="my_form"):

            f = st.file_uploader("", type=[".wav"])

            st.info(
                f"""
                    Upload a .wav file. Or try a sample: [Wav sample](https://github.com/CharlyWargnier/CSVHub/blob/main/Wave_files_demos/The_National_Park.wav?raw=true)
                    """
            )

            submit_button = st.form_submit_button(label="Transcribe")

    if f is not None:
        path_in = f.name
        # Get file size from buffer
        # Source: https://stackoverflow.com/a/19079887
        old_file_position = f.tell()
        f.seek(0, os.SEEK_END)
        getsize = f.tell()  # os.path.getsize(path_in)
        f.seek(old_file_position, os.SEEK_SET)
        getsize = round((getsize / 1000000), 1)

        if getsize < 5:  # File more than 5MB
            # To read file as bytes:
            bytes_data = f.getvalue()

            # Load your API key from an environment variable or secret management service
            api_token = st.secrets["api_token"]

            ## endregion API key
            headers = {"Authorization": f"Bearer {api_token}"}
            API_URL = "https://api-inference.huggingface.co/models/openai/whisper-medium"

            def query(data):
                response = requests.request("POST", API_URL, headers=headers, data=data)
                return json.loads(response.content.decode("utf-8"))

            data = query(bytes_data)

            values_view = data.values()
            value_iterator = iter(values_view)
            text_value = next(value_iterator)
            text_value = text_value.lower()

            st.success(text_value)

            c0, c1 = st.columns([2, 2])

            with c0:
                st.download_button(
                    "Download the transcription",
                    text_value,
                    file_name=None,
                    mime=None,
                    key=None,
                    help=None,
                    on_click=None,
                    args=None,
                    kwargs=None,
                )

        else:
            st.warning(
                " The file you uploaded is more than 5MB! "
            )
            st.stop()

    else:
        path_in = None
        st.stop()


# About -------------------------------------------------
with st.expander("ℹ️ - About", expanded=False):

    st.write(
        """     
-   Upload a wav audio file of up to 5MB to be transcribed to text. 
-   This app is modified from Charly Wargnier's Speech-to-text app using Streamlit and Hugging Face:
    https://github.com/CharlyWargnier/speech-to-text-streamlit-app
	    """
    )
    st.markdown("")


if __name__ == "__main__":
    main()