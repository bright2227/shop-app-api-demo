import axios from 'axios'

const getAPI = axios.create({
    // baseURL: 'http://localhost',
    timeout: 5000,
})

const getAPIwithToken = axios.create({
    // baseURL: 'http://localhost',
    timeout: 5000,
})

export { getAPI, getAPIwithToken }