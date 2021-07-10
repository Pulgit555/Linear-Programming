import os
import json
import numpy as np 
import cvxpy as cp 
from itertools import chain


flagg = True
flagr = True
flagt = False
possible_states = ['N','S','E','W','C']
materials = [0,1,2]
arrows = [0,1,2,3]
health = [0,25,50,75,100]
MM_accept_states = ['D','R']
step_cost = -10
hit_reward = -40
num_states = 600
states = []
A=[]
r=[]
alpha = np.zeros(num_states)
tupple = np.zeros(num_states)
ab = []
possible_actions = []
allowed_moves = {
    'N':['C','N','CA'],
    'S':['C','S','G'],
    'E':['C','E','A','B'],
    'W':['C','W','A'],
    'C':['C','W','N','S','E','A','B']
}

def init():
	for a in possible_states:
		for b in  materials:
			for c in arrows:
				for d in MM_accept_states:
					for e in health:
						states.append([a,b,c,d,e])

def save_json(to_write):
    file = open("./outputs/part_3_output.json", "w")
    json.dump(to_write, file)
    file.close()

def action_ctop(st):
	if(st=='A'):
		return "SHOOT"
	elif(st=='B'):
		return "HIT"
	elif(st=='C'):
		return "CRAFT"
	elif(st=='G'):
		return "GATHER"
	elif(st=='s'):
		return "STAY"
	elif(st=='r'):
		return "RIGHT"
	elif(st=='l'):
		return "LEFT"
	elif(st=='u'):
		return "UP"
	elif(st=='d'):
		return "DOWN"
	elif(st=='n'):
		return "NONE"

def give_me_A_and_B():
	for a in possible_states:
		for b in  materials:
			for c in arrows:
				for d in MM_accept_states:
					for e in health:
						if(e!=0):
							if(a=='N'):
								for act in allowed_moves[a]:
									if(d=='D'):
										if(act == 'C'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('d')
											temp[states.index(['C',b,c,"D",e])]+=-0.85*0.8
											temp[states.index(['E',b,c,"D",e])]+=-0.15*0.8
											temp[states.index(['C',b,c,"R",e])]+=-0.85*0.2
											temp[states.index(['E',b,c,"R",e])]+=-0.15*0.2
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost)
										if(act == 'N'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]=+1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('s')
											if(flagr):
												temp[states.index([a,b,c,"D",e])]+=-0.85*0.8 
											temp[states.index([a,b,c,"R",e])]+=-0.85*0.2
											temp[states.index(['E',b,c,"D",e])]+=-0.15*0.8
											temp[states.index(['E',b,c,"R",e])]+=-0.15*0.2
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost)
										if(act == 'CA'):
											if(b>0):
												if(c==0):
													temp = np.zeros(num_states)
													temp[states.index([a,b,c,d,e])]+=1
													tupple[states.index([a,b,c,d,e])]+=1
													possible_actions.append('C')
													temp[states.index([a,b-1,c+1,"D",e])]+=-0.50*0.8
													temp[states.index([a,b-1,c+2,"D",e])]+=-0.35*0.8
													temp[states.index([a,b-1,c+3,"D",e])]+=-0.15*0.8
													temp[states.index([a,b-1,c+1,"R",e])]+=-0.50*0.2
													temp[states.index([a,b-1,c+2,"R",e])]+=-0.35*0.2
													temp[states.index([a,b-1,c+3,"R",e])]+=-0.15*0.2
													if(flagt):
														temp[states.index([a,b,c,d,e])]=1
													A.append(temp.tolist())
													ab.append(states.index([a,b,c,d,e]))
													r.append(step_cost)
												if(c==1):
													temp = np.zeros(num_states)
													temp[states.index([a,b,c,d,e])]+=1
													tupple[states.index([a,b,c,d,e])]+=1
													possible_actions.append('C')
													temp[states.index([a,b-1,c+1,"D",e])]+=-0.50*0.8
													temp[states.index([a,b-1,c+2,"D",e])]+=-0.50*0.8
													temp[states.index([a,b-1,c+1,"R",e])]+=-0.50*0.2
													temp[states.index([a,b-1,c+2,"R",e])]+=-0.50*0.2
													if(flagt):
														temp[states.index([a,b,c,d,e])]=1
													A.append(temp.tolist())
													ab.append(states.index([a,b,c,d,e]))
													r.append(step_cost)
												if(c==2):
													temp = np.zeros(num_states)
													temp[states.index([a,b,c,d,e])]+=1
													tupple[states.index([a,b,c,d,e])]+=1
													possible_actions.append('C')
													temp[states.index([a,b-1,c+1,"D",e])]+=-1*0.8
													temp[states.index([a,b-1,c+1,"R",e])]+=-1*0.2
													if(flagt):
														temp[states.index([a,b,c,d,e])]=1
													A.append(temp.tolist())
													ab.append(states.index([a,b,c,d,e]))
													r.append(step_cost)
												if(c==3 and flagg == True):
													temp = np.zeros(num_states)
													temp[states.index([a,b,c,d,e])]+=1
													tupple[states.index([a,b,c,d,e])]+=1
													possible_actions.append('C')
													temp[states.index([a,b-1,c,"D",e])]+=-1*0.8
													temp[states.index([a,b-1,c,"R",e])]+=-1*0.2
													if(flagt):
														temp[states.index([a,b,c,d,e])]=1
													A.append(temp.tolist())
													ab.append(states.index([a,b,c,d,e]))
													r.append(step_cost)
									if(d=='R'): 
										if(act == 'C'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('d')
											temp[states.index(['C', b,c,"D",e])]+=-0.85*0.5
											temp[states.index(['E', b,c,"D",e])]+=-0.15*0.5
											temp[states.index(['C',b,c,"R",e])]+=-0.85*0.5
											temp[states.index(['E',b,c,"R",e])]+=-0.15*0.5
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost)
										if(act == 'N'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('s')
											if(flagr):
												temp[states.index([a,b,c,"D",e])]+=-0.85*0.50 
											temp[states.index(['E',b,c,"D",e])]+=-0.15*0.50
											temp[states.index([a,b,c,"R",e])]+=-0.85*0.50
											temp[states.index(['E',b,c,"R",e])]+=-0.15*0.50
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost)
										if(act == 'CA'):
											if(b>0):
												if(c==0):
													temp = np.zeros(num_states)
													temp[states.index([a,b,c,d,e])]+=1
													tupple[states.index([a,b,c,d,e])]+=1
													possible_actions.append('C')
													temp[states.index([a,b-1,c+1,"D",e])]+=-0.50*0.5
													temp[states.index([a,b-1,c+2,"D",e])]+=-0.35*0.5
													temp[states.index([a,b-1,c+3,"D",e])]+=-0.15*0.5
													temp[states.index([a,b-1,c+1,"R",e])]+=-0.50*0.5
													temp[states.index([a,b-1,c+2,"R",e])]+=-0.35*0.5
													temp[states.index([a,b-1,c+3,"R",e])]+=-0.15*0.5
													if(flagt):
														temp[states.index([a,b,c,d,e])]=1
													A.append(temp.tolist())
													ab.append(states.index([a,b,c,d,e]))
													r.append(step_cost)
												if(c==1):
													temp = np.zeros(num_states)
													temp[states.index([a,b,c,d,e])]+=1
													tupple[states.index([a,b,c,d,e])]+=1
													possible_actions.append('C')
													temp[states.index([a,b-1,c+1,"D",e])]+=-0.50*0.5
													temp[states.index([a,b-1,c+2,"D",e])]+=-0.50*0.5
													temp[states.index([a,b-1,c+1,"R",e])]+=-0.50*0.5
													temp[states.index([a,b-1,c+2,"R",e])]+=-0.50*0.5
													if(flagt):
														temp[states.index([a,b,c,d,e])]=1
													A.append(temp.tolist())
													ab.append(states.index([a,b,c,d,e]))
													r.append(step_cost)
												if(c==2):
													temp = np.zeros(num_states)
													temp[states.index([a,b,c,d,e])]+=1
													tupple[states.index([a,b,c,d,e])]+=1
													possible_actions.append('C')
													temp[states.index([a,b-1,c+1,"D",e])]+=-1*0.5
													temp[states.index([a,b-1,c+1,"R",e])]+=-1*0.5
													if(flagt):
														temp[states.index([a,b,c,d,e])]=1
													A.append(temp.tolist())
													ab.append(states.index([a,b,c,d,e]))
													r.append(step_cost)
												if(c==3 and flagg == True):
													temp = np.zeros(num_states)
													temp[states.index([a,b,c,d,e])]+=1
													tupple[states.index([a,b,c,d,e])]+=1
													possible_actions.append('C')
													temp[states.index([a,b-1,c,"D",e])]+=-1*0.5
													temp[states.index([a,b-1,c,"R",e])]+=-1*0.5
													if(flagt):
														temp[states.index([a,b,c,d,e])]=1
													A.append(temp.tolist())
													ab.append(states.index([a,b,c,d,e]))
													r.append(step_cost)
							if(a=='S'):
								for act in allowed_moves[a]:
									if(d=='D'):
										if(act == 'C'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('u')
											temp[states.index(['C',b,c,"D",e])]+=-0.85*0.8
											temp[states.index(['E',b,c,"D",e])]+=-0.15*0.8
											temp[states.index(['C',b,c,"R",e])]+=-0.85*0.2
											temp[states.index(['E',b,c,"R",e])]+=-0.15*0.2
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost)
										if(act == 'S'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('s')
											if(flagr):
												temp[states.index(['S',b,c,"D",e])]+=-0.85*0.8
											temp[states.index(['E',b,c,"D",e])]+=-0.15*0.8
											temp[states.index(['S',b,c,"R",e])]+=-0.85*0.2
											temp[states.index(['E',b,c,"R",e])]+=-0.15*0.2
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost)
										if(act == 'G'):
											if(b<2):
												temp = np.zeros(num_states)
												temp[states.index([a,b,c,d,e])]+=1
												tupple[states.index([a,b,c,d,e])]+=1
												possible_actions.append('G')
												temp[states.index([a,b+1,c,"D",e])]+=-0.75*0.8
												temp[states.index([a,b+1,c,"R",e])]+=-0.75*0.2
												temp[states.index([a,b,c,"R",e])]+=-0.25*0.2
												if(flagr):
													temp[states.index([a,b,c,"D",e])]+=-0.25*0.8
												if(flagt):
													temp[states.index([a,b,c,d,e])]=1
												A.append(temp.tolist())
												ab.append(states.index([a,b,c,d,e]))
												r.append(step_cost)
											if(b==2 and flagg == True):
												temp = np.zeros(num_states)
												temp[states.index([a,b,c,d,e])]+=1
												tupple[states.index([a,b,c,d,e])]+=1
												possible_actions.append('G')
												if(flagr):
													temp[states.index([a,b,c,"D",e])]+=-1*0.8
												temp[states.index([a,b,c,"R",e])]+=-0.75*0.2
												temp[states.index([a,b,c,"R",e])]+=-0.25*0.2
												if(flagt):
													temp[states.index([a,b,c,d,e])]=1
												A.append(temp.tolist())
												ab.append(states.index([a,b,c,d,e]))
												r.append(step_cost)
									if(d=='R'):
										if(act == 'C'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('u')
											temp[states.index(['C',b,c,"D",e])]+=-0.85*0.5
											temp[states.index(['E',b,c,"D",e])]+=-0.15*0.5
											temp[states.index(['C',b,c,"R",e])]+=-0.85*0.5
											temp[states.index(['E',b,c,"R",e])]+=-0.15*0.5
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost)
										if(act == 'S'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('s')
											temp[states.index(['S',b,c,"D",e])]+=-0.85*0.5
											temp[states.index(['E',b,c,"D",e])]+=-0.15*0.5
											if(flagr):
												temp[states.index(['S',b,c,"R",e])]+=-0.85*0.5
											temp[states.index(['E',b,c,"R",e])]+=-0.15*0.5
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost)
										if(act == 'G'):
											if(b<2):
												temp = np.zeros(num_states)
												temp[states.index([a,b,c,d,e])]+=1
												tupple[states.index([a,b,c,d,e])]+=1
												possible_actions.append('G')
												temp[states.index([a,b+1,c,"D",e])]+=-0.75*0.5
												temp[states.index([a,b+1,c,"R",e])]+=-0.75*0.5
												temp[states.index([a,b,c,"D",e])]+=-0.25*0.5
												if(flagr):
													temp[states.index([a,b,c,"R",e])]+=-0.25*0.5
												if(flagt):
													temp[states.index([a,b,c,d,e])]=1
												A.append(temp.tolist())
												ab.append(states.index([a,b,c,d,e]))
												r.append(step_cost)
											if(b==2 and flagg == True):
												temp = np.zeros(num_states)
												temp[states.index([a,b,c,d,e])]+=1
												tupple[states.index([a,b,c,d,e])]+=1
												possible_actions.append('G')
												temp[states.index([a,b,c,"D",e])]+=-0.75*0.5
												if(flagr):
													temp[states.index([a,b,c,"R",e])]+=-1*0.5
												temp[states.index([a,b,c,"D",e])]+=-0.25*0.5
												if(flagt):
													temp[states.index([a,b,c,d,e])]=1
												A.append(temp.tolist())
												ab.append(states.index([a,b,c,d,e]))
												r.append(step_cost)
							if(a=='E'):
								for act in allowed_moves[a]:
									if(d=='D'):
										if(act == 'C'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('l')
											temp[states.index(['C',b,c,"D",e])]+=-1*0.8
											temp[states.index(['C',b,c,"R",e])]+=-1*0.2
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost)
										if(act == 'E'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('s')
											if(flagr):
												temp[states.index([a,b,c,"D",e])]+=-1*0.8 
											temp[states.index([a,b,c,"R",e])]+=-1*0.2
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost)
										if(act == 'A'):
											if(c>0):
												temp = np.zeros(num_states)
												temp[states.index([a,b,c,d,e])]+=1
												tupple[states.index([a,b,c,d,e])]+=1
												possible_actions.append('A')
												temp[states.index([a,b,c-1,'D',e-25])]+=-0.90*0.8
												temp[states.index([a,b,c-1,'R',e-25])]+=-0.90*0.2
												temp[states.index([a,b,c-1,'D',e])]+=-0.10*0.8
												temp[states.index([a,b,c-1,'R',e])]+=-0.10*0.2
												if(flagt):
													temp[states.index([a,b,c,d,e])]=1
												A.append(temp.tolist())
												ab.append(states.index([a,b,c,d,e]))
												r.append(step_cost)
										if(act == 'B'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('B')
											temp[states.index([a,b,c,"D",max(0,e-50)])]+=-0.20*0.8
											temp[states.index([a,b,c,"R",max(0,e-50)])]+=-0.20*0.2
											if(flagr):
												temp[states.index([a,b,c,"D",e])]+=-0.80*0.8
											temp[states.index([a,b,c,"R",e])]+=-0.80*0.2
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost)
									if(d=='R'):
										if(act == 'C'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('l')
											temp[states.index(['E',b,0,"D",min(100,e+25)])]+=-1*0.5
											temp[states.index(['C',b,c,"R",e])]+=-1*0.5
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost+hit_reward/2)
										if(act == 'E'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('s')
											if(flagr):
												temp[states.index([a,b,c,"R",e])]+=-1*0.5
											temp[states.index([a,b,0,"D",min(100,e+25)])]+=-1*0.5
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost+hit_reward/2)
										if(act == 'A'):
											if(c>0):
												temp = np.zeros(num_states)
												temp[states.index([a,b,c,d,e])]+=1
												tupple[states.index([a,b,c,d,e])]+=1
												possible_actions.append('A')
												temp[states.index([a,b,0,'D',min(100,e+25)])]+=-1*0.5
												temp[states.index([a,b,c-1,'R',e-25])]+=-0.90*0.5
												temp[states.index([a,b,c-1,'R',e])]+=-0.1*0.5
												if(flagt):
													temp[states.index([a,b,c,d,e])]=1
												A.append(temp.tolist())
												ab.append(states.index([a,b,c,d,e]))
												r.append(step_cost + hit_reward/2)
										if(act == 'B'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('B')
											temp[states.index([a,b,0,"D",min(100,e+25)])]+=-1*0.5
											temp[states.index([a,b,c,"R",max(0,e-50)])]+=-0.20*0.5
											temp[states.index([a,b,c,"R",e])]+=-0.80*0.5
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost+hit_reward/2)
							if(a=='W'):
								for act in allowed_moves[a]:
									if(d=='D'):
										if(act == 'C'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]=+1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('r')
											temp[states.index(['C',b,c,"D",e])]+=-1*0.8
											temp[states.index(['C',b,c,"R",e])]+=-1*0.2
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost)
										if(act == 'W'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('s')
											if(flagr):
												temp[states.index([a,b,c,"D",e])]+=(-1*0.80)
											temp[states.index([a,b,c,"R",e])]+=-1*0.2
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost)
										if(act == 'A'):
											if(c>0):
												temp = np.zeros(num_states)
												temp[states.index([a,b,c,d,e])]+=1
												tupple[states.index([a,b,c,d,e])]+=1
												possible_actions.append('A')
												temp[states.index([a,b,c-1,"D",e-25])]+=-0.25*0.8
												temp[states.index([a,b,c-1,"R",e-25])]+=-0.25*0.2
												temp[states.index([a,b,c-1,"D",e])]+=-0.75*0.8
												temp[states.index([a,b,c-1,"R",e])]+=-0.75*0.2
												if(flagt):
													temp[states.index([a,b,c,d,e])]=1
												A.append(temp.tolist())
												ab.append(states.index([a,b,c,d,e]))
												r.append(step_cost) 
									if(d=='R'):
										if(act == 'C'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]=+1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('r')
											temp[states.index(['C',b,c,"D",e])]+=-1*0.5
											temp[states.index(['C',b,c,"R",e])]+=-1*0.5
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost)
										if(act == 'W'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('s')
											if(flagr):
												temp[states.index([a,b,c,"R",e])]+=-1*0.5
											temp[states.index([a,b,c,"D",e])]+=-1*0.5
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost)
										if(act == 'A'):
											if(c>0):
												temp = np.zeros(num_states)
												temp[states.index([a,b,c,d,e])]+=1
												tupple[states.index([a,b,c,d,e])]+=1
												possible_actions.append('A')
												temp[states.index([a,b,c-1,"D",e-25])]+=-0.25*0.5
												temp[states.index([a,b,c-1,"R",e-25])]+=-0.25*0.5
												temp[states.index([a,b,c-1,"D",e])]+=-0.75*0.5
												temp[states.index([a,b,c-1,"R",e])]+=-0.75*0.5
												if(flagt):
													temp[states.index([a,b,c,d,e])]=1
												A.append(temp.tolist())
												ab.append(states.index([a,b,c,d,e]))
												r.append(step_cost)
							if(a=='C'):
								for act in allowed_moves[a]:
									if(d=='D'):
										if(act == 'C'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('s')
											temp[states.index(['C',b,c,'D',e])]+=-0.85*0.8
											temp[states.index(['E',b,c,'D',e])]+=-0.15*0.8
											temp[states.index(['C',b,c,'R',e])]+=-0.85*0.2
											temp[states.index(['E',b,c,'R',e])]+=-0.15*0.2
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost)
										if(act == 'E'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('r')
											temp[states.index(['E',b,c,'D',e])]+=-1*0.8
											temp[states.index(['E',b,c,'R',e])]+=-1*0.2
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost)
										if(act == 'W'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('l')
											temp[states.index(['W',b,c,'D',e])]+=-0.85*0.8
											temp[states.index(['E',b,c,'D',e])]+=-0.15*0.8
											temp[states.index(['W',b,c,'R',e])]+=-0.85*0.2
											temp[states.index(['E',b,c,'R',e])]+=-0.15*0.2
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost)
										if(act == 'N'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('u')
											temp[states.index(['N',b,c,'D',e])]+=-0.85*0.8
											temp[states.index(['E',b,c,'D',e])]+=-0.15*0.8
											temp[states.index(['N',b,c,'R',e])]+=-0.85*0.2
											temp[states.index(['E',b,c,'R',e])]+=-0.15*0.2
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost)
										if(act == 'S'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('d')
											temp[states.index(['S',b,c,'D',e])]+=-0.85*0.8
											temp[states.index(['E',b,c,'D',e])]+=-0.15*0.8
											temp[states.index(['S',b,c,'R',e])]+=-0.85*0.2
											temp[states.index(['E',b,c,'R',e])]+=-0.15*0.2
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost)
										if(act == 'A'):
											if(c>0):
												temp = np.zeros(num_states)
												temp[states.index([a,b,c,d,e])]+=1
												tupple[states.index([a,b,c,d,e])]+=1
												possible_actions.append('A')
												temp[states.index([a,b,c-1,'D',e-25])]+=-0.50*0.8
												temp[states.index([a,b,c-1,'D',e])]+=-0.50*0.8
												temp[states.index([a,b,c-1,'R',e-25])]+=-0.50*0.2
												temp[states.index([a,b,c-1,'R',e])]+=-0.50*0.2
												if(flagt):
													temp[states.index([a,b,c,d,e])]=1
												A.append(temp.tolist())
												ab.append(states.index([a,b,c,d,e]))
												r.append(step_cost)
										if(act == 'B'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('B')
											temp[states.index([a,b,c,'D',max(0,e-50)])]+=-0.10*0.8
											temp[states.index([a,b,c,'D',e])]+=-0.90*0.8
											temp[states.index([a,b,c,'R',max(0,e-50)])]+=-0.10*0.2
											temp[states.index([a,b,c,'R',e])]+=-0.90*0.2
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost)
									if(d=='R'):
										if(act == 'C'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('s')
											temp[states.index([a,b,0,'D',min(100,e+25)])]+=-0.85*0.5
											temp[states.index([a,b,0,'D',min(100,e+25)])]+=-0.15*0.5
											temp[states.index(['C',b,c,'R',e])]+=-0.85*0.5
											temp[states.index(['E',b,c,'R',e])]+=-0.15*0.5
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost+(0.5)*hit_reward)
										if(act == 'E'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('r')
											temp[states.index([a,b,0,'D',min(100,e+25)])]+=-1*0.5
											temp[states.index(['E',b,c,'R',e])]+=-1*0.5
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost+(0.5)*hit_reward)
										if(act == 'W'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('l')
											temp[states.index([a,b,0,'D',min(100,e+25)])]+=-0.85*0.5
											temp[states.index([a,b,0,'D',min(100,e+25)])]+=-0.15*0.5
											temp[states.index(['W',b,c,'R',e])]+=-0.85*0.5
											temp[states.index(['E',b,c,'R',e])]+=-0.15*0.5
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost+(0.5)*hit_reward)
										if(act == 'N'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('u')
											temp[states.index([a,b,0,'D',min(100,e+25)])]+=-0.85*0.5
											temp[states.index([a,b,0,'D',min(100,e+25)])]+=-0.15*0.5
											temp[states.index(['N',b,c,'R',e])]+=-0.85*0.5
											temp[states.index(['E',b,c,'R',e])]+=-0.15*0.5
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost+(0.5)*hit_reward)
										if(act == 'S'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('d')
											temp[states.index([a,b,0,'D',min(100,e+25)])]+=-0.85*0.5
											temp[states.index([a,b,0,'D',min(100,e+25)])]+=-0.15*0.5
											temp[states.index(['S',b,c,'R',e])]+=-0.85*0.5
											temp[states.index(['E',b,c,'R',e])]+=-0.15*0.5
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost+(0.5)*hit_reward)
										if(act == 'A'):
											if(c>0):
												temp = np.zeros(num_states)
												temp[states.index([a,b,c,d,e])]+=1
												tupple[states.index([a,b,c,d,e])]+=1
												possible_actions.append('A')
												temp[states.index([a,b,0,'D',min(100,e+25)])]+=-1*0.5
												temp[states.index([a,b,c-1,'R',e-25])]+=-0.50*0.5
												temp[states.index([a,b,c-1,'R',e])]+=-0.50*0.5
												if(flagt):
													temp[states.index([a,b,c,d,e])]=1
												A.append(temp.tolist())
												ab.append(states.index([a,b,c,d,e]))
												r.append(step_cost+(0.5)*hit_reward)
										if(act == 'B'):
											temp = np.zeros(num_states)
											temp[states.index([a,b,c,d,e])]+=1
											tupple[states.index([a,b,c,d,e])]+=1
											possible_actions.append('B')
											temp[states.index([a,b,0,'D',min(100,e+25)])]+=-1*0.5
											temp[states.index([a,b,c,'R',e])]+=-0.90*0.5
											temp[states.index([a,b,c,'R',max(0,e-50)])]+=-0.10*0.5
											if(flagt):
												temp[states.index([a,b,c,d,e])]=1
											A.append(temp.tolist())
											ab.append(states.index([a,b,c,d,e]))
											r.append(step_cost+(0.5)*hit_reward)
						if(e==0):
							temp = np.zeros(num_states)
							temp[states.index([a,b,c,d,e])]+=1
							tupple[states.index([a,b,c,d,e])]+=1
							possible_actions.append('n')
							if(flagt):
								temp[states.index([a,b,c,d,e])]=1
							A.append(temp.tolist())
							ab.append(states.index([a,b,c,d,e]))
							r.append(0)

def give_me_alpha():
    alpha[states.index(['C',2,3,'R',100])]=1

def complete_my_assignment():
	global X 
	size = len(A[0])
	X = cp.Variable(shape=(size,1),name="X")
	constraints = [cp.matmul(A,X)== alpha, X>=0]
	objective = cp.Maximize(cp.matmul(r,X))
	problem = cp.Problem(objective,constraints)
	return problem.solve()

def give_me_policy():
	arr = [0]*600
	arr1 = [0]*600
	arr2 = ['']*600
	policy = []
	for i in range(0,1936):
		ss = ab[i]
		if(arr1[ss]==0):
			arr[ss] = X[i]
			arr2[ss] = possible_actions[i]
			arr1[ss] = 1
		elif(arr[ss]<X[i]):
			arr[ss] = X[i]
			arr2[ss] = possible_actions[i]
	for a in possible_states:
		for b in  materials:
			for c in arrows:
				for d in MM_accept_states:
					for e in health:
						policy.append([(a,b,c,d,e),action_ctop(arr2[states.index([a,b,c,d,e])])])
	return policy

if not os.path.exists("outputs"):
    os.makedirs("outputs")

init()
give_me_A_and_B()
give_me_alpha()
A=np.array(A)
A=A.transpose()
r=np.array(r)
r=r[:,np.newaxis]
r=r.transpose()
alpha=np.array(alpha)
alpha = alpha[:,np.newaxis]
objective = complete_my_assignment()
X=X.value
X=list(chain.from_iterable(X))
policy=give_me_policy()

dictionary = {
	"a":A.tolist(),
	"r":r.tolist(),
	"alpha":alpha.tolist(),
	"x":X,
	"policy":policy,
	"objective":objective,
}
save_json(dictionary)
print("objective ->",objective)
