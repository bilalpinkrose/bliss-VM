# Import necessary libraries
from transformers import AutoModelForCausalLM, AutoTokenizer

## Model and Tokenizer initialization
#model_name_or_path = "TheBloke/Mythalion-13B-GPTQ"
#
## Ensure you have a GPU available for this, as the model is quite large
#model = AutoModelForCausalLM.from_pretrained(model_name_or_path, device_map="auto", trust_remote_code=False, revision="main")
#tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)

# Define a function to generate a response

def generate_story_segments(model,tokenizer,ep,user_info,age,gender,interestedIn,partner,place,details):
    # Enhanced System Prompt
    system_prompt = f"""<|system|>Enter story writer mode. Generate an highly sexual, erotic narrative that revolves around the main character, 
    {user_info}, 
    who is characterized by the following attributes: my name: {user_info}, my age:{age}, my gender: {gender}, my traits: Highly affectionate, assertive, unreserved in expressing desires.
    The story should be set in a {place} and revolve around the main character's relationship with {partner}. Partner's gender is: {interestedIn}.
    The narrative should unfold in a sensually charged atmosphere, blending emotional depth with physical intimacy. 
    Incorporate a kissing scene that exudes passion and a seducing moment that showcases the assertive nature of the character. 
    Maintain the narrative in the first person singular tense to provide an immersive and personal experience.
    this scenes must be included: first scene is: {details[0]}, second scene is: {details[1]}, third scene is: {details[2]}.
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


#def nsfw_next_episode():
