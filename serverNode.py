from uuid import uuid4
from flask import Flask, jsonify, request
from blockchain import BlockChain

# Makes it easy to map endpoints to Python functions.
# This allows us talk to our blockchain over the web using HTTP requests.

# Setting up Flask
# Instantiating our Node
app = Flask(__name__)

# Our “server” will form a single node in our blockchain network.
# Generating a globally unique address for this particular Node
node_ID = str(uuid4()).replace('-', '')

# Instantiating our blockchain
our_blockchain = BlockChain()


@app.route('/nodes/register')
# accepts a list of new nodes in the form of URLs
def register_nodes():
    return "Registered"

@app.route('/nodes/resolve')
# implement consensus algorithm, which rsolves any conflicts, ensuring a node has the correct chain
def resolve():
     return "Resolved"


@app.route('/chain', methods=['GET'])
# /chain to return the full Blockchain
def chain():
    response = {
        'fullChain': our_blockchain.chain,
        'length': len(our_blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
# /transactions/new to create a new transaction to a block
def transactions():

    values = request.get_json()

    # checking if the required fields were in the posted data
    required_data = ['sender', 'recipient', 'amount']

    # just sees if value elements are == the required elements. If a single value is false, then returns error
    # not sure if i understand how the for loop is structured
    if not all(k in values for k in required_data):
        return 'Missing Required Data', 400

    index = our_blockchain.add_transaction(
        values['sender'], values['recipient'], values['amount'])

    response = {
        'message': f'Transaction pending for insertion in block {index}'
    }

    return jsonify(response), 201


@app.route('/mine', methods=['GET'])
# /mine to tell our server to mine a new block.
def mine():

    # Retrieving the most current block, and extracting the last proof used. We use that to get the current proof by running PoW algorithm
    latest_block = our_blockchain.latest_block
    last_proof = latest_block['proof']
    proof = our_blockchain.proof_of_work(last_proof)

    # Reward the miner (us) by adding a transaction granting us 1 coin. Sender is "0" to signify that this node has mined a new coin
    our_blockchain.add_transaction(sender=0, recipient=node_ID, amount=1)

    # Forge the new Block by adding it to the chain
    previous_hash = our_blockchain.hasher(latest_block)
    block = our_blockchain.add_block(proof, previous_hash)

    response = {
        "message": "New block has been created",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
