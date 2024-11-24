<!-- src/views/NewsPostsView.vue -->
<template>
    <Layout>
      <div class="news-post-page">
        <section class="news-main">
          <!-- 뉴스 상세 내용 영역 -->
          <div class="news-content">
            <div class="news-header">
              <div class="category">{{ newsData.category || '카테고리' }}</div>
              <h1 class="title">{{ newsData.title || '뉴스 제목' }}</h1>
              <h2 class="subtitle">{{ newsData.subtitle || '부제목' }}</h2>
              <div class="news-meta">
                <span class="news-date">{{ newsData.date || 'YYYY-MM-DD' }}</span>
                <div class="meta-actions">
                  <div class="like-section">
                    <button class="like-button" @click="likeNews" aria-label="좋아요">
                      👍
                    </button>
                    <span class="like-count">{{ newsData.likes || 0 }}</span>
                  </div>
                  <div class="view-section">
                    <span class="view-icon">👀</span>
                    <span class="view-count">{{ newsData.views || 0 }}</span>
                  </div>
                  <button class="link-button" @click="goToOriginalArticle">기사 원문보기</button>
                </div>
              </div>
            </div>
            <div class="news-body">
              <p>{{ newsData.content || '뉴스 내용이 표시됩니다.' }}</p>
            </div>
          </div>
          <!-- 유사한 뉴스 영역 -->
          <aside class="similar-news">
            <h3>유사한 뉴스</h3>
            <div class="similar-news-cards">
              <div
                class="news-card"
                v-for="(news, index) in similarNews"
                :key="index"
                @click="navigateToNews(news.id)"
              >
                <h4 class="news-title">{{ news.title }}</h4>
                <p class="news-summary">{{ news.summary }}</p>
                <span class="news-date">{{ news.date }}</span>
              </div>
            </div>
          </aside>
        </section>
      </div>
    </Layout>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
//   import { useNewsStore } from '@/stores/news'
  import Layout from '@/components/Layout.vue'
  
  const route = useRoute()
  const router = useRouter()
//   const newsStore = useNewsStore()


//   // 뉴스 데이터 로딩
//   onMounted(() => {
//     const newsId = route.params.id
//     newsStore.fetchNewsItem(newsId)
//     newsStore.fetchSimilarNews(newsId)
//   })

//   // 뉴스 데이터 가져오기
//   const newsData = computed(() => newsStore.newsItem)
//   const similarNews = computed(() => newsStore.similarNews)

//   // 좋아요 기능
//   const likeNews = () => {
//     // TODO: 실제 좋아요 기능 구현 (API 호출 등)
//     if (newsData.value) {
//       newsData.value.likes += 1
//     }
//   }
  
  // 뉴스 데이터 상태 변수
  const newsData = ref({
    id: null,
    category: '',
    title: '',
    subtitle: '',
    date: '',
    likes: 0,
    views: 0,
    content: '',
    originalUrl: ''
  })
  
  // 유사한 뉴스 상태 변수
  const similarNews = ref([
    // 임의의 데이터
    {
      id: 1,
      title: '유사한 뉴스 제목 1',
      summary: '유사한 뉴스 요약 1...',
      date: '2024-11-20'
    },
    {
      id: 2,
      title: '유사한 뉴스 제목 2',
      summary: '유사한 뉴스 요약 2...',
      date: '2024-11-19'
    },
    {
      id: 3,
      title: '유사한 뉴스 제목 3',
      summary: '유사한 뉴스 요약 3...',
      date: '2024-11-18'
    },
    {
      id: 4,
      title: '유사한 뉴스 제목 4',
      summary: '유사한 뉴스 요약 4...',
      date: '2024-11-17'
    },
    {
      id: 5,
      title: '유사한 뉴스 제목 5',
      summary: '유사한 뉴스 요약 5...',
      date: '2024-11-16'
    }
  ])
  
  // 뉴스 데이터 로딩
  onMounted(() => {
    const newsId = route.params.id
    // TODO: 실제 API 호출로 데이터 가져오기
    // 임의의 데이터 설정
    newsData.value = {
      id: newsId,
      category: '경제',
      title: `뉴스 제목 ${newsId}`,
      subtitle: '이것은 뉴스의 부제목입니다.',
      date: '2024-11-21',
      likes: 10,
      views: 100,
      content: '여기에 뉴스의 자세한 내용이 표시됩니다.',
      originalUrl: 'https://example.com/original-article'
    }
  })
  
  // 좋아요 기능
  const likeNews = () => {
    // TODO: 실제 좋아요 기능 구현
    newsData.value.likes += 1
  }
  
  // 기사 원문보기
  const goToOriginalArticle = () => {
    window.open(newsData.value.originalUrl, '_blank')
  }
  
  // 다른 뉴스로 이동
  const navigateToNews = (id) => {
    router.push(`/news-posts/${id}`)
  }
  </script>
  
  <style scoped>
  .news-post-page {
    background-color: #F7F7F7;
    font-family: 'Noto Sans KR', sans-serif;
    padding: 20px;
  }
  
  .news-main {
    display: flex;
    max-width: 1440px;
    margin: 0 auto;
  }
  
  .news-content {
    flex: 3;
    margin-right: 20px;
  }
  
  .news-header {
    margin-bottom: 20px;
  }
  
  .category {
    font-size: 18px;
    color: #828282;
    margin-bottom: 10px;
  }
  
  .title {
    font-size: 36px;
    font-weight: bold;
    margin-bottom: 10px;
  }
  
  .subtitle {
    font-size: 24px;
    color: #555555;
    margin-bottom: 20px;
  }
  
  .news-meta {
    display: flex;
    align-items: center;
    gap: 20px;
  }
  
  .news-date {
    font-size: 16px;
    color: #828282;
  }
  
  .meta-actions {
    display: flex;
    align-items: center;
    gap: 15px;
  }
  
  .like-section,
  .view-section {
    display: flex;
    align-items: center;
    gap: 5px;
  }
  
  .like-button {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 20px;
  }
  
  .link-button {
    background: none;
    border: none;
    color: #0000EE;
    text-decoration: underline;
    cursor: pointer;
  }
  
  .news-body {
    font-size: 18px;
    line-height: 1.6;
  }
  
  .similar-news {
    flex: 1;
  }
  
  .similar-news h3 {
    font-size: 24px;
    margin-bottom: 15px;
  }
  
  .similar-news-cards {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  
  .news-card {
    background-color: #FFFFFF;
    border: 1px solid #707070;
    border-radius: 10px;
    padding: 15px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .news-card:hover {
    background-color: #EFEFEF;
  }
  
  .news-card .news-title {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 10px;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
  }
  
  .news-card .news-summary {
    font-size: 16px;
    color: #555555;
    margin-bottom: 10px;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
  }
  
  .news-card .news-date {
    font-size: 14px;
    color: #828282;
  }
  </style>
  