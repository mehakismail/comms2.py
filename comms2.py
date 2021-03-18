import socketio
import eventlet
import json
import os
import time
import functions
import subprocess

# print(os.environ['I_1'])

sio = socketio.Server(cors_allowed_origins=[])
app = socketio.WSGIApp(sio)

@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)
    time.sleep(1)
      
@sio.on('__RAM')
def message(sid, data):
    print(sid, data)
    sio.emit('__RAM', data)
   
@sio.on('__STORAGE')
def message(sid, data):
    print(sid, data)
    sio.emit('__STORAGE', data)

@sio.on('__RESUME_TEST')
def message(sid, data):
    print(sid, data)
    sio.emit('__RESUME_TEST', data)

@sio.on('__HALT_TEST')
def message(sid, data):
    print(sid, data)
    sio.emit('__HALT_TEST', data)

@sio.on('__INIT_TEST')
def message(sid, data):
    print(sid, data)
    sio.emit('__INIT_TEST', data)
    
@sio.on('__SETTINGS')
def message(sid):
    print(sid)
    try:
        settings=functions.read_settings()
        sio.emit('__SETTINGS',settings)
    except Exception as e:
        sio.emit('__SETTINGS','unable to read settings')

@sio.on('__UPDATE_SETTINGS')
def on_message(sid,data):
    print(data)
    print("new settings recieved-------------------------------------------")
    
##    print(data)
    try:
        functions.update_settings(data)
        sio.emit('__UPDATE_SETTINGS','OK')
    except Exception as e:
        print("Unable to Update",e)
        sio.emit('__UPDATE_SETTINGS', 'UNABLE TO UPDATE')

@sio.on('__SOUND_PLAY')
def message(sid, data):
    print(sid, data)
    if data['play']== True :
        functions.play_sound()

@sio.on('__SOUND_PE_PLAY')
def message(sid, data):
    print(sid, data)
    print("inside sound_PE_play")
    if data['play']== True :
        functions.play_sound()
        functions.play_sound()
        functions.play_sound()

@sio.on('__EMAIL_RESULTS')
def message(sid, data):
    print(sid, data)
    print("insida email results")
##    print(data)
    try:
        functions.send_email(data)
        sio.emit('__EMAIL_RESULTS', 'Email Sent')
    except Exception as e:
        print("unable to email", e)

@sio.on('__RESULTS')
def message(sid, data):
    print(sid, data)
    sio.emit('__RESULTS', data)
    

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)


@sio.on('__ELEMENTS')
def message(sid):
    print(sid)
   
    with open("/home/pi/colloid-generator/electrolysis/elements/elements.json","r") as f:

        data=json.load(f)
##        print(data)
        sio.emit('__ELEMENTS', data)

@sio.on('__SHUTDOWN')
def message(sid, data):
    print(sid, data)

    if data['action']=='shutdown':
        time.sleep(5)
        os.system('sudo poweroff')

@sio.on('__UPDATE_ELEMENT')
def message(sid, data):
##    print(sid, data)
    print("UPDATE ELEMENT")
    element = data
    print("data recieved====", element)
    try:
        with open('/home/pi/colloid-generator/electrolysis/elements/elements.json','r+') as f:

            data=json.load(f)
        ##    print(data[0])
            for i in range(len(data)):
                if data[i]["chemical_symbol"] == element["chemical_symbol"]:
                    data[i]["element_name"] = element["element_name"]
                    data[i]["chemical_symbol"]= element["chemical_symbol"]
                    data[i]["decomposition"]= element["decomposition"]
                    data[i]["polarity"]= element["polarity"]
                    data[i]["element_fr"]=element["element_fr"]
                    data[i]["element_en"]=element["element_en"]
                    data[i]["element_it"]=element["element_it"]
                    data[i]["element_de"]=element["element_de"]
                    data[i]["element_es"]=element["element_es"]
                    break

        # Output the updated file with pretty JSON                                      
        ##open("updated-file.json", "w").write(
            print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
            f.seek(0)  # rewind
            f.truncate()
            json.dump(data, f)
            sio.emit('__UPDATE_ELEMENT', "OK")
    except Exception as e:
        
        sio.emit('__UPDATE_ELEMENTS', "Unable to update")
        print("Unable to Update")


@sio.on('__ADD_ELEMENT')
def message(sid, data):
##    print(sid, data)
    print("ADD ELEMENT")
    x=data

    try:
        with open('/home/pi/colloid-generator/electrolysis/elements/elements.json','r+') as f:

            data=json.load(f)
            data.append((x))

            print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
            f.seek(0)  # rewind
            f.truncate()
            json.dump(data, f)
        sio.emit('__ADD_ELEMENT', "OK")

    except Exception as e:
        sio.emit('__ADD_ELEMENT', "Unable to ADD")
        print("Unable to ADD")

@sio.on('__DELETE_ELEMENT')
def message(sid, data):
##    print(sid, data)
    print("DELETE ELEMENT")
    element= data

    try :
        with open('/home/pi/colloid-generator/electrolysis/elements/elements.json','r+') as f:

            data=json.load(f)
        ##    print(data[0])
            for i in range(len(data)):
                if data[i]["chemical_symbol"] == element["chemical_symbol"]:
                    data.pop(i)
                    break

        # Output the updated file with pretty JSON                                      
        ##open("updated-file.json", "w").write(
            print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
            f.seek(0)  # rewind
            f.truncate()
            json.dump(data, f)
        sio.emit('__DELETE_ELEMENT', "OK")
            
    except Exception :
        sio.emit('__DELETE_ELEMENT', "Unable to delete")
        print("Unable to delete")
    
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 3000)), app)
    
        
    
        
