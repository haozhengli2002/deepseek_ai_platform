import axios from 'axios'

const api = axios.create({ baseURL: 'http://localhost:5000/api' })

export const register = (data) => api.post('/register', data)
export const login = (data) => api.post('/login', data)
export const chat = (data) => api.post('/chat', data)

