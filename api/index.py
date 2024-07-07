from flask import Flask
from flask import  jsonify, request
from pytube import YouTube
import requests
import re

app = Flask(__name__)

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
        
        yt = YouTube(videoUrl)
        videoResValidate = None
        
        if (mp3): 
            urls = yt.streams.filter(only_audio=True).first().url
            mp3Res = { 
            'dataDetail': [
                {
                'urlLinks': urls,
                }
            ]}
            
            return jsonify(mp3Res), 200

        if videoRes == '360p':
            videoResValidate = '18'
        elif videoRes == '720p':
            videoResValidate = '22'
        elif videoRes == '1080p':
            videoResValidate = '137'
        else:
            return jsonify({'message': 'Invalid Video Resolution'})
        
        get_urlLinks = yt.streams.get_by_itag(videoResValidate).url

        channelVideo = yt.channel_url
        channelVideoId = yt.channel_id
        videoTitle = yt.title
        videoDesc = yt.captions.get_by_language_code('en').generate_srt_captions() if yt.captions.get_by_language_code('en') else 'No captions available'
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
            return jsonify({'message': 'Terjadi Kesalahan Saat Mengurai Data !'}), 500
        else:
            return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

# if __name__ == "__main__":
#     app.run(debug=True)