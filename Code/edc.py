import os, pickle, sys, argparse
import numpy as np
from public_functions import create_folder


def softmax_each_row(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


def EDC(input_file, ouput_file, length, alpha, normal=False):
    exponential_y = [np.exp(-i / alpha) for i in range(length)]
    exponential_y_len = len(exponential_y)

    if not os.path.exists(ouput_file):
        framewise_data = pickle.load(open(input_file, 'rb'))
        framewise_data_min = np.min(framewise_data)
        framewise_data_max = np.max(framewise_data)
        framewise_data_norm = (framewise_data - framewise_data_min) / (framewise_data_max - framewise_data_min)

        # 深拷贝动作Q
        if normal:
            Q = framewise_data.copy()
            K = framewise_data.copy()
        else:
            Q = framewise_data_norm.copy()
            K = framewise_data_norm.copy()

        similarity_matrix = Q.dot(K.T)

        mask_matrix = []
        for current_index in range(similarity_matrix.shape[0]):
            before = similarity_matrix[current_index][:current_index + 1]
            after = similarity_matrix[current_index][current_index:]

            before_score = softmax_each_row(before)
            after_score = softmax_each_row(after)

            ###########################################################################################################
            before_score = np.array(before_score)
            decay = np.array(exponential_y[:current_index + 1][::-1])
            assert len(before_score) == len(decay)
            before_score = before_score * decay
            after_score = np.array(after_score)

            decay = np.array(exponential_y[:exponential_y_len - current_index])
            assert len(after_score) == len(decay)
            after_score = after_score * decay

            after_decay = np.concatenate([before_score, after_score], axis=0)
            assert len(after_decay) - similarity_matrix.shape[1] == 1
            ###########################################################################################################

            expectation_before_scope = 0
            for id, num in enumerate(before_score):
                expectation_before_scope += (len(before_score) - id - 1) * num

            expectation_after_scope = 0
            for id, num in enumerate(after_score):
                expectation_after_scope += id * num

            # window_d = 1
            # before_id = int(np.round(current_index - expectation_before_scope / window_d))
            # after_id = int(np.round(current_index + expectation_after_scope / window_d))

            before_id = int(current_index - expectation_before_scope)
            after_id = int(current_index + expectation_after_scope)

            zero_list = [0 for i in range(len(similarity_matrix[current_index]))]
            zero_list[before_id:after_id + 1] = [1 for i in range(after_id - before_id + 1)]
            zero_list[current_index] = 3

            mask_matrix.append(zero_list)

        mask_matrix = np.array(mask_matrix)

        scope_matrix = np.zeros_like(mask_matrix)
        scope_matrix = scope_matrix.astype('float')
        for m_j in range(mask_matrix.shape[0]):
            for m_i in range(mask_matrix.shape[1]):
                if mask_matrix[m_j, m_i]:
                    scope_matrix[m_j, m_i] = similarity_matrix[m_j, m_i]
                else:
                    scope_matrix[m_j, m_i] = -float('inf')

        scores = []
        for i in range(scope_matrix.shape[0]):
            scores.append(softmax_each_row(scope_matrix[i]))
            # print(i, scope_matrix[i], softmax_each_row(scope_matrix[i]))
        scores = np.array(scores)

        scores = np.nan_to_num(scores)

        result = scores.dot(Q)

        pickle.dump(result, open(ouput_file, 'wb'))  # pickle.HIGHEST_PROTOCOL
        print('EDC output : ', ouput_file)
    else:
        print('Done: ', ouput_file)




def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-alpha', type=int, default=10)
    parser.add_argument('-length', type=int, default=500)
    parser.add_argument('-sub_dir', type=str, default='weak')
    args = parser.parse_args()

    alpha = args.alpha
    length = args.length
    sub_dir = args.sub_dir

    ################################################################################################################

    source_dir = os.path.join(os.getcwd(), 'mel_feature')
    output_pickle_path = source_dir + '_edc_alpha_' + str(alpha)

    feature_path = os.path.join(output_pickle_path, sub_dir)
    create_folder(feature_path)

    sub_dir_path = os.path.join(source_dir, sub_dir)

    for filename in os.listdir(sub_dir_path):
        if filename.endswith('.pickle'):
            audioname = filename.split('.pickle')[0]
        elif filename.endswith('.cpickle'):
            audioname = filename.split('.cpickle')[0]

        ouput_file = os.path.join(feature_path, audioname + '.pickle')
        input_file = os.path.join(sub_dir_path, filename)

        print('Input : ', input_file)
        EDC(input_file, ouput_file, length, alpha)







if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv))
    except (ValueError, IOError) as e:
        sys.exit(e)






