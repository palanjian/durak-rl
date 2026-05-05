can turn 'hands', 'attacker_hands', 'defender_hands' into sets, to make checking for legality O(1)

right now, there is no ability to throw in more than one card. The flow is 
Attack -> defend
Attack -> defend
Next player
Attacker -> defend

May want to change this, but it presumably would just cause unstable training/bad signal for learning what to attack/defend w.
# Important:
can turn cards into two different lists, suits and ranks just to ensure checks like:
if card.rank not in {c.rank for c in self.attacker_hands}:
run faster