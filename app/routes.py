from app import app
from app.worldmanager import WorldManager
from app.player import Player
from flask import request, session, json

print("TEST1")

users = []
world = WorldManager()
world.generate(5000, 5000) # small enough of a world for now

print("TEST")

@app.route("/view", methods=['GET'])
def worldState():
    # NOTE: Holy **** this is going to be super easy for someone to attack
    # NOTE: Good thing this isn't a security final

    # TODO: return all the pixels and online player positions
    if not 'loggedin' in session or not session['player'].logged:
        return
    
    position = session['player'].position

    # Player windows will be 500x500 until I decides otherwise
    pixels = world.getView(position[0], position[1], 500, 500)
    pixelX = ""
    pixelY = ""
    pixelRGB = ""
    for pixel in pixels:
        pixelRGB += ("," if len(pixelX) > 0 else "") + str(pixel[2])[1:-1].replace(",","|").replace(" ","")
        pixelY   += ("," if len(pixelX) > 0 else "") + (str(pixel[1]))
        pixelX   += ("," if len(pixelX) > 0 else "") + (str(pixel[0]))

    playerX = ""
    playerY = ""
    playerID = ""
    for user in users:
        if user.logged:
            playerID += ("," if len(playerX) > 0 else "") + user.userID
            playerY  += ("," if len(playerX) > 0 else "") + user.position[1]
            playerX  += ("," if len(playerX) > 0 else "") + user.position[0]


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
                    playerID=payerID)



# the player acting in the world
@app.route("/act", methods=['POST'])
def playerState():
    if not 'loggedin' in session:
        return
    if session['loggedin']:
        if session['player'].logged:
            x = request.values['moveX'] # -1 to 1
            y = request.values['moveY'] # -1 to 1
            mx = request.values['controlX'] # -1 to 1
            my = request.values['controlY'] # -1 to 1
            breaking = (request.values['breaking'] == 1) # 0 or 1
            # player us reverified
            session['player'].reverify()
            # Move and do cursor position, create bounds because I don't trust people
            session['player'].move(max(-1, min(1, x)), max(-1, min(1, y)))
            session['player'].cursourPosition = [max(-1, min(1, mx)), max(-1, min(1, my))]
            session['player'].isMining = breaking
        else:
            session['loggedin'] = False
            session['player'] = None

# Ticks stuff
def update():
    world.tick()
    for user in users:
        if user.logged:
            user.tick()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'un' in request.values and 'pw' in request.values:
            session['un'] = request.values['un']
            session['pw'] = request.values['pw']
            session['loggedin'] = False
            exists = False
            for n in users:
                if n.userID == session['un']:
                    exists = True
                    if not n.logged and n.userPW == session['pw']:
                        session['loggedin'] = True
                        session['player'] = n
                    break
            if not exists:
                player = Player(session['un'], session['pw'])
                player.logged = True
                session['player'] = player
                users.append(player) 
            return jsonify(result=session['loggedin'])
    elif request.method == 'GET' and 'un' in session and 'pw' in session and session['loggedin'] and session['player'].logged:
        return jsonify(result=True)
    return jsonify(result=False)

