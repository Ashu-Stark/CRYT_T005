import os
import json
from aes_handler import encrypt_vote_with_aes, decrypt_vote_with_aes
from rsa_handler import ensure_rsa_keys, rsa_encrypt_string, rsa_decrypt_list, save_rsa_keys, load_rsa_keys

VOTERS_FILE = "voters.txt"            
ENCRYPTED_VOTES_FILE = "encrypted_votes.txt"
RSA_KEYFILE = "rsa_keys.txt"

CANDIDATES = ["Candidate - A", "Candidate - B", "Candidate - C"]

def init_files():
    """Initialize required files if they don't exist"""
    if not os.path.exists(VOTERS_FILE):
        sample = ["1001,0", "1002,0", "1003,0", "1004,0"]
        with open(VOTERS_FILE, "w") as f:
            f.write("\n".join(sample) + "\n")
    if not os.path.exists(ENCRYPTED_VOTES_FILE):
        open(ENCRYPTED_VOTES_FILE, "w").close()
    ensure_rsa_keys()

def load_voters():
    """Load voters from file"""
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
    """Save voters to file"""
    with open(VOTERS_FILE, "w") as f:
        for vid, status in voters.items():
            f.write(f"{vid},{status}\n")

def check_voter_exists(voterid):
    """Check if voter ID exists"""
    return voterid in load_voters()

def has_voted(voterid):
    """Check if voter has already voted"""
    voters = load_voters()
    return voters.get(voterid, 0) == 1

def set_voted(voterid):
    """Mark voter as voted"""
    voters = load_voters()
    voters[voterid] = 1
    save_voters(voters)

def voter_flow():
    """Handle voter voting process"""
    voterid = input("Enter voter id (or 'back'): ").strip()
    if voterid.lower() == "back":
        return
    if not check_voter_exists(voterid):
        print("Voter id not found.")
        return
    if has_voted(voterid):
        print("You have already voted.")
        return

    print("\nCandidates:")
    for i, c in enumerate(CANDIDATES, 1):
        print(f"{i}. {c}")
    choice = input("Choose candidate number: ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(CANDIDATES):
        print("Invalid choice.")
        return
    candidate = CANDIDATES[int(choice) - 1]

    encrypted_vote_text, aes_key = encrypt_vote_with_aes(candidate)
    
    keys = load_rsa_keys()
    if keys is None:
        keys = ensure_rsa_keys()
    e, n = keys['e'], keys['n']
    rsa_enc_key_list = rsa_encrypt_string(aes_key, e, n)

    entry = {
        "voterid": voterid,
        "enc_vote": encrypted_vote_text,
        "enc_aes_key": ",".join(map(str, rsa_enc_key_list))
    }
    with open(ENCRYPTED_VOTES_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

    set_voted(voterid)
    print("Vote submitted successfully.")

def admin_panel():
    """Handle admin panel operations"""
    aid = input("Admin id: ").strip()
    apw = input("Admin password: ").strip()
    if aid != "gov" or apw != "gov@123":
        print("Invalid admin credentials.")
        return
    while True:
        print("\n--- Admin Panel ---")
        print("1. Decrypt and show result")
        print("2. Encrypted files")
        print("3. Reset votes")
        print("4. Back")
        ch = input("Choice: ").strip()
        if ch == "1":
            decrypt_and_tally()
        elif ch == "2":
            show_raw()
        elif ch == "3":
            reset_votes()
        else:
            break

def decrypt_and_tally():
    """Decrypt votes and show tally"""
    keys = load_rsa_keys()
    if not keys:
        print("RSA keys not available.")
        return
    d, n = keys['d'], keys['n']
    votes_plain = []
    if not os.path.exists(ENCRYPTED_VOTES_FILE):
        print("No votes file.")
        return
    for line in open(ENCRYPTED_VOTES_FILE):
        line = line.strip()
        if not line:
            continue
        entry = json.loads(line)
        enc_vote = entry.get("enc_vote", "")
        enc_aes_csv = entry.get("enc_aes_key", "")
        enc_aes_list = [int(x) for x in enc_aes_csv.split(",")] if enc_aes_csv else []
        try:
            aes_key = rsa_decrypt_list(enc_aes_list, d, n)  
            plain_vote = decrypt_vote_with_aes(enc_vote, aes_key)  
            votes_plain.append(plain_vote)
        except Exception as e:
            votes_plain.append(f"[DECRYPT_ERROR: {e}]")

    if not votes_plain:
        print("No votes to show.")
        return

    tally = {}
    for v in votes_plain:
        if not v.startswith("[DECRYPT_ERROR"):
            tally[v] = tally.get(v, 0) + 1

    print("\nDecrypted votes:")
    for i, v in enumerate(votes_plain, 1):
        print(f"{i}. {v}")

    print("\nTally:")
    for cand, cnt in tally.items():
        print(f"{cand}: {cnt}")

    if tally:
        max_votes = max(tally.values())
        winners = [c for c, cnt in tally.items() if cnt == max_votes]
        print("\nWinner: " + ", ".join(winners))

def show_raw():
    """Show raw encrypted votes file"""
    print("\n--- Encrypted Vote ---")
    if os.path.exists(ENCRYPTED_VOTES_FILE):
        with open(ENCRYPTED_VOTES_FILE, "r") as f:
            data = f.read().strip()
            if data:
                print(data)
            else:
                print("(No encrypted votes yet.)")
    else:
        print("(Encrypted votes file missing.)")

def reset_votes():
    """Reset all votes and voter statuses"""
    open(ENCRYPTED_VOTES_FILE, "w").close()
    voters = load_voters()
    for vid in voters.keys():
        voters[vid] = 0
    save_voters(voters)
    print("All votes cleared and voter statuses set to 0.")

def main_menu():
    """Main menu loop"""
    init_files()
    while True:
        print("\n=== Voting System ===")
        print("1. Voter login ")
        print("2. Admin panel")
        print("3. Exit")
        ch = input("Choice: ").strip()
        if ch == "1":
            voter_flow()
        elif ch == "2":
            admin_panel()
        elif ch == "3":
            print("Exiting....")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()

