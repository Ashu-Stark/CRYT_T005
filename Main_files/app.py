from flask import Flask, render_template, request, jsonify
import os
import json
from aes_handler import encrypt_vote_with_aes, decrypt_vote_with_aes
from rsa_handler import ensure_rsa_keys, rsa_encrypt_string, rsa_decrypt_list, save_rsa_keys, load_rsa_keys

app = Flask(__name__)

VOTERS_FILE = "voters.txt"
ENCRYPTED_VOTES_FILE = "encrypted_votes.txt"
CANDIDATES = ["Candidate - A", "Candidate - B", "Candidate - C"]

# Initialize files
def init_files():
    if not os.path.exists(VOTERS_FILE):
        sample = ["1001,0", "1002,0", "1003,0", "1004,0"]
        with open(VOTERS_FILE, "w") as f:
            f.write("\n".join(sample) + "\n")
    if not os.path.exists(ENCRYPTED_VOTES_FILE):
        open(ENCRYPTED_VOTES_FILE, "w").close()
    ensure_rsa_keys()

def load_voters():
    voters = {}
    if not os.path.exists(VOTERS_FILE):
        return voters
    with open(VOTERS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) >= 2:
                vid = parts[0].strip()
                status = int(parts[1].strip())
                voters[vid] = status
    return voters

def save_voters(voters):
    with open(VOTERS_FILE, "w") as f:
        for vid, status in voters.items():
            f.write(f"{vid},{status}\n")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/check_voter', methods=['POST'])
def check_voter():
    data = request.json
    voterid = data.get('voterid', '').strip()
    
    voters = load_voters()
    if voterid not in voters:
        return jsonify({'exists': False, 'message': 'Voter ID not found.'})
    
    if voters[voterid] == 1:
        return jsonify({'exists': True, 'voted': True, 'message': 'You have already voted.'})
    
    return jsonify({'exists': True, 'voted': False, 'candidates': CANDIDATES})

@app.route('/api/submit_vote', methods=['POST'])
def submit_vote():
    data = request.json
    voterid = data.get('voterid', '').strip()
    candidate_index = data.get('candidate_index')
    
    if candidate_index is None or candidate_index < 0 or candidate_index >= len(CANDIDATES):
        return jsonify({'success': False, 'message': 'Invalid candidate selection.'})
    
    voters = load_voters()
    if voterid not in voters:
        return jsonify({'success': False, 'message': 'Voter ID not found.'})
    
    if voters[voterid] == 1:
        return jsonify({'success': False, 'message': 'You have already voted.'})
    
    candidate = CANDIDATES[candidate_index]
    
    # Encrypt vote with AES
    encrypted_vote_text, aes_key = encrypt_vote_with_aes(candidate)
    
    # Encrypt AES key with RSA
    keys = load_rsa_keys()
    if keys is None:
        keys = ensure_rsa_keys()
    e, n = keys['e'], keys['n']
    rsa_enc_key_list = rsa_encrypt_string(aes_key, e, n)
    
    # Save encrypted vote
    entry = {
        "voterid": voterid,
        "enc_vote": encrypted_vote_text,
        "enc_aes_key": ",".join(map(str, rsa_enc_key_list))
    }
    with open(ENCRYPTED_VOTES_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
    
    # Mark voter as voted
    voters[voterid] = 1
    save_voters(voters)
    
    return jsonify({'success': True, 'message': 'Vote submitted successfully!'})

@app.route('/api/admin_login', methods=['POST'])
def admin_login():
    data = request.json
    aid = data.get('admin_id', '').strip()
    apw = data.get('admin_password', '').strip()
    
    if aid == "gov" and apw == "gov@123":
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Invalid admin credentials.'})

@app.route('/api/decrypt_votes', methods=['POST'])
def decrypt_votes():
    keys = load_rsa_keys()
    if not keys:
        return jsonify({'success': False, 'message': 'RSA keys not available.'})
    
    d, n = keys['d'], keys['n']
    votes_plain = []
    
    if not os.path.exists(ENCRYPTED_VOTES_FILE):
        return jsonify({'success': True, 'votes': [], 'tally': {}, 'winners': []})
    
    for line in open(ENCRYPTED_VOTES_FILE):
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
            enc_vote = entry.get("enc_vote", "")
            enc_aes_csv = entry.get("enc_aes_key", "")
            enc_aes_list = [int(x) for x in enc_aes_csv.split(",")] if enc_aes_csv else []
            
            aes_key = rsa_decrypt_list(enc_aes_list, d, n)
            plain_vote = decrypt_vote_with_aes(enc_vote, aes_key)
            votes_plain.append(plain_vote)
        except Exception as e:
            votes_plain.append(f"[DECRYPT_ERROR: {e}]")
    
    # Tally votes
    tally = {}
    for v in votes_plain:
        if not v.startswith("[DECRYPT_ERROR"):
            tally[v] = tally.get(v, 0) + 1
    
    # Find winners
    winners = []
    if tally:
        max_votes = max(tally.values())
        winners = [c for c, cnt in tally.items() if cnt == max_votes]
    
    return jsonify({
        'success': True,
        'votes': votes_plain,
        'tally': tally,
        'winners': winners
    })

@app.route('/api/reset_votes', methods=['POST'])
def reset_votes():
    open(ENCRYPTED_VOTES_FILE, "w").close()
    voters = load_voters()
    for vid in voters.keys():
        voters[vid] = 0
    save_voters(voters)
    return jsonify({'success': True, 'message': 'All votes cleared and voter statuses reset.'})

if __name__ == '__main__':
    init_files()
    print("\n=== E-Voting System ===")
    print("Server starting on http://localhost:5000")
    print("Open your browser and navigate to http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

