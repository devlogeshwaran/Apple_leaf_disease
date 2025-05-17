from flask import Flask, render_template, request, session, flash, send_file
from datetime import datetime
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aaa'

conn = mysql.connector.connect(user='root', password='admin', host='localhost', database='2citrustdb')
cur = conn.cursor()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/AdminLogin')
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route('/FarmerLogin')
def FarmerLogin():
    return render_template('FarmerLogin.html')


@app.route('/NewFarmer')
def NewFarmer():
    return render_template('NewFarmer.html')


@app.route("/AdminHome")
def AdminHome():
    cur.execute("SELECT * FROM regtb")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/AFarmerInfo")
def AFarmerInfo():
    cur.execute("SELECT * FROM farmertb ")
    data = cur.fetchall()
    return render_template('AFarmerInfo.html', data=data)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

            cur.execute("SELECT * FROM regtb;")
            data = cur.fetchall()
            flash("Login successfully")
            return render_template('AdminHome.html', data=data)

        else:
            flash("UserName Or Password Incorrect!")
            return render_template('AdminLogin.html')


@app.route("/newfarmer", methods=['GET', 'POST'])
def newfarmer():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        uname = request.form['uname']
        password = request.form['password']

        cursor = conn.cursor()
        cursor.execute(
        "INSERT INTO farmertb (name, mobile, email, address, username, password) VALUES (%s, %s, %s, %s, %s, %s)",
        (name, mobile, email, address, uname, password)
    )
        conn.commit()
        conn.close()
        flash('User Register successfully')
    return render_template('FarmerLogin.html')


@app.route("/flogin", methods=['GET', 'POST'])
def flogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['fname'] = request.form['uname']
        conn = mysql.connector.connect(user='root', password='admin', host='localhost', database='2citrustdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from farmertb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('FarmerLogin.html')
        else:

            session['mob'] = data[2]

            cur.execute("SELECT * FROM farmertb where username='" + username + "' and Password='" + password + "'")
            data = cur.fetchall()
            flash("Login successfully")
            return render_template('FarmerHome.html', data=data)


@app.route("/FarmerHome")
def FarmerHome():
    fname = session['fname']
    cur.execute("SELECT * FROM farmertb where UserName='" + fname + "'  ")
    data = cur.fetchall()
    return render_template('FarmerHome.html', data=data)


@app.route("/Predict")
def Predict():
    return render_template('Predict.html')


@app.route("/pred", methods=['GET', 'POST'])
def pred():
    if request.method == 'POST':
        import os
        file = request.files['file']
        fname = file.filename
        file.save('static/Out/'+fname)

        import warnings
        warnings.filterwarnings('ignore')

        import tensorflow as tf
        classifierLoad = tf.keras.models.load_model('model.h5')

        import numpy as np
        from keras.preprocessing import image
        from keras.applications.vgg16 import preprocess_input

        base_dir = 'Dataset/'
        catgo = os.listdir(base_dir)

        #test_image = image.load_img('static/Out/Test.jpg', target_size=(100, 100))

        org = 'static/Out/'+ fname

        #test_image = np.expand_dims(test_image, axis=0)
        #result = classifierLoad.predict(test_image)
        #ind = np.argmax(result)
        #print(ind)
        img = image.load_img('static/Out/'+fname, target_size=(100, 100))
        x = image.img_to_array(img)
        x = preprocess_input(x)
        # Rescale image.
        #x = x / 255.
        x = np.expand_dims(x, axis=0)
        images = np.vstack([x])
        result = classifierLoad.predict(images)

        ind = np.argmax(result)
        print(ind)
        print(catgo[ind])

        out = ''
        pre = ''
        predicted_class = catgo[ind]

        out = predicted_class

        if (predicted_class == "Alternaria leaf spot"):
            out = predicted_class

            pre = 'Alternaria Leaf Spot:To control Alternaria leaf spot organically, use neem oil spray (5ml neem oil' \
                  ' + 5ml liquid soap ' \
                  'per liter of water, applied every 10 days), garlic-chili spray (10 crushed garlic cloves + ' \
                  '5 dried chilies soaked in 1L water), or baking soda solution (1 tsp baking soda + 1 tsp oil ' \
                  'per liter of water). These natural fungicides work by disrupting fungal growth while being safe' \
                  ' for plants and the environment. For best results, apply sprays in the early morning or evening,' \
                  ' covering both sides of leaves, and combine with good cultural practices like removing infected ' \
                  'foliage and improving air circulation around trees. Regular applications every 7-14 days during ' \
                  'humid conditions provide optimal protection against this fungal disease.'



        elif (predicted_class == "Brown spot"):
            out = predicted_class
            pre = 'Brown Spot:To manage brown spot disease in apple leaves, natural fertilizers and organic remedies' \
                  ' can be' \
                  ' highly effective. Buttermilk or curd water (mix 100 mL in 1 liter of water) can be sprayed on ' \
                  'leaves to combat fungal infections. Compost tea enriches soil health and boosts plant immunity,' \
                  ' while fish emulsion provides essential nutrients for stronger growth. Neem-based solutions ' \
                  '(neem oil or neem leaf extract) act as natural fungicides and pest repellents. Additionally, ' \
                  'vermicompost and blue-green algae (Azolla) improve soil fertility and promote healthy leaf ' \
                  'development. These organic methods help prevent disease spread while enhancing the tree’s ' \
                  'overall resistance. For best results, apply these treatments early in the morning or late ' \
                  'evening and repeat every 10–15 days.'


        elif (predicted_class == "Frogeye leaf spot"):
            out = predicted_class
            pre = 'Frog Eye Leaf Spot:To control Frog Eye Leaf Spot in apple leaves, natural fertilizers and' \
                  ' organic fungicides can be' \
                  ' used effectively. Neem oil (5 mL per 1 liter of water) acts as a natural antifungal spray. ' \
                  'Panchagavya (in a 5-5-5 or 3-3-3 ratio) enhances soil nutrients and plant immunity. Compost tea' \
                  ' and fish emulsion improve disease resistance, while buttermilk spray (100 mL per liter of water)' \
                  ' and diluted cow urine (1:10 ratio) help prevent fungal growth. Apply these organic treatments' \
                  ' every 10–15 days for best results.'

        elif (predicted_class == "Grey spot"):
            out = predicted_class
            pre ='To treat Gray Spot Disease in apple leaves, natural remedies can effectively control the fungal' \
                 ' infection. Neem oil (5 mL per 1 liter of water) acts as a natural antifungal spray. Panchagavya' \
                 ' (in a 3-3-3 ratio) boosts the tree’s immunity, while vermicompost and compost tea improve soil ' \
                 'health. Additionally, buttermilk spray (100 mL per liter of water) and diluted cow urine (1:10 ' \
                 'ratio) help prevent fungal spread. Apply these organic treatments every 07–10 days for best results. '



        elif (predicted_class == "Health"):
            out = predicted_class
            pre = 'No treatment needed. Maintain regular care and organic nutrition.'

        elif (predicted_class == "Mosaic"):
            out = predicted_class
            pre = 'Apple Mosaic Virus Disease – Natural Management Approaches:' \
                  'For Apple Mosaic Virus Disease management, adopt these organic approaches since it is a viral ' \
                  'infection. Neem oil spray (5 mL per liter) helps control insect vectors. Aloe vera solution ' \
                  '(1:5 ratio) enhances plant immunity. Enrich soil with vermicompost and groundnut cake fertilizer ' \
                  'to improve tree vitality. Moringa leaf extract (100g leaves/1L water) sprayed twice weekly boosts ' \
                  'resistance. Immediately prune and destroy infected branches to prevent spread. Maintain proper ' \
                  'sanitation and avoid using tools on healthy plants after handling infected ones.' \
                  'Important Note:While these methods help manage symptoms and improve plant health, a complete cure ' \
                  'for viral diseases is challenging. Focus on prevention through vector control and maintaining ' \
                  'vigorous plant growth.'

        elif (predicted_class == "Powdery mildew"):
            out = predicted_class
            pre = 'Powdery Mildew Disease in Apple Leaves-Natural Remedies:For Powdery Mildew on apple leaves, try ' \
                  'these effective organic solutions: Baking soda spray ' \
                  '(1 tbsp soda + 1 tbsp oil in 1L water) disrupts fungal growth. Garlic-chili paste (5 garlic cloves' \
                  ' + 10 chilies + 1L water) acts as a potent natural fungicide. Apply moringa leaf decoction (100g ' \
                  'leaves boiled in 1L water) twice weekly. Boost plant immunity with vermicompost and compost ' \
                  'fertilizers. Always remove and burn infected leaves to prevent spore spread. Ensure good air ' \
                  'circulation around trees by proper pruning.Prevention Tip: Spray treatments early morning and ' \
                  'avoid overhead watering. Milk spray (1:5 ratio with water) can also create a protective film on ' \
                  'leaves against fungal spores when applied preventatively.'

        elif (predicted_class == "Rust"):
            out = predicted_class
            pre = 'Apple Leaf Rust Disease-Natural Remedies:For treating Rust Disease in apple leaves, natural' \
                  ' solutions work effectively. Spray neem oil ' \
                  'mixture (5 mL per 1 liter water) to control fungal growth. Panchagavya spray (3-3-3 ratio) ' \
                  'enhances plant immunity while improving soil nutrition. Cow urine solution (1:10 dilution)' \
                  ' prevents disease spread. Apply these organic treatments every 10-15 days for optimal results.' \
                  'Additional Tip: Remove and destroy infected leaves to prevent further spread of the disease. ' \
                  'Maintaining proper air circulation around trees also helps prevent rust infections.'

        elif (predicted_class == "Scab"):
            out = predicted_class
            pre = 'Apple Leaf Scab Disease-Natural Remedies:To combat Apple Scab Disease organically, try these ' \
                  'effective home remedies. Prepare a neem oil ' \
                  'spray (10 mL per 1 liter water) and apply thoroughly. Garlic solution (5 crushed cloves in 1 liter' \
                  ' water) works as a natural fungicide. Enhance soil health with vermicompost and compost to help' \
                  ' prevent infection. Remove and destroy all infected leaves to control the spread. Apply these' \
                  ' treatments weekly for best results.Prevention Tip: Prune trees to improve air circulation and ' \
                  'avoid overhead watering to minimize leaf wetness duration, which discourages infection.'


    return render_template('Result.html', org=org, out=out, pre=pre)


@app.route("/pred1", methods=['GET', 'POST'])
def pred1():
    if request.method == 'POST':
        return render_template('Predict.html')

@app.route("/FertilizerPesticideRecommendation", methods=["GET","POST"])
def Recommending_fertPest():
    if request.method == 'GET':
        return render_template('FertPestRecommend.html')
    if request.method == 'POST':
        # Get form data
        soil_ph = request.form['soil_ph']
        soil_npk = request.form['soil_npk']
        latitude = request.form['latitude']
        longitude = request.form['longitude']

    weather_data = {}
    if latitude and longitude:
        try:
            # Open-Meteo API (no key required)
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m"
            response = requests.get(weather_url)
            if response.status_code == 200:
                raw_data = response.json()
                weather_data = {
                    "temp": raw_data.get("current", {}).get("temperature_2m", 20),
                    "humidity": raw_data.get("current", {}).get("relative_humidity_2m", 50)
                }
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            weather_data = {"temp": 20, "humidity": 50}

    # Generate recommendations based on soil and weather conditions
    fertilizer_recommendations = get_fertilizer_recommendations(soil_ph, soil_npk, weather_data)
    pesticide_recommendations = get_pesticide_recommendations(soil_ph, soil_npk, weather_data)


    return render_template(
        'FertPestResults.html',
        soil_ph=soil_ph,
        soil_npk=soil_npk,
        fertilizer_recommendations=fertilizer_recommendations,
        pesticide_recommendations=pesticide_recommendations,
        weather=weather_data
    )


def get_fertilizer_recommendations(soil_ph, soil_npk, weather_data):
    """Generate fertilizer recommendations for apple farming based on soil health and weather data."""
    recommendations = {
        'primary': '',
        'secondary': '',
        'application_method': '',
        'timing': '',
        'organic_options': []
    }

    # Extract season if weather data is available
    season = "spring"  # Default
    if weather_data and 'main' in weather_data:
        temp = weather_data.get('temp', 20)
        month = datetime.now().month

        if 3 <= month <= 5:  # Spring
            season = "spring"
        elif 6 <= month <= 8:  # Summer
            season = "summer"
        elif 9 <= month <= 11:  # Fall
            season = "fall"
        else:  # Winter
            season = "winter"

    # Process soil pH
    if "Strongly Acidic" in soil_ph:
        recommendations[
            'primary'] = "Apple trees prefer slightly acidic soil. Apply dolomitic lime (calcium magnesium carbonate) to raise pH gradually."
        recommendations['organic_options'].append(
            "Wood ash (1-2 kg per tree applied in a ring around the tree but not touching the trunk)")

    elif "Moderately Acidic" in soil_ph:
        recommendations[
            'primary'] = "This pH range is ideal for apple trees. Maintain with regular organic matter additions."
        recommendations['organic_options'].append("Well-composted manure or leaf mold (5-10 kg per tree annually)")

    elif "Neutral" in soil_ph:
        recommendations[
            'primary'] = "This pH is acceptable for apple trees but slightly higher than ideal. Monitor nutrients carefully."
        recommendations['organic_options'].append(
            "Pine needle mulch or coffee grounds can help maintain slight acidity")

    elif "Slightly Alkaline" in soil_ph:
        recommendations[
            'primary'] = "This pH is higher than ideal for apples. Apply elemental sulfur to gradually lower pH."
        recommendations['organic_options'].append("Elemental sulfur (100-200g per tree) applied in early spring")
        recommendations['organic_options'].append("Conifer needles or oak leaf mulch to help acidify soil gradually")

    elif "Strongly Alkaline" in soil_ph:
        recommendations[
            'primary'] = "This pH is too high for optimal apple growth. Apply elemental sulfur and incorporate peat moss or composted pine bark into soil."
        recommendations['organic_options'].append("Elemental sulfur (200-300g per tree) applied in early spring")
        recommendations['organic_options'].append("Ferrous sulfate as a foliar spray (2-5g per liter of water)")

    # Process NPK levels
    if "Low N" in soil_npk:
        recommendations[
            'secondary'] = "Nitrogen deficiency detected. Apply nitrogen-rich fertilizers split into multiple applications."
        recommendations['organic_options'].append("Blood meal (12% N): 0.5-1 kg per tree")
        recommendations['organic_options'].append("Alfalfa meal (4% N): 2-3 kg per tree")
        recommendations['organic_options'].append(
            "Fish emulsion (5% N): 500ml diluted in 10L water, applied monthly during growing season")

    elif "Medium N" in soil_npk:
        if season == "spring":
            recommendations[
                'secondary'] = "Moderate nitrogen appropriate for vegetative growth. Apply balanced organic fertilizer."
            recommendations['organic_options'].append("Compost tea application bi-weekly")
            recommendations['organic_options'].append("Balanced organic fertilizer (5-5-5): 1-2 kg per tree")

    elif "High N" in soil_npk:
        recommendations[
            'secondary'] = "Nitrogen levels are high. Avoid additional nitrogen fertilizers this season to prevent excessive vegetative growth at the expense of fruiting."
        recommendations['organic_options'].append("Apply potassium and phosphorus-rich amendments to balance nutrients")
        recommendations['organic_options'].append("Rock phosphate: 1-2 kg per tree")
        recommendations['organic_options'].append("Greensand or wood ash for potassium: 1 kg per tree")

    # Application methods based on season
    if season == "spring":
        recommendations[
            'application_method'] = "Apply fertilizers in a ring around the tree at the drip line, not touching the trunk. Water thoroughly after application."
        recommendations[
            'timing'] = "Apply main fertilizer dose when buds begin to swell, with follow-up applications every 4-6 weeks through June."

    elif season == "summer":
        recommendations[
            'application_method'] = "Apply light foliar feeds during fruit development phase. Avoid heavy nitrogen application."
        recommendations[
            'timing'] = "Apply calcium foliar sprays every 2-3 weeks to prevent bitter pit in developing fruit."
        recommendations['organic_options'].append("Seaweed extract foliar spray: 5ml per liter of water")
        recommendations['organic_options'].append("Calcium chloride foliar spray: 5g per liter of water")

    elif season == "fall":
        recommendations[
            'application_method'] = "Apply amendments after harvest but before ground freezes. Focus on soil building for next season."
        recommendations[
            'timing'] = "Apply compost and slow-release amendments in October/November to build soil for spring."
        recommendations['organic_options'].append("Compost: 5-10cm layer spread under the canopy")
        recommendations['organic_options'].append("Cover crop seeding: white clover or winter rye")

    elif season == "winter":
        recommendations[
            'application_method'] = "Focus on planning and soil testing rather than application during dormant period."
        recommendations['timing'] = "Plan for early spring applications when soil thaws."

    return recommendations


def get_pesticide_recommendations(soil_ph, soil_npk, weather_data):
    """Generate pesticide recommendations for apple farming based on soil health and weather data."""
    recommendations = {
        'preventative': [],
        'pest_specific': [],
        'disease_specific': [],
        'application_tips': '',
        'organic_options': []
    }

    # Extract weather conditions if available
    humidity = 50  # Default moderate humidity
    temp = 20  # Default moderate temperature
    if weather_data:
        humidity = weather_data.get('humidity', 50)
        temp = weather_data.get('temp', 20)

    # Preventative measures (always recommended)
    recommendations['preventative'] = [
        "Maintain orchard sanitation by removing fallen leaves and fruit",
        "Prune trees annually to improve air circulation and light penetration",
        "Install sticky traps to monitor pest populations",
        "Encourage beneficial insects with companion planting (yarrow, dill, fennel)"
    ]

    # Pest-specific recommendations based on season and conditions
    month = datetime.now().month

    # Spring recommendations (bud break through bloom)
    if 3 <= month <= 5:
        recommendations['pest_specific'] = [
            "Apply dormant oil before bud break to smother overwintering insects and eggs",
            "Monitor for apple aphids and apply insecticidal soap if detected",
            "Install codling moth traps at bloom time"
        ]

        recommendations['disease_specific'] = [
            "Apply copper or sulfur fungicide before bud break for apple scab prevention",
            "Begin fire blight prevention during bloom if conditions are warm and humid"
        ]

        if humidity > 70:
            recommendations['disease_specific'].append(
                "Increase fungicide application frequency for apple scab due to high humidity conditions"
            )

    # Summer recommendations (post-bloom through fruit development)
    elif 6 <= month <= 8:
        recommendations['pest_specific'] = [
            "Monitor for codling moth and apply targeted controls 10 days after peak moth flight",
            "Check for apple maggot fly and hang red sticky traps",
            "Scout for spider mites during hot, dry periods"
        ]

        recommendations['disease_specific'] = [
            "Continue fungicide program for summer diseases like sooty blotch and flyspeck",
            "Monitor for cedar apple rust if cedar trees are in vicinity"
        ]

        if temp > 25 and humidity < 50:
            recommendations['pest_specific'].append(
                "Increase monitoring for spider mites due to hot, dry conditions favorable for their development"
            )

    # Fall recommendations (harvest and post-harvest)
    elif 9 <= month <= 11:
        recommendations['pest_specific'] = [
            "Apply trunk guards to prevent rodent damage in winter",
            "Clean up all dropped fruit to prevent pest overwintering"
        ]

        recommendations['disease_specific'] = [
            "Apply one final fungicide spray after harvest to reduce disease pressure next season",
            "Remove any cankers or diseased branches during fall cleanup"
        ]

    # Winter recommendations (dormant season)
    else:
        recommendations['pest_specific'] = [
            "Apply winter oil spray during dormant period to control overwintering pests",
            "Check rodent guards and fencing"
        ]

        recommendations['disease_specific'] = [
            "Prune out fire blight cankers and other diseased wood during dormancy",
            "Plan spray schedule for coming season based on previous year's disease pressure"
        ]

    # Organic pesticide options
    recommendations['organic_options'] = [
        "Neem oil: 5-10ml per liter of water for insect pests",
        "Bacillus thuringiensis (Bt): For caterpillar control including codling moth",
        "Insecticidal soap: For soft-bodied insects like aphids and mites",
        "Kaolin clay: As a protective barrier against insects and sunburn",
        "Spinosad: For leafroller and codling moth control",
        "Sulfur or copper-based fungicides: For disease prevention (use according to organic standards)"
    ]

    # Application tips
    recommendations['application_tips'] = (
        "Apply sprays in early morning or evening to avoid harming beneficial insects. "
        "Ensure complete coverage including leaf undersides. "
        "Always follow product instructions for organic certification requirements. "
        "Rotate organic pesticides to prevent resistance development."
    )

    return recommendations

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
