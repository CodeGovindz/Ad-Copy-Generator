from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import random
import os
import boto3
import uuid
from datetime import datetime

app = Flask(__name__)
# Load environment variables from .env file
load_dotenv()

# API configuration
API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")
headers = {"Authorization": f"Bearer {API_KEY}"}

# DynamoDB configuration
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "AdCopyGenerator")

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
table = dynamodb.Table(DYNAMODB_TABLE)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def run_ai_model(model, inputs):
    input_data = {"messages": inputs}
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input_data)
    response.raise_for_status()  
    return response.json()

def scrape_website(url):
    response = requests.get(url)
    response.raise_for_status()  
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string if soup.title else "No Title Found"
    description = soup.find('meta', attrs={'name': 'description'})
    description = description['content'] if description else "No Description Found"
    return title, description

def save_to_dynamodb(user_inputs, ad_copy):
    """
    Save user inputs and generated ad copy to DynamoDB
    """
    item = {
        'id': str(uuid.uuid4()),  # Generate a unique ID
        'timestamp': datetime.utcnow().isoformat(),
        'product_title': user_inputs.get('product_title', 'No Title'),
        'product_description': user_inputs.get('product_description', 'No Description'),
        'url': user_inputs.get('url', ''),
        'audience': user_inputs.get('audience', ''),
        'tone': user_inputs.get('tone', ''),
        'platform': user_inputs.get('platform', ''),
        'max_length': user_inputs.get('max_length', ''),
        'ad_copy': ad_copy
    }
    
    try:
        table.put_item(Item=item)
        return True, item['id']
    except Exception as e:
        print(f"Error saving to DynamoDB: {str(e)}")
        return False, None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    product_title = data.get('product', 'No Title')
    product_description = data.get('description', 'No Description')
    url = data.get('url', '')
    
    if url:
        try:
            title, description = scrape_website(url)
            product_title = title
            product_description = description
        except Exception as e:
            return jsonify({'error': f'Failed to scrape website: {str(e)}'}), 500

    system_prompt = """You are an expert copywriter specializing in creating compelling, concise, and effective ad copy for various platforms and audiences. Your task is to generate ad copy based on the given parameters. Follow these guidelines:

1. Tone: Adapt your writing style to match the specified tone (professional, casual, humorous, Luxury, Adventurous, Friendly etc.).
2. Audience: Tailor the language and messaging to resonate with the target audience.
3. Platform: Consider the typical constraints and best practices of the specified platform.
4. Length: Strictly adhere to the maximum character count provided.
5. Clarity: Ensure the main message and call-to-action are clear and prominent.
6. Engagement: Use language that grabs attention and encourages user interaction.
7. Uniqueness: Highlight what makes the product or service stand out from competitors.
8. Benefits: Focus on the benefits to the user rather than just listing features.
9. Brand Voice: Maintain a consistent brand voice if any brand information is provided.
10. Compliance: Avoid making unsupported claims or using potentially offensive language.
11. output: output should not contain any other extra information."""

    user_prompt = f"""Create a compelling {data['tone']} ad copy for {product_title} & {product_description}. 
    The target audience is {data['audience']}. 
    The ad will be posted on {data['platform']}. 
    Keep it under {data['max_length']} characters."""

    inputs = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        output = run_ai_model("@cf/meta/llama-3.1-8b-instruct", inputs)
        ad_copy = output.get('result', {}).get('response', 'No response')
        
        # Prepare data for DynamoDB
        user_inputs = {
            'product_title': product_title,
            'product_description': product_description,
            'url': url,
            'audience': data.get('audience', ''),
            'tone': data.get('tone', ''),
            'platform': data.get('platform', ''),
            'max_length': data.get('max_length', '')
        }
        
        # Save to DynamoDB
        success, record_id = save_to_dynamodb(user_inputs, ad_copy)
        
        # Return the generated ad copy and record ID
        response = {'ad_copy': ad_copy}
        if success:
            response['record_id'] = record_id
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': f'Failed to generate ad copy: {str(e)}'}), 500

@app.route('/history', methods=['GET'])
def get_history():
    """
    Endpoint to retrieve ad generation history
    """
    try:
        response = table.scan()
        items = response.get('Items', [])
        return jsonify({'history': items})
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve history: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
