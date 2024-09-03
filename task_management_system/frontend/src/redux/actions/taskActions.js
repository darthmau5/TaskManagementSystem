import axios from 'axios';

export const getTasks = () => dispatch => {
    axios.get('/tasks')
        .then(response => {
            dispatch({
                type: 'GET_TASKS',
                payload: response.data
            });
        })
        .catch(error => console.error('Error fetching tasks:', error));
};

export const addTask = task => dispatch => {
    axios.post('/tasks', task)
        .then(response => {
            dispatch({
                type: 'ADD_TASK',
                payload: response.data
            });
        })
        .catch(error => console.error('Error adding task:', error));
};
