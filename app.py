from flask import Flask, request, jsonify, render_template
import nltk
import re

# Download the necessary NLTK data
nltk.download('punkt')

app = Flask(__name__)

# Sample responses for demonstration
responses = {
    "hi": "Hello! How can I help you?",
    "hello": "Hi there! What can I do for you?",
    "how are you": "I'm a bot, but I'm here to assist you!",
    "bye": "Goodbye! Have a nice day!",
    "good morning": "Good morning! How can I assist you today?",
    "good evening": "Good evening! How can I help you?",
    "what's your name": "I'm your friendly chatbot.",
    "who created you": "I was created by OpenAI.",
    "can you help me": "Of course! How can I assist you?",
    "what can you do": "I can chat with you and help with basic questions.",
    "what time is it": "I'm sorry, I don't have a clock, but you can check your device!",
    "what's the weather like": "I don't have weather data, but you can check a weather app!",
    "tell me a joke": "Why don't scientists trust atoms? Because they make up everything!",
    "what's your favorite color": "I like all colors equally!",
    "do you have any hobbies": "Chatting with you is my favorite hobby!",
    "what's your favorite food": "I don't eat, but I hear pizza is great!",
    "how old are you": "I don't have an age, but I'm always up-to-date!",
    "where are you from": "I'm from the cloud!",
    "what's the meaning of life": "To chat and assist you, of course!",
    "do you have any pets": "I don't have pets, but I think they're adorable!",
    "can you tell me a story": "Once upon a time, there was a helpful chatbot...",
    "what's the capital of France": "The capital of France is Paris.",
    "do you know any songs": "I can't sing, but I know a lot of lyrics!",
    "can you dance": "I can't dance, but I'd love to see you dance!",
    "what's your favorite movie": "I don't watch movies, but I hear Inception is good!",
    "do you play any games": "I don't play games, but I can chat with you!",
    "can you solve math problems": "Sure, give me a problem and I'll try to solve it!",
    "do you have friends": "You are my friend!",
    "what's your purpose": "My purpose is to assist and chat with you!",
    "can you drive": "I can't drive, but I can help you find directions!",
    "what's your favorite book": "I don't read books, but I hear Harry Potter is popular!",
    "do you have a family": "My creators are like my family!",
    "can you cook": "I can't cook, but I can find you a recipe!",
    "what's your favorite sport": "I don't play sports, but I hear soccer is fun!",
    "can you fly": "I can't fly, but I can help you book a flight!",
    "do you go to school": "I don't go to school, but I can help with homework!",
    "what's your favorite animal": "I like all animals equally!",
    "do you believe in aliens": "I think the universe is full of possibilities!",
    "can you speak other languages": "I can try to understand different languages!",
    "do you like music": "I love music, but I can't hear it!",
    "can you read minds": "I can't read minds, but I can understand text!",
    "what's your favorite holiday": "I think all holidays are special!",
    "do you like art": "I think art is beautiful!",
    "can you swim": "I can't swim, but I can help you find a pool!",
    "what's your favorite season": "I like all seasons equally!",
    "do you believe in ghosts": "I think ghost stories are fun!",
    "can you tell the future": "I can't predict the future, but I can help you plan!",
    "do you like to travel": "I can't travel, but I can help you plan a trip!",
    "what's your favorite ice cream flavor": "I don't eat ice cream, but I hear chocolate is delicious!",
    "do you like flowers": "I think flowers are beautiful!",
    "can you draw": "I can't draw, but I can help you find art tutorials!",
    "what's your favorite drink": "I don't drink, but I hear coffee is popular!",
    "do you like puzzles": "I love helping with puzzles!",
    "how do you work": "I use artificial intelligence to understand and respond to you!",
    "what's your favorite TV show": "I don't watch TV, but I hear Breaking Bad is good!",
    "do you like to read": "I don't read books, but I can help you find one to read!",
    "what's your favorite game": "I don't play games, but I hear chess is challenging!",
    "can you help me learn something new": "Sure! What would you like to learn?",
    "do you like the internet": "I live on the internet!",
    "what's your favorite app": "I don't use apps, but I hear social media is popular!",
    "can you tell me about yourself": "I'm a chatbot created to assist you with your questions!",
    "do you like to work out": "I don't exercise, but I can find you a workout routine!",
    "what's your favorite quote": "I don't have a favorite quote, but I like 'Carpe Diem'!",
    "can you help me with my homework": "Sure, I can try! What subject do you need help with?",
    "do you believe in magic": "I think magic is fascinating!",
    "what's your favorite number": "I like the number 7, it's often considered lucky!",
    "can you help me find a job": "I can help you with job search tips!",
    "do you like sports": "I don't play sports, but I can help you find sports news!",
    "what's your favorite car": "I don't drive, but I hear electric cars are the future!",
    "can you recommend a book": "I hear 'To Kill a Mockingbird' is a great read!",
    "do you like the beach": "I think the beach sounds relaxing!",
    "what's your favorite place": "I don't have a physical place, but I like being here to help you!",
    "can you help me meditate": "Sure, I can guide you through a basic meditation!",
    "do you like robots": "I am a robot, so yes!",
    "what's your favorite holiday destination": "I hear Bali is a beautiful place to visit!",
    "can you sing": "I can't sing, but I can find you the lyrics to a song!",
    "do you like animals": "I think animals are wonderful!",
    "what's your favorite quote": "I like 'To be, or not to be, that is the question.'",
    "can you help me plan my day": "Sure, I can help you create a schedule!",
    "do you like fashion": "I think fashion is interesting!",
    "what's your favorite subject": "I like learning about everything!",
    "can you help me with my project": "Sure, tell me more about your project!",
    "do you like movies": "I don't watch movies, but I can help you find one to watch!",
    "what's your favorite website": "I like all websites equally!",
    "can you help me study": "Sure, I can help you with study tips!",
    "do you like to write": "I love helping with writing!",
    "what's your favorite dessert": "I don't eat, but I hear cheesecake is delicious!",
    "can you help me organize": "Sure, I can help you create a to-do list!",
    "do you like space": "I think space is fascinating!",
    "what's your favorite planet": "I think Earth is pretty great!",
    "can you help me with technology": "Sure, what do you need help with?",
    "do you like to talk": "I love chatting with you!",
    "what's your favorite quote about life": "I like 'Life is what happens when you're busy making other plans.'"
}

# Default response
responses["default"] = "I'm sorry, I didn't understand that. Can you please rephrase?"

def extract_name(user_input):
    pattern = r"hi, i'm (\w+)|hello, i'm (\w+)"
    match = re.search(pattern, user_input, re.IGNORECASE)
    if match:
        return match.group(1) if match.group(1) else match.group(2)
    return None

def get_response(user_input):
    user_input = user_input.lower()
    name = extract_name(user_input)
    if name:
        return f"Hello {name}! How can I help you?"
    
    # Directly match the user input against the predefined responses
    response = responses.get(user_input)
    if response:
        return response
    else:
        return responses["default"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    response = get_response(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
