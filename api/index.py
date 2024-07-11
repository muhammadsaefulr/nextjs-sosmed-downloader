from flask import Flask
from flask import  jsonify, request
from pytube import YouTube
import requests
import re
import threading
import time
import os
import tempfile

app = Flask(__name__)

def remove_file_after_delay(file_path, delay):
    time.sleep(delay)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File {file_path} telah dihapus setelah {delay} detik.")

@app.route('/api/youtube', methods=['GET'])
def get_video_youtube():
    try: 
        videoUrl = request.args.get('url')
        videoRes = request.args.get('res')
        mp3 = request.args.get('mp3')

        if(videoUrl == None):
            return jsonify({'message': 'Url Tidak Boleh Bernilai Null !'})

        if(videoRes == None):
            return jsonify({'message': 'Argumen ?res= Tidak Boleh Kosong !'})

        videoResValidate = None

        if videoRes == '360p':
            videoResValidate = '18'
        elif videoRes == '720p':
            videoResValidate = '22'
        elif videoRes == '1080p':
            videoResValidate = '137'
        else:
            return jsonify({'message': 'Invalid Video Resolution'})

        yt = YouTube(videoUrl)
        get_urlLinks = yt.streams.get_by_itag(videoResValidate).url
        
        save_dir = tempfile.gettempdir()
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        if mp3 == "true":
            urlsmp3 = yt.streams.filter(only_audio=True).first()
            outFile = urlsmp3.download(output_path=save_dir)
            newFile = os.path.join(save_dir, 'result_downloads' + '.mp3')
            os.rename(outFile, newFile)
            
            with open(newFile, 'rb') as file:
                responseUpload = requests.post('https://file.io', files={'file': file})
                upload_url = responseUpload.json().get('link')
            
            # resultsMp3 = requests.get(upload_url).json()

            threading.Thread(target=remove_file_after_delay, args=(newFile, 20)).start()

            mp3Res = { 
                'dataDetail': [
                    {
                        'urlLinks': upload_url,
                    }
                ]
            }
            return jsonify(mp3Res), 200


        channelVideo = yt.channel_url
        channelVideoId = yt.channel_id
        videoTitle = yt.title
        videoDesc = yt.captions.get_by_language_code('en')

        response = { 
            'dataDetail': [
                {
                'urlLinks': get_urlLinks,
                'videoRes': videoRes,
                'videoResId': videoResValidate
                },
                {
                'videoChannel': channelVideo,
                'videoChannelId': channelVideoId,
                'videoTitle': videoTitle,
                'videoDesc': videoDesc
                }
            ]
        }

        if get_urlLinks == None:
            return jsonify({'message': 'Terjadi Kesalahan Saat Mengurai Data !'})
        else:
            return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/instagram', methods=['GET'])
def get_post_instagram():
    try:
        postUrl = request.args.get('url')
        
        url = "https://v3.igdownloader.app/api/ajaxSearch"
        dataPost = {
           "recaptchaToken": "",
           "q": postUrl,
           "t": "media",
           "lang": "en"
        }
        
        result = [""]
       
        responseApi = requests.post(url, data=dataPost)
        
        if responseApi.status_code == 200:
            regexResp = r'<a[^>]*onclick="ga\(\'send\', \'event\', \'home\', \'click_download_video\'\)"\s+href="([^"]+)"[^>]*>'
            dataResReq = responseApi.json()
            regexRespApiMatch = re.findall(regexResp, dataResReq['data'], re.IGNORECASE | re.DOTALL)
            
            if regexRespApiMatch: 
                result = regexRespApiMatch
            else:
                result = []
                
        if not result:
            return jsonify({
                "message": "Result Is Null"
            })
                
        response = {
            'dataDetail': [
                {
                'postUrl': result,
                }

            ]
        }
        
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 501
    
if __name__ == "__main__":
    app.run(debug=True)