import random
import json
from flask import Flask, render_template, jsonify, request
from datetime import datetime

app = Flask(__name__)

class FinancialScenario:
    def __init__(self, question, choices, outcomes, consequences, skill_check=None):
        self.question = question
        self.choices = choices
        self.outcomes = outcomes
        self.consequences = consequences
        self.skill_check = skill_check

class PlayerProfile:
    def __init__(self):
        self.balance = 2000  # Starting balance
        self.initial_balance = self.balance
        self.credit_score = random.randint(650, 750)
        self.stress_level = 50
        self.skills = {
            'financial_literacy': random.randint(50, 80),
            'risk_management': random.randint(40, 70),
            'negotiation': random.randint(40, 70)
        }
        self.achievements = []
        self.game_history = []

class FinancialGameEngine:
    def __init__(self):
        self.scenarios = self._load_scenarios()
        self.player = PlayerProfile()

    def _load_scenarios(self):
        return [
            # Interest Rate Dilemma
            FinancialScenario(
                question="You have $1000 to invest. Option A offers a 5% annual interest rate compounded quarterly. Option B offers a 4.5% annual interest rate compounded monthly. Which option will yield the highest return after 3 years?",
                choices=[
                    "Option A - higher annual rate",
                    "Option B - more frequent compounding",
                    "Both options will yield roughly the same return"
                ],
                outcomes=[150, 120, 50],  #  Higher for correct choice, less for wrong, least for random
                consequences=[
                    "Smart choice, you understand compounding!",
                    "Not quite, frequent compounding can be powerful",
                    "A little more research needed on interest calculations"
                ],
                skill_check={
                    'financial_literacy': 80
                }
            ),

            # Inflation & Purchasing Power
            FinancialScenario(
                question="The current inflation rate is 3%. You have $500 saved for a new laptop that costs $600 today. If you wait 2 years to buy the laptop, assuming inflation stays constant, how much will you need to save to afford it?",
                choices=[
                    "You'll need about $630",
                    "You'll need about $660",
                    "You'll need about $690"
                ],
                outcomes=[100, 50, -50],
                consequences=[
                    "Good grasp of inflation's impact",
                    "Close, but inflation affects prices over time",
                    "Remember, inflation erodes your purchasing power"
                ],
                skill_check={
                    'financial_literacy': 75
                }
            ),

            # Risk vs. Reward
            FinancialScenario(
                question="You're considering investing in a startup company. Option A promises a 10% return within a year, but carries a high risk of failure. Option B offers a 2% guaranteed return with low risk. Given a $500 investment, which option aligns with your risk tolerance?",
                choices=[
                    "Option A - high potential but high risk",
                    "Option B - low risk, steady return",
                    "Split the investment between both options"
                ],
                outcomes=[150, 100, 50],
                consequences=[
                    "High risk, high reward, but you're comfortable with it",
                    "Safe and sound, but you'll miss out on potential growth",
                    "Balancing risk and reward, a sensible approach"
                ],
                skill_check={
                    'risk_management': 70
                }
            ),

            # Credit Card Debt
            FinancialScenario(
                question="You have a credit card with a $500 balance and an 18% APR. You can afford to pay $100 per month. How long will it take to pay off the debt, assuming no further purchases?",
                choices=[
                    "Less than a year",
                    "More than a year but less than two",
                    "More than two years"
                ],
                outcomes=[100, 50, 0],
 consequences=[
                    "Great job, you understand debt repayment!",
                    "Close, but the interest adds up quickly",
                    "Debt can be tricky, keep an eye on those rates"
                ],
                skill_check={
                    'financial_literacy': 85
                }
            ),

            # Retirement Planning
            FinancialScenario(
                question="You're 30 years old and want to retire at 65. If you plan to save $500 a month and expect an average annual return of 6%, how much will you have by retirement?",
                choices=[
                    "About $500,000",
                    "About $1,000,000",
                    "About $1,500,000"
                ],
                outcomes=[150, 100, 50],
                consequences=[
                    "Excellent calculation, compounding works in your favor!",
                    "Not quite, but you're on the right track",
                    "Retirement planning requires careful consideration"
                ],
                skill_check={
                    'financial_literacy': 80
                }
            ),

            # Emergency Fund
            FinancialScenario(
                question="You want to build an emergency fund that covers 6 months of expenses. If your monthly expenses are $1,200, how much should you aim to save?",
                choices=[
                    "About $5,000",
                    "About $7,200",
                    "About $10,000"
                ],
                outcomes=[150, 100, 50],
                consequences=[
                    "Smart move, you understand the importance of an emergency fund!",
                    "Close, but remember to cover all expenses",
                    "Emergency funds are crucial, keep saving!"
                ],
                skill_check={
                    'financial_literacy': 70
                }
            ),

            # Investment Diversification
            FinancialScenario(
                question="You have $2,000 to invest. You can either put it all in one stock or diversify into four different stocks. What is the best strategy to minimize risk?",
                choices=[
                    "Invest all in one stock for potential high returns",
                    "Diversify into four different stocks to spread risk",
                    "Invest in a mix of stocks and bonds for balance"
                ],
                outcomes=[150, 100, 50],
                consequences=[
                    "Wise choice, diversification is key!",
                    "Good idea, but spreading risk is more effective",
                    "Balanced approach, but consider your risk tolerance"
                ],
                skill_check={
                    'risk_management': 75
                }
            ),

            # Tax Implications
            FinancialScenario(
                question="You sold an asset for a profit of $10,000. If your tax rate on capital gains is 15%, how much will you owe in taxes?",
                choices=[
                    "About $1,500",
                    "About $2,000",
                    "About $2,500"
                ],
                outcomes=[150, 100, 50],
                consequences=[
                    "Great job, you understand capital gains tax!",
                    "Close, but remember to calculate the percentage correctly",
                    "Tax implications can be tricky, keep learning"
                ],
                skill_check={
                    'financial_literacy': 80
                }
            ),

            # Housing Market Decision
            FinancialScenario(
                question="You're considering buying a house worth $300,000. If you put down 20% and take a 30-year mortgage at 4% interest, what will your monthly payment be (excluding taxes and insurance)?",
                choices=[
                    "About $1,200",
                    "About $1,400",
                    "About $1,600"
                ],
                outcomes=[150, 100, 50],
                consequences=[
                    "Excellent calculation, you understand mortgage payments!",
                    "Close, but don't forget to factor in the interest",
                    "Home buying requires careful financial planning"
                ],
                skill_check={
                    'financial_literacy': 85
                }
            ),

            # Stock Market Volatility
            FinancialScenario(
                question="You invested $1,000 in a stock that has fluctuated between $800 and $1,200 over the past year. If you sell now, what is your potential loss or gain?",
                choices=[
                    "You will break even",
                    "You will incur a loss of $200",
                    "You will gain $200"
                ],
                outcomes=[100, -200, 200],
                consequences=[
                    "Good analysis, you understand market fluctuations!",
                    "Remember, selling at a loss can be a tough decision",
                    "Well done, you capitalized on the market's ups and downs"
                ],
                skill_check={
                    'risk_management': 70
                }
            ),

            # Savings Account vs. Investment
            FinancialScenario(
                question="You have $5,000 to either put in a savings account with a 1% interest rate or invest in a stock with an expected return of 8% per year. Which option is more beneficial in the long run?",
                choices=[
                    "Savings account for guaranteed returns",
                    "Invest in the stock for higher potential returns",
                    "Split the amount between both options"
                ],
                outcomes=[100, 150, 50],
                consequences=[
                    "Smart choice, investing can yield better returns!",
                    "Good thinking, but don't underestimate the power of compounding",
                    "Balanced approach, but consider your risk tolerance"
                ],
                skill_check={
                    'financial_literacy': 75
                }
            ),

            # Real Estate Investment
            FinancialScenario(
                question="You are considering purchasing a rental property for $250,000. If you expect to earn $1,500 per month in rent and your expenses are $1,000 per month, what is your annual cash flow?",
                choices=[
                    "About $6,000",
                    "About $12,000",
                    "About $18,000"
                ],
                outcomes=[150, 100, 50],
                consequences=[
                    "Excellent calculation, you understand cash flow!",
                    "Close, but remember to calculate annual totals",
                    "Good effort, but cash flow analysis is crucial"
                ],
                skill_check={
                    'financial_literacy': 80
                }
            ),

            # Insurance Needs
            FinancialScenario(
                question="You have a family and are considering life insurance. If your annual income is $60,000, what is a common recommendation for life insurance coverage?",
                choices=[
                    "5 times your annual income",
                    "10 times your annual income",
                    "15 times your annual income"
                ],
                outcomes=[150, 100, 50],
                consequences=[
                    "Great choice, you understand insurance needs!",
                    "Good thinking, but consider your family's future expenses",
                    "Insurance is complex, keep learning about it"
                ],
                skill_check={
                    'financial_literacy': 70
                }
            ),

            # College Savings Plan
            FinancialScenario(
                question="You want to save for your child's college education, which is expected to cost $100,000 in 15 years. If you want to save this amount with an average annual return of 5%, how much do you need to save each month?",
                choices=[
                    "About $400",
                    "About $600",
                    "About $800"
                ],
                outcomes=[150, 100, 50],
                consequences=[
                    "Excellent planning, you understand future savings needs!",
                    "Close, but remember to factor in inflation",
                    "Good effort, but college costs can be unpredictable"
                ],
                skill_check={
                    'financial_literacy': 80
                }
            ),

            # Business Investment
            FinancialScenario(
                question="You are considering investing $10,000 in a small business. If the business has a projected return of 20% per year, how much will your investment be worth in 5 years?",
                choices=[
                    "About $12,000",
                    "About $15,000",
                    "About $20,000"
                ],
                outcomes=[150, 100, 50],
                consequences=[
                    "Great job, you understand investment growth!",
                    "Close, but compounding can significantly increase returns",
                    "Good effort, but business investments carry risks"
                ],
                skill_check={
                    'risk_management': 75
                }
            )
        ]

    def play_scenario(self, scenario_index, choice_index):
        scenario = self.scenarios[scenario_index]
        outcome = scenario.outcomes[choice_index]
        
        # Skill check logic
        if scenario.skill_check:
            for skill, threshold in scenario.skill_check.items():
                if self.player.skills[skill] < threshold:
                    outcome *= 0.5  # Penalty for low skill
        
        # Update player stats
        self.player.balance += outcome
        
        # Stress and skill adjustments
        self.player.stress_level += random.randint(-10, 10)
        
        # Record game history
        self.player.game_history.append({
            'scenario': scenario.question,
            'choice': scenario.choices[choice_index],
            'outcome': outcome,
            'timestamp': datetime.now().isoformat()
        })
        
        return {
            'scenario': scenario.question,
            'choice': scenario.choices[choice_index],
            'outcome': outcome,
            'balance': self.player.balance,
            'consequence': scenario.consequences[choice_index]
        }

    def get_game_summary(self):
        total_gain = self.player.balance - self.player.initial_balance
        performance_score = (self.player.balance / self.player.initial_balance) * 100
        


        reward_tier = None
        if self.player.balance >= 3250:
            reward_tier = 'gold'
        elif self.player.balance >= 3000:
            reward_tier = 'silver'
        elif self.player.balance >= 2750:
            reward_tier = 'bronze'


        return {
            'initial_balance': self.player.initial_balance,
            'final_balance': self.player.balance,
            'total_gain': total_gain,
            'performance_score': performance_score,
            'game_history': self.player.game_history,
            'skills': self.player.skills,
            'reward_tier': reward_tier,
            'day': len(self.player.game_history)
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
    current_game = FinancialGameEngine()
    return jsonify({
        'balance': current_game.player.balance,
        'initial_balance': current_game.player.initial_balance,
        'scenarios_available': len(current_game.scenarios)
    })

@app.route('/get_scenario', methods=['GET'])
def get_scenario():
    global current_game
    scenario_index = random.randint(0, len(current_game.scenarios) - 1)
    scenario = current_game.scenarios[scenario_index]
    
    return jsonify({
        'scenario_index': scenario_index,
        'question': scenario.question,
        'choices': scenario.choices
    })

@app.route('/play_scenario', methods=['POST'])
def play_scenario():
    global current_game
    data = request.json
    scenario_index = data['scenario_index']
    choice_index = data['choice_index']
    
    result = current_game.play_scenario(scenario_index, choice_index)
    
    # Determine if game should end
    game_over = current_game.player.balance <= 0 or len(current_game.player.game_history) >= 15
    
    if game_over:
        summary = current_game.get_game_summary()
        return jsonify({
            'game_over': True,
            **summary
        })
    
    return jsonify({
        'game_over': False,
        **result
    })

if __name__ == "__main__":
    app.run(debug=True)