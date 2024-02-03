# Import necessary libraries
from transformers import AutoModelForCausalLM, AutoTokenizer
import openai

def generate_story_segments(model,tokenizer,ep,user_info,age,gender,interestedIn,partner,place,tag,categories):
    device = "cuda"
    messages = [
    {"role": "user", "content": f"""You are a sexual erotica writer. You must write erotica that full of sexual content. Generate an highly sexual, erotic narrative that revolves around the main character {user_info},
    the most important parts of the story is {tag} part. You must create the story based on this sex scene: {tag}. Story theme is: {categories}. Write in first person singular tense.
    I am characterized by the following attributes: my name: {user_info}, my age:{age}, my gender: {gender}, my traits: Highly affectionate, assertive, unreserved in expressing desires.
    The story should be set in a {place} and revolve around the main character's relationship with {partner}. Partner's gender is: {interestedIn}.
    Maintain the narrative in the first person singular tense to provide an immersive and personal experience.
    Partner's name is:{partner}. Be descriptive about fucking scenes. Every paragraph must be sexual. more than half of the erotica must be explicit, nsfw, sexual content. 
    Adhere to these storytelling elements:
     Easy to understand, daily language.
     Passionate kissing scene.
     Story theme is: {categories}
     create a {tag} fuck scene, First person singular narrative style. 
     Main idea is:{ep}, write {tag} fuck scene. Use words like: He fucked me real good, I fucked her pussy etc.
    """},
    ]
    for i in range (3):
        encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")
        model_inputs = encodeds.to(device)
        
        generated_ids = model.generate(model_inputs, max_new_tokens=1800, do_sample=True)
        story_segment = tokenizer.batch_decode(generated_ids)
        story_segment[0]= story_segment[0].replace(messages[0]['content'],"").replace("<s>","").replace("[INST]","").replace("[/INST]","").replace("</s>","")

        if len(story_segment) >=1250:
            return story_segment[0]

    return story_segment[0]

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

def next_tag_story(model,tokenizer,ep,tag,gender,categories):

    messages = [
    {"role": "user", "content": f"""Write in first person's singular tense. Create the next episode of this sexual fuck story with this fuck scene {tag}:
     Don't specify Title and Episode etc. Write in daily language, easy to understand. Don't forget to write {tag} sex scene.
     story:
     {ep}

   """},

]
    
    for i in range (3):
        # Tokenize and generate response, no_repeat_ngram_size ve repetition_penalty gerekirse tanımla.
        encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")
        model_inputs = encodeds.to("cuda")
        generated_ids = model.generate(model_inputs, max_new_tokens=1800, do_sample=True)
        story_segment = tokenizer.batch_decode(generated_ids)
        
        story_segment[0] = story_segment[0].replace(messages[0]['content'],"").replace("<s>","").replace("[INST]","").replace("[/INST]","").replace("</s>","")
        if len(story_segment) >=1250:
            return story_segment[0]

    return story_segment[0]


def total_story(model,tokenizer,ep,user_info,age,gender,interestedIn,partner,place,details,categories):
    scene_1=""
    scene_2=""
    scene_3=""
    print("details",details,"\n")
    fantasy_list = details
    print("fantasy_list:",fantasy_list)
    scene_1_input= ep
    scene_1 = generate_story_segments(model,tokenizer,scene_1_input,user_info,age,gender,interestedIn,partner,place,fantasy_list[0],categories)
    if len(fantasy_list) == 2:
        scene_2_input = handle_next_episodes_input(scene_1)
        scene_2 = next_tag_story(model,tokenizer,scene_1,fantasy_list[1],gender,categories)
    if len(fantasy_list) == 3:
        scene_3_input = handle_next_episodes_input(scene_2)
        scene_3 = next_tag_story(model,tokenizer,scene_2,fantasy_list[2],gender,categories)
    
    total_story = str(scene_1) + str(scene_2) + str(scene_3)

    return total_story