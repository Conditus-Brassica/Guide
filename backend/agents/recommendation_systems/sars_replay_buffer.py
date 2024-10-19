# Author: Vodohleb04
import json
from typing import Tuple, List
from uuid import uuid4
import tensorflow as tf
import numpy as np


class SARSReplayBuffer:
    """Buffer to save SARS records (check https://arxiv.org/pdf/1509.02971 to get more information)"""
    def _init_on_load(self, dtype, load_json_dict):
        """
        load_json_dict is used in case of loading sars_buffer from file,
        load_json_dict: {
            "_buffer_capacity": int,
            "_batch_size": int,
            "_current_index": int,
            "_buffer_is_filled": bool,
            "_state_buffer": List[List[float]],
            "_action_buffer": List[List[float]],
            "_reward_buffer": List[List[float]],
            "_next_state_buffer": List[List[float]],
            "_completed_rows_indexes": List[int],
            "_row_uuids": List[uuid.hex]
        }
        """
        self._buffer_capacity = int(load_json_dict["_buffer_capacity"])
        self._batch_size = load_json_dict["_batch_size"]
        
        self._current_index = load_json_dict["_current_index"]
        self._buffer_is_filled = load_json_dict["_buffer_is_filled"]

        self._state_buffer = np.asarray(load_json_dict["_state_buffer"], dtype=dtype)
        self._action_buffer = np.asarray(load_json_dict["_action_buffer"], dtype=dtype)
        self._reward_buffer = np.asarray(load_json_dict["_reward_buffer"], dtype=dtype)
        self._next_state_buffer = np.asarray(load_json_dict["_next_state_buffer"], dtype=dtype)

        self._completed_rows_indexes = load_json_dict["_completed_rows_indexes"]
        self._row_uuids: List = load_json_dict["_row_uuids"]


    def __init__(
        self, dtype, save_file,
        state_size = None, action_size = None, buffer_capacity=1e7, batch_size=64, load_json_dict=None
    ):
        """
        load_json_dict is used in case of loading sars_buffer from file,
        load_json_dict: {
            "_buffer_capacity": int,
            "_batch_size": int,
            "_current_index": int,
            "_buffer_is_filled": bool,
            "_state_buffer": List[List[float]],
            "_action_buffer": List[List[float]],
            "_reward_buffer": List[List[float]],
            "_next_state_buffer": List[List[float]],
            "_completed_rows_indexes": List[int],
            "_row_uuids": List[uuid.hex]
        }
        """
        if load_json_dict is None:
            self._buffer_capacity = int(buffer_capacity)
            self._batch_size = batch_size

            self._current_index = 0
            self._buffer_is_filled = False

            self._state_buffer = np.zeros((self._buffer_capacity, state_size), dtype=dtype)
            self._action_buffer = np.zeros((self._buffer_capacity, action_size), dtype=dtype)
            self._reward_buffer = np.zeros((self._buffer_capacity, 1), dtype=dtype)
            self._next_state_buffer = np.zeros((self._buffer_capacity, state_size), dtype=dtype)

            self._completed_rows_indexes = []
            self._row_uuids: List = [None for _ in range(self._buffer_capacity)]
        else:
            self._init_on_load(dtype, load_json_dict)

        self._save_file = save_file


    def partial_record(self, state: np.ndarray, action: np.ndarray):
        """
        Is used to write first part of sars tuple. This tuple will be saved, but won't be used in training samples

        ###
        1. state: numpy.ndarray
        2. action: numpy.ndarray

        returns: Tuple[int, uuid] - index of row in buffer and uuid of row.
        """
        row_uuid = uuid4().hex
        row_index = self._current_index
        self._state_buffer[row_index] = state
        self._action_buffer[row_index] = action

        self._row_uuids[row_index] = row_uuid

        try:
            if self._buffer_is_filled:
                self._completed_rows_indexes.remove(row_index)
        except ValueError:  # If row_index is not in self._completed_rows_indexes
            pass

        self._current_index += 1
        if self._current_index == self._buffer_capacity:
            self._buffer_is_filled = True
            self._current_index = 0
        
        return row_index, row_uuid
    

    def fill_up_partial_record(self, row_index, row_uuid, reward: np.ndarray, next_state: np.ndarray):
        """
        Is used to write the last part of sars tuple. If the given uuid was found in buffer, reward and next_state will be saved
            and the row may be used in training batch.

        1. row_index: int
            - index of the row in buffer (such index is returned as result of partial_record method) 
        2. row_uuid: uuid
            - uuid of the row in buffer (such uuid is returned as result of partial_record method)
        3. reward: numpy.ndarray
        4. next_state: numpy.ndarray

        returns: bool - True if uuid is correct, False otherwise
        """
        if self._row_uuids[row_index] == row_uuid:
            self._reward_buffer[row_index] = reward
            self._next_state_buffer[row_index] = next_state
            
            self._completed_rows_indexes.append(row_index)

            return True
        else:
            return False
        

    def fill_up_partial_record_no_index(self, row_uuid, reward: np.ndarray, next_state: np.ndarray):
        """
        Is used to write the last part of sars tuple. If the given uuid was found in buffer, reward and next_state will be saved
            and the row may be used in training batch. Linear search is used to find out uuid.

        1. row_uuid: uuid
            - uuid of the row in buffer (such uuid is returned as result of partial_record method)
        2. reward: numpy.ndarray
        3. next_state: numpy.ndarray

        returns: bool - True if uuid was found out, False otherwise
        """
        for index, uuid in enumerate(self._row_uuids):
            if uuid == row_uuid:
                self._reward_buffer[index] = reward
                self._next_state_buffer[index] = next_state

                self._completed_rows_indexes.append(index)

                return True
        return False
        

    def record(self, sars_tuple: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]):
        """
        SARS - state, action, reward, state (next state)
        If the buffer is full, the oldest record will be replaced with the new one
        """
        row_uuid = uuid4().hex
        row_index = self._current_index

        self._state_buffer[row_index] = sars_tuple[0]
        self._action_buffer[row_index] = sars_tuple[1]
        self._reward_buffer[row_index] = sars_tuple[2]
        self._next_state_buffer[row_index] = sars_tuple[3]

        self._row_uuids[row_index] = row_uuid
        self._completed_rows_indexes.append(row_index)

        self._current_index += 1
        if self._current_index == self._buffer_capacity:
            self._buffer_is_filled = True
            self._current_index = 0
        
        return row_index, row_uuid
    

    def completed_record_exist(self) -> bool:
        return len(self._completed_rows_indexes) > 0


    def sample_sars_batch(
        self, return_tf_tensors=False
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray] | Tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor] | Tuple[None, None, None, None]:
        """
        Samples random batch of SARS from the replay buffer
        """
        if not self._completed_rows_indexes:
            return None, None, None, None
        
        batch_indices = np.random.choice(self._completed_rows_indexes, size=self._batch_size)

        if return_tf_tensors:
            return (
                tf.convert_to_tensor(self._state_buffer[batch_indices]),
                tf.convert_to_tensor(self._action_buffer[batch_indices]),
                tf.convert_to_tensor(self._reward_buffer[batch_indices]),
                tf.convert_to_tensor(self._next_state_buffer[batch_indices])
            )
        else:
            return (
                self._state_buffer[batch_indices],
                self._action_buffer[batch_indices],
                self._reward_buffer[batch_indices],
                self._next_state_buffer[batch_indices]
            )
        
    
    def get_state(self, row_index, row_uuid) -> np.ndarray | None:
        if self._row_uuids[row_index] == row_uuid:
            return self._state_buffer[row_index]
        else:
            return None
        

    def save(self):
        with open(self._save_file, 'w') as fout:
            json.dump(
                {
                    "_buffer_capacity": self._buffer_capacity,
                    "_batch_size": self._batch_size,
                    "_current_index": self._current_index,
                    "_buffer_is_filled": self._buffer_is_filled,
                    "_state_buffer": self._state_buffer.tolist(),
                    "_action_buffer": self._action_buffer.tolist(),
                    "_reward_buffer": self._reward_buffer.tolist(),
                    "_next_state_buffer": self._next_state_buffer.tolist(),
                    "_completed_rows_indexes": self._completed_rows_indexes,
                    "_row_uuids": self._row_uuids,
                },
                fout
            )


    @staticmethod
    def load(dtype, save_file):
        """
        returns: SARSReplayBuffer | None
        """
        with open(save_file, 'r') as fin:
            load_json_dict = json.load(fin)

        if load_json_dict:
            sars_replay_buffer = SARSReplayBuffer(
                dtype, save_file, load_json_dict=load_json_dict
            )
            return sars_replay_buffer
        else:
            return None



async def main():
    #buffer = SARSReplayBuffer.load(np.float32,"./chep.save")
    buffer = SARSReplayBuffer(np.float32, "./chep.save", 3, 2, buffer_capacity=10)
    #print()
    state1 = np.array([1, 1, 1], dtype=np.float32)
    action1 = np.array([1, 1], dtype=np.float32)
    reward1 = np.array([1], dtype=np.float32) 
    next_state1 = np.array([1, 1, 1], dtype=np.float32)

    index1, uuid1 = buffer.partial_record(state1, action1)
    s1, a1, r1, ns1 = buffer.sample_sars_batch()
    buffer.fill_up_partial_record(index1, uuid1, reward1, next_state1)

    state2 = np.array([2, 2, 2], dtype=np.float32)
    action2 = np.array([2, 2], dtype=np.float32)
    reward2 = np.array([2], dtype=np.float32) 
    next_state2 = np.array([2, 2, 2], dtype=np.float32)

    index2, uuid2 = buffer.partial_record(state2, action2)

    s2, a2, r2, ns2 = buffer.sample_sars_batch()

    state3 = np.array([3, 3, 3], dtype=np.float32)
    action3 = np.array([3, 3], dtype=np.float32)
    reward3 = np.array([3], dtype=np.float32) 
    next_state3 = np.array([3, 3, 3], dtype=np.float32)

    index3, uuid3 = buffer.partial_record(state3, action3)


    buffer.fill_up_partial_record(index2, uuid2, reward2, next_state2)
    buffer.fill_up_partial_record(index3, uuid3, reward3, next_state3)
    s3, a3, r3, ns3 = buffer.sample_sars_batch()


    state4 = np.array([4, 4, 4], dtype=np.float32)
    action4 = np.array([4, 4], dtype=np.float32)
    reward4 = np.array([4], dtype=np.float32) 
    next_state4 = np.array([4, 4, 4], dtype=np.float32)

    index4, uuid_4 = buffer.partial_record(state4, action4)
    buffer.fill_up_partial_record(index4, uuid_4, reward4, next_state4)

    s4, a4, r4, ns4 = buffer.sample_sars_batch()

    state5 = np.array([5, 5, 5], dtype=np.float32)
    action5 = np.array([5, 5], dtype=np.float32)
    reward5 = np.array([5], dtype=np.float32) 
    next_state5 = np.array([5, 5, 5], dtype=np.float32)

    index5, uuid5 = buffer.partial_record(state5, action5)

    uuid5_wrong = uuid4()

    buffer.fill_up_partial_record(index5, uuid5_wrong, reward5, next_state5)

    buffer.fill_up_partial_record(index5, uuid5, reward5, next_state5)

    s5, a5, r5, ns5 = buffer.sample_sars_batch()

    buffer.save()



if __name__ == "__main__":
    import asyncio
    asyncio.run(main())