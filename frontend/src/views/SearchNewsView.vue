<!-- src/views/SearchNewsView.vue -->
<template>
    <Layout>
      <div class="search-news-page">
        <section class="search-results">
          <h1 class="search-title">검색 결과: "{{ searchQuery }}"</h1>
          <div class="news-cards">
            <div
              v-for="(news, index) in searchResults"
              :key="index"
              class="news-card"
              @click="navigateToNews(news.id)"
            >
              <h2 class="news-title">{{ news.title }}</h2>
              <p class="news-summary">{{ news.summary }}</p>
              <span class="news-date">{{ news.date }}</span>
            </div>
            <!-- 데이터가 없을 때 표시할 영역 -->
            <div v-if="searchResults.length === 0" class="no-results">
              검색 결과가 없습니다.
            </div>
          </div>
        </section>
      </div>
    </Layout>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { useNewsStore } from '@/stores/news' // 스토어 임포트
  import Layout from '@/components/Layout.vue'
  
  const route = useRoute()
  const router = useRouter()

  const newsStore = useNewsStore()

  
  // 검색어와 검색 결과 상태 변수
  const searchQuery = ref('')
  const searchResults = ref([])
  
  // 컴포넌트 마운트 시 검색어와 결과를 가져옴
  onMounted(() => {
    searchQuery.value = route.query.query || ''
    fetchSearchResults()
  })
  
  // 검색 결과를 가져오는 함수 (모의 데이터 사용)
  const fetchSearchResults = async () => {
    await newsStore.searchNews(searchQuery.value)  // Pinia 스토어의 searchNews 액션 호출
    searchResults.value = newsStore.searchResults
    // TODO: 실제 API 호출로 데이터 가져오기
    // if (searchQuery.value) {
    //   // 임의의 데이터 설정
    //   searchResults.value = [
    //     {
    //       id: 1,
    //       title: `검색된 뉴스 제목 1 (${searchQuery.value})`,
    //       summary: '이것은 검색된 뉴스의 요약입니다.',
    //       date: '2024-11-22'
    //     },
    //     {
    //       id: 2,
    //       title: `검색된 뉴스 제목 2 (${searchQuery.value})`,
    //       summary: '이것은 검색된 뉴스의 요약입니다.',
    //       date: '2024-11-21'
    //     }
    //   ]
    // } else {
    //   searchResults.value = []
    // }
  }
  
  // 뉴스 게시물 페이지로 이동
  const navigateToNews = (id) => {
    router.push(`/news-posts/${id}`)
  }
  </script>
  
  <style scoped>
  .search-news-page {
    background-color: #F7F7F7;
    font-family: 'Noto Sans KR', sans-serif;
    padding: 20px;
  }
  
  .search-results {
    max-width: 1440px;
    margin: 0 auto;
  }
  
  .search-title {
    font-size: 24px;
    margin-bottom: 20px;
  }
  
  .news-cards {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  .news-card {
    background-color: #FFFFFF;
    border: 1px solid #707070;
    border-radius: 10px;
    padding: 20px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .news-card:hover {
    background-color: #EFEFEF;
  }
  
  .news-title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 10px;
  }
  
  .news-summary {
    font-size: 16px;
    color: #555555;
    margin-bottom: 10px;
  }
  
  .news-date {
    font-size: 14px;
    color: #828282;
  }
  
  .no-results {
    padding: 50px;
    text-align: center;
    font-size: 18px;
    color: #828282;
  }
  </style>
  