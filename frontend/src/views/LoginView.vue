<!-- src/views/LoginView.vue -->
<template>
  <div class="login-page">
    <section class="login-main">
      <h1>로그인</h1>
      <form @submit.prevent="handleLogin" class="login-form">
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
          <label for="password">비밀번호</label>
          <input
            v-model="password"
            type="password"
            id="password"
            placeholder="비밀번호를 입력하세요"
            required
            class="input-field"
          />
        </div>

        <div class="button-group">
          <button type="submit" class="login-button">로그인</button>
          <button type="button" class="cancel-button" @click="cancelLogin">취소</button>
        </div>
      </form>
      <p class="signup-link">
        계정이 없으신가요?
        <RouterLink to="/signup" class="signup-button">회원가입</RouterLink>
      </p>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const store = useUserStore()
const router = useRouter()

// 상태 변수
const username = ref('')
const password = ref('')

// 로그인 핸들러
const handleLogin = async () => {
  const payload = {
    username: username.value,
    password: password.value
  }
  await store.logIn(payload)
  
  // 로그인 성공 여부 확인 (스토어에서 token이 설정되면 로그인 성공)
  if (store.token) {
    // 로그인이 성공했을 때, 헤더와 푸터에 있는 '로그인'을 '로그아웃'으로 변경
    // 이는 Header.vue와 Footer.vue에서 자동으로 반영됩니다.
    router.push('/dashboard')
  } else {
    alert('로그인 실패: 이메일 또는 비밀번호가 올바르지 않습니다.')
  }
}

// 취소 버튼 핸들러
const cancelLogin = () => {
  router.push('/') // 메인 페이지로 돌아가기
}
</script>

<style scoped>
.login-page {
  background-color: #F7F7F7;
  font-family: 'Noto Sans KR', sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  /* height: calc(100vh - 142px - 50px); /* 헤더(142px)와 푸터(50px) 높이 제외 */
  height: 100vh;
}

.login-main {
  background-color: #FFFFFF;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 3px 5px rgba(0, 0, 0, 0.16);
  width: 400px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.login-main h1 {
  font-size: 28px;
  margin-bottom: 30px;
}

.login-form {
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
  gap: 10px;
}

.login-button {
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

.login-button:hover {
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

.signup-link {
  margin-top: 20px;
  font-size: 16px;
}

.signup-button {
  color: #0000EE;
  text-decoration: underline;
  cursor: pointer;
}

.signup-button:hover {
  color: #5555FF;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .login-main {
    width: 90%;
    padding: 30px;
  }

  .login-main h1 {
    font-size: 24px;
    margin-bottom: 20px;
  }

  .input-field {
    font-size: 14px;
  }

  .login-button,
  .cancel-button {
    font-size: 14px;
    padding: 10px;
  }

  .signup-link {
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .login-main {
    width: 95%;
    padding: 20px;
  }

  .login-main h1 {
    font-size: 20px;
    margin-bottom: 15px;
  }

  .input-field {
    font-size: 12px;
    padding: 8px 10px;
  }

  .login-button,
  .cancel-button {
    font-size: 14px;
    padding: 8px;
  }

  .signup-link {
    font-size: 14px;
  }
}
</style>
