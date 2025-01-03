# 🦄 OGD MetaFairy

**Easily create high quality dataset descriptions – with a little help from ✨ AI.**

![GitHub License](https://img.shields.io/github/license/machinelearningzh/ogd_ai-metafairy)
[![PyPI - Python](https://img.shields.io/badge/python-v3.9+-blue.svg)](https://github.com/machinelearningZH/ogd_ai-metafairy)
[![GitHub Stars](https://img.shields.io/github/stars/machinelearningZH/ogd_ai-metafairy.svg)](https://github.com/machinelearningZH/ogd_ai-metafairy/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/machinelearningZH/ogd_ai-metafairy.svg)](https://github.com/machinelearningZH/ogd_ai-metafairy/issues)
[![GitHub Issues](https://img.shields.io/github/issues-pr/machinelearningZH/ogd_ai-metafairy.svg)](https://img.shields.io/github/issues-pr/machinelearningZH/ogd_ai-metafairy)
[![Current Version](https://img.shields.io/badge/version-0.1-green.svg)](https://github.com/machinelearningZH/ogd_ai-metafairy)
<a href="https://github.com/astral-sh/ruff"><img alt="linting - Ruff" class="off-glb" loading="lazy" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json"></a>

<details>
<summary>Contents</summary>

- [Usage](#usage)
- [What does the app do?](#what-does-the-app-do)
- [Project team](#project-team)
- [Feedback and contributing](#feedback-and-contributing)

</details>

![](_imgs/app_ui.png)

## Usage

- Create a [Conda](https://conda.io/projects/conda/en/latest/index.html) environment: `conda create -n metafairy python=3.9`
- Activate environment: `conda activate metafairy`
- Clone this repo.
- Change into the project directory.
- Install packages: `pip install -r requirements.txt`
- Create an `.env` file and input your OpenAI API keys like so:

```
    OPENAI_API_KEY=sk-...
```

- Change into the app directory: `cd _streamlit_app/`
- Start the app: `streamlit run metafairy.py`

## What does the app do?

This app aims to simplify the creation of **meaningful, complete, and well-written dataset descriptions**. You can either **analyze** a description or **create** one.

- To **analyze** a given data set description simply copy it into the input window and click «Beschreibung analyisieren».
- To **create** a description simply input keywords and basic information about your dataset and click «Beschreibung generieren».

We offer this tool to our data publishers and stewards to facilitate their work. We believe you might find it helpful as well.

The app structures the analysis and the drafts along these four key points:

1. **Data Content** (*Dateninhalt*) - What is the data about? What can be found in this data?
2. **Context of Creation** (*Entstehungszusammenhang*) - How were the data measured and for what purpose? What is the source?
3. **Data Quality** (*Datenqualität*) - Are the data complete? Are there any changes in the collection? What conclusions can and can not be drawn from the data?
4. **Spatial Reference** (*Räumlicher Bezug*) - How are the data spatially collected and aggregated? In which area are the data points located?

> [!Important]
> At the risk of stating the obvious: By using the app **you send data to a third-party provider** namely [OpenAI](https://platform.openai.com/docs/overview). **Therefore strictly only use non-sensitive data.** Again, stating the obvious: **LLMs make errors.** They regularly hallucinate, make things up, and get things wrong. They often do so in subtle, non-obvious ways, that may be hard to detect. This app is **meant to be used as an assistive system**. It **only yields a draft, that you always should double- and triple-check.**

## Project team

This is a project of [Team Data of the Statistical Office of the Canton of Zurich](https://www.zh.ch/de/direktion-der-justiz-und-des-innern/statistisches-amt/data.html). Responsible: Laure Stadler and Patrick Arnecke. Many thanks go to **Corinna Grobe** and our former colleague **Adrian Rupp**. Merci! ❤️

## What we learned so far

1. Metafairy provides a scaffold for writing a good data description. This scaffold is valuable to our data stewards. They don't really need or use the generated description itself or as is.
2. Generating descriptions is fun, though. And some fun must be had during a long work day. 🤓
3. More useful than newly generated descriptions is AI improving *existing* descriptions. We implemented this feature upon request of our data stewards.

## Feedback and contributing

We would love to hear from you. Please share your feedback and let us know how you use the code. You can [write an email](mailto:datashop@statistik.zh.ch) or share your ideas by opening an issue or a pull requests.

Please note that we use [Ruff](https://docs.astral.sh/ruff/) for linting and code formatting with default settings.
