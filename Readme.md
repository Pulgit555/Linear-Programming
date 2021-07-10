# Linear Programming

> + ### Team
> + Team : 76 : Platypus_Perry
> + Archit Jain (2019101053)
> + Pulkit Gupta (2019101078)

This part of assignment covers the concept of the Linear programming for solving MDPs.

## How to run

Run the following command to obtain the `output.json` in `outputs` folder
```
    > python3 part_3.py
``` 

## Making matrix A
Each state is uniquely identified by a tuple of three values. The tuple is ordered as <Postion of IJ, Number of materials, Number of arrows, MM's state, MM's health>.

- The domains for the tuple values are as follows:
```
    Postion of IJ : N, S, E, W, C
    Number of materials : 0, 1, 2
    Number of arrows : 0, 1, 2, 3  
    MM's state : R, D 
    MM's health : 0, 25, 50, 75, 100
```
Hence, there are 600 states in total.
- We iterate over all possible combinations of ***<Postion of IJ, Number of materials, Number of arrows, MM's state, MM's health>***. 
- For each such unique state, we check the possible actions between ***RIGHT, LEFT, UP, DOWN, STAY, CRAFT, GATHER, SHOOT, HIT and STAY***.
- Each state has its own index value based on incrementation in the order: Postion of IJ, Number of materials, Number of arrows, MM's state, MM's health 
- For every possible action, we make a vector of length equivalent to the number of states. All values in this vector are zero except that at the index of the current state and the indices of the next states to which the action takes us.
- Say, if an action can take you from state A to B with probability ***P***. The value ***-P*** will be assigned at the index of state B. And ***P*** will be added to the index corresponding to state A.
- We append the created vector for a state **only** when at least one action is valid from a state.

## Making policy and analyzing it
- A policy suggests the best action for a particular state and is represented by a sequence of ***STATE - ACTION*** pairs. Now that we have X calculated using the cvxpy library with the use of A, r and alpha and then choosing the action for a particular state that have maximum x value in policy generation. 

### Interpretations from policy
- When IJ has no arrows to shoot and no material to craft his decision depends on MM's state, when MM is in Ready state he will try to GATHER material so that it can craft the arrows and to be present in a safe state else if MM in Dormant state he will move to CENTER or EAST to HIT MM with his blade. More suprisingly in this policy due to no positive reward on killing MM, IJ will prefer to STAY on NORTH all time
- Another result we obatin is he will always wait in safe state till MM goes back to Dormant state and when it goes back IJ will move towards EAST via CENTER and then start attacking MM by shooting the arrrows than hitting by blade due to more success probability to SHOOT than HIT 
- IJ will move to safe state as MM changes its state to Ready state and waits for MM to change its state to Dormant when not present in EAST and when he is in EAST he will continue to SHOOT till his arrows are over and then starts performing HIT action to hit MM with his blade till MM's health is zero 


## Multiple policies?
+ Answer is ***Yes***
### Reasons
+ The the policy can be changed for a state-action pair having same X values are interchangeable since we are updating the action only is it has more X value from the action taken earlier for same state.
    + no change in any output lists except `policy` 
+ Irrespective of X values order it also depends on the order in which we proceeds currently we are ***Postion of IJ, Number of materials, Number of arrows, MM's state, MM's health***  - if we change that then some other action may lead to the first highest value than the one in the current set up. An example is to change the movement array 
    ```
        allowed_moves = {
            'N':['C','N','CA'],
            'S':['C','S','G'],
            'E':['C','E','A','B'],
            'W':['C','W','A'],
            'C':['C','W','N','S','E','A','B']
        }
    ```

    + This does not affect the ***A*** matrix as that is created before solving the LPP. 

    + The ***alpha*** vector holds the initial probabilities of the states which is `["C",2,3,"R",100]` this does not change during the algorithm as the start state of the scenario is fixed.
  
    + The ***R*** vector holds the reward of taking a *valid* action from each state. This is determined using the step cost of the action before solving the LPP and will hence not be affected by the policy.

    + The ***X*** vector is the solution to the LPP with A, alpha and R as parameters. Since neither of the three vectors change, X will not change either. However the actions that take place in order to produce X will differ for a different policy

    + ***Objective*** will also remains unchanged due to no change in A, alpha and R

+ Other ways to change the policy are to change the parameters like starting state can change alpha or change the step costs which would change the R vector or changing the probabilites of sucessfull steps or been attacked by MM as well as bad reward on attacked by MM. These changes will obviously impact the policy as the LPP solver gets different variables. However, this changes the question altogether. If we want to solve the same question, yet generate a different policy, only above points are applicable.