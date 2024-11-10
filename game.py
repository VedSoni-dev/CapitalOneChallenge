import random
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Define financial scenarios
def generate_scenario():
    scenarios = {
        1: {'question': 'You found a wallet with $100. What do you do?', 
            'choices': ['Turn it in to the police', 'Keep it', 'Donate it to charity'], 
            'outcomes': [0, 100, 0]},
        
        2: {'question': 'You have the chance to invest in a stock. Do you?', 
            'choices': ['Invest all your money', 'Research before investing', 'Ignore the opportunity'], 
            'outcomes': [-100, 50, 0]},
        
        3: {'question': 'Your car breaks down. What do you do?', 
            'choices': ['Call a tow truck', 'Try to fix it yourself', 'Ignore the problem'], 
            'outcomes': [-200, -50, -300]},
        
        4: {'question': 'A friend asks to borrow money. What do you say?', 
            'choices': ['Lend it if you can', 'Say no', 'Offer advice instead'], 
            'outcomes': [-50, 0, 0]},
        
        5: {'question': 'You receive an unexpected bill of $150. How do you handle it?', 
            'choices': ['Pay immediately', 'Delay payment', 'Ignore it'], 
            'outcomes': [-150, -50, -200]},
        
        6: {'question': 'You get a bonus at work! What do you do with the $200?', 
            'choices': ['Save it', 'Spend it all', 'Invest half'], 
            'outcomes': [200, -200, 100]},

        7: {'question': 'You notice a error in your favor on your bank statement. What do you do?',
            'choices': ['Report it to the bank', 'Keep quiet about it', 'Withdraw the money quickly'],
            'outcomes': [-10, 200, -300]},

        8: {'question': 'Your roof starts leaking. How do you handle it?',
            'choices': ['Hire a professional', 'DIY repair', 'Use a bucket for now'],
            'outcomes': [-500, -200, -800]},

        9: {'question': 'You receive a suspicious email about winning a prize. What do you do?',
            'choices': ['Ignore it', 'Click the link', 'Forward it to others'],
            'outcomes': [0, -400, -200]},

        10: {'question': 'A street vendor offers you a "genuine" luxury watch for $50. Do you:',
            'choices': ['Buy it', 'Decline politely', 'Try to negotiate'],
            'outcomes': [-50, 0, -30]},

        11: {'question': 'Your favorite streaming service raises prices. What do you do?',
            'choices': ['Cancel subscription', 'Keep it', 'Switch to a cheaper plan'],
            'outcomes': [150, -180, 60]},

        12: {'question': 'You find a high-yield savings account offer. What do you do?',
            'choices': ['Transfer all savings', 'Research first', 'Stick with current bank'],
            'outcomes': [-100, 200, 0]},

        13: {'question': 'Your phone is getting old. What do you do?',
            'choices': ['Buy latest model', 'Get a budget phone', 'Keep current phone'],
            'outcomes': [-1000, -300, 0]},

        14: {'question': 'You receive a tax refund of $500. How do you use it?',
            'choices': ['Pay off debt', 'Go shopping', 'Start emergency fund'],
            'outcomes': [600, -500, 500]},

        15: {'question': 'Your credit card offers a credit limit increase. Do you:',
            'choices': ['Accept it', 'Decline it', 'Ask for details'],
            'outcomes': [-200, 0, 0]},

        16: {'question': 'You see a great deal on bulk groceries. What do you do?',
            'choices': ['Buy in bulk', 'Buy normal amount', 'Skip shopping today'],
            'outcomes': [100, 0, -50]},

        17: {'question': 'A friend invites you to join a multi-level marketing scheme. Do you:',
            'choices': ['Join immediately', 'Decline', 'Ask for more information'],
            'outcomes': [-500, 0, -100]},

        18: {'question': 'Your utility bill seems unusually high. What do you do?',
            'choices': ['Pay it anyway', 'Contest the bill', 'Ignore it'],
            'outcomes': [-200, 0, -400]},

        19: {'question': 'You receive a credit card offer with 0% APR. Do you:',
            'choices': ['Apply immediately', 'Read the fine print', 'Shred it'],
            'outcomes': [-300, 100, 0]},

        20: {'question': 'Your neighbor is selling their car below market value. Do you:',
            'choices': ['Buy it immediately', 'Get it inspected first', 'Pass on the offer'],
            'outcomes': [-1000, 500, 0]},

        21: {'question': 'You find a $50 coupon for a store you never shop at. Do you:',
            'choices': ['Use it anyway', 'Give it away', 'Throw it out'],
            'outcomes': [-100, 0, 0]},

        22: {'question': 'Your workplace offers a 401(k) match. Do you:',
            'choices': ['Contribute maximum', 'Contribute minimum', 'Opt out'],
            'outcomes': [400, 200, -200]},

        23: {'question': 'You receive an inheritance of $1000. What do you do?',
            'choices': ['Invest it all', 'Save half, spend half', 'Spend it all'],
            'outcomes': [1200, 600, -1000]},

        24: {'question': 'Your rent is increasing by $200. Do you:',
            'choices': ['Move to cheaper place', 'Negotiate with landlord', 'Accept increase'],
            'outcomes': [-500, -100, -200]},

        25: {'question': 'You find a side gig opportunity. Do you:',
            'choices': ['Take it immediately', 'Research it first', 'Decline it'],
            'outcomes': [300, 400, 0]},

        26: {'question': 'Your computer needs upgrading. What do you do?',
            'choices': ['Buy new one', 'Upgrade components', 'Keep using old one'],
            'outcomes': [-800, -200, -100]},

        27: {'question': 'You receive a store credit card application. Do you:',
            'choices': ['Apply for rewards', 'Decline offer', 'Ask about terms'],
            'outcomes': [-150, 0, 50]},

        28: {'question': 'Your health insurance premium increases. Do you:',
            'choices': ['Switch providers', 'Increase deductible', 'Keep current plan'],
            'outcomes': [200, 100, -300]},

        29: {'question': 'You find a great deal on vacation packages. Do you:',
            'choices': ['Book immediately', 'Compare prices', 'Skip vacation'],
            'outcomes': [-600, 200, 0]},

        30: {'question': 'Your smartphone offers an expensive app upgrade. Do you:',
            'choices': ['Buy upgrade', 'Keep free version', 'Look for alternatives'],
            'outcomes': [-50, 0, 25]},

        31: {'question': 'You discover a new cryptocurrency. Do you:',
            'choices': ['Invest heavily', 'Invest small amount', 'Stay away'],
            'outcomes': [-800, -200, 0]},

        32: {'question': 'A relative needs help with medical bills. Do you:', 
            'choices': ['Contribute $200', 'Offer advice', 'Ignore request'], 
            'outcomes': [-200, 0, 0]},
            
        33: {'question': 'A new tech gadget is on sale for $300. Do you:', 
            'choices': ['Buy it', 'Wait for a better deal', 'Skip it'], 
            'outcomes': [-300, 0, 0]},
            
        34: {'question': 'You are offered a discount on a gym membership. Do you:', 
            'choices': ['Sign up', 'Ask for a trial', 'Ignore the offer'], 
            'outcomes': [-100, 0, 0]},
            
        35: {'question': 'A subscription service offers a free trial. Do you:', 
            'choices': ['Sign up and cancel later', 'Pay for a month', 'Ignore it'], 
            'outcomes': [-10, -50, 0]},
            
        36: {'question': 'A friend suggests a business opportunity. Do you:', 
            'choices': ['Invest $500', 'Ask for more details', 'Decline politely'], 
            'outcomes': [-500, 0, 0]},
            
        37: {'question': 'You win a small lottery prize of $150. Do you:', 
            'choices': ['Save it', 'Treat yourself', 'Give it away'], 
            'outcomes': [150, -150, 0]},
            
        38: {'question': 'You need a new laptop for work. Do you:', 
            'choices': ['Buy a high-end model', 'Buy a budget option', 'Wait for sales'], 
            'outcomes': [-1000, -300, 0]},
            
        39: {'question': 'A charity calls asking for donations. Do you:', 
            'choices': ['Donate $100', 'Donate $10', 'Decline'], 
            'outcomes': [-100, -10, 0]},
            
        40: {'question': 'You see an ad for a timeshare vacation. Do you:', 
            'choices': ['Invest in it', 'Ignore it', 'Research more'], 
            'outcomes': [-700, 0, 0]},
            
        41: {'question': 'You accidentally damage a friend’s property. Do you:', 
            'choices': ['Offer to pay $200', 'Apologize', 'Do nothing'], 
            'outcomes': [-200, 0, -50]},
            
        42: {'question': 'You get a $200 tax refund. Do you:', 
            'choices': ['Invest it', 'Spend it on a hobby', 'Save it'], 
            'outcomes': [200, -200, 200]},
            
        43: {'question': 'You’re offered a part-time job on weekends. Do you:', 
            'choices': ['Accept it', 'Decline it', 'Ask about flexibility'], 
            'outcomes': [400, 0, 0]},
            
        44: {'question': 'A friend is selling collectibles for $100. Do you:', 
            'choices': ['Buy them', 'Negotiate price', 'Decline'], 
            'outcomes': [-100, -50, 0]},
            
        45: {'question': 'You’re invited to an expensive event. Do you:', 
            'choices': ['Attend', 'Decline', 'Offer to volunteer'], 
            'outcomes': [-200, 0, 0]},
            
        46: {'question': 'Your car insurance premium rises. Do you:', 
            'choices': ['Switch providers', 'Negotiate', 'Accept the increase'], 
            'outcomes': [100, -50, -100]},
            
        47: {'question': 'You find a 2-for-1 sale on a popular item. Do you:', 
            'choices': ['Buy extra', 'Buy one', 'Skip the sale'], 
            'outcomes': [0, 0, -10]},
            
        48: {'question': 'You discover a free online course to improve skills. Do you:', 
            'choices': ['Enroll', 'Ignore', 'Save it for later'], 
            'outcomes': [100, 0, 0]},
            
        49: {'question': 'You see a designer item on clearance for $200. Do you:', 
            'choices': ['Buy it', 'Compare with other deals', 'Skip it'], 
            'outcomes': [-200, 0, 0]},
            
        50: {'question': 'Your friend is raising money for a cause. Do you:', 
            'choices': ['Donate $50', 'Spread the word', 'Decline'], 
            'outcomes': [-50, 0, 0]},
            
        51: {'question': 'You need to travel for work. Do you:', 
            'choices': ['Book first class', 'Book economy', 'Look for discounts'], 
            'outcomes': [-500, -200, -100]},
            
        52: {'question': 'You have the chance to earn interest on $1000 in a CD. Do you:', 
            'choices': ['Invest in the CD', 'Put it in savings', 'Spend it now'], 
            'outcomes': [50, 10, -100]},
            
        53: {'question': 'You’re offered an online freelance project. Do you:', 
            'choices': ['Accept immediately', 'Negotiate terms', 'Decline'], 
            'outcomes': [300, 200, 0]},
            
        54: {'question': 'You’re offered cash back to open a credit card. Do you:', 
            'choices': ['Open the card', 'Decline', 'Ask about fees'], 
            'outcomes': [100, 0, 0]},
            
        55: {'question': 'Your family member needs financial help for rent. Do you:', 
            'choices': ['Lend $300', 'Lend $50', 'Decline politely'], 
            'outcomes': [-300, -50, 0]},
            
        56: {'question': 'You see a limited-time sale on home goods. Do you:', 
            'choices': ['Buy extra', 'Buy only needed items', 'Skip the sale'], 
            'outcomes': [0, -50, 0]}
    }
    scenario_id = random.choice(list(scenarios.keys()))
    return scenarios[scenario_id]

# Provide feedback based on the outcome
def provide_feedback(outcome):
    if outcome > 0:
        return "Great choice! You gained money."
    elif outcome == 0:
        return "Neutral choice. No gain or loss." 
    else:
        return "Bad choice! You lost money."

class FinancialGame:
    def __init__(self):
        self.balance = round(random.uniform(100, 2000), 2)  # Random starting balance between 100 and 2000
        self.initial_balance = self.balance  # Store initial balance for summary
        self.scenario_count = 0
        self.history = []

    def play_round(self, user_choice):
        scenario = generate_scenario()
        outcome = scenario['outcomes'][user_choice]
        self.balance += outcome
        feedback = provide_feedback(outcome)
        
        # Store the round's results
        self.history.append({
            'scenario': scenario['question'],
            'choice': scenario['choices'][user_choice],
            'outcome': outcome
        })
        
        self.scenario_count += 1

        return {
            'scenario': scenario,
            'balance': self.balance,
            'outcome': outcome,
            'feedback': feedback,
            'scenario_count': self.scenario_count
        }

    def check_status(self):
        if self.balance <= 0:
            return False
        if self.scenario_count >= 5:
            return False
        return True

    def show_summary(self):
        profit_loss = self.balance - self.initial_balance
        performance = (self.balance / self.initial_balance) * 100
        
        # Coupon calculation
        coupon = 0
        if 50 < performance:
            coupon = 2.5
        if 75 <= performance < 100:
            coupon = 5
        elif 100 <= performance < 125:
            coupon = 7.5
        elif performance >= 125:
            coupon = 10

        return {
            'initial_balance': self.initial_balance,
            'final_balance': self.balance,
            'total_profit_loss': profit_loss,
            'scenarios_played': self.scenario_count,
            'performance_percentage': performance,
            'coupon': coupon,
            'history': self.history
        }

# Global game instance
current_game = None

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['GET'])
def start_game():
    global current_game
    current_game = FinancialGame()
    return jsonify({
        'balance': current_game.balance,
        'initial_balance': current_game.initial_balance
    })

@app.route('/next_scenario', methods=['GET'])
def next_scenario():
    return jsonify(generate_scenario())

@app.route('/make_choice', methods=['POST'])
def make_choice():
    global current_game
    
    # Get the choice index from the request
    data = request.json
    choice_index = data['choice_index']
    
    # Play the round
    round_result = current_game.play_round(choice_index)
    
    # Check if game is over
    game_over = not current_game.check_status()
    
    if game_over:
        # If game is over, get the summary
        summary = current_game.show_summary()
        return jsonify({
            'game_over': True,
            **summary
        })
    
    return jsonify({
        'game_over': False,
        'balance': round_result['balance'],
        'scenario_count': round_result['scenario_count'],
        'feedback': round_result['feedback']
    })

if __name__ == "__main__":
    app.run(debug=True)