<!-- src/views/SignupView.vue -->
<template>
  <div class="signup-page">
    <section class="signup-main">
      <h1>회원가입</h1>
      <form @submit.prevent="handleSignup" class="signup-form">
        <div class="form-group">
          <label for="username">이메일</label>
          <input
            v-model="username"
            type="email"
            id="username"
            placeholder="이메일을 입력하세요"
            required
            class="input-field"
          />
        </div>

        <div class="form-group">
          <label for="password1">비밀번호</label>
          <input
            v-model="password1"
            type="password"
            id="password1"
            placeholder="비밀번호를 입력하세요"
            required
            class="input-field"
          />
        </div>

        <div class="form-group">
          <label for="password2">비밀번호 확인</label>
          <input
            v-model="password2"
            type="password"
            id="password2"
            placeholder="비밀번호를 다시 입력하세요"
            required
            class="input-field"
          />
        </div>

        <!-- 에러 메시지 표시 -->
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <div class="button-group">
          <button type="submit" class="signup-button">회원가입</button>
          <button type="button" class="cancel-button" @click="cancelSignup">취소</button>
          <RouterLink to="/" class="home-button" aria-label="홈으로 이동">
            🏠
          </RouterLink>
        </div>
      </form>
      <p class="login-link">
        이미 계정이 있으신가요?
        <RouterLink to="/login" class="login-button">로그인</RouterLink>
      </p>
    </section>
  </div>
</template>

<!-- 에러 메시지 상태 변수 추가 -->
<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const store = useUserStore()
const router = useRouter()

const username = ref('')
const password1 = ref('')
const password2 = ref('')
const errorMessage = ref('') // 에러 메시지 상태 변수

const handleSignup = async () => {
  if (password1.value !== password2.value) {
    errorMessage.value = '비밀번호가 일치하지 않습니다.'
    return
  }

  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    email: username.value // 이메일을 username으로 사용
  }

  const success = await store.signUp(payload)
  if (success) {
    router.push('/dashboard')
  } else {
    errorMessage.value = '회원가입에 실패했습니다. 다시 시도해주세요.'
  }
}

const cancelSignup = () => {
  router.push('/login')
}
</script>

<style scoped>
.signup-page {
  background-color: #F7F7F7;
  font-family: 'Noto Sans KR', sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* 전체 화면 높이 사용 */
  padding: 20px;
  box-sizing: border-box;
}

.signup-main {
  background-color: #FFFFFF;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 3px 5px rgba(0, 0, 0, 0.16);
  width: 400px;
  max-width: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.signup-main h1 {
  font-size: 28px;
  margin-bottom: 30px;
  text-align: center;
}

.signup-form {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-size: 18px;
  margin-bottom: 5px;
}

.input-field {
  padding: 10px 15px;
  border: 1px solid #707070;
  border-radius: 5px;
  font-size: 16px;
}

.button-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
}

.signup-button {
  flex: 1;
  padding: 12px;
  background-color: #000000;
  color: #FFFFFF;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.signup-button:hover {
  background-color: #333333;
}

.cancel-button {
  flex: 1;
  padding: 12px;
  background-color: #CCCCCC;
  color: #000000;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.cancel-button:hover {
  background-color: #AAAAAA;
}

.home-button {
  padding: 12px;
  background-color: #FFFFFF;
  color: #000000;
  border: 1px solid #707070;
  border-radius: 5px;
  cursor: pointer;
  font-size: 20px;
  text-decoration: none;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s, color 0.3s;
}

.home-button:hover {
  background-color: #000000;
  color: #FFFFFF;
}

.login-link {
  margin-top: 20px;
  font-size: 16px;
}

.login-button {
  color: #0000EE;
  text-decoration: underline;
  cursor: pointer;
}

.login-button:hover {
  color: #5555FF;
}

.error-message {
  color: red;
  font-size: 14px;
  text-align: center;
  margin-bottom: 10px;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .signup-main {
    padding: 30px;
  }

  .signup-main h1 {
    font-size: 24px;
    margin-bottom: 20px;
  }

  .input-field {
    font-size: 14px;
  }

  .signup-button,
  .cancel-button {
    font-size: 14px;
    padding: 10px;
  }

  .home-button {
    font-size: 18px;
    padding: 10px;
  }

  .login-link {
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .signup-main {
    padding: 20px;
  }

  .signup-main h1 {
    font-size: 20px;
    margin-bottom: 15px;
  }

  .input-field {
    font-size: 12px;
    padding: 8px 10px;
  }

  .signup-button,
  .cancel-button {
    font-size: 14px;
    padding: 8px;
  }

  .home-button {
    font-size: 16px;
    padding: 8px;
  }

  .login-link {
    font-size: 14px;
  }
}
</style>
