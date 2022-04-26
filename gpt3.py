import os
import openai
import json
import requests
from contentfilter import is_too_toxic
from dotenv import load_dotenv
import random

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
# 4/23 TODO: PULL FIRST, AND THEN SHUFFLE PREPROCESSED AND ACCEPTED/REJECTEDMESSAGES. TAKE RANDOM 3 AND LAST ONES.
# USE NORMAL PUSHING PROCESS THEN PUSH TO HEROKU APP using "git push heroku main" ON TOP OF THAT 
def gpt3Rephrase(message, acceptedValues, rejectedValues): # these all will need changed parameters to message, AND acceptedMessages which is formatted correctly
  #print("Accepted values: ", acceptedValues)
  if (is_too_toxic(message)):
    return "message inappropriate"
  completedSample = ""
  completedSampleR = ""
  samples = [
  "The food is very good. --> The food is superb.", "What do you do? --> How do you like to spend your day?",
  "I really don't like that --> I actually oppose that."]
  samplesR = ["The food is good --> The food is alright", 
  "I like to play outside --> I love to play outside", "That sounds fun --> That is fun"]
  for i in range(len(acceptedValues) - 1): #because this isn't going to be factored in the random, no double counting
    completedSample += acceptedValues[i]['original']
    completedSample += " --> "
    completedSample += acceptedValues[i]['rephrased']
    completedSample += "\n"
    samples.append(completedSample)
    completedSample = ""
  randomSamples = random.sample(samples, 3) # this needs adequate size but we guarantee it with 3 bad examples

  for i in range(len(rejectedValues) - 1): #because this isn't going to be factored in the random, no double counting
    completedSampleR += rejectedValues[i]['original']
    completedSampleR += " --> "
    completedSampleR += rejectedValues[i]['rephrased']
    completedSampleR += "\n"
    samplesR.append(completedSampleR)
    completedSampleR = ""
  randomSamplesR = random.sample(samplesR, 3)
  preprocessedStrings = ""
  #perform a merging process similar to merge sort to alternate them
  i = 0
  j = 0
  count = 0
  while (i < len(randomSamples) and j < len(randomSamplesR)):
    if (count % 2 == 0):
      preprocessedStrings += "Good example:"
      preprocessedStrings += "\n"
      preprocessedStrings += randomSamples[i]
      preprocessedStrings += "\n"
      i += 1
    if (count % 2 == 1):
      preprocessedStrings += "Bad example:"
      preprocessedStrings += "\n"
      preprocessedStrings += randomSamplesR[j]
      preprocessedStrings += "\n"
      j += 1
    count += 1
  while (i < len(randomSamples)):
    preprocessedStrings += "Good example:"
    preprocessedStrings += "\n"
    preprocessedStrings += randomSamples[i]
    preprocessedStrings += "\n"
    i += 1
  while (j < len(randomSamplesR)):
    preprocessedStrings += "Bad example:"
    preprocessedStrings += "\n"
    preprocessedStrings += randomSamplesR[j]
    preprocessedStrings += "\n"
    j += 1
  lastValueString = "Good example:"
  lastValueString += "\n"
  lastValueString += acceptedValues[len(acceptedValues) - 1]['original']
  lastValueString += " --> "
  lastValueString += acceptedValues[len(acceptedValues) - 1]['rephrased']
  preprocessedStrings += lastValueString
  preprocessedStrings += "\n" #separator
  lastValueStringR = "Bad example:"
  lastValueStringR += "\n"
  lastValueStringR += rejectedValues[len(rejectedValues) - 1]['original']
  lastValueStringR += " --> "
  lastValueStringR += rejectedValues[len(rejectedValues) - 1]['rephrased']
  preprocessedStrings += lastValueStringR
  
  

  
  
  #print(acceptedValues[0]['rephrased']) # these are rephrased
  #print(acceptedValues[0]['original']) # these are original
  prompt = \
  f"""
	I am a sentence rephrasing bot. I will rephrase any sentence you give me.
	{preprocessedStrings}
	{message} -->""" # above message put {parsed_db}
  # return prompt # testing prompt correctness.
  response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    temperature=0,
    max_tokens=60,
    top_p=1,
    frequency_penalty=0.4,
    presence_penalty=0
  )
  print("This is the prompt", prompt)
  #data = requests.get("http://localhost:5000/rephrase-requests")
  #data_json = data.json()

  #print("type of data")
  response_dict = response["choices"][0] # was a pain parsing this, save lines 38 and 39
  parsed_response = response_dict.text.strip() #this still has newlines in it. 
  parsed_response = parsed_response.replace("\n", "")
  if (is_too_toxic(parsed_response)):
    return "message inappropriate"

  return parsed_response

def gpt3SentenceCompletion(message, acceptedValues, rejectedValues): #honestly this should be renamed to "commands or misc or something else"
  if (is_too_toxic(message)):
    return "message inappropriate"
  print(acceptedValues)
  if len(acceptedValues) == 0:
    acceptedValues = []
  token = len(message) - 1
  while (message[token] == " "):
    token = token - 1
  message = message[:token + 1]
  completedSample = ""
  completedSampleR = ""
  samples = [
  "I can't get over --> I can't get over how incredible the human world is.",
  "He's building  --> He's building an Army of Souls to attack the human world.", "Treat others --> Treat others how you wish to be treated."]
  samplesR = ["You are -- > You are not good", 
  "I am --> I am a bot", "That sounds --> That sounds good"]
  for i in range(len(acceptedValues) - 1): #because this isn't going to be factored in the random, no double counting
    completedSample += acceptedValues[i]['original']
    completedSample += " --> "
    completedSample += acceptedValues[i]['rephrased']
    completedSample += "\n"
    samples.append(completedSample)
    completedSample = ""
  randomSamples = random.sample(samples, 3) # this needs adequate size but we guarantee it with 3 bad examples

  for i in range(len(rejectedValues) - 1): #because this isn't going to be factored in the random, no double counting
    completedSampleR += rejectedValues[i]['original']
    completedSampleR += " --> "
    completedSampleR += rejectedValues[i]['rephrased']
    completedSampleR += "\n"
    samplesR.append(completedSampleR)
    completedSampleR = ""
  randomSamplesR = random.sample(samplesR, 3)
  preprocessedStrings = ""
  #perform a merging process similar to merge sort to alternate them
  i = 0
  j = 0
  count = 0
  while (i < len(randomSamples) and j < len(randomSamplesR)):
    if (count % 2 == 0):
      preprocessedStrings += "Good example:"
      preprocessedStrings += "\n"
      preprocessedStrings += randomSamples[i]
      preprocessedStrings += "\n"
      i += 1
    if (count % 2 == 1):
      preprocessedStrings += "Bad example:"
      preprocessedStrings += "\n"
      preprocessedStrings += randomSamplesR[j]
      preprocessedStrings += "\n"
      j += 1
    count += 1
  while (i < len(randomSamples)):
    preprocessedStrings += "Good example:"
    preprocessedStrings += "\n"
    preprocessedStrings += randomSamples[i]
    preprocessedStrings += "\n"
    i += 1
  while (j < len(randomSamplesR)):
    preprocessedStrings += "Bad example:"
    preprocessedStrings += "\n"
    preprocessedStrings += randomSamplesR[j]
    preprocessedStrings += "\n"
    j += 1
  lastValueString = "Good example:"
  lastValueString += "\n"
  lastValueString += acceptedValues[len(acceptedValues) - 1]['original']
  lastValueString += " --> "
  lastValueString += acceptedValues[len(acceptedValues) - 1]['rephrased']
  preprocessedStrings += lastValueString
  preprocessedStrings += "\n" #separator
  lastValueStringR = "Bad example:"
  lastValueStringR += "\n"
  lastValueStringR += rejectedValues[len(rejectedValues) - 1]['original']
  lastValueStringR += " --> "
  lastValueStringR += rejectedValues[len(rejectedValues) - 1]['rephrased']
  preprocessedStrings += lastValueStringR
  
  prompt = \
  f"""
	I am a sentence completion bot and will complete any sentence you give me.
	Here are some examples:
	{preprocessedStrings}
	Good example:
	{message} -->""" # above message put {parsed_db} 
  # this could be edited, to be more focused towards completing sentence for essays of a particular topic/question.
  print("Prompt is", prompt)
  response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    temperature=0,
    max_tokens=60,
    top_p=1,
    frequency_penalty=0.4,
    presence_penalty=0
  )
  response_dict = response["choices"][0] # was a pain parsing this, save lines 38 and 39
  parsed_response = response_dict.text.strip() #this still has newlines in it. 
  parsed_response = parsed_response.replace("\n", "")
  if (is_too_toxic(parsed_response)):
    return "message inappropriate"

  return parsed_response
  
def gpt3QA(message): 
  """requires a single question."""
  if (is_too_toxic(message)):
    return "message inappropriate"
  qmark = "?"
  message = message.replace("?","")
  #print("Checked message: " + message)
  prompt = \
  f"""
  I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with "Unknown".

  Q: What is human life expectancy in the United States?
  A: Human life expectancy in the United States is 78 years.

  Q: Who was president of the United States in 1955?
  A: Dwight D. Eisenhower was president of the United States in 1955.

  Q: Which party did he belong to?
  A: He belonged to the Republican Party.

  Q: What is the square root of banana?
  A: Unknown

  Q: How does a telescope work?
  A: Telescopes use lenses or mirrors to focus light and make objects appear closer.

  Q: Where were the 1992 Olympics held?
  A: The 1992 Olympics were held in Barcelona, Spain.

  Q: {message}?
  A:""" # above message put {parsed_db}
  response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    temperature=0,
    max_tokens=60,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  response_dict = response["choices"][0] # was a pain parsing this, save lines 38 and 39
  parsed_response = response_dict.text.strip() #this still has newlines in it. 
  parsed_response = parsed_response.replace("\n", "")
  if (is_too_toxic(parsed_response)):
    return "message inappropriate"
  return parsed_response

def gpt3StudyTools(message): 
  if (is_too_toxic(message)):
    return "message inappropriate"
  prompt = \
  f""" I am a bot designed to help a user study by answering the following question: {message}""" # above message put {parsed_db}
  response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    temperature=0,
    max_tokens=60,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  response_dict = response["choices"][0] # was a pain parsing this, save lines 38 and 39
  parsed_response = response_dict.text.strip() #this still has newlines in it. 
  parsed_response = parsed_response.replace("\n", "")
  if (is_too_toxic(parsed_response)):
    return "message inappropriate"
  return parsed_response

def gpt3SummarizeForSecondGrader(message): 
  if (is_too_toxic(message)):
    return "message inappropriate"
  prompt = \
  f""" Summarize this for a second grader: {message}""" # above message put {parsed_db}
  response = openai.Completion.create(
    engine="text-davinci-001",
    prompt=prompt,
    temperature=0,
    max_tokens=60,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  response_dict = response["choices"][0] # was a pain parsing this, save lines 38 and 39
  parsed_response = response_dict.text.strip() #this still has newlines in it. 
  parsed_response = parsed_response.replace("\n", "")
  if (is_too_toxic(message)):
    return "message inappropriate"
  return parsed_response

def gpt3EssayOutline(text, acceptedValues, rejectedValues):
  if (is_too_toxic(text)):
    return "message inappropriate"
  acceptedMessages = ""
  for i in range(len(acceptedValues)):
    acceptedMessages += acceptedValues[i]['original']
    acceptedMessages += " --> "
    acceptedMessages += acceptedValues[i]['rephrased']
    acceptedMessages += "\n"
  response = openai.Completion.create( #greatly simplified this method to not even take accepted values, no point.
  engine="text-davinci-002",
  prompt=f"I am a highly intelligent bot that creates a formal essay outline:\n '{text}'", 
  temperature=0,
  max_tokens=64,
  top_p=1.0,
  frequency_penalty=0.4,
  presence_penalty=0.0
	)
  response = response.choices[0].text.strip()
  if (is_too_toxic(response)):
    return "message inappropriate"
  return response

def gpt3GrammarCorrection(text):
  if (is_too_toxic(text)):
    return "message inappropriate"
  response = openai.Completion.create(
  engine="text-davinci-002",
  prompt=f"I am a highly intelligent bot that corrects sentences to standard English:\n\n '{text}'", 
  temperature=0,
  max_tokens=60,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
	)
  response = response.choices[0].text.strip()
  if (is_too_toxic(response)):
    return "message inappropriate"
  return response


if __name__ == "__main__":
    # put code here
  print(gpt3GrammarCorrection("She no went to the market."))
  print(gpt3EssayOutline("Create an outline for an essay about Walt Disney and his contributions to animation:"))
  print(gpt3SummarizeForSecondGrader("Jupiter is the fifth planet from the Sun and the largest in the Solar System. It is a gas giant with a mass one-thousandth that of the Sun, but two-and-a-half times that of all the other planets in the Solar System combined. Jupiter is one of the brightest objects visible to the naked eye in the night sky, and has been known to ancient civilizations since before recorded history."))
  print(gpt3StudyTools("What are the 5 most important facts about modern history?"))
  print(gpt3Rephrase("That was well done"))
  print(gpt3SentenceCompletion("Gone. Reduced to "))
  print(gpt3QA("Who was the first president of the US"))