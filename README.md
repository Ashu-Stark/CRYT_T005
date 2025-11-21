# E-Voting System

A secure, web-based electronic voting system built with Flask, featuring dual-layer encryption (AES + RSA) for vote security and anonymity.

## 🎯 Features

- **Secure Voting**: Dual-layer encryption using AES and RSA algorithms
- **Voter Authentication**: Unique Voter ID system
- **One Vote Per Voter**: Prevents duplicate voting
- **Admin Panel**: Government login to view encrypted votes, voter status, and decrypt results
- **Real-time Statistics**: Live voter status tracking with visualizations
- **Auto-refresh**: Automatic data updates in admin panel
- **Interactive UI**: Modern, responsive web interface

## 🔐 Security Features

- **AES Encryption**: Votes are encrypted using Advanced Encryption Standard (AES)
- **RSA Encryption**: AES keys are protected using RSA public-key cryptography
- **Vote Integrity**: Each vote is cryptographically secured
- **Voter Privacy**: Votes remain encrypted until decryption by authorized admin

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CRYT_T005/Main_files
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃 Running the Application

### Option 1: Using the batch file (Windows)
```bash
start_server.bat
```

### Option 2: Using Python directly
```bash
python app.py
```

The server will start on `http://localhost:5000`

Open your browser and navigate to `http://localhost:5000`

## 📖 Usage

### For Voters

1. Click **"Voter Login"** on the main page
2. Enter your Voter ID (e.g., 1001, 1002, 1003, 1004)
3. Select a candidate from the list
4. Click **"Submit Vote"**
5. Your vote will be encrypted and stored securely

### For Administrators

1. Click **"Admin Panel"** on the main page
2. Login with credentials:
   - **Admin ID**: `gov`
   - **Password**: `gov@123`
3. View encrypted votes, voter status, and statistics
4. Click **"Decrypt & Show Results"** to view decrypted votes and tally
5. Use **"Enable Auto-Refresh"** to automatically update data every 5 seconds
6. Use **"Reset Votes"** to clear all votes and reset voter statuses

## 📁 Project Structure

```
Main_files/
├── app.py                 # Main Flask application
├── aes_handler.py         # AES encryption handler
├── aes.py                # AES encryption implementation
├── rsa_handler.py        # RSA key management handler
├── rsa.py                # RSA encryption implementation
├── requirements.txt      # Python dependencies
├── start_server.bat      # Server startup script (Windows)
├── templates/
│   └── index.html        # Frontend HTML template
├── static/
│   └── images/          # Team member images
├── voters.txt           # Voter database (auto-generated)
├── encrypted_votes.txt  # Encrypted votes storage (auto-generated)
└── rsa_keys.txt         # RSA keys storage (auto-generated)
```

## 🔧 API Endpoints

### Voter Endpoints

- `POST /api/check_voter` - Check if voter exists and has voted
- `POST /api/submit_vote` - Submit an encrypted vote

### Admin Endpoints

- `POST /api/admin_login` - Authenticate admin user
- `GET /api/get_encrypted_votes` - Get all encrypted votes
- `GET /api/get_voter_status` - Get voter list with voting status
- `POST /api/decrypt_votes` - Decrypt and tally all votes
- `POST /api/reset_votes` - Reset all votes and voter statuses

## 🔑 Default Voters

The system comes with 4 default voters:
- Voter ID: 1001
- Voter ID: 1002
- Voter ID: 1003
- Voter ID: 1004

All voters start with status "Not Voted" (0).

## 🎨 Features in Detail

### Encryption Process

1. **Vote Submission**: When a voter selects a candidate, the vote is encrypted using AES
2. **Key Protection**: The AES key is then encrypted using RSA public key
3. **Storage**: Both encrypted vote and encrypted AES key are stored
4. **Decryption**: Only authorized admin can decrypt using RSA private key

### Admin Panel Features

- **Encrypted Votes Display**: View all encrypted votes in a table format
- **Voter Status Statistics**: 
  - Total voters count
  - Voted count with percentage
  - Not voted count with percentage
- **Interactive Voter Table**:
  - Filter by All/Voted/Not Voted
  - Sort by Voter ID or Status
  - Real-time updates
- **Auto-refresh**: Automatically refresh data every 5 seconds
- **Decrypt Results**: View decrypted votes, tally, and winner

## 🛠️ Technology Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML, CSS, JavaScript
- **Encryption**: AES (Advanced Encryption Standard) + RSA (Rivest-Shamir-Adleman)
- **Storage**: Text files (voters.txt, encrypted_votes.txt, rsa_keys.txt)

## 📝 Notes

- RSA keys are automatically generated on first run
- Data files (voters.txt, encrypted_votes.txt, rsa_keys.txt) are auto-generated
- The system ensures one vote per voter
- All votes remain encrypted until decrypted by admin
- Server runs in debug mode for development

## 👥 Team

- Aniket Singh (ID: 24021921)
- Ashutosh (ID: 24021603)
- Shoyam Bishnoi (ID: 240211797)
- Tanishk Gupta (ID: 240111241)

## 📄 License

This project is developed for educational purposes as part of CRYT_T005 course.

## 🐛 Troubleshooting

### Server won't start
- Ensure Python 3.7+ is installed
- Check if port 5000 is available
- Verify Flask is installed: `pip install Flask`

### Votes not displaying
- Check if encrypted_votes.txt exists
- Verify RSA keys are generated (rsa_keys.txt)
- Check browser console for errors

### Admin login fails
- Verify credentials: Admin ID: `gov`, Password: `gov@123`
- Check server logs for errors

## 🔄 Updates

- Enhanced error handling and validation
- Real-time statistics and visualizations
- Auto-refresh functionality
- Improved UI/UX with loading states
- Interactive filtering and sorting
- Keyboard navigation support

---

**Developed by Encoders Team | Graphic Era University**

