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
        self.balance = random.randint(500, 2000)  # Lower starting balance
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
            # Career & Income Scenarios
            FinancialScenario(
                question="You've been offered a high-paying job that requires you to relocate to a city with a high cost of living. Do you take it?",
                choices=[
                    "Accept the job and relocate", 
                    "Negotiate a higher salary", 
                    "Decline and seek local opportunities"
                ],
                outcomes=[1000, 500, 0],
                consequences=[
                    "High potential income but high living expenses",
                    "Attempt to balance income and cost of living",
                    "Stay in comfort but risk stagnation"
                ],
                skill_check={
                    'negotiation': 70
                }
            ),
            
            # Investment Scenarios
            FinancialScenario(
                question="You have $1500 to invest. A friend recommends a volatile cryptocurrency. What do you do?",
                choices=[
                    "Invest all in cryptocurrency", 
                    "Diversify into stocks and bonds", 
                    "Hold onto cash until market stabilizes"
                ],
                outcomes=[3000, 500, -100],
                consequences=[
                    "High risk with potential for massive gains or losses",
                    "Moderate growth with reduced risk",
                    "Preserve capital but miss investment opportunities"
                ],
                skill_check={
                    'risk_management': 65
                }
            ),
            
            # Unexpected Expense Scenarios
            FinancialScenario(
                question="Your home needs urgent repairs costing $2500. You have no emergency fund. How do you handle it?",
                choices=[
                    "Take out a high-interest personal loan", 
                    "Borrow from friends or family", 
                    "Negotiate a payment plan with the contractor"
                ],
                outcomes=[-3000, -2000, -1000],
                consequences=[
                    "Immediate debt with high interest",
                    "Potential strain on personal relationships",
                    "Avoid immediate debt but may incur additional costs"
                ]
            ),
            
            # Side Hustle & Income Opportunities
            FinancialScenario(
                question="You discover a lucrative side hustle but it requires significant time commitment. What's your approach?",
                choices=[
                    "Quit your job to pursue it full-time", 
                    "Balance both but risk burnout", 
                    "Research and plan before committing"
                ],
                outcomes=[2000, 1000, 500],
                consequences=[
                    "High reward but major risk to stability",
                    "Potential for dual income but high stress",
                    "Informed decision may lead to better outcomes"
                ],
                skill_check={
                    'financial_literacy': 70
                }
            ),
            
            # Lifestyle and Spending
            FinancialScenario(
                question="You receive a $1000 bonus. How do you allocate it considering your long-term goals?",
                choices=[
                    "Invest 100%, no spending", 
                    "Save 50%, spend 50%", 
                    "Spend most on immediate desires"
                ],
                outcomes=[500, 300, -200],
                consequences=[
                    "Long-term growth but immediate sacrifices",
                    "Balanced approach but not maximizing potential",
                    "Short-term pleasure at the cost of future security"
                ]
            ),

            # Major Life Decisions
            FinancialScenario(
                question="You are considering buying a house but it requires a 20% down payment and you only have 10%. What do you do?",
                choices=[
                    "Wait and save more for a larger down payment", 
                    "Use all savings and take a loan for the rest", 
                    "Look for a cheaper property"
                ],
                outcomes=[-20000, -25000, -15000],
                consequences=[
                    "Financial stability but delayed home ownership",
                    "Immediate home ownership but high debt risk",
                    "Potentially more manageable payments but less ideal property"
                ]
            ),

            # Retirement Planning
            FinancialScenario(
                question="You have the option to contribute to a retirement plan with employer matching. However, it reduces your current take-home pay. What do you do?",
                choices=[
                    "Max out contributions for future security", 
                    "Contribute minimally to maintain current lifestyle", 
                    "Opt out and invest elsewhere"
                ],
                outcomes=[2000, 500, -100],
                consequences=[
                    "Strong future security but less cash now",
                    "Balanced approach but may miss out on employer match",
                    "Immediate cash but potential long-term loss"
                ]
            ),

            # Education Investment
            FinancialScenario(
                question="You have the chance to enroll in an expensive course that promises a high-paying job. However, it requires taking on debt. What do you do?",
                choices=[
                    "Enroll and take on the debt", 
                    "Seek cheaper alternatives", 
                    "Delay education until you can afford it"
                ],
                outcomes=[3000, 1000, 0],
                consequences=[
                    "High risk with potential for high reward",
                    "Safer but may limit future opportunities",
                    "Preserve current finances but risk stagnation"
                ]
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
        
        return {
            'initial_balance': self.player.initial_balance,
            'final_balance': self.player.balance,
            'total_gain': total_gain,
            'performance_score': performance_score,
            'game_history': self.player.game_history,
            'skills': self.player.skills
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
    game_over = current_game.player.balance <= 0 or len(current_game.player.game_history) >= 5
    
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