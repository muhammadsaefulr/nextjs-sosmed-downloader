from flask import Flask
from flask_cors import CORS
from flask import Blueprint, jsonify, request
from pytube import YouTube
import instaloader

app = Flask(__name__)
CORS(app, origins='*')

@app.route('/api/youtube', methods=['GET'])
def get_video_youtube():
    try: 
        videoUrl = request.args.get('url')
        videoRes = request.args.get('res')

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
        loader = instaloader.Instaloader()
        url = postUrl

        shortcode = url.split('/')[4].split('?')[0]
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        
        username_url = post.owner_username
        post_url = post.video_url
        desc_url = post.caption
        thumbnail_url = post.url

        response = {
            'dataDetail': [
                {
                'username': username_url,
                'postUrl': post_url,
                'thumbnailUrl': thumbnail_url,
                'postDesc': desc_url
                }

            ]
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 501

# if __name__ == "__main__":
#     app.run(debug=True)