import api from './api'

export const authService = {
  login: (email, password) => {
    return api.post('/auth/login', { email, password })
  },

  register: (email, password, name) => {
    return api.post('/auth/register', { email, password, name })
  },

  logout: () => {
    localStorage.removeItem('token')
  },

  getToken: () => {
    return localStorage.getItem('token')
  },

  setToken: (token) => {
    localStorage.setItem('token', token)
  },

  isAuthenticated: () => {
    return !!localStorage.getItem('token')
  }
}

export const habitService = {
  getHabits: () => {
    return api.get('/habits')
  },

  getHabit: (id) => {
    return api.get(`/habits/${id}`)
  },

  createHabit: (data) => {
    return api.post('/habits', data)
  },

  updateHabit: (id, data) => {
    return api.put(`/habits/${id}`, data)
  },

  deleteHabit: (id) => {
    return api.delete(`/habits/${id}`)
  },

  completeHabit: (id, date) => {
    return api.post(`/habits/${id}/complete`, { date })
  },

  getHabitHistory: (id) => {
    return api.get(`/habits/${id}/history`)
  }
}
