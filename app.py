
from flask import Flask, render_template, Response
import random
import cv2
from camera import VideoCamera

import sys
import spotipy
import spotipy.util as util

import random
import requests

from moodtape_functions import authenticate_spotify, aggregate_top_artists, aggregate_top_tracks, select_tracks, \
	create_playlist

client_id =  "0825da0780ca4eb1903d85a94948990d"
client_secret = "31ee017c7d9645dd811266441e1ca2f3"
redirect_uri = "http://127.0.0.1:5000/"

scope = 'user-library-read user-top-read playlist-modify-public user-follow-read'

username = "ádi45"
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

app = Flask(__name__)
final_mood='NULL'
pre_mood='NULL'
minimum_frames=20
confirm=0
counter=0
scan=0
rev=0

@app.route('/')
def index():
	return render_template('index.html')




def gen(camera):
	global confirm
	global counter
	global scan
	global rev

	while True:
		frame,mood = camera.get_frame()





		if(confirm!=1):

			check(mood)
			frame = cv2.line(frame, (0, scan), (frame.shape[1], scan), (170,205,254), 4)
			if (rev == 0):
				scan += 30
			else:
				scan -= 30
			if (scan > frame.shape[0]):
				scan = frame.shape[0]
				rev = 1
			elif (scan < 0):
				scan = 0
				rev = 0
			ret, jpeg = cv2.imencode('.jpg', frame)
			frame = jpeg.tobytes()
		else:

			frame = cv2.GaussianBlur(frame,(47,47),cv2.BORDER_DEFAULT)
			frame = cv2.putText(frame, 'Done!', (120,170), cv2.FONT_HERSHEY_SIMPLEX ,
								2, (170,205,254), 4, cv2.LINE_AA)

			ret, jpeg = cv2.imencode('.jpg', frame)
			frame = jpeg.tobytes()
			yield (b'--frame\r\n'
				   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

			confirm=0
			counter=0
			break



		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')





@app.route('/video_feed')
def video_feed():
	global confirm



	return Response(gen(VideoCamera()),
					mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/cam')
def cam_on():
	obj = VideoCamera()

	return render_template('cam_on.html')



@app.route('/playlist')
def moodtape():
	global final_mood

	if(final_mood=='Happy'):
		mood = 1.0
		mood=(round(random.uniform(0.8, 1.0), 2))

	elif(final_mood=='Sad'):
		mood=0.1
		mood = (round(random.uniform(0.1, 0.3), 2))
	elif(final_mood=='Neutral'):
		mood=0.5
		mood = (round(random.uniform(0.4, 0.7), 2))

	# username = request.form['username']
	mood = float(mood)
	# token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
	spotify_auth = authenticate_spotify(token)
	top_artists = aggregate_top_artists(spotify_auth)
	top_tracks = aggregate_top_tracks(spotify_auth, top_artists)
	selected_tracks = select_tracks(spotify_auth, top_tracks, mood)
	#all_playlists='https://api.spotify.com/v1/users/'+username+'/playlists'
	#x = requests.get(all_playlists,params {Authorization: 49c660ae3c0242deb395127c50aa4971})
	#print(x.response)
	#resp_dict = json.load(x)
	playlist = create_playlist(spotify_auth, selected_tracks, mood,final_mood)
	playlist='https://open.spotify.com/playlist/'+playlist.split(':')[2]

	print(playlist)

	if(final_mood=='Happy'):
		return render_template('playlist_happy.html', playlist=playlist)

	elif(final_mood=='Sad'):
		return render_template('playlist_sad.html', playlist=playlist)

	elif(final_mood=='Neutral'):
		return render_template('playlist_neutral.html', playlist=playlist)



def check(mood):
	global confirm
	global minimum_frames
	global pre_mood
	global counter
	global final_mood
	print("---------------------------> ",counter)

	if(counter==minimum_frames):
		final_mood=mood
		confirm=1
	elif(pre_mood==mood):
		counter+=1
	elif(counter==0):
		pre_mood = mood
		counter+=1

	elif(pre_mood!=mood):
		counter=0
		pre_mood=mood



if __name__ == '__main__':
	app.run(debug=True)
