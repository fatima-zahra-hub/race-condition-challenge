from flask import Flask, request, jsonify
import time
import threading

app = Flask(__name__)

# Initial state: 100 balance, coupon not used
user_wallet = {"balance": 100, "coupon_used": False}
lock = threading.Lock() # Hum isko use nahi karenge taake vulnerability rahe

@app.route('/redeem', methods=['POST'])
def redeem_coupon():
    global user_wallet
    
    # 1. CHECK PHASE (Vulnerability: Not atomic)
    if user_wallet["coupon_used"]:
        return jsonify({"error": "Coupon already used"}), 400
    
    if user_wallet["balance"] < 50:
        return jsonify({"error": "Insufficient balance"}), 400

    # 2. TIME WINDOW (Delay to make the race condition exploitable)
    # Yeh delay real-world databases ya network ki latency ko represent karta hai
    time.sleep(0.5) 
    
    # 3. ACT PHASE
    user_wallet["balance"] -= 50
    user_wallet["coupon_used"] = True
    
    return jsonify({
        "message": "Coupon Redeemed Successfully!", 
        "flag": "SECDIM{RACE_CONDITION_BYPASS_SUCCESS}",
        "new_balance": user_wallet["balance"]
    })

if __name__ == '__main__':
    app.run(debug=True, threaded=True)