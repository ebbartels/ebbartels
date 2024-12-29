import gymnasium as gym
import random
import numpy as np
import time
from collections import deque
import pickle


from collections import defaultdict

EPISODES =  3000
LEARNING_RATE = .1
DISCOUNT_FACTOR = .99
EPSILON = 1
EPSILON_DECAY = .99


def default_Q_value():
    return 0

if __name__ == "__main__":
    env_name = "CliffWalking-v0"
    env = gym.envs.make(env_name)
    env.reset(seed=1)

    # You will need to update the Q_table in your iteration
    Q_table = defaultdict(default_Q_value) # starts with a pessimistic estimate of zero reward for each state.
    episode_reward_record = deque(maxlen=100)

    for i in range(EPISODES):
        episode_reward = 0
        done = False
        obs = env.reset()[0]

        ##########################################################
        # YOU DO NOT NEED TO CHANGE ANYTHING ABOVE THIS LINE
        # TODO: Replace the following with Q-Learning
       
        if random.random() < EPSILON:
            action = env.action_space.sample()
        else:
            action = np.argmax([Q_table[(obs, a)] for a in range(env.action_space.n)])

        while (not done):
                
            next_obs,reward,terminated,truncated,info = env.step(action)
            episode_reward += reward # update episode reward
            done = terminated or truncated
            
            if random.random() < EPSILON:
                next_action = env.action_space.sample()
            else:
                next_action = np.argmax([Q_table[(next_obs, a)] for a in range(env.action_space.n)])

            if not done:
                Q_table[(obs, action)] = (1-LEARNING_RATE) * Q_table[(obs, action)] + LEARNING_RATE * (
                    reward + DISCOUNT_FACTOR * np.max([Q_table[(next_obs, a)] for a in range(env.action_space.n)]) 
                )
            # 
            else:  # If the episode is done, no next state or action
                Q_table[(obs, action)] = (1 - LEARNING_RATE) * Q_table[(obs, action)] + LEARNING_RATE * reward

            obs, action = next_obs, next_action
            
       
        EPSILON *= EPSILON_DECAY
            
        # END of TODO
        # YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE
        ##########################################################

        # record the reward for this episode
        episode_reward_record.append(episode_reward) 
     
        if i % 100 == 0 and i > 0:
            print("LAST 100 EPISODE AVERAGE REWARD: " + str(sum(list(episode_reward_record))/100))
            print("EPSILON: " + str(EPSILON) )
    
    
    #### DO NOT MODIFY ######
    model_file = open(f'Q_TABLE_QLearning.pkl' ,'wb')
    pickle.dump([Q_table,EPSILON],model_file)
    model_file.close()
    #########################


