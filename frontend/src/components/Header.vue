<!-- src/components/Header.vue -->
<template>
  <header class="header">
    <div class="header-container">
      <!-- Logo and Title -->
      <RouterLink to="/" class="logo-title-container">
        <img :src="logoIcon" alt="UNIBUZZ 360 Logo" class="logo" />
        <h1 class="title">UNIBUZZ 360</h1>
      </RouterLink>
      <!-- Search Bar -->
      <div class="search-container">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="검색"
          class="search-bar"
          @keyup.enter="handleSearch"
        />
        <button @click="handleSearch" class="search-button" aria-label="검색">🔍</button>
      </div>
      <!-- Navigation Links -->
      <nav class="nav-links">
        <RouterLink to="/dashboard" class="nav-link">대시보드</RouterLink>
        <RouterLink to="/chatbot" class="nav-link">Chat Bot</RouterLink>
        <template v-if="!isLoggedIn">
          <RouterLink to="/login" class="nav-link">로그인</RouterLink>
        </template>
        <template v-else>
          <span @click="logout" class="nav-link logout-link">로그아웃</span>
        </template>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import logoIcon from '@/assets/logo_icon.png' // 로고 아이콘 경로 확인

const userStore = useUserStore()
const router = useRouter()

const searchQuery = ref('')

// Computed property to check if user is logged in
const isLoggedIn = computed(() => !!userStore.token)

// Handle search button click
const handleSearch = () => {
  if (searchQuery.value.trim() !== '') {
    console.log('Searching for:', searchQuery.value)
    router.push(`/search?query=${encodeURIComponent(searchQuery.value.trim())}`)
    searchQuery.value = ''
  } else {
    alert('검색어를 입력해주세요.')
  }
}

// Logout function
const logout = () => {
  userStore.logout()
}
</script>

<style scoped>
.header {
  background-color: #FFFFFF;
  height: 142px;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0 20px;
}

.header-container {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 1440px;
  justify-content: space-between;
}

.logo-title-container {
  display: flex;
  align-items: center;
  cursor: pointer; /* 클릭 가능함을 시각적으로 표시 */
}

.logo {
  width: 70px;
  height: 70px;
  margin-right: 10px;
}

.title {
  font-size: 40px;
  font-weight: bold;
  color: #000000;
  text-align: left;
}

.search-container {
  display: flex;
  align-items: center;
}

.search-bar {
  width: 600px;
  height: 50px;
  border-radius: 25px;
  border: 1px solid #707070;
  padding: 0 15px;
  background-color: #FFFFFF;
  font-size: 16px;
}

.search-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  margin-left: 10px;
}

.nav-links {
  display: flex;
  gap: 30px;
}

.nav-link {
  font-size: 20px;
  font-weight: bold;
  color: #000000;
  text-align: left;
  text-decoration: none;
  cursor: pointer;
}

.nav-link:hover {
  color: #555555;
  text-decoration: underline;
}

.logout-link {
  cursor: pointer;
}

@media (max-width: 768px) {
  .search-bar {
    width: 300px;
  }
}

@media (max-width: 480px) {
  .search-bar {
    width: 200px;
    height: 40px;
    font-size: 14px;
  }

  .search-button {
    font-size: 20px;
    margin-left: 5px;
  }

  .title {
    font-size: 30px;
  }

  .nav-link {
    font-size: 18px;
  }
}
</style>
