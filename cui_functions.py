from cuis import blood_glucose_secondary_aspects,insulin_pump_device_secondary_aspects,carbohydrates_secondary_aspects

def return_secondary_blood_glucose_aspect(mini_soup,primary_aspect,primary_cui):
	cui = mini_soup.get('cui')
	if cui == primary_cui:
		return 'N'
	else:
		if cui in blood_glucose_secondary_aspects:
			return primary_aspect + ' ' + blood_glucose_secondary_aspects[cui]
		else:
			return 'N'

def return_secondary_insulin_pump_device_secondary_aspects(mini_soup,primary_aspect,primary_cui):
	cui = mini_soup.get('cui')
	if cui == primary_cui:
		return 'N'
	else:
		if cui in insulin_pump_device_secondary_aspects:
			return primary_aspect + ' ' + insulin_pump_device_secondary_aspects[cui]
		else:
			return 'N'

def return_secondary_carbohydrates_secondary_aspects(mini_soup,primary_aspect,primary_cui):
	cui = mini_soup.get('cui')
	if cui == primary_cui:
		return 'N'
	else:
		if cui in insulin_pump_device_secondary_aspects:
			return primary_aspect + ' ' + carbohydrates_secondary_aspects[cui]
		else:
			return 'N'