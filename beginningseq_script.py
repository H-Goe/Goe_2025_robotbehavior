#copyright (c) Helena Goeddaeus, 2025

import qi
import keyboard
#import time
import sys

# Robot connection details
robotIP = "130.149.242.141"
robotPort = 9559

# Establish session with the robot
try:
    session = qi.Session()
    session.connect("tcp://" + robotIP + ":" + str(robotPort))
    print("Successfully connected to the robot.")
except RuntimeError:
    print("Can't connect to Naoqi at ip \"" + robotIP + "\" on port " + str(robotPort) + ".\n")
    sys.exit(1)

# Services
try:
    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")
    tts_service = session.service("ALTextToSpeech")
    animated_speech_service = session.service("ALAnimatedSpeech")
    
except Exception as e:
    print("Error initializing services: ", e)
    sys.exit(1)

# Settings:
## Variable to set experimental condition (0 = extraverted; 1 = introverted)

expcond = 0

## Voice Speed 
if expcond==0:
    tts_service.setParameter("defaultVoiceSpeed",105)
elif expcond==1:
    tts_service.setParameter("defaultVoiceSpeed",80)
else: print("Voice speed not set due to wrong expcond value. Please adjust and restart.")

## Behaviors from Choregraphe
if expcond ==0:
    behavior_1 = "beginningseq_e_1-fa9596/behavior_1"
    behavior_2 = "beginningseq_e_2-742994/behavior_1"
    behavior_3 = "beginningseq_e_3-171892/behavior_1"
elif expcond==1:
    behavior_1 = "beginningseq_i_1-e46586/behavior_1"
    behavior_2 = "beginningseq_i_2-468fda/behavior_1"
    behavior_3 = "beginningseq_i_3-e9a2b1/behavior_1"
else: print("Behavior files not set due to wrong expcond value. Please adjust and restart.")


# Functions
def wait_howareyou():
    print("""Wait for keyboard input for how-are-you response.""")
    print("""Good --> m
Bad --> x
Repeat --> Space""")
    if expcond ==0:
        while True:
            try:
                if keyboard.is_pressed("space"):
                    tts_service.say("Please repeat your answer: How are you today?") #ToDo: Repeat-schleife
                elif keyboard.is_pressed("x"):
                    tts_service.say("Oh no, I am so sorry to hear that.")
                    break
                elif keyboard.is_pressed("m"):
                    tts_service.say("Great, I am really happy to hear that you are fine!")
                    break
            except Exception as e:
                print("Error in wait_howareyou: ", e)
                break
    else: 
        while True:
            try:
                if keyboard.is_pressed("space"):
                    tts_service.say("Please repeat your answer: How are you. today.") #ToDo: Repeat-schleife
                elif keyboard.is_pressed("x"):
                    tts_service.say("Sorry to hear that.")
                    break
                elif keyboard.is_pressed("m"):
                    tts_service.say("That's nice? mmm")
                    break
            except Exception as e:
                print("Error in wait_howareyou: ", e)
                break

def wait_name():
    print("""Wait for keyboard input for what-is-your-name response.""")
    print("""Continue --> M
Repeat --> Space""")
    while True:
        try:
            if keyboard.is_pressed("space"):
                    tts_service.say("Please repeat your name.") #ToDo: Repeat-schleife
            elif keyboard.is_pressed("m"):
                    break
        except Exception as e:
                print("Error in wait_howareyou: ", e)
                break


# Main program
if __name__ == "__main__":
    try:
        tts_service.say("Hello Helena, I will be waiting for your signal!")
    except Exception as e:
        print("Error in main program: ", e)
#Behavior 1 each
from naoqi import ALProxy

try:
    behavior_manager = ALProxy("ALBehaviorManager", robotIP , robotPort)
    
    installed_behaviors = behavior_manager.getInstalledBehaviors()
    print(installed_behaviors)

    if behavior_manager.isBehaviorInstalled(behavior_1):
        print("Behavior 1: Touch left foot hand or press right foot bumper.")
        behavior_manager.runBehavior(behavior_1)
    
        #if not behavior_manager.isBehaviorRunning(behavior_name):
        #    behavior_manager.runBehavior(behavior_name)
            
        #else:
        #    print("The Application is already running")
            
    else:
        print("The Behavior seems to not be installed")
        
except Exception as e:
    print("Error with starting the behavior: {e}")
        
#key press how are you
wait_howareyou()
#asking for name
if expcond == 0:
    animated_text = "\\rspd=105\\ And what is your name?"
    speech_config = {"bodyLanguageMode": "contextual"}  # Kann "contextual", "random" oder "disabled" sein
    animated_speech_service.say(animated_text, speech_config)
else: tts_service.say("what is \\rspd=65\\ your \\toi=lhp\\ n'e&Im*?\\eos=0\\ \\toi=orth\\")
#wait to continue
wait_name()
#Behavior 2 each
print("Behavior 2:")
behavior_manager.runBehavior(behavior_2)
#key press are you here for experiment? (continue or repeat)
#and continue with behavior 3 or break
print("""Wait for keyboard input for here-for-experiment response.""")
print("""Yes --> m
No --> x
Repeat --> Space""")
while True:
    try:
        if keyboard.is_pressed("space"):
            tts_service.say("Please repeat your answer.")
        elif keyboard.is_pressed("x"):
            tts_service.say("Oh, sorry. Please talk to the instructor then.")
            break
        elif keyboard.is_pressed("m"):
            #Behavior 3 each
            print("Behavior 3:")
            behavior_manager.runBehavior(behavior_3)
            #Please get our instructor to start the experiment. each
            if expcond == 0:
                animated_text = "Please ask our instructor to start the experiment."
                speech_config = {"bodyLanguageMode": "contextual"}  # Kann "contextual", "random" oder "disabled" sein
                animated_speech_service.say(animated_text, speech_config)
            else: tts_service.say("Please ask our instructor to start the experiment")
            break
    except Exception as e:
        print("Error in wait_yesno: ", e)
        break

print("End of introduction code: Please start experiment")


#are you here for the experiment?
#no: Oh, sorry. Please talk to the instructor then.

