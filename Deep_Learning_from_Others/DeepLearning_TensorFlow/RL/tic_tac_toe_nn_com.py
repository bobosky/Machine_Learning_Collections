#encoding: utf-8
'''
Sarsa λ AIコム
'''
import random
from mark import Mark
from maru_mark import Maru
from batsu_mark import Batsu
from empty_mark import Empty

from collections import defaultdict

import tensorflow as tf
import model_mlp as model

import numpy as np

class SarsaNNCom:
    def __init__(self, mark, epsilon=0.1, step_size=0.1, td_lambda=0.6):
        '''
        初期化
        arguments:
            どちらのマークのプレイヤーとして行動するか
            ソフト方策用のepsilon(前回の実装ではstaticに定義していた)
            TD(λ)のステップ数
            TD(λ)のλ
        '''
        self.mark = mark
        self.epsilon = epsilon
        self.step_size = step_size
        self.td_lambda = td_lambda

        # tensorflow Session
        self.sess = tf.InteractiveSession()
        # input placeholder
        self.x = tf.placeholder(tf.float32, shape=[None, 9])
        self.logits = model.inference(self.x, str(mark.to_int()))
   
        # initialize
        init_op = tf.initialize_all_variables()
        self.sess.run(init_op)
 
        # 価値テーブルを保持(Comを保存できるようにする)
        # stateはhashableにしてvalueのkeyにする
        self.value = defaultdict(lambda: 0.0)

        # TD(λ)で使う直前の状態
        self.previous_state = None
        # TD(λ)で使う現在の状態
        self.current_state = None
        # 各状態の適格度
        self.accumulated_weights = defaultdict(lambda: 0.0)

        self.training = True
        self.verbose = False

    def is_training(self):
        return self.training

    def is_verbose(self):
        return self.verbose

    def select_index(self, state):
        '''
        AIの行動選択
        arguments:
            状態
        return:
            行動
        '''
        # 行動とその価値をニューラルネットワークで推定
        state_array = np.asarray(state.to_array())
        state_array = state_array.reshape(-1, 9)
        action_values = self.sess.run([self.logits], feed_dict={self.x: state_array})
        print np.shape(action_values)
        selected_action = np.argmax(action_values)
        print selected_action

        if self.training:
            if random.random() < self.epsilon:
                # ランダム(ε-greedy)
                selected_action = random.choice(state.get_valid_actions()) 
            else:
                # 行動価値
                value = action_values[0][0][selected_action]
                if self.verbose:
                    print("action %s, value: %f" % (selected_action, value))
        # 行動後の状態を保持
        self.current_state = state.set(selected_action, self.mark)
        return selected_action

    def learn(self, reward, finished=False):
        '''
        価値の更新
        arguments:
            報酬
            終端状態かどうか
        '''
        if self.training and self.previous_state:
            if self.verbose:
                print("Player %s training: " % (self.mark.to_string()))
            previous_value = self.value[self.previous_state]
            
            # 適確度の計算
            for state in self.accumulated_weights:
                # ステップごとにλをかける
                self.accumulated_weights[state] *= self.td_lambda
            # 状態が一致していれば+1
            self.accumulated_weights[self.previous_state] += 1.0

            # 価値の更新
            if self.current_state:
                current_value = self.value[self.current_state]
                value_diff = reward + current_value - previous_value
            else:
                value_diff = reward - previous_value

            for state, weight in self.accumulated_weights.iteritems():
                self.value[state] += self.step_size * value_diff * weight
       
            if self.verbose:
                print("previous value: %f" % (previous_value))
                print("value diff: %f" % (value_diff)) 
                updated_value = self.value[self.previous_state]
                print("updated value: %f" % (updated_value))

            # 適格度の初期化
            if self.current_state is None:
                self.accumurated_weights = defaultdict(lambda: 0.0)

        self.previous_state = self.current_state
        self.current_state = None

