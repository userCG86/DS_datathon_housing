# House Price Predictor Leaderboard

This is a Streamlit application designed to host a competition for predicting house prices. Participants upload their predictions, and the leaderboard shows their accuracy and ranking.

## Getting Started

These instructions will help you set up the application on your local machine for development and testing purposes.

## Deployment on Streamlit

To deploy the application on Streamlit, you will need to create a new app on the Streamlit sharing platform. You can do this by following the instructions [here](https://docs.streamlit.io/en/stable/sharing.html).

Look at the Notion page for more details.

## Acknowledgements

House price data and inspiration for this project are based on the [Kaggle House Prices: Advanced Regression Techniques](https://www.kaggle.com/c/house-prices-advanced-regression-techniques) competition.

# Virtual Environment (venv) Setup & Activation Guide

Setting up a virtual environment can help you manage dependencies for your Python project. Here's a step-by-step guide to set up and activate a virtual environment using the built-in venv module in Python.

## Prerequisites

- Python 3.3 or later (check with python --version or python3 --version)

## Step 1: Create a Virtual Environment

Navigate to your project directory (or wherever you want to create the virtual environment) and run one of the following commands:

### For Linux/Mac:

```bash
python3 -m venv myenv
```

### For Windows:

```bash
py -m venv myenv
```

This will create a directory called myenv (or whatever you named it) that contains the virtual environment (basically a bunch of directories and files).

## Step 2: Activate the Virtual Environment

### For Linux/Mac:

```bash
source myenv/bin/activate
```

### For Windows:

```bash
myenv\Scripts\activate
```

You should see (myenv) at the beginning of your command line prompt, indicating that you are in the virtual environment. Now you can install dependencies and run your project without worrying about dependency conflicts.

## Step 3: Deactivate the Virtual Environment

When you're done working in the virtual environment, you can deactivate it by running the following command:

```bash
deactivate
```
