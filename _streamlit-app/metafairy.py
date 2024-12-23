import streamlit as st

st.set_page_config(layout="wide")

import time
from datetime import datetime
from dotenv import load_dotenv
import os

from openai import OpenAI
import logging

logging.basicConfig(
    filename="app.log",
    filemode="w",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.WARNING,
)

# load_dotenv("/root/.env_stat")
load_dotenv("/Volumes/1TB Home SSD/GitHub/.env_stat")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_SYSTEM_MESSAGE = """"You are a helpful assistant."""

from utils_prompts import SYSTEM_MESSAGE_GENERATE, BASE_PROMPT_GENERATE
from utils_prompts import SYSTEM_MESSAGE_ANALYZE, BASE_PROMPT_ANALYZE
from utils_functions import parse_analysis_results, create_download_link


# ----------------------------------------------------------------


@st.cache_resource
def get_project_info():
    """Get project info."""
    with open("utils_projectinfo.md") as f:
        return f.read()


@st.cache_resource
def get_openai_client():
    return OpenAI(api_key=OPENAI_API_KEY)


def call_openai(
    prompt, modelId="gpt-4o-mini", max_tokens=4096, system_message=SYSTEM_MESSAGE_GENERATE
):
    try:
        completion = openai_client.chat.completions.create(
            model=modelId,
            temperature=0.5,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
        )
        return True, completion.choices[0].message.content

    except Exception as e:
        print(f"Error: {e}")
        return False, None


def create_prompt_generate(
    title,
    data_content,
    data_context,
    data_quality,
    data_spatial,
):
    return f"""Schreibe eine Beschreibung für einen Datensatz. Die Metadaten des Datensatzes in Stichworten sind diese:

    Titel:\n{title}\n\n
    Dateninhalt:\n{data_content}\n\n
    Entstehungszusammenhang:\n{data_context}\n\n
    Datenqualität:\n{data_quality}\n\n
    Räumlicher Bezug:\n{data_spatial}\n\n
    {BASE_PROMPT_GENERATE}
    """


# ----------------------------------------------------------------

openai_client = get_openai_client()


# Create sidebar.
with st.sidebar:
    select_mode = st.radio(
        "Wähle den Modus:",
        ("Beschreibung generieren", "Beschreibung analysieren"),
        index=0,
    )
    st.caption(
        "Achtung: Die App nutzt ein grosses Sprachmodell (LLM). LLMs machen Fehler. Überprüfe die generierten Analysen und Beschreibungen immer. Nutze die App nur für öffentliche, nicht sensible Eingaben, da diese auf externen Rechnern des Drittanbieters OpenAI verarbeitet werden."
    )
    with st.expander("Über diese App"):
        st.markdown(get_project_info())

# Create main content.
if select_mode == "Beschreibung generieren":
    cols = st.columns((3, 3))
    with cols[0]:
        st.subheader("🙋‍♀️ Datensätze einfach beschreiben")

    with cols[1]:
        generate_description = st.button("**💬 :green[Beschreibung generieren]**")

    cols = st.columns((3, 3))

    with cols[0]:
        title = st.text_input(
            "Titel des Datensatzes", value="Verkehrsaufkommen in Zürich"
        )
        data_content = st.text_area(
            ":red[**Dateninhalt**] - ***Worum geht es? Was finde ich in diesen Daten?***",
            value="Die Menge an Verkehr im Kanton Zürich, gezählt auf Strassen und an Kreuzungen. Inkl. Verkehrsunfälle, gemessener Verkehrsmittel und CO2-Belastung.",
            height=100,
        )
        data_context = st.text_area(
            ":red[**Entstehungszusammenhang**] - ***Wie wurden die Daten gemessen und wofür? Was ist die Quelle?***",
            value="Kantonale Verkehrszählung, Verkehrsüberwachung, Verkehrsunfallstatistik. Daten gesammelt mit Kameras und Sensoren durch Polizei und Verkehrsamt.",
            height=100,
        )
        data_quality = st.text_area(
            ":red[**Datenqualität**] - ***Sind die Daten vollständig? Gibt es Änderungen in der Erhebung? Welche Rückschlüsse lassen sich aus den Daten ziehen und welche nicht?***",
            value="Daten aufgrund Wetter, Verkehrsdichte, Genauigkeit Sensoren nicht absolut genau. Daten wurden nur jährlich erhoben. Geringfügige methodische Veränderungen von Jahr zu Jahr sind möglich.",
            height=100,
        )
        data_spatial = st.text_area(
            "Räumlicher Bezug - *Wie sind die Daten räumlich aggregiert? In welchem Gebiet sind die Datenpunkte angesiedelt?*",
            value="Kanton Zürich, Genauigkeit: 10 Meter",
            height=100,
        )

    with cols[1]:
        if generate_description:
            if all([title, data_content, data_context]):
                with st.spinner("🚀 Bin am Schreiben..."):
                    start_time = time.time()
                    prompt = create_prompt_generate(
                        title,
                        data_content,
                        data_spatial,
                        data_context,
                        data_quality,
                    )
                    success, response = call_openai(
                        prompt, system_message=SYSTEM_MESSAGE_GENERATE
                    )
                    if success:
                        response = response.replace("\n", " ")
                        response = response.replace("  ", " ")
                        st.markdown("**Generierte Beschreibung**")
                        st.markdown(f"{response}", unsafe_allow_html=True)
                        time_processed = time.time() - start_time
                        logging.warning(
                            f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\t{prompt}\t{response}\t{time_processed:.3f}\t{success}'
                        )
                        create_download_link(response, time_processed, title)
                        st.caption(f"Verarbeitet in {time_processed:.1f} Sekunden.")
                    else:
                        st.error(f"Es ist ein Fehler aufgetreten: {response}")
                    time_processed = time.time() - start_time
                    logging.warning(
                        f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\t{prompt}\t{response}\t{time_processed:.3f}\t{success}'
                    )
            else:
                st.warning("Bitte fülle alle Felder aus.")
else:
    cols = st.columns((3, 3))
    with cols[0]:
        st.subheader("🙋 Datensätze einfach analysieren")

    with cols[1]:
        generate_description = st.button("**💬 :green[Beschreibung analysieren]**")

    cols = st.columns((3, 3))

    with cols[0]:
        source_title = st.text_area(
            "Datensatztitel, den du analysieren willst",
            value="Anteil EFH am Wohnungsbestand [%]",
            height=68,
        )
        source_description = st.text_area(
            "Datensatzbeschreibung, die du analysieren willst",
            value="Anteil EFH am Wohnungsbestand. Wohnungsbestand gemäss GWS. Wohnungsbestand bis 2009 aus Fortschreibung des Wohnungsbestandes der GWZ aufgrund der WBT.",
            height=200,
        )

    with cols[1]:
        if generate_description:
            if all([source_title, source_description]):
                with st.spinner("🚀 Bin am Analysieren..."):
                    start_time = time.time()

                    prompt = BASE_PROMPT_ANALYZE.format(
                        title=source_title, description=source_description
                    )
                    success, response = call_openai(
                        prompt, system_message=SYSTEM_MESSAGE_ANALYZE
                    )
                    if success:
                        response = parse_analysis_results(response)
                        st.caption("Dateninhalt")
                        st.markdown(response["content"].values[0])
                        st.caption("Entstehungszusammenhang")
                        st.markdown(response["context"].values[0])
                        st.caption("Datenqualität")
                        st.markdown(response["quality"].values[0])
                        st.caption("Räumlicher Bezug")
                        st.markdown(response["spacial"].values[0])
                        time_processed = time.time() - start_time
                        logging.warning(
                            f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\t{prompt}\t{response}\t{time_processed:.3f}\t{success}'
                        )
                        st.caption(f"Verarbeitet in {time_processed:.1f} Sekunden.")
                    else:
                        st.error(f"Es ist ein Fehler aufgetreten.")
                    time_processed = time.time() - start_time
                    logging.warning(
                        f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\t{prompt}\tError\t{time_processed:.3f}\t{success}'
                    )
            else:
                st.warning("Bitte fülle alle Felder aus.")
