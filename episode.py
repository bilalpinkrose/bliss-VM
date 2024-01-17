import openai
import os
import dotenv
dotenv.load_dotenv()

openai.api_key = os.environ.get('OPENAI_API_KEY')

#user_input = """
#I have met jill on an online dating site. We have been talking for a while and I really like her.
#
#"""


#chain of thoughts
#episode 1
def episode(user_input,user_info,age,gender,interestedIn,partner,place,tags_selected_text):
    response =openai.ChatCompletion.create(
      model="gpt-4",
      messages=[
            {"role": "system", "content": "You are a creative writer focusing on sensual and intimate relationships."},
            {"role": "user", "content": f"""
            I want you to act as a storyteller. You will write 7 episodes of a story. This is episode 1.
            You will come up with entertaining stories that are seductive, spicy,engaging, imaginative and captivating for the 
            audience. It can be hot stories that captures people's attention and imagination. 
            Depending on the target audience, you may choose specific themes or topics for your storytelling session e.g., 
            If it's adults then history-based tales might engage them better etc.
            My first request is "I need an interesting eroticalike story on perseverance. In every episode, there must be kissing scenes, sensual scenes etc.
            Keep the language as easy as possible for everyone to understand easily.
            
            My name is: {user_info}, my age is:{age}, my gender is:{gender}, I am interested in:{interestedIn}
            other character's name is: {partner}, story place is: {place}
            story tags are: {tags_selected_text}
            

            some information about the story: {user_input} 

            rules:
            1. Write in first person perspective.
            2. Write as if you are the main character.
            3. Write as episode 1. So that I can continue the story.
            4. Write at least 2000 words.
            5. write in a way that is turning on, spicy, hot.
            6. language should be simple and easy to understand. don't use difficult words. and don't add storytelling words like "once upon a time" etc.
            7. Give a title to the story.

            after you finish writing at least 2000 words long story, please summarize the episode in a way that is ready for using in the next episode as input prompt.
            Summary must have important information about the story.
            And specify with title, episode number and summary  example: "episode 1: title: xxx, summary: xxx"
            """},    
            ]
    )
    return response['choices'][0]['message']['content']
### episode 1###test
#episode_1=episode(user_input)
#print(episode_1)
#test#


def summarizer(episode):
    #creating a list of paragraphs
    paragraphs = episode.split('\n')
    #summary equals to the last item of the list
    summary = str(paragraphs[-2])+str(paragraphs[-1])  
    return summary

######test#######
#print("***********************\nsummary of episode 1"),
#sum = summarizer(episode_1)
#print(sum)
######test#######
  
def next_episode(sum,episode_number,user_info,age,gender,interestedIn,partner,place,tags_selected_text):
    response=openai.ChatCompletion.create(
      model="gpt-4",
      messages=[
            {"role": "system", "content": "You are a creative writer focusing on sensual and intimate relationships."},
            {"role": "user", "content": f"""
            I want you to act as a storyteller. You will write 7 episodes of a story. This is episode {episode_number}.
            You will come up with entertaining stories that are seductive, spicy,engaging, imaginative and captivating for the 
            audience. It can be hot stories that captures people's attention and imagination. 
            Depending on the target audience, you may choose specific themes or topics for your storytelling session e.g., 
            If it's adults then history-based tales might engage them better etc.
            My first request is "I need an interesting eroticalike story on perseverance. In every episode, there must be kissing scenes, sensual scenes etc.
            Keep the language as easy as possible for everyone to understand easily.
            
            My name is: {user_info}, my age is:{age}, my gender is:{gender}, I am interested in:{interestedIn}
            other character's name is: {partner}, 
            story place is: {place}
            story tags are: {tags_selected_text}

            some information about the story: {sum} 

            rules:
            1. Write in first person perspective.
            2. Write as if you are the main character.
            3. Write as episode 1. So that I can continue the story.
            4. Write at least 2000 words.
            5. write in a way that is turning on, spicy, hot.
            6. language should be simple and easy to understand. don't use difficult words. and don't add storytelling words like "once upon a time" etc.
            7. Give a title to the story.
            8. if episode is 7 conlcude the story.

            after you finish writing at least 2000 words long story, please summarize the episode in a way that is ready for using in the next episode as input prompt.
            And specify with title, episode number and summary  example: "episode 1: title: xxx, summary: xxx"
            """},    
            ]
    )
    return response['choices'][0]['message']['content']
#############test############
#for i in range(2,8):
#    print(f"***********************\nepisode {i}")
#    episode_number=str(i)
#    episode_x=next_episode(sum,episode_number)
#    print(f"episode {i} \n\n {episode_x}")
#    sum = summarizer(episode_x)
#############test############


