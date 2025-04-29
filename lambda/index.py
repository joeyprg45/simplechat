
import json
import os
import urllib.request
import time

COLAB_API_URL = os.environ.get("COLAB_API_URL", "https://3f73-34-75-191-61.ngrok-free.app/generate")  

def lambda_handler(event, context):
    print("Received event:", event)

    try:
        if 'body' in event:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            body = event 
        
        prompt = body['prompt']
        max_new_tokens = body.get('max_new_tokens', 512)
        do_sample = body.get('do_sample', True)
        temperature = body.get('temperature', 0.7)
        top_p = body.get('top_p', 0.9)

        start_time = time.time()

        request_data = {
            "prompt": prompt,
            "max_new_tokens": max_new_tokens,
            "do_sample": do_sample,
            "temperature": temperature,
            "top_p": top_p
        }

        req = urllib.request.Request(COLAB_API_URL, json.dumps(request_data).encode('utf-8'), headers={'Content-Type': 'application/json'})
        
        with urllib.request.urlopen(req) as response:
            response_data = json.load(response)


        generated_text = response_data.get("generated_text", "")
        end_time = time.time()
        response_time = end_time - start_time

        return {
            'statusCode': 200,
            'body': json.dumps({
                'generated_text': generated_text,
                'response_time': response_time
            })
        }
    except Exception as e:
        print("エラーが発生:", e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
