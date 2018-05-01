#initialise

from flask import Flask, session, redirect, url_for, render_template, request
from flask_socketio import SocketIO, send, emit, render_template, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yeah-i-am-so-fucked'
socketio = SocketIO(app)


#events

# @socketio.on('message', namespace='/public_chat')
# def handleMessage(msg):
# 	print('Message: ' + msg)
# 	send(msg, broadcast=True)

@socketio.on('joined_public', namespace='/public_chat')
def joined_public(message):
	"""Sent by clients when they enter a room.
	A status message is broadcast to all people in the room."""
	room = 'free-for-all' #open chat session.get('room')
	join_room(room)
	emit('status', {'msg': session.get('name') + ' has joined.'}, room=room)

@socketio.on('text_public', namespace='/public_chat')
def text_public(message):
	"""Sent by a client when the user entered a new message.
	The message is sent to all people in the room."""
	room = 'free-for-all' #open chat session.get('room')
	emit('message', {'msg': session.get('name') + ' : ' + message['msg']}, room=room)

@socketio.on('left_public', namespace='/public_chat')
def left_public(message):
	"""Sent by clients when they leave a room.
	A status message is broadcast to all people in the room."""
	room = 'free-for-all' #open chat session.get('room')
	leave_room(room)
	emit('status', {'msg': session.get('name') + ' has left.'}, room=room)


@socketio.on('joined_private', namespace='/public_chat')
def joined_private(message):
	"""Sent by clients when they enter a room.
	A status message is broadcast to all people in the room."""
	room = 'two-to-tango' #open chat session.get('room')
	join_room(room)
	emit('status', {'msg': session.get('name') + ' is online.'}, room=room)

@socketio.on('text_private', namespace='/public_chat')
def text_private(message):
	"""Sent by a client when the user entered a new message.
	The message is sent to all people in the room."""
	room = 'two-to-tango' #open chat session.get('room')
	emit('message', {'msg': session.get('name') + ' : ' + message['msg']}, room=room)

@socketio.on('left_private', namespace='/public_chat')
def left_private(message):
	"""Sent by clients when they leave a room.
	A status message is broadcast to all people in the room."""
	room = 'two-to-tango' #open chat session.get('room')
	leave_room(room)
	emit('status', {'msg': session.get('name') + ' is offline.'}, room=room)


#routes

@app.route('/', methods=['GET', 'POST'])
def index():
	# """Login form to enter a room."""
	# form = LoginForm()
	# if form.validate_on_submit():
	# 	session['name'] = form.name.data
	# 	session['room'] = form.room.data
	# 	return redirect(url_for('.chat'))
	# elif request.method == 'GET':
	# 	form.name.data = session.get('name', '')
	# 	form.room.data = session.get('room', '')
	# return render_template('index.html', form=form)
	session['name'] = 'shelly'
	return redirect(url_for('public_chat'))

# @main.route('/profile', methods=['GET', 'POST'])
# def index():
# 	"""Login form to enter a room."""
# 	form = LoginForm()
# 	if form.validate_on_submit():
# 		session['name'] = form.name.data
# 		session['room'] = form.room.data
# 		return redirect(url_for('.chat'))
# 	elif request.method == 'GET':
# 		form.name.data = session.get('name', '')
# 		form.room.data = session.get('room', '')
# 	return render_template('index.html', form=form)

@app.route('/public_chat') #public chat
def public_chat():
	"""Chat room. The user's name and room must be stored in
	the session."""
	name = session.get('name', '')
	room = 'free-for-all' #open chat session.get('room')
	return render_template('public_chat.html', name=name, room=room)

@app.route('/private_chat') #private chat
def private_chat():
	"""Chat room. The user's name and room must be stored in
	the session."""
	name = session.get('name', '')
	room = 'two-to-tango' #closed chat session.get('room')
	return render_template('private_chat.html', name=name, room=room)


#execute

if __name__ == '__main__':
	socketio.run(app)