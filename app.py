from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib
from helper import load_data, plot_age,plot_incident,plot_premium,plot_report

matplotlib.use('Agg')

app = Flask(__name__)

data = load_data()

@app.route("/")
def index():
	# copy data as raw
	raw = data.copy()

	# # generate value for cards

	percent_fraud = float(pd.crosstab(index=raw.fraud_reported,columns='count',normalize=True).loc['Y']*100)
	fraud_loss = raw.groupby('fraud_reported').sum()['total_claim_amount'].loc['Y']
	average_claim = raw.total_claim_amount.median()
	# compile card values as card_data
	 
	card_data = dict(
		percent_fraud = f'{percent_fraud}%',
		fraud_loss = f'US$ {fraud_loss:,}',
		average_claim = f'US$ {average_claim:,}'
	)

	# generate plot
	plot_age_res = plot_age(raw)
	plot_premium_res = plot_premium(raw)
	plot_incident_res = plot_incident(raw)
	plot_report_res = plot_report(raw)

	# render to html
	return render_template('index.html',
		   card_data = card_data, 
		 plot_age_res=plot_age_res,
		 plot_premium_res=plot_premium_res,
		 plot_incident_res=plot_incident_res,
		 plot_report_res=plot_report_res
		)


if __name__ == "__main__": 
    app.run(debug=True)
