// src/stores/user.js
import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore('user', () => {
  const API_URL = 'http://127.0.0.1:8000' // 백엔드 API URL
  const token = ref(null)
  const loginUsername = ref(null)

  // 로그인 액션
  const logIn = async (payload) => {
    const { username, password } = payload

    try {
      const response = await axios.post(`${API_URL}/dj-rest-auth/login/`, {
        username,
        password
      })
      console.log("response = ", response)
      token.value = response.data.key
      loginUsername.value = username
      return true
    } catch (error) {
      console.error("로그인 오류:", error)
      return false
    }
  }

  // 회원가입 액션
  const signUp = async (payload) => {
    const { username, password1, password2, email } = payload

    try {
      const response = await axios.post(`${API_URL}/dj-rest-auth/registration/`, {
        username,
        password1,
        password2,
        email
      })
      alert('회원가입 성공!')
      // 회원가입 후 자동 로그인
      await logIn({ username, password: password1 })
      return true
    } catch (error) {
      console.error("회원가입 오류:", error)
      return false
    }
  }

  // 로그아웃 액션
  const logout = async () => {
    try {
      // 백엔드 로그아웃 API가 있다면 호출
      // await axios.post(`${API_URL}/dj-rest-auth/logout/`, {}, {
      //   headers: {
      //     Authorization: `Token ${token.value}`
      //   }
      // })
    } catch (error) {
      console.error('로그아웃 오류:', error)
    }
    // 클라이언트 측에서 토큰 제거
    token.value = null
    loginUsername.value = null
  }

  return { token, loginUsername, logIn, signUp, logout }
}, {
  persist: true // 상태 유지 (pinia-plugin-persistedstate 사용 시)
})
