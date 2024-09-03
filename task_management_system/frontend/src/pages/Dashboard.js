import React, { useState, useEffect } from 'react';
import TaskList from '../components/TaskList';
import TaskForm from '../components/TaskForm';
import axios from 'axios';

function Dashboard() {
    const [tasks, setTasks] = useState([]);

    useEffect(() => {
        axios.get('/tasks')
            .then(response => setTasks(response.data))
            .catch(error => console.error('Error fetching tasks:', error));
    }, []);

    const addTask = (task) => {
        axios.post('/tasks', task)
            .then(response => setTasks([...tasks, response.data]))
            .catch(error => console.error('Error adding task:', error));
    };

    return (
        <div>
            <h1>Dashboard</h1>
            <TaskForm addTask={addTask} />
            <TaskList tasks={tasks} />
        </div>
    );
}

export default Dashboard;
