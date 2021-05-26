from flask import Flask, jsonify, request
from uuid import uuid4
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
    return "Mining a new block!"


# /transactions/new
# to create a new transaction to a block
@app.route('/transactions/new', methods=['POST'])
def transactions():
    return "Adding a new transaction!"



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

