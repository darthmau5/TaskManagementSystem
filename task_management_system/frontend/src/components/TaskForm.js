import React, { useState } from 'react';

function TaskForm({ addTask }) {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');

    const handleSubmit = e => {
        e.preventDefault();
        addTask({ title, description });
        setTitle('');
        setDescription('');
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="Task Title"
                value={title}
                onChange={e => setTitle(e.target.value)}
            />
            <textarea
                placeholder="Task Description"
                value={description}
                onChange={e => setDescription(e.target.value)}
            />
            <button type="submit">Add Task</button>
        </form>
    );
}

export default TaskForm;
