from os import write
from flask import Flask ,render_template , request
import nltk
from nltk.chat.util import Chat
from flask_sqlalchemy import SQLAlchemy
import random
import rsa

# encription and decription message step

#public_key,private_key=rsa.newkeys(1024)

#saving the public key and private key 
#which is used to encript and decript the message 
#we are save permanantell the key in file , so simmilar key used to encript and decript the message
#we have save the key after the we have commant out the code becouse we dont want the key overight and change
#code run succesfull and we have save the file and comment out the code


# with open("public.pem",'wb') as f:
#     f.write(public_key.save_pkcs1("PEM"))

# with open("private.pem",'wb') as f:
#     f.write(private_key.save_pkcs1("PEM"))

#read the key
with open("public.pem",'rb') as f:
    public_key=rsa.PublicKey.load_pkcs1(f.read())

with open("private.pem",'rb') as f:
    private_key=rsa.PrivateKey.load_pkcs1(f.read())

#Flask instalization
app = Flask(__name__)
#data base insillize
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/chat_bots'
db = SQLAlchemy(app)
db.create_all()
db.session.commit()

qa_pairs = [    [ 'what is your owner name' ,                               ['ishu'] ]  ,
                [ '(.*)name' ,                                              [ 'ishu kumar' ] ]  ,           
                [ 'what is your favourate colour' ,                         ['black'] ]  ,
                [ 'what is your age'              ,                         [ '12' ] ]                     ,
                [ 'what is your favourate book'    ,                        ['Java'] ]        ,
                [ 'what is your favourate food' ,                           [ 'chiken' ] ]      ,                                      
                [ 'who is your creater' ,                                  [ 'ishu kumar' ] ]       ,       
                [ 'what is the favourate colour of your owner' ,            ['black'] ]    ,            
                [ '(hi|HI|Hi|hey|HEY|Hey|HELLO|Hello|hello)',               [' \t hello 👋 \n how can i help u'  ,  '👋 '] ] ,            
                [ '(.*)(location|city|address|place|Place) ?',              ['khagaria bihar']   ]   ,
                [ '(.*)contact(.*)' ,                                       ['call - 7004718739 for more information ℹ '] ]   ,
                [  '(.*)weather(.*)' ,                                      ['it cool 😎 ']    ] ,
                [ '(.*)',                                                   ['sorry']  ]
                
            ]

cb = Chat(qa_pairs)

    
class chat_bots_encription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    enc = db.Column(db.String(20), unique=False, nullable=False)
    decp = db.Column(db.String(20), unique=False, nullable=False)


@app.route('/',methods=['GET','POST'])
def chatbot_responses():
    response=''
    if request.method == 'POST':
        msg = request.form['name']
        response= cb.respond(msg)
        
        name = request.form.get('name')
        #encrypt the message
        enc=rsa.encrypt(name.encode(),public_key)
        #decript the message
        decp=rsa.decrypt(enc,private_key)
        decp=decp.decode()


        #add to data base
        entry=chat_bots_encription(decp=decp,enc=enc,name=name)
        #entry=chat_bots_encription(enc=enc,name=name)
        db.session.add(entry)
        db.session.commit()


    return render_template('database_of_chatbot.html',response1=response)

if __name__ == '__main__':
    app.run(debug=True)
        
           
