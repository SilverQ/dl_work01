import tensorflow as tf
import numpy as np


def long_rnn():
    sample = 'if you want to'
    # idx2char = set(sample)
    # print(idx2char)
    # {'t', 'w', ' ', 'n', 'o', 'u', 'y', 'a', 'i', 'f'}

    idx2char = list(set(sample))

    char2idx = {c: i for i, c in enumerate(idx2char)}
    print(char2idx)
    # {'i': 0, 't': 1, 'y': 2, 'o': 3, 'f': 8, ' ': 4, 'u': 5, 'n': 6, 'w': 7, 'a': 9}

    sample_idx = [char2idx[c] for c in sample]
    print(sample_idx)
    # [9, 4, 5, 7, 3, 2, 5, 6, 0, 8, 1, 5, 1, 3]

    seq_len = 5
    depth = len(idx2char)
    hidden_size = depth
    batch_size = 1
    print(depth)

    # x_data = sample_idx[:-1]    # 입력 : if you want t
    # y_data = sample_idx[1:]     # 출력 : f you want to
    x_data = [sample_idx[:-1]]    # []를 씌워줌으로써, x_data 추출시 rank를 2로 만들었다.
    y_data = [sample_idx[1:]]

    seq_len = len(x_data[0])
    print(seq_len)

    # print(x_data)
    # print(y_data)

    X = tf.placeholder(dtype=tf.int32, shape=[None, seq_len])
    Y = tf.placeholder(dtype=tf.int32, shape=[None, seq_len])

    X_one_hot = tf.one_hot(indices=X, depth=depth)

    rnn_cell = tf.nn.rnn_cell.BasicRNNCell(num_units=hidden_size)
    initial_state = rnn_cell.zero_state(batch_size=batch_size, dtype=tf.float32)


    # sequence_loss가 어떻게 동작하는지는 lab12-1에서 해보는 중
    outputs, _states = tf.nn.dynamic_rnn(rnn_cell, X_one_hot, initial_state=initial_state, dtype=tf.float32)

    weights = tf.ones([batch_size, seq_len])
    sequence_loss = tf.contrib.seq2seq.sequence_loss(logits=outputs, targets=Y, weights=weights)
    loss = tf.reduce_mean(sequence_loss)
    train = tf.train.AdamOptimizer(learning_rate=0.1).minimize(loss=loss)

    pred = tf.argmax(outputs, axis=2)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for step in range(10):
            l, _ = sess.run([loss, train], feed_dict={X: x_data, Y: y_data})
            result = sess.run(pred, feed_dict={X: x_data})
            print(step, "loss: ", l, "prediction: ", result, "Y: ", y_data)

            result_str = [idx2char[c] for c in np.squeeze(result)]
            print("\tPrediction string: ", ''.join(result_str))

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        test = sess.run([X_one_hot, Y], feed_dict={X: x_data, Y: y_data})
        print(test)


# long_rnn()


sentence = 'An open API (often referred to as a public API) is a publicly available application programming interface that provides developers with programmatic access to a proprietary software application or web service. APIs are sets of requirements that govern how one application can communicate and interact with another.'
# sentence = 'An open'
# https://www.youtube.com/watch?v=2R6nfCNNz1U
# 9:25 진행 중
char_set = list(set(sentence))
char2idx = {c: i for i, c in enumerate(char_set)}
sample_idx = [char2idx[c] for c in sentence]

input_len = len(sentence)
data_dim = len(char_set)
num_classes = len(char_set)
hidden_size = len(char_set)
seq_len = 5
batch_size = 20
epoch = 21

x_data = []
y_data = []

# input batch를 만들어보자.
# for i in range(input_len - seq_len):
#     x_data.append(sentence[i:i+seq_len])        # seq_len을 감안해서, 마지막 글자까지 학습시키도록 잘라보자.
#     y_data.append(sentence[i+1:i+seq_len+1])    # append하는 과정에서 차원이 증가하니까 []는 이제 빼준다.
# print(x_data)
# print(y_data)

for i in range(input_len - seq_len):
    x_data.append(sample_idx[i:i + seq_len])  # []를 씌워줌으로써, x_data 추출시 rank를 2로 만들었다.
    y_data.append(sample_idx[i + 1:i + seq_len + 1])
print(np.shape(x_data))     # (309, 5)
data_size = np.shape(x_data)[0]
iter = np.int32(data_size / batch_size)
print(np.shape(y_data))     # (309, 5)
print(data_size)    # 309
print(iter)

X = tf.placeholder(dtype=tf.int32, shape=[batch_size, seq_len])
Y = tf.placeholder(dtype=tf.int32, shape=[batch_size, seq_len])
X_one_hot = tf.one_hot(indices=X, depth=num_classes)

rnn_cell = tf.nn.rnn_cell.BasicRNNCell(num_units=hidden_size)
initial_state = rnn_cell.zero_state(batch_size=batch_size, dtype=tf.float32)

outputs, _states = tf.nn.dynamic_rnn(rnn_cell, X_one_hot, initial_state=initial_state, dtype=tf.float32)

weights = tf.ones([batch_size, seq_len])
sequence_loss = tf.contrib.seq2seq.sequence_loss(logits=outputs, targets=Y, weights=weights)
loss = tf.reduce_mean(sequence_loss)
train = tf.train.AdamOptimizer(learning_rate=0.01).minimize(loss=loss)

pred = tf.argmax(outputs, axis=2)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for j in range(epoch):
        for i in range(iter):
            feed_dict = {X: x_data[i:i+batch_size], Y: y_data[i+1:i+batch_size+1]}
            l, _ = sess.run([loss, train], feed_dict=feed_dict)
            print('epoch: ', j, 'iter: ', i, 'loss: ', l)
        if j % 10 == 0:
            prediction = sess.run(pred, feed_dict=feed_dict)
            print("prediction: ", prediction)
            print("Y: ", y_data[i+1:i+batch_size+1])
            print(np.squeeze(prediction))

            # result_str = [char_set[27, 23]]       # TypeError: list indices must be integers or slices, not tuple
            # result_str = [char_set[c] for c in np.squeeze(prediction)]
            # print("\tPrediction string: ", ''.join(result_str))
            # 오류 메시지 : TypeError: only integer scalar arrays can be converted to a scalar index
            # 다시 character로 변환하는 과정을 익혀야 함. 나중에 꼭 확인하자.

# with tf.Session() as sess:
#     sess.run(tf.global_variables_initializer())
#     for j in range(epoch):
#         for i in range(iter):
#             feed_dict = {X: x_data[i:i+batch_size], Y: y_data[i+1:i+batch_size+1]}
#             test = sess.run([X_one_hot, Y], feed_dict=feed_dict)
#             print(i, test)
