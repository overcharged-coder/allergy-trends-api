from flask import Flask, jsonify
from pytrends.request import TrendReq
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Allergy Trends API!"

@app.route("/trends")
def get_trends():
    pytrends = TrendReq(hl='en-US', tz=360)
    all_keywords = [
        "pollen allergy symptoms", "hay fever", "allergy season", "what causes pollen allergies",
        "pollen count today", "pollen forecast", "seasonal allergies", "allergy relief",
        "antihistamines", "claritin", "zyrtec", "allegra",
        "best allergy medicine", "nasal spray for allergies", "natural remedies for allergies", "allergy shot side effects",
        "is pollen high today", "tree pollen vs grass pollen", "when is allergy season", "how to stop sneezing from pollen",
        "pollen allergy in children", "grass pollen allergy", "indoor pollen protection", "air purifier for allergies",
        "how to reduce pollen in home", "mask for pollen allergy", "how to block pollen", "HEPA filter for allergies"
    ]

    merged_df = pd.DataFrame()
    #for i in range(0, len(all_keywords), 4):
    kw_list = all_keywords[0:3]
    pytrends.build_payload(kw_list, timeframe='today 12-m', geo='US')
    data = pytrends.interest_over_time()
    if not data.empty:
        data = data.drop(columns=['isPartial'], errors='ignore')
        if merged_df.empty:
            merged_df = data
        else:
            merged_df = merged_df.join(data, how='outer')

    merged_df = merged_df.fillna(0)
    merged_df.index = merged_df.index.astype(str)  # Convert dates to strings for JSON
    return merged_df.tail(10).to_json(orient="index")

if __name__ == "__main__":
    app.run(debug=True)
