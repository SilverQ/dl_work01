import tensorflow as tf
import numpy as np
import keras
np.set_printoptions(precision=2)


# input data
input_sentence = 'An open API (often referred to as a public API) is a publicly available application programming interface that provides developers with programmatic access to a proprietary software application or web service. APIs are sets of requirements that govern how one application can communicate and interact with another.'

# create index
char_set = list(set(input_sentence))
char2idx = {c: i for i, c in enumerate(sorted(char_set))}
idx2char = {char2idx[c]: c for c in char2idx}
'''
이 방식의 문제는 index가 생성할 때마다 바뀐다는 것. char-index가 매번 바뀐다면, 그에 따른 각 layer의 weight도 바뀌어야 할 것 같다.
따라서 index를 고정시킬 방안이 필요할 것으로 보인다. char_set을 정렬시켜서 사용해야 할 것 같다.
print(char_set)
print(char2idx)
print(idx2char)
['a', 'y', 'I', 'q', 'r', 'o', 'u', 'p', 'g', 'l', 'e', ' ', 'P', 'c', 'n', 'm', 'A', 'f', ')', 's', 'i', 'v', '.', 'h', 't', 'w', 'd', 'b', '(']
{'t': 24, 'a': 0, 'A': 16, ')': 18, 's': 19, 'i': 20, 'v': 21, 'q': 3, 'g': 8, ' ': 11, 'f': 17, 'P': 12, 'o': 5, '.': 22, 'u': 6, 'r': 4, 'p': 7, 'y': 1, 'h': 23, 'w': 25, 'l': 9, 'I': 2, 'e': 10, 'c': 13, 'n': 14, 'm': 15, 'd': 26, 'b': 27, '(': 28}
{0: 'a', 1: 'y', 2: 'I', 3: 'q', 4: 'r', 5: 'o', 6: 'u', 7: 'p', 8: 'g', 9: 'l', 10: 'e', 11: ' ', 12: 'P', 13: 'c', 14: 'n', 15: 'm', 16: 'A', 17: 'f', 18: ')', 19: 's', 20: 'i', 21: 'v', 22: '.', 23: 'h', 24: 't', 25: 'w', 26: 'd', 27: 'b', 28: '('}

['P', ' ', '(', 'o', 'u', 'a', 'l', 'g', '.', 'b', 'f', 'c', 'w', 'h', 'I', 'm', 's', 't', 'r', 'e', 'i', 'v', 'A', 'q', 'y', 'n', ')', 'p', 'd']
{'t': 17, 'y': 24, 'r': 18, 'P': 0, ' ': 1, 'e': 19, '(': 2, 'o': 3, 'u': 4, 'a': 5, 'l': 6, '.': 8, 'i': 20, 'b': 9, 'v': 21, 'A': 22, 'f': 10, 'q': 23, 'c': 11, 'n': 25, ')': 26, 'w': 12, 'h': 13, 'p': 27, 'I': 14, 'd': 28, 'g': 7, 'm': 15, 's': 16}
{0: 'P', 1: ' ', 2: '(', 3: 'o', 4: 'u', 5: 'a', 6: 'l', 7: 'g', 8: '.', 9: 'b', 10: 'f', 11: 'c', 12: 'w', 13: 'h', 14: 'I', 15: 'm', 16: 's', 17: 't', 18: 'r', 19: 'e', 20: 'i', 21: 'v', 22: 'A', 23: 'q', 24: 'y', 25: 'n', 26: ')', 27: 'p', 28: 'd'}

sorted(char_set) 적용 후
['d', 'I', 'i', 'A', 'o', 'l', 'r', ' ', 'w', 'p', 'm', 'n', '.', 'P', 'u', ')', 'h', 'b', 'v', 't', 'c', 'g', 's', '(', 'a', 'y', 'e', 'q', 'f']
{'d': 10, 'p': 20, 'u': 25, 'I': 5, 'b': 8, 'A': 4, ')': 2, 'o': 19, 'h': 14, 'l': 16, 'r': 22, ' ': 0, 'v': 26, 't': 24, 'c': 9, 'm': 17, 'n': 18, '.': 3, 'g': 13, 's': 23, '(': 1, 'P': 6, 'a': 7, 'y': 28, 'i': 15, 'e': 11, 'w': 27, 'q': 21, 'f': 12}
{0: ' ', 1: '(', 2: ')', 3: '.', 4: 'A', 5: 'I', 6: 'P', 7: 'a', 8: 'b', 9: 'c', 10: 'd', 11: 'e', 12: 'f', 13: 'g', 14: 'h', 15: 'i', 16: 'l', 17: 'm', 18: 'n', 19: 'o', 20: 'p', 21: 'q', 22: 'r', 23: 's', 24: 't', 25: 'u', 26: 'v', 27: 'w', 28: 'y'}

['g', '(', ')', 'I', 'f', 'y', 'u', 'e', 't', 'q', 'o', 'v', 'P', 'd', 's', 'r', 'm', ' ', 'l', 'i', 'b', 'w', 'n', '.', 'c', 'h', 'a', 'A', 'p']
{'d': 10, 'g': 13, '(': 1, 'r': 22, 'm': 17, ' ': 0, ')': 2, 'f': 12, 'y': 28, 'b': 8, 'e': 11, 'n': 18, 's': 23, 't': 24, 'i': 15, 'w': 27, 'I': 5, '.': 3, 'q': 21, 'c': 9, 'o': 19, 'h': 14, 'a': 7, 'v': 26, 'A': 4, 'p': 20, 'u': 25, 'l': 16, 'P': 6}
{0: ' ', 1: '(', 2: ')', 3: '.', 4: 'A', 5: 'I', 6: 'P', 7: 'a', 8: 'b', 9: 'c', 10: 'd', 11: 'e', 12: 'f', 13: 'g', 14: 'h', 15: 'i', 16: 'l', 17: 'm', 18: 'n', 19: 'o', 20: 'p', 21: 'q', 22: 'r', 23: 's', 24: 't', 25: 'u', 26: 'v', 27: 'w', 28: 'y'}

'''

# encoding sentence to index sequence
encoded_sentence = [char2idx[c] for c in input_sentence]
'''
print(encoded_sentence)
[10, 20, 15, 11, 22, 23, 20, 15, 10, 27, 25, 15, 21, 11, 1, 3, 23, 20, 15, 28, 23, 1, 23, 28, 28, 23, 9, 15, 3, 11, 15, 12, 19, 15, 12, 15, 22, 16, 8, 13, 5, 26, 15, 10, 27, 25, 0, 15, 5, 19, 15, 12, 15, 22, 16, 8, 13, 5, 26, 13, 2, 15, 12, 6, 12, 5, 13, 12, 8, 13, 23, 15, 12, 22, 22, 13, 5, 26, 12, 3, 5, 11, 20, 15, 22, 28, 11, 4, 28, 12, 14, 14, 5, 20, 4, 15, 5, 20, 3, 23, 28, 1, 12, 26, 23, 15, 3, 18, 12, 3, 15, 22, 28, 11, 6, 5, 9, 23, 19, 15, 9, 23, 6, 23, 13, 11, 22, 23, 28, 19, 15, 17, 5, 3, 18, 15, 22, 28, 11, 4, 28, 12, 14, 14, 12, 3, 5, 26, 15, 12, 26, 26, 23, 19, 19, 15, 3, 11, 15, 12, 15, 22, 28, 11, 22, 28, 5, 23, 3, 12, 28, 2, 15, 19, 11, 1, 3, 17, 12, 28, 23, 15, 12, 22, 22, 13, 5, 26, 12, 3, 5, 11, 20, 15, 11, 28, 15, 17, 23, 8, 15, 19, 23, 28, 6, 5, 26, 23, 24, 15, 10, 27, 25, 19, 15, 12, 28, 23, 15, 19, 23, 3, 19, 15, 11, 1, 15, 28, 23, 7, 16, 5, 28, 23, 14, 23, 20, 3, 19, 15, 3, 18, 12, 3, 15, 4, 11, 6, 23, 28, 20, 15, 18, 11, 17, 15, 11, 20, 23, 15, 12, 22, 22, 13, 5, 26, 12, 3, 5, 11, 20, 15, 26, 12, 20, 15, 26, 11, 14, 14, 16, 20, 5, 26, 12, 3, 23, 15, 12, 20, 9, 15, 5, 20, 3, 23, 28, 12, 26, 3, 15, 17, 5, 3, 18, 15, 12, 20, 11, 3, 18, 23, 28, 24]
sorted(char_set) 적용 후
[4, 18, 0, 19, 20, 11, 18, 0, 4, 6, 5, 0, 1, 19, 12, 24, 11, 18, 0, 22, 11, 12, 11, 22, 22, 11, 10, 0, 24, 19, 0, 7, 23, 0, 7, 0, 20, 25, 8, 16, 15, 9, 0, 4, 6, 5, 2, 0, 15, 23, 0, 7, 0, 20, 25, 8, 16, 15, 9, 16, 28, 0, 7, 26, 7, 15, 16, 7, 8, 16, 11, 0, 7, 20, 20, 16, 15, 9, 7, 24, 15, 19, 18, 0, 20, 22, 19, 13, 22, 7, 17, 17, 15, 18, 13, 0, 15, 18, 24, 11, 22, 12, 7, 9, 11, 0, 24, 14, 7, 24, 0, 20, 22, 19, 26, 15, 10, 11, 23, 0, 10, 11, 26, 11, 16, 19, 20, 11, 22, 23, 0, 27, 15, 24, 14, 0, 20, 22, 19, 13, 22, 7, 17, 17, 7, 24, 15, 9, 0, 7, 9, 9, 11, 23, 23, 0, 24, 19, 0, 7, 0, 20, 22, 19, 20, 22, 15, 11, 24, 7, 22, 28, 0, 23, 19, 12, 24, 27, 7, 22, 11, 0, 7, 20, 20, 16, 15, 9, 7, 24, 15, 19, 18, 0, 19, 22, 0, 27, 11, 8, 0, 23, 11, 22, 26, 15, 9, 11, 3, 0, 4, 6, 5, 23, 0, 7, 22, 11, 0, 23, 11, 24, 23, 0, 19, 12, 0, 22, 11, 21, 25, 15, 22, 11, 17, 11, 18, 24, 23, 0, 24, 14, 7, 24, 0, 13, 19, 26, 11, 22, 18, 0, 14, 19, 27, 0, 19, 18, 11, 0, 7, 20, 20, 16, 15, 9, 7, 24, 15, 19, 18, 0, 9, 7, 18, 0, 9, 19, 17, 17, 25, 18, 15, 9, 7, 24, 11, 0, 7, 18, 10, 0, 15, 18, 24, 11, 22, 7, 9, 24, 0, 27, 15, 24, 14, 0, 7, 18, 19, 24, 14, 11, 22, 3]
'''

# create batch
window_size = 5

x_data = []
y_data = []
for i in range(len(input_sentence)-window_size):
    x_data.append(encoded_sentence[i:i+window_size])
    y_data.append(encoded_sentence[i+1:i+window_size+1])
'''
    # x_data.append(input_sentence[i:i+window_size])
    # y_data.append(input_sentence[i+1:i+window_size+1])
print(x_data[-3:])
print(y_data[-3:])
.
.
.
print(x_data[:3])
print(y_data[:3])
['An op', 'n ope', ' open']
['n ope', ' open', 'open ']
.
.
.
['anoth', 'nothe', 'other']
['nothe', 'other', 'ther.']

[[4, 18, 0, 19, 20], [18, 0, 19, 20, 11], [0, 19, 20, 11, 18]]
[[18, 0, 19, 20, 11], [0, 19, 20, 11, 18], [19, 20, 11, 18, 0]]
.
.
.
[[7, 18, 19, 24, 14], [18, 19, 24, 14, 11], [19, 24, 14, 11, 22]]
[[18, 19, 24, 14, 11], [19, 24, 14, 11, 22], [24, 14, 11, 22, 3]]
'''
# print(np.shape(x_data))     # (309, 5)

X = tf.placeholder(dtype=tf.int32, shape=[None, None], name='input_data_x')
Y = tf.placeholder(dtype=tf.int32, shape=[None, None], name='label_data_y')

X_one_hot = tf.one_hot(indices=X, depth=len(char_set))
'''
print(X)
print(X_one_hot)
Tensor("input_data_x:0", shape=(?, 5), dtype=int32)
Tensor("one_hot:0", shape=(?, 5, 29), dtype=float32)
'''


def show_tensor(tensor, input):
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        print(sess.run(tensor, feed_dict=input))

'''
show_tensor(X, {X: x_data[:5]})
[[ 4. 18.  0. 19. 20.]
 [18.  0. 19. 20. 11.]
 [ 0. 19. 20. 11. 18.]
 [19. 20. 11. 18.  0.]
 [20. 11. 18.  0.  4.]]

show_tensor(X_one_hot, {X: x_data[:2]})
[[[0. 0. 0. 0. 1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.
   0. 0. 0. 0. 0. 0.]
  [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 1. 0. 0. 0. 0.
   0. 0. 0. 0. 0. 0.]
  [1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.
   0. 0. 0. 0. 0. 0.]
  [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 1. 0. 0. 0.
   0. 0. 0. 0. 0. 0.]
  [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 1. 0. 0.
   0. 0. 0. 0. 0. 0.]]

 [[0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 1. 0. 0. 0. 0.
   0. 0. 0. 0. 0. 0.]
  [1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.
   0. 0. 0. 0. 0. 0.]
  [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 1. 0. 0. 0.
   0. 0. 0. 0. 0. 0.]
  [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 1. 0. 0.
   0. 0. 0. 0. 0. 0.]
  [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.
   0. 0. 0. 0. 0. 0.]]]
'''

# create a BasicRNNCell
hidden_size = 4
# basic_rnn_cell = tf.nn.rnn_cell.BasicRNNCell(hidden_size)
# multi_rnn_cell = tf.nn.rnn_cell.MultiRNNCell([basic_rnn_cell] * 2)


def lstm_cell():
    cell = tf.contrib.rnn.BasicLSTMCell(hidden_size, state_is_tuple=True)
    return cell


multi_cells = tf.contrib.rnn.MultiRNNCell([lstm_cell() for _ in range(2)], state_is_tuple=True)

batch_size = 10

# 'state' is a tensor of shape [batch_size, cell_state_size]
rnn_outputs, _states = tf.nn.dynamic_rnn(multi_cells, X_one_hot, dtype=tf.float32)
X_for_fc = tf.reshape(rnn_outputs, [-1, hidden_size])
fc_outputs = tf.contrib.layers.fully_connected(X_for_fc, len(char_set), activation_fn=None)
fc_outputs1 = tf.reshape(fc_outputs, [-1, window_size, len(char_set)])

# print(x_data[:2])
# show_tensor(outputs, {X: x_data[:3]})

weights = tf.ones([batch_size, window_size])
sequence_loss = tf.contrib.seq2seq.sequence_loss(logits=fc_outputs1, targets=Y, weights=weights)
loss = tf.reduce_mean(sequence_loss)
train = tf.train.AdamOptimizer(learning_rate=0.01).minimize(loss=loss)

pred = tf.argmax(fc_outputs1, axis=2)

# show_tensor(rnn_outputs, {X: x_data[:3], Y: y_data[:3]})
# print(rnn_outputs)      # Tensor("rnn/transpose_1:0", shape=(?, ?, 4), dtype=float32), (3, 5, 4)
# print(_states)      # (LSTMStateTuple(c=<tf.Tensor 'rnn/while/Exit_3:0' shape=(?, 4) dtype=float32>, h=<tf.Tensor 'rnn/while/Exit_4:0' shape=(?, 4) dtype=float32>), LSTMStateTuple(c=<tf.Tensor 'rnn/while/Exit_5:0' shape=(?, 4) dtype=float32>, h=<tf.Tensor 'rnn/while/Exit_6:0' shape=(?, 4) dtype=float32>))
''' 지금은 hidden_size = 4
[[[ 0.   -0.01 -0.    0.02]
  [ 0.   -0.01 -0.01  0.05]
  [ 0.01 -0.   -0.    0.05]
  [ 0.01  0.    0.02  0.04]
  [ 0.01 -0.    0.02  0.04]]

 [[ 0.   -0.   -0.01  0.02]
  [ 0.01  0.   -0.    0.03]
  [ 0.01  0.    0.02  0.01]
  [ 0.01 -0.    0.03  0.02]
  [ 0.02 -0.    0.04  0.01]]

 [[ 0.01  0.    0.01 -0.  ]
  [ 0.01 -0.    0.04 -0.02]
  [ 0.01 -0.01  0.04 -0.01]
  [ 0.01 -0.01  0.05 -0.01]
  [ 0.02 -0.01  0.04  0.01]]]
'''
# show_tensor(_states, {X: x_data[:3], Y: y_data[:3]})
'''     # c is the hidden state and h is the output
(LSTMStateTuple(c=array([[-0.02,  0.19,  0.02, -0.01],
                         [-0.19,  0.18, -0.05, -0.02],
                         [-0.12, -0.01, -0.18, -0.13]], dtype=float32),
                h=array([[-0.01,  0.09,  0.01, -0.  ],
                         [-0.11,  0.1 , -0.03, -0.01],
                         [-0.06, -0.01, -0.08, -0.05]], dtype=float32)),
 LSTMStateTuple(c=array([[-0.07, -0.08,  0.02,  0.04],
                         [-0.02, -0.02, -0.01,  0.07],
                         [ 0.  ,  0.02, -0.01,  0.08]], dtype=float32),
                h=array([[-0.03, -0.04,  0.01,  0.02],
                         [-0.01, -0.01, -0.  ,  0.03],
                         [ 0.  ,  0.01, -0.  ,  0.04]], dtype=float32)))
'''
# show_tensor(X_for_fc, {X: x_data[:3], Y: y_data[:3]})
'''
[[ 6.99e-03  1.01e-02  1.24e-02 -1.49e-03]
 [ 1.66e-02  2.06e-02  2.08e-02 -1.44e-02]
 [ 2.46e-02  2.99e-02  2.60e-02 -3.25e-02]
 [ 3.12e-02  2.99e-02  2.12e-02 -2.26e-02]
 [ 3.69e-02  2.26e-02  7.99e-03  7.54e-03]
 [ 2.47e-03  2.23e-03 -9.71e-05 -1.27e-02]
 [ 5.03e-03  7.80e-03  3.62e-03 -3.36e-02]
 [ 6.87e-03  6.62e-03  5.54e-04 -2.65e-02]
 [ 9.91e-03 -2.43e-04 -1.02e-02  1.95e-03]
 [ 1.41e-02  6.48e-03 -1.00e-02  1.34e-02]
 [ 1.50e-03  7.04e-03  7.48e-03 -1.86e-02]
 [ 3.73e-03  7.76e-03  7.13e-03 -1.12e-02]
 [ 6.95e-03  1.58e-03 -2.33e-03  1.72e-02]
 [ 1.24e-02  9.24e-03 -1.16e-03  2.81e-02]
 [ 1.92e-02  1.76e-02  3.44e-04  1.95e-02]]
'''
# show_tensor(fc_outputs, {X: x_data[:3], Y: y_data[:3]})
'''
[[-5.30e-05  2.44e-03 -2.85e-03  8.16e-04  2.49e-03 -2.33e-03  4.96e-03
   2.39e-03  2.88e-03 -3.66e-03  1.04e-04  1.15e-03 -3.25e-04 -4.03e-04
  -3.05e-03  2.46e-03 -4.07e-04 -3.74e-03  1.37e-03  1.76e-03  8.08e-04
  -3.09e-04 -1.83e-03  1.44e-03  1.77e-04 -2.12e-03 -3.76e-03 -1.94e-04
  -2.25e-03]
 [-1.97e-03  5.21e-03 -5.72e-03  4.39e-03  2.43e-03 -2.54e-03  7.44e-03
   6.02e-03  5.19e-03 -5.17e-03  3.06e-03  1.58e-03  2.55e-03 -3.91e-03
  -4.26e-03  2.97e-03 -9.52e-05 -5.16e-03  1.57e-03  4.46e-03  1.94e-03
  -7.51e-04 -5.90e-03  2.14e-03  5.52e-04 -6.62e-03 -6.82e-03 -2.77e-04
  -4.39e-03]
 [-3.19e-03  3.60e-03 -7.15e-03  7.91e-03 -9.38e-04  1.46e-03  5.47e-03
   8.11e-03  3.50e-03 -4.32e-03  6.83e-03  3.57e-04  6.38e-03 -7.71e-03
  -1.69e-03  1.21e-03 -4.52e-04 -1.33e-03  1.96e-03  4.82e-03  3.52e-04
  -4.61e-04 -1.00e-02  1.63e-03  1.90e-03 -7.41e-03 -5.36e-03 -2.92e-04
  -5.20e-03]
 [-3.94e-03  1.37e-03 -5.33e-03  8.90e-03 -4.32e-03  4.77e-03  4.78e-04
   7.18e-03  6.97e-04 -8.59e-04  8.42e-03 -1.10e-03  8.42e-03 -9.09e-03
   2.04e-03 -1.84e-03  9.57e-05  3.17e-03  6.33e-04  3.83e-03 -4.41e-04
  -2.02e-04 -1.03e-02  9.27e-05  2.18e-03 -6.53e-03 -1.87e-03 -8.98e-05
  -3.71e-03]
 [-5.38e-03 -1.92e-03 -5.20e-03  1.26e-02 -1.02e-02  1.13e-02 -4.86e-03
   7.92e-03 -3.12e-03  3.10e-03  1.30e-02 -2.94e-03  1.33e-02 -1.38e-02
   5.83e-03 -4.54e-03 -7.56e-04  9.90e-03  5.88e-04  2.99e-03 -3.59e-03
   4.32e-04 -1.42e-02 -9.02e-04  3.60e-03 -6.50e-03  2.07e-03 -1.22e-04
  -2.97e-03]
 [-1.22e-03  1.17e-03 -1.29e-03  2.20e-03 -7.97e-04  6.30e-04  5.36e-04
   1.80e-03  7.71e-04  2.06e-08  2.04e-03  8.74e-05  2.05e-03 -2.41e-03
  -4.21e-04  7.80e-05  8.64e-06 -2.00e-05  2.19e-05  1.27e-03  1.86e-04
  -1.59e-04 -2.41e-03  3.00e-04  2.53e-04 -2.48e-03 -1.13e-03 -6.17e-05
  -8.37e-04]
 [-1.76e-03 -1.71e-03 -1.67e-03  4.61e-03 -4.72e-03  5.38e-03 -2.61e-03
   2.45e-03 -2.09e-03  1.94e-03  5.09e-03 -1.25e-03  5.18e-03 -5.45e-03
   2.24e-03 -1.53e-03 -9.44e-04  4.74e-03  6.08e-04  4.25e-04 -2.53e-03
   4.12e-04 -5.40e-03 -2.42e-04  1.56e-03 -1.65e-03  1.69e-03 -1.26e-04
  -6.83e-04]
 [-2.03e-03 -4.44e-03  3.98e-04  4.96e-03 -8.11e-03  8.87e-03 -7.57e-03
   8.90e-04 -5.24e-03  5.62e-03  6.21e-03 -2.56e-03  6.68e-03 -6.40e-03
   5.39e-03 -3.94e-03 -9.73e-04  9.26e-03 -3.01e-04 -1.14e-03 -4.09e-03
   8.32e-04 -5.13e-03 -1.50e-03  1.84e-03 -6.77e-06  5.50e-03 -8.85e-06
   1.14e-03]
 [-3.10e-03 -7.85e-03  3.68e-04  8.25e-03 -1.38e-02  1.53e-02 -1.23e-02
   1.42e-03 -9.01e-03  9.36e-03  1.05e-02 -4.14e-03  1.12e-02 -1.09e-02
   8.33e-03 -5.82e-03 -2.37e-03  1.56e-02  1.79e-04 -2.24e-03 -7.81e-03
   1.57e-03 -8.93e-03 -2.08e-03  3.29e-03  3.57e-04  9.25e-03 -1.38e-04
   1.88e-03]
 [-5.11e-03 -4.45e-03 -1.19e-03  1.09e-02 -1.36e-02  1.43e-02 -1.06e-02
   3.89e-03 -6.52e-03  9.14e-03  1.26e-02 -3.43e-03  1.33e-02 -1.37e-02
   6.60e-03 -5.25e-03 -1.73e-03  1.36e-02 -4.47e-04  2.68e-04 -6.07e-03
   1.00e-03 -1.13e-02 -1.51e-03  2.95e-03 -4.42e-03  6.30e-03 -1.79e-04
   7.46e-04]
 [-1.86e-05 -3.44e-03  9.45e-05  1.55e-03 -3.78e-03  4.72e-03 -3.34e-03
  -1.16e-04 -3.25e-03  2.10e-03  2.33e-03 -1.30e-03  2.38e-03 -2.25e-03
   2.54e-03 -1.36e-03 -1.22e-03  4.83e-03  7.59e-04 -1.45e-03 -3.13e-03
   6.91e-04 -2.15e-03 -5.05e-04  1.25e-03  1.82e-03  3.31e-03 -8.67e-05
   5.49e-04]
 [-2.77e-04 -6.22e-03  2.00e-03  2.02e-03 -7.33e-03  8.44e-03 -8.16e-03
  -1.62e-03 -6.44e-03  5.83e-03  3.63e-03 -2.54e-03  4.02e-03 -3.46e-03
   5.35e-03 -3.45e-03 -1.54e-03  9.37e-03  9.56e-05 -3.06e-03 -5.05e-03
   1.17e-03 -2.15e-03 -1.57e-03  1.60e-03  3.41e-03  7.06e-03 -2.32e-05
   2.34e-03]
 [-1.45e-03 -9.59e-03  1.90e-03  5.52e-03 -1.33e-02  1.52e-02 -1.29e-02
  -1.01e-03 -1.02e-02  9.77e-03  8.17e-03 -4.08e-03  8.75e-03 -8.32e-03
   8.10e-03 -5.19e-03 -3.10e-03  1.58e-02  6.50e-04 -4.14e-03 -8.98e-03
   1.92e-03 -6.20e-03 -2.05e-03  3.08e-03  3.55e-03  1.08e-02 -1.85e-04
   3.10e-03]
 [-3.61e-03 -6.09e-03  1.23e-04  8.45e-03 -1.33e-02  1.43e-02 -1.11e-02
   1.71e-03 -7.68e-03  9.56e-03  1.06e-02 -3.35e-03  1.12e-02 -1.15e-02
   6.25e-03 -4.54e-03 -2.54e-03  1.39e-02  1.00e-04 -1.48e-03 -7.33e-03
   1.36e-03 -9.02e-03 -1.39e-03  2.80e-03 -1.55e-03  7.70e-03 -2.48e-04
   1.84e-03]
 [-4.80e-03 -2.97e-03 -1.72e-03  1.01e-02 -1.19e-02  1.23e-02 -8.22e-03
   4.00e-03 -4.94e-03  7.88e-03  1.15e-02 -2.51e-03  1.21e-02 -1.29e-02
   4.26e-03 -3.49e-03 -1.99e-03  1.10e-02  5.79e-06  7.51e-04 -5.53e-03
   8.26e-04 -1.08e-02 -6.49e-04  2.54e-03 -5.15e-03  4.43e-03 -2.93e-04
   3.29e-04]]
'''
# show_tensor(fc_outputs1, {X: x_data[:3], Y: y_data[:3]})
'''
[[[-5.41e-04 -3.11e-04  3.13e-03  1.20e-03 -1.92e-04  8.79e-04 -7.62e-04
    5.95e-04 -1.76e-03  6.53e-04  5.75e-04 -4.93e-04  6.39e-04 -2.08e-03
   -4.02e-04  9.53e-04 -1.57e-03  1.41e-03  1.36e-04  2.04e-03 -2.85e-03
   -3.55e-03 -1.91e-03 -9.41e-04 -3.08e-03 -2.24e-03  6.13e-04 -2.43e-03
    1.54e-04]
  [ 5.61e-04  1.54e-03  5.29e-03  1.79e-03  4.56e-04  1.10e-03 -1.74e-03
   -1.58e-04 -2.93e-03  7.84e-04  2.03e-03 -9.74e-04  2.50e-03 -3.42e-03
   -1.59e-03  1.70e-03 -1.78e-03  2.27e-03 -5.17e-04  3.13e-03 -5.30e-03
   -5.82e-03 -1.55e-03 -2.08e-03 -5.07e-03 -3.51e-03  4.21e-04 -4.50e-03
   -1.26e-03]
  [-8.29e-04 -3.93e-04  3.06e-03  2.21e-03 -8.56e-04  1.64e-03 -1.89e-03
    3.57e-04 -1.71e-03  3.74e-04 -1.01e-04 -5.28e-04  6.32e-04 -1.34e-03
   -4.76e-05  1.27e-03 -1.83e-03  2.67e-03 -7.90e-05  2.84e-03 -2.60e-03
   -3.21e-03 -1.87e-03 -1.45e-03 -2.70e-03 -2.55e-03  6.16e-04 -1.66e-03
    1.17e-03]
  [-4.27e-03 -6.16e-03 -8.73e-03  5.53e-06 -3.86e-03  7.07e-04  1.63e-03
    2.11e-03  5.24e-03 -1.67e-03 -7.28e-03  2.57e-03 -6.72e-03  7.13e-03
    6.15e-03 -3.11e-03  7.56e-04 -1.28e-03  1.68e-03 -2.17e-03  1.06e-02
    1.12e-02  9.32e-04  3.72e-03  1.02e-02  5.11e-03 -4.56e-04  9.93e-03
    7.63e-03]
  [-8.43e-03 -1.27e-02 -1.10e-02 -3.13e-04 -5.93e-03  1.21e-03  2.81e-03
    4.91e-03  5.81e-03 -7.34e-04 -1.03e-02  2.32e-03 -1.15e-02  8.35e-03
    7.87e-03 -2.89e-03 -8.47e-04 -1.01e-03  3.92e-03 -3.28e-03  1.35e-02
    1.16e-02 -4.57e-03  5.14e-03  1.04e-02  5.04e-03  2.15e-03  1.27e-02
    1.16e-02]]

 [[ 1.22e-03  1.74e-03  6.35e-04 -1.26e-04  7.41e-04 -2.78e-04 -3.47e-04
   -8.44e-04 -3.08e-04 -1.09e-04  1.13e-03 -1.97e-04  1.35e-03 -4.57e-04
   -9.02e-04  1.95e-04  4.81e-04 -4.02e-05 -5.86e-04  1.51e-05 -1.01e-03
   -5.85e-04  1.09e-03 -5.18e-04 -5.35e-04 -1.37e-04 -4.30e-04 -9.44e-04
   -1.44e-03]
  [-4.97e-04 -6.73e-04 -2.67e-03  1.74e-04 -9.00e-04  2.27e-04 -1.90e-04
   -1.59e-04  1.60e-03 -7.59e-04 -1.75e-03  6.17e-04 -1.18e-03  2.45e-03
    1.34e-03 -7.15e-04  6.61e-04  2.29e-06 -7.84e-06 -6.21e-04  2.96e-03
    3.50e-03  1.19e-03  6.18e-04  3.17e-03  1.57e-03 -4.35e-04  3.00e-03
    1.69e-03]
  [-4.05e-03 -6.58e-03 -1.45e-02 -2.06e-03 -3.98e-03 -7.17e-04  3.53e-03
    1.74e-03  8.67e-03 -2.83e-03 -9.11e-03  3.88e-03 -8.70e-03  1.09e-02
    7.81e-03 -5.29e-03  3.22e-03 -4.13e-03  1.83e-03 -5.61e-03  1.64e-02
    1.82e-02  4.11e-03  5.98e-03  1.63e-02  9.38e-03 -1.61e-03  1.47e-02
    8.33e-03]
  [-8.47e-03 -1.34e-02 -1.67e-02 -2.17e-03 -6.26e-03 -4.47e-05  4.72e-03
    4.74e-03  9.25e-03 -1.92e-03 -1.24e-02  3.76e-03 -1.36e-02  1.22e-02
    9.85e-03 -5.17e-03  1.43e-03 -3.78e-03  4.14e-03 -6.46e-03  1.93e-02
    1.87e-02 -1.46e-03  7.47e-03  1.66e-02  9.27e-03  9.48e-04  1.76e-02
    1.27e-02]
  [-1.27e-02 -1.89e-02 -1.84e-02  5.40e-04 -9.82e-03  2.60e-03  2.44e-03
    6.44e-03  9.64e-03 -1.85e-03 -1.67e-02  3.40e-03 -1.75e-02  1.50e-02
    1.22e-02 -3.99e-03 -8.04e-04  1.07e-04  5.39e-03 -4.86e-03  2.20e-02
    1.96e-02 -6.09e-03  7.11e-03  1.75e-02  8.07e-03  3.17e-03  2.17e-02
    1.89e-02]]

 [[-2.18e-03 -3.22e-03 -3.63e-03  7.15e-05 -1.79e-03  4.27e-04  4.92e-04
    1.06e-03  1.99e-03 -4.94e-04 -3.14e-03  7.83e-04 -3.13e-03  2.97e-03
    2.39e-03 -9.34e-04  4.77e-05 -1.41e-04  8.92e-04 -9.51e-04  4.33e-03
    4.12e-03 -5.83e-04  1.40e-03  3.70e-03  1.77e-03  3.25e-04  4.21e-03
    3.45e-03]
  [-5.96e-03 -9.56e-03 -1.59e-02 -2.33e-03 -4.95e-03 -5.82e-04  4.35e-03
    3.09e-03  9.20e-03 -2.52e-03 -1.07e-02  4.01e-03 -1.10e-02  1.17e-02
    8.91e-03 -5.52e-03  2.63e-03 -4.36e-03  2.88e-03 -6.24e-03  1.81e-02
    1.90e-02  2.01e-03  6.91e-03  1.70e-02  9.72e-03 -6.62e-04  1.62e-02
    1.03e-02]
  [-1.04e-02 -1.64e-02 -1.83e-02 -2.61e-03 -7.17e-03 -1.61e-05  5.60e-03
    6.06e-03  9.82e-03 -1.57e-03 -1.40e-02  3.80e-03 -1.60e-02  1.30e-02
    1.08e-02 -5.33e-03  9.19e-04 -4.08e-03  5.23e-03 -7.34e-03  2.12e-02
    1.95e-02 -3.71e-03  8.42e-03  1.73e-02  9.66e-03  2.03e-03  1.92e-02
    1.46e-02]
  [-1.44e-02 -2.18e-02 -2.00e-02 -6.86e-05 -1.05e-02  2.48e-03  3.32e-03
    7.61e-03  1.02e-02 -1.46e-03 -1.80e-02  3.32e-03 -1.97e-02  1.57e-02
    1.28e-02 -4.07e-03 -1.18e-03 -2.70e-04  6.41e-03 -5.95e-03  2.37e-02
    2.02e-02 -8.31e-03  7.98e-03  1.79e-02  8.46e-03  4.28e-03  2.32e-02
    2.03e-02]
  [-1.44e-02 -2.16e-02 -2.01e-02  4.89e-04 -1.08e-02  2.89e-03  2.50e-03
    7.28e-03  1.02e-02 -1.63e-03 -1.82e-02  3.18e-03 -1.95e-02  1.62e-02
    1.28e-02 -3.75e-03 -1.22e-03  5.65e-04  6.20e-03 -5.59e-03  2.38e-02
    2.03e-02 -8.25e-03  7.54e-03  1.80e-02  8.25e-03  4.33e-03  2.36e-02
    2.07e-02]]]
'''
# show_tensor(pred, {X: x_data[:10], Y: y_data[:10]})
'''
[[21 21 15 21 21]
 [23 23  0 15 15]
 [18  1 21 15 15]
 [ 1 21 21  0  0]
 [21  0  0  0  0]
 [ 9 23 23  0 15]
 [23 23 15 15 15]
 [18 21 21 21 21]
 [21 21 21 21 21]
 [15 15 21 21 21]]
'''
# show_tensor(initial_state, {X: x_data[:2]})
# show_tensor(sequence_loss, {X: x_data[:10], Y: y_data[:10]})    # 3.3689792
#
epoch = 11
iter = len(input_sentence) // batch_size
# print(iter)

# training
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for step in range(epoch):
        loss_val = 0
        for i in range(iter):
            # print(step, i)
            # print(x_data[i:i+batch_size])
            feed_dict = {X: x_data[i:i+batch_size], Y: y_data[i+1: i+batch_size+1]}
            sess.run(train, feed_dict=feed_dict)
            loss_val += sess.run(loss, feed_dict=feed_dict)

        print(step, loss_val/iter)

    expected_sentence = sess.run(tf.reshape(pred, [-1]), feed_dict={X: x_data})