import datetime
import hashlib
import json
from flask import Flask, jsonify

# 1. Building Blockchain

class BlockChain:
    def __init__(self):
        self.chain = []
        self.createBlock(proof = 1, prevHash = '0')
    
    def createBlock(self, proof, prevHash):
        block = {
            'index': len(self.chain)+1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'prevHash': prevHash
        }

        self.chain.append(block)
        return block


    def getPrevBlock(self):
        return self.chain[-1]
    
    def proofOfWork(self, prevProof):
        newProof = 1
        checkProof = False

        while checkProof is False:
            hashOperation = hashlib.sha256(str(newProof**2 - prevProof**2).encode()).hexdigest()
            if hashOperation[:4] == '0000':
                checkProof = True
            else:
                newProof += 1
        
        return newProof

    def hash(self, block):
        encodedBlock = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encodedBlock).hexdigest()
    
    def isChainValid(self, chain):
        prevBlock = chain[0]
        blockIndex = 1

        while blockIndex < len(chain):
            block = chain[blockIndex]
            prevProof = prevBlock['proof']
            proof = block['proof']
            hashOperation = hashlib.sha256(str(proof**2 - prevProof**2).encode()).hexdigest()

            if block['prevHash'] != self.hash(prevBlock) or hashOperation[:4] != '0000':
                return False

            prevBlock = block
            blockIndex += 1

        return True
    
        

# 2. Mining the blockchain

# Creating a web app

app = Flask(__name__)

blockchain = BlockChain()

# Mining a new block

@app.route('/mineblock', methods=['GET'])
def mineBlock():
    prevBlock = blockchain.getPrevBlock()
    proof = blockchain.proofOfWork(prevBlock['proof'])
    block = blockchain.createBlock(proof, blockchain.hash(prevBlock))

    response = {
        'message': 'Congratulations, you just mined a block!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'prevHash': block['prevHash']
    }

    return jsonify(response), 200

@app.route('/getchain', methods=['GET'])
def getChain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }

    return jsonify(response), 200

@app.route('/isvalid', methods=['GET'])
def isValid():
    isValid = blockchain.isChainValid(blockchain.chain)
    if isValid:
        response = {'message': 'Blockchain is valid.'}
    else:
        response = {'message': 'Blockchain is invalid.'}

    return jsonify(response), 200

# Running the app
app.run(host='0.0.0.0', port=5000)