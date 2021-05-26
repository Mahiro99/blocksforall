from uuid import uuid4
from flask import Flask, jsonify, request
from blockchain import BlockChain

# Makes it easy to map endpoints to Python functions. 
# This allows us talk to our blockchain over the web using HTTP requests.

# Setting up Flask
#Instantiating our Node
app =  Flask(__name__)

# Our “server” will form a single node in our blockchain network. 
#Generating a globally unique address for this particular Node
node_ID = str(uuid4()).replace('-', '')

#Instantiating our blockchain
our_blockchain = BlockChain()


# We’ll create three methods:
# /mine
# to tell our server to mine a new block.
@app.route('/mine', methods=['GET'])
def mine():

    #Retrieving the most current block, and extracting the last proof used. We use that to get the current proof by running POW algorithm
    latest_block = our_blockchain.latest_block()
    last_proof = latest_block['proof']
    proof = our_blockchain.proof_of_work(last_proof)

    # Reward the miner (us) by adding a transaction granting us 1 coin. Sender is "0" to signify that this node has mined a new coin
    our_blockchain.add_transaction(sender = 0, receiver = node_ID, mony = 1 )

    # Forge the new Block by adding it to the chain
    previous_hash = our_blockchain.hasher(latest_block)
    block = our_blockchain.add_block(proof, previous_hash)

    response  = {
        "message" : "New block has been created",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'], 
        'previous_hash': block['previous_hash']
    }

    return jsonify(response), 200


# /transactions/new
# to create a new transaction to a block
@app.route('/transactions/new', methods=['POST'])
def transactions():

    values = request.get_json()

    #checking if the required fields were in the posted data
    required_data = ['sender', 'reciever', 'mony']
    
    #just sees if value elements are == the required elements. If a single value is false, then returns error
    if(not all(k in values for k in required_data)): ## not sure if i understand how the for loop is structured
        return 'Missing Required Data', 400

    index = our_blockchain.add_transaction(values['sender'], values['reciever'], values['mony'])
   
    response = {
        'message': f'Transaction pending for block {index} insertion'
    }
    return jsonify(response), 201



# /chain
# to return the full Blockchain
@app.route('/chain', methods=['GET'])
def chain():
    response = {
        'fullChain' : our_blockchain.chain,
        'length' : len(our_blockchain.chain)
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)