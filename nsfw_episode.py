# Import necessary libraries
from transformers import AutoModelForCausalLM, AutoTokenizer
import openai

def generate_story_segments(model,tokenizer,ep,user_info,age,gender,interestedIn,partner,place,tag,categories):
    system_prompt = f"""<|system|>Enter highly sexual erotica writer mode. Generate an highly sexual, erotic narrative that revolves around the main character {user_info},
    the most important parts of the story is {tag} part. You must create the story based on this sex scene: {tag}. Story theme is: {categories}. Write in first person singular tense.

    <|user|>I am characterized by the following attributes: my name: {user_info}, my age:{age}, my gender: {gender}, my traits: Highly affectionate, assertive, unreserved in expressing desires.
    The story should be set in a {place} and revolve around the main character's relationship with {partner}. Partner's gender is: {interestedIn}.
    Maintain the narrative in the first person singular tense to provide an immersive and personal experience.
    Partner's name is:{partner}
    Adhere to these storytelling elements:
     Passionate kissing scene.
     Story theme is: {categories}
     create a {tag} sex scene,
     First person singular narrative style.
     Main idea is:{ep}, write {tag} sex scene.<|model|>
    """
    prompt = system_prompt
    for i in range (3):
        # Tokenize and generate response, no_repeat_ngram_size ve repetition_penalty gerekirse tanımla.
        inputs = tokenizer(prompt, return_tensors='pt', truncation=True, max_length=2500).to('cuda')
        outputs = model.generate(**inputs,
                                max_length=1800,
                                pad_token_id=tokenizer.eos_token_id,
                                do_sample=True,
                                temperature=0.6,
                                no_repeat_ngram_size=4,
                                 )
        # Decode the generated text
        story_segment = tokenizer.decode(outputs[0], skip_special_tokens=True)
        story_segment = story_segment.replace(system_prompt,'')
        story_segment = story_segment.replace('<|system|>', '').replace('<|user|>', '').replace('<|model|>', '')
        if len(story_segment) >=1250:
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

def next_tag_story(model,tokenizer,ep,tag,gender,categories):
    system_prompt = f"""<|system|>Enter highly sexual erotica writer mode. Generate an highly sexual, erotic narrative that revolves around the main character me, my gender is: {gender}
    the most important parts of the story is {tag} part. You must create the story based on this sex scene: {tag}. Story theme is: {categories}. Write in first person singular tense.
    <|user|>this is the story: {ep}

    continue the story with {tag} scenes. and remember my gender is: {gender}. write the story in my first person singular tense. and remember the story is about {tag} scene. Story theme is: {categories}.
    <|model|>
    """
    prompt = system_prompt
    for i in range (3):
        # Tokenize and generate response, no_repeat_ngram_size ve repetition_penalty gerekirse tanımla.
        inputs = tokenizer(prompt, return_tensors='pt', truncation=True, max_length=2500).to('cuda')
        outputs = model.generate(**inputs,
                                max_length=1800,
                                pad_token_id=tokenizer.eos_token_id,
                                do_sample=True,
                                temperature=0.6,
                                no_repeat_ngram_size=4,
                                 )
        # Decode the generated text
        story_segment = tokenizer.decode(outputs[0], skip_special_tokens=True)
        story_segment = story_segment.replace(system_prompt,'')
        story_segment = story_segment.replace('<|system|>', '').replace('<|user|>', '').replace('<|model|>', '')
        if len(story_segment) >=1250:
            return story_segment

    return story_segment


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