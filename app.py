from transformers import AutoTokenizer, AutoModelForCausalLM
import openai
from dotenv import load_dotenv
import os
from flask import Flask, request,jsonify
from supabase import create_client, Client
import json
import http.client
import requests
from better_profanity import profanity
from episode import episode, summarizer,next_episode
from nsfw_episode import generate_story_segments,handle_next_episodes_input
from transformers import AutoTokenizer, AutoModelForCausalLM

#load dotenv



load_dotenv()



# Model and Tokenizer initialization
model_name_or_path = "TheBloke/Mythalion-13B-GPTQ"

# Ensure you have a GPU available for this, as the model is quite large
model = AutoModelForCausalLM.from_pretrained(model_name_or_path, device_map="auto", trust_remote_code=False, revision="main")
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)


#supabase
url = 'SUPABASE_URL'
key = 'SUPABASE_KEY'
fcm = 'FCM_KEY'
slackUrl = 'SLACK_URL'
eleven = 'ELEVENLABS_API'
oa = 'OPENAI_API_KEY'
#supabase

slackUrl: str = os.environ.get("SLACK_URL")
eleven: str = os.environ.get("ELEVENLABS_API")
fcm: str = os.environ.get("FCM_KEY")
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
oa: str = os.environ.get('OPENAI_API_KEY')

supabase: Client = create_client(url, key)
#openai

openai.api_key = oa

app = Flask(__name__)

@app.route('/ai', methods=['POST'])
def ai():
  return check_params()

def check_params():
    episode_level = request.form.get('episode_level')
    
    episode_number = request.form.get('episode_number')

    user_id = request.form.get('user')
    if user_id is None:
        print("No user provided", 400)
    prompt = request.form.get('prompt')
    if prompt is None:
        print("No prompt provided", 400)
    device_token = request.form.get('device_token')#new
    if device_token is None:
        print("No device_token provided", 400)
    details = request.form.getlist('details')
    if details is None:
        print("No details provided", 400)
    age = request.form.get('age')#new
    if age is None:
        print("No age provided", 400)
    gender = request.form.get('gender')#user's gender
    if gender is None:
        print("No gender is provided", 400)
    interestedIn = request.form.get('interestedIn')#interested gender
    if interestedIn is None:
        print("No interestedIn is provided", 400)
    place = request.form.get('place')#fuck place
    if place is None:
        print("No place is provided",400)
    partner = request.form.get('partner')#partner name
    if partner is None:
        print("No partner is provided",400)
    user_info =request.form.get('user_info')#partner name
    if user_info is None:
        print("No user_info provided",400)
    return main_events(episode_level,episode_number,user_id,prompt,device_token,details,age,gender,interestedIn,place,partner,user_info)

def main_events(episode_level,episode_number,user_id,prompt,device_token,details,age,gender,interestedIn,place,partner,user_info):
    episode_level = int(episode_level)
    episode_number = int(episode_number)
    if episode_level in (1, 2) and 1 <= episode_number <= 7:
        Episode=episode(prompt,user_info,age,gender,interestedIn,partner,place,details)
        summary=summarizer(Episode)
        Episode=Episode.replace(str(summary),"")
        return jsonify(Episode)


    if episode_level in (3, 4) and 1 <= episode_number <= 7:
        nsfw_episode=generate_story_segments(model,tokenizer,prompt,user_info,age,gender,interestedIn,partner,place,details)
    return jsonify(nsfw_episode)

def handle_generate_episode(user_info,age,gender,interestedIn,partner,place,prompt):
    Episode=episode(user_info,age,gender,interestedIn,partner,place,prompt)
    return Episode



if __name__ == '__main__':
    app.run(port=8000)