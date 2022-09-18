import axios_api from './api';


class AuthService {
    login(user) {
        return axios_api.post('token/', user)
    }
    logout() {
        localStorage.removeItem('user');
    }
}

export default new AuthService();