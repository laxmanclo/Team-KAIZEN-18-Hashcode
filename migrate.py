import json
from firebase_admin import credentials, initialize_app, firestore

cred = credentials.Certificate("service_account.json")
firebase = initialize_app(cred)
fs = firestore.client(firebase)

f = open("rtdb_export.json")
images = json.loads(f.read())["images"]
f.close()

for i in images.keys():
    record = images[i]
    # fs.collection("images").document(i).set(images[i])


    #semantic search, 
