from flask import Flask, render_template, request, session, flash, send_file

import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aaa'


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
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2citrustdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb  ")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/AFarmerInfo")
def AFarmerInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2citrustdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM farmertb  ")
    data = cur.fetchall()
    return render_template('AFarmerInfo.html', data=data)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2citrustdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
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

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2citrustdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO farmertb VALUES ('','" + name + "','" + mobile + "','" + email + "','" + address + "','" + uname + "','" + password + "')")
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

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2citrustdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from farmertb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('FarmerLogin.html')
        else:

            session['mob'] = data[2]

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2citrustdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM farmertb where username='" + username + "' and Password='" + password + "'")
            data = cur.fetchall()
            flash("Login successfully")
            return render_template('FarmerHome.html', data=data)


@app.route("/FarmerHome")
def FarmerHome():
    fname = session['fname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2citrustdb')
    cur = conn.cursor()
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
        input = request.body

        return render_template('Predict.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
