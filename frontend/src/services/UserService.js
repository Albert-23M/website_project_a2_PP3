import http from '../http-common'
class UserService {
  readUsers (skip = 0, limit = 100) {
    const config = {
      headers: {
        'accept': 'application/json'
      },
      params: {
        skip: skip,
        limit: limit
      }
    }

    const path = '/api/v1/users'

    return http.get(path, config)
      .then((res) => {
        return res
      })
      .catch((error) => {
        return Promise.reject(error)
      })
  }

  readTop5MatchedUsers (keyword) {
    const config = {
      headers: {
        'accept': 'application/json'
      }
    }

    const path = '/api/v1/users/' + keyword

    return http.get(path, config)
      .then((res) => {
        return res
      })
      .catch((error) => {
        return Promise.reject(error)
      })
  }

  readUserById (id) {
    const config = {
      headers: {
        'accept': 'application/json'
      }
    }

    const path = '/api/v1/users/by-id/' + id

    return http.get(path, config)
      .then((res) => {
        return res
      })
      .catch((error) => {
        return Promise.reject(error)
      })
  }
}

export default new UserService()
