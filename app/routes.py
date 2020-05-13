from app import app
from app.worldmanager import WorldManager
from app.player import PlayerObj
from flask import request, session, json, jsonify

print("TEST1")

users = []
world = WorldManager()
world.generate(120, 120) # small enough of a world for now
    
# NOTE: This is going to be super easy for someone to attack
# NOTE: Good thing this isn't a security final

print("TEST")

@app.route("/view", methods=['GET'])
def worldState():
    
    if not 'loggedin' in session or not session['loggedin'] or not users[session['user_player']].logged:
        if (not _login()):
            return jsonify(err=1)
    
    position = users[session['user_player']].position
    # Player windows will be 100x100 until I decides otherwise
    pixels = world.getView(position[0], position[1], 100, 100)
    pixelX = ""
    pixelY = ""
    pixelRGB = ""
    for pixel in pixels:
        pixelRGB += ("," if len(pixelX) > 0 else "") + str(pixel[2])[1:-1].replace(",","|").replace(" ","")
        pixelY   += ("," if len(pixelX) > 0 else "") + (str(pixel[1] - position[1]))
        pixelX   += ("," if len(pixelX) > 0 else "") + (str(pixel[0] - position[1]))

    playerX = ""
    playerY = ""
    playerID = ""
    for user in users:
        if user.logged:
            playerID += ("," if len(playerX) > 0 else "") + user.userID
            playerY  += ("," if len(playerX) > 0 else "") + str(user.position[1])
            playerX  += ("," if len(playerX) > 0 else "") + str(user.position[0])


    # Output:
    # TODO: Figure out if I'm doing pixel tails
    # pixelX: "0,1,2,3..."
    # pixelY: "0,1,2,3..."
    # pixelRGB: "255|255|255,255|255|255,255|255|255,255|255|255..."
    # playerX: "0,1,2,3..."
    # playerY: "0,1,2,3..."
    # playerID: "billy,bobby,bub,brown..."
    return jsonify(pixelX=pixelX,
                    pixelY=pixelY,
                    pixelRGB=pixelRGB,
                    playerX=playerX,
                    playerY=playerY,
                    playerID=playerID)



# the player acting in the world
@app.route("/act", methods=['POST'])
def playerState():
    if not 'loggedin' in session:
        if (not _login()):
            return jsonify(err=1)
    if session['loggedin']:
        if users[session['user_player']].logged:
            x = float(request.values['moveX']) # -1 to 1
            y = float(request.values['moveY']) # -1 to 1
            mx = float(request.values['controlX']) # -1 to 1
            my = float(request.values['controlY']) # -1 to 1
            breaking = (int(request.values['breaking']) == 1) # 0 or 1
            # player us reverified
            users[session['user_player']].reverify()
            # Move and do cursor position, create bounds because I don't trust people
            users[session['user_player']].move(max(-1, min(1, x)), max(-1, min(1, y)))
            users[session['user_player']].cursourPosition = [max(-1, min(1, mx)), max(-1, min(1, my))]
            users[session['user_player']].isMining = breaking
        else:
            session['loggedin'] = False
            session['user_player'] = None
    return jsonify(ret=True)

# Ticks stuff
def update():
    world.tick()
    for user in users:
        if user.logged:
            user.tick()

def _login():
    if 'un' in request.values and 'pw' in request.values:
        if len(request.values['un']) < 1 or len(request.values['pw']) < 1:
            return jsonify(ret=False)
        session['un'] = request.values['un']
        session['pw'] = request.values['pw']
        session['loggedin'] = False
        exists = False
        for n in users:
            if n.userID == session['un']:
                exists = True
                if n.userPW == session['pw']:
                    session['loggedin'] = True
                    session['user_player'] = users.index(n)
                    n.logged = True
                break
        if not exists:
            _player = PlayerObj(session['un'], session['pw'])
            _player.logged = True
            users.append(_player)
            session['user_player'] = users.index(_player)
            session['loggedin'] = True
        if session['loggedin']:
            return jsonify(ret=True)
        else:
            return jsonify(ret=False)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ret = _login()
        if not ret == False:
            return ret
    elif request.method == 'GET' and 'un' in session and 'pw' in session and session['loggedin'] and users[session['user_player']].logged:
        return jsonify(ret=True)
    return jsonify(ret=False)

