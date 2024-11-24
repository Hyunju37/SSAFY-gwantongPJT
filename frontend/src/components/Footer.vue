<!-- src/components/Footer.vue -->
<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-menu">
        <RouterLink to="/privacy" class="footer-link">개인정보처리방침</RouterLink>
        <RouterLink to="/terms" class="footer-link">이용약관 및 고객 유의 | 사항</RouterLink>
        <template v-if="!isLoggedIn">
          <RouterLink to="/login" class="footer-link">로그인</RouterLink>
        </template>
        <template v-else>
          <span @click="logout" class="footer-link logout-link">로그아웃</span>
        </template>
      </div>
      <div class="copyright">
        © 2024 UNIBUZZ360. ALL RIGHTS RESERVED.
      </div>
      <button class="back-to-top" @click="scrollToTop" aria-label="맨 위로 이동">⬆️</button>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

// Computed property to check if user is logged in
const isLoggedIn = computed(() => !!userStore.token)

// Logout function
const logout = () => {
  userStore.logout()
}

// Scroll to top function
const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<style scoped>
.footer {
  background-color: #EFEFEF;
  padding: 20px;
  margin-top: 25px; /* 위쪽 margin을 25px로 설정 */
  position: relative;
}

.footer-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.footer-menu {
  display: flex;
  justify-content: center;
  gap: 40px;
  font-family: 'Noto Sans KR', sans-serif;
  font-size: 16px;
  color: #BEBEBE;
  margin-bottom: 20px;
}

.footer-link {
  cursor: pointer;
  transition: color 0.3s;
  text-decoration: none;
  color: inherit;
}

.footer-link:hover {
  color: #8C8C8C;
}

.footer-link:last-child {
  color: #8C8C8C;
}

.footer-link:last-child:hover {
  color: #555555;
}

.logout-link {
  cursor: pointer;
}

.copyright{
  color: #8C8C8C
}

.back-to-top {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #000000;
  color: #FFFFFF;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  border: none;
  cursor: pointer;
  font-size: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s, transform 0.3s;
}

.back-to-top:hover {
  background-color: #333333;
  transform: scale(1.1);
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .footer-menu {
    gap: 20px;
  }

  .back-to-top {
    width: 40px;
    height: 40px;
    font-size: 20px;
  }
}

@media (max-width: 480px) {
  .footer-menu {
    flex-direction: column;
    gap: 20px;
  }

  .back-to-top {
    width: 30px;
    height: 30px;
    font-size: 18px;
  }
}
</style>
