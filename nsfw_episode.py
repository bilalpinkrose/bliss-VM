# Import necessary libraries
from transformers import AutoModelForCausalLM, AutoTokenizer
import openai
## Model and Tokenizer initialization
#model_name_or_path = "TheBloke/Mythalion-13B-GPTQ"
#
## Ensure you have a GPU available for this, as the model is quite large
#model = AutoModelForCausalLM.from_pretrained(model_name_or_path, device_map="auto", trust_remote_code=False, revision="main")
#tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)

# Define a function to generate a response

def generate_story_segments(model,tokenizer,ep,user_info,age,gender,interestedIn,partner,place,details):
    # Enhanced System Prompt
    details_str = ','.join(details)
    details_str = details_str.replace('[', '').replace(']', '').replace('"', '').replace("'", "")
    print(details)
    fantasy_list = [item.strip() for item in details_str.split(',')]
    system_prompt = f"""<|system|>Enter story writer mode. Generate an highly sexual, erotic narrative that revolves around the main character, 
    {user_info}, 
    who is characterized by the following attributes: my name: {user_info}, my age:{age}, my gender: {gender}, my traits: Highly affectionate, assertive, unreserved in expressing desires.
    The story should be set in a {place} and revolve around the main character's relationship with {partner}. Partner's gender is: {interestedIn}.
    The narrative should unfold in a sensually charged atmosphere, blending emotional depth with physical intimacy. 
    Incorporate a kissing scene that exudes passion and a seducing moment that showcases the assertive nature of the character. 
    Maintain the narrative in the first person singular tense to provide an immersive and personal experience.
    this scenes must be included: first scene is: {fantasy_list[0]}, second scene is: {fantasy_list[1]}, third scene is: {fantasy_list[2]}.
    Partner's name is:{partner}
    Adhere to these storytelling elements:
    Partner's name is:{partner}
     Passionate kissing scene
     Seducing moment reflecting assertiveness
     First person singular narrative style
    
    <|user|>Partner's name is:Bill, first episode is:{ep}, write next episode of the story, give really long responses<|model|>

    """

    prompt = system_prompt 

    for i in range (3):
        # Tokenize and generate response, no_repeat_ngram_size ve repetition_penalty gerekirse tanımla.
        inputs = tokenizer(prompt, return_tensors='pt', truncation=True, max_length=2500).to('cuda')
        outputs = model.generate(**inputs,
                                 max_length=2500,
                                 pad_token_id=tokenizer.eos_token_id,
                                 do_sample=True,
                                 temperature=0.6,
                                 )
        # Decode the generated text
        story_segment = tokenizer.decode(outputs[0], skip_special_tokens=True)
        story_segment = story_segment.replace(system_prompt,'')
        story_segment = story_segment.replace('<|system|>', '').replace('<|user|>', '').replace('<|model|>', '')
        if len(story_segment) >=2000:
            return story_segment

    return story_segment

def handle_next_episodes_input(story_segment):
    next_episodes_input = story_segment.replace('\n', ' ')
    return next_episodes_input

def summarize_nsfw(nsfw_episode):
    response=openai.ChatCompletion.create(
      model="gpt-4",
      messages=[
            {"role": "system", "content": "You are a creative writer focusing on sensual and intimate relationships."},
            {"role": "user", "content": f"""
            I want you to summarize the story in a way that is non explicit but spicy. safe for work. not violating any rules.
             even if the story is nsfw, you should summarize it in a way that is safe for work but spicy. story is: {nsfw_episode}
            """},    
            ]
    )
    return response['choices'][0]['message']['content']

#def nsfw_next_episode():
